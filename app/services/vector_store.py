"""
Vector Store and Knowledge Retrieval Engine for Agricultural Drone Chatbot.
Supports dense vector embeddings via Google GenAI / Gemini API,
with automatic fallback to keyword/semantic token scoring for offline test suites.
"""
import math
import re
from typing import List, Dict, Any, Tuple
from app.config import settings
from app.services.knowledge_data import KNOWLEDGE_BASE

try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class VectorStore:
    def __init__(self):
        self.documents: List[Dict[str, Any]] = KNOWLEDGE_BASE.copy()
        self.embeddings: Dict[str, List[float]] = {}
        self.client = None
        # Only initialize if a real Gemini API key is provided (not empty or dummy placeholder)
        if GENAI_AVAILABLE and settings.GEMINI_API_KEY and not settings.GEMINI_API_KEY.startswith("your_"):
            try:
                self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
            except Exception as e:
                print(f"[VectorStore] Warning: Could not initialize GenAI client: {e}")

    def _cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    def _tokenize(self, text: str) -> List[str]:
        # Simple Thai and English word boundary tokenizer
        tokens = re.findall(r'\w+', text.lower())
        return tokens

    STOP_WORDS = {"to", "the", "a", "an", "is", "in", "it", "how", "what", "can", "of", "and", "or", "for", "on", "at", "by", "with"}

    def _fallback_keyword_search(self, query: str, top_k: int = 3) -> List[Tuple[Dict[str, Any], float]]:
        query_tokens = [t for t in self._tokenize(query) if t not in self.STOP_WORDS and len(t) >= 3]
        scored_docs = []

        for doc in self.documents:
            score = 0.0
            doc_text = f"{doc['title']} {doc['content']} {' '.join(doc.get('keywords', []))}".lower()
            
            # Exact match checks for domain keywords
            for kw in doc.get("keywords", []):
                if kw in query.lower():
                    score += 3.0
            
            # Significant token overlap
            for token in query_tokens:
                # Use word-boundary or distinct token match
                if re.search(r'\b' + re.escape(token) + r'\b', doc_text, re.IGNORECASE) or (len(token) >= 4 and token in doc_text):
                    score += 1.5

            if score >= 2.0:
                scored_docs.append((doc, score))

        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return scored_docs[:top_k]

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Searches the knowledge base for top-k most relevant documents.
        Returns document metadata including title, official URL, and text chunk.
        """
        # If API key is available, use semantic embedding retrieval
        if self.client and settings.GEMINI_API_KEY:
            try:
                # Generate query embedding
                response = self.client.models.embed_content(
                    model=settings.EMBEDDING_MODEL,
                    contents=query
                )
                query_vector = response.embedding.values

                # Score against indexed documents
                results = []
                for doc in self.documents:
                    doc_id = doc["id"]
                    if doc_id not in self.embeddings:
                        doc_resp = self.client.models.embed_content(
                            model=settings.EMBEDDING_MODEL,
                            contents=doc["content"]
                        )
                        self.embeddings[doc_id] = doc_resp.embedding.values
                    
                    sim = self._cosine_similarity(query_vector, self.embeddings[doc_id])
                    results.append((doc, sim))

                results.sort(key=lambda x: x[1], reverse=True)
                return [
                    {**doc, "relevance_score": score}
                    for doc, score in results[:top_k] if score > 0.4
                ]
            except Exception as e:
                print(f"[VectorStore] Embedding retrieval failed, falling back to keyword search: {e}")

        # Fallback scoring
        fallback_results = self._fallback_keyword_search(query, top_k=top_k)
        return [
            {**doc, "relevance_score": round(min(score / 5.0, 1.0), 2)}
            for doc, score in fallback_results
        ]

    def add_document(self, doc_data: Dict[str, Any]) -> str:
        self.documents.append(doc_data)
        return doc_data.get("id", str(len(self.documents)))

vector_store = VectorStore()
