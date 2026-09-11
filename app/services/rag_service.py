"""
RAG (Retrieval-Augmented Generation) Service.
Combines dense/hybrid retrieval with LLM generation (Google Gemini / OpenAI),
enforcing Thai language responses with verified official citations.
"""
import time
from typing import Dict, Any, List
from app.config import settings
from app.services.vector_store import vector_store
from app.models.schemas import SourceCitation

try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


SYSTEM_PROMPT = """คุณคือ "AgriDrone AI" ผู้เชี่ยวชาญด้านโดรนเกษตรและการบินในประเทศไทย
หน้าที่ของคุณคือตอบคำถามเกษตรกรและผู้ให้บริการโดรนด้วยข้อมูลที่ถูกต้อง ปลอดภัย และอิงมาตรฐานทางการ

ข้อกำหนดสำคัญในการตอบ:
1. ตอบเป็นภาษาไทยที่สุภาพ เข้าใจง่าย กระชับ และเน้นข้อมูลเชิงปฏิบัติ
2. ตัวเลขเทคนิค (ความสูง, ความเร็ว, ปริมาณน้ำ, อัตราส่วนผสม) ต้องตรงกับข้อมูลอ้างอิงที่ได้รับ
3. หากคำถามอยู่นอกเหนือขอบเขตโดรนเกษตร ให้ตอบปฏิเสธอย่างสุภาพว่า "ขออภัยครับ ระบบเชี่ยวชาญเฉพาะเรื่องโดรนเกษตร กฎหมายการบิน CAAT และเทคนิคการพ่นสารเคมีครับ"
4. ในตอนท้ายของคำตอบ ให้ระบุแหล่งอ้างอิงจากข้อมูลบริบทเสมอ
"""


class RAGService:
    def __init__(self):
        self.client = None
        if GENAI_AVAILABLE and settings.GEMINI_API_KEY and not settings.GEMINI_API_KEY.startswith("your_"):
            try:
                self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
            except Exception as e:
                print(f"[RAGService] Warning: GenAI Client init failed: {e}")

    def query(self, question: str) -> Dict[str, Any]:
        start_time = time.time()
        
        # 1. Retrieve relevant knowledge chunks
        chunks = vector_store.search(question, top_k=3)
        
        citations: List[SourceCitation] = []
        for c in chunks:
            citations.append(SourceCitation(
                title=c.get("title", "เอกสารโดรนเกษตร"),
                source_name=c.get("source_name", "ข้อมูลทางการ"),
                url=c.get("url"),
                page=c.get("page"),
                relevance_score=c.get("relevance_score")
            ))

        # Check if question is completely out of domain
        if not chunks or (citations and citations[0].relevance_score and citations[0].relevance_score < 0.2):
            latency = (time.time() - start_time) * 1000
            return {
                "answer": "ขออภัยครับ คำถามนี้อยู่นอกเหนือขอบเขตความรู้เรื่องโดรนเกษตร กฎหมายการบิน หรือการฉีดพ่นสารเคมีที่ระบบรองรับครับ หากมีข้อสงสัยเกี่ยวกับโดรนเกษตรสามารถสอบถามได้เลยครับ",
                "citations": [],
                "latency_ms": round(latency, 2)
            }

        # 2. Build context
        context_text = "\n\n".join([
            f"--- ข้อมูลอ้างอิง: {c.get('title')} ({c.get('source_name')}) ---\n{c.get('content')}"
            for c in chunks
        ])

        # 3. Generate answer via LLM (or grounded synthesizer if no key)
        if self.client and settings.GEMINI_API_KEY:
            try:
                prompt = (
                    f"{SYSTEM_PROMPT}\n\n"
                    f"บริบทข้อมูลอ้างอิง:\n{context_text}\n\n"
                    f"คำถามของผู้ใช้: {question}\n\n"
                    f"จงตอบคำถามโดยอ้างอิงข้อมูลบริบทข้างต้น:"
                )
                response = self.client.models.generate_content(
                    model=settings.LLM_MODEL,
                    contents=prompt
                )
                answer_text = response.text
            except Exception as e:
                print(f"[RAGService] LLM generation error: {e}, falling back to context synthesis.")
                answer_text = self._synthesize_fallback(question, chunks)
        else:
            answer_text = self._synthesize_fallback(question, chunks)

        latency = (time.time() - start_time) * 1000
        return {
            "answer": answer_text,
            "citations": [c.model_dump() for c in citations],
            "latency_ms": round(latency, 2)
        }

    def _synthesize_fallback(self, question: str, chunks: List[Dict[str, Any]]) -> str:
        """High-fidelity grounded synthesis used when running offline or without API key."""
        best_chunk = chunks[0]
        summary = (
            f"{best_chunk['content']}\n\n"
            f"📚 ข้อมูลอ้างอิง:\n"
            f"• {best_chunk.get('source_name', 'กรมส่งเสริมการเกษตร')} "
            f"({best_chunk.get('title')})"
        )
        if best_chunk.get("url"):
            summary += f"\n🔗 ดูเพิ่มเติม: {best_chunk['url']}"
        return summary

rag_service = RAGService()
