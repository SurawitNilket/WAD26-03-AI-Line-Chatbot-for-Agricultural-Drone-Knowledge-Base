"""
Event Dispatcher and Routing Logic.
Decides whether an incoming query/event is handled deterministically by the Rule Engine,
or routed to the semantic RAG pipeline.
"""
import urllib.parse
from typing import Dict, Any, Optional
from app.services.rule_engine import rule_engine
from app.services.rag_service import rag_service
from app.core.line_client import line_client
from app.templates.flex_messages import create_rag_answer_flex

class Dispatcher:
    def handle_text_message(self, user_id: str, reply_token: str, text: str) -> Dict[str, Any]:
        """
        Processes free-text messages from LINE users or test endpoints.
        """
        # 1. Check deterministic rule engine first
        match_result = rule_engine.match(text)
        if match_result:
            topic, flex_data, text_summary = match_result
            if reply_token and reply_token != "test_token":
                line_client.reply_flex(reply_token, f"ข้อมูล: {topic}", flex_data)
            return {
                "handled_by": "rule_engine",
                "topic": topic,
                "response": text_summary,
                "flex_data": flex_data,
                "is_rule_based": True,
                "citations": []
            }

        # 2. Open-ended question -> Route to RAG
        if reply_token and reply_token != "test_token":
            # Display typing loading animation
            line_client.show_loading(user_id=user_id, loading_seconds=10)

        rag_result = rag_service.query(text)
        answer = rag_result["answer"]
        citations = rag_result["citations"]

        # 3. Format and send response
        if reply_token and reply_token != "test_token":
            if citations:
                flex_bubble = create_rag_answer_flex(answer, citations)
                line_client.reply_flex(reply_token, "คำตอบจาก AgriDrone AI", flex_bubble)
            else:
                line_client.reply_text(reply_token, answer)

        return {
            "handled_by": "rag_service",
            "response": answer,
            "citations": citations,
            "is_rule_based": False,
            "latency_ms": rag_result.get("latency_ms", 0.0)
        }

    def handle_postback(self, user_id: str, reply_token: str, postback_data: str) -> Dict[str, Any]:
        """
        Handles postbacks triggered by LINE Rich Menu clicks or rating actions.
        """
        parsed_data = dict(urllib.parse.parse_qsl(postback_data))
        action = parsed_data.get("action")
        topic = parsed_data.get("topic")

        # Handle Rich Menu Quick FAQ
        if action in ("quick_faq", "guide") and topic:
            rule_data = rule_engine.get_by_topic(topic)
            if rule_data:
                flex_payload, text_summary = rule_data
                if reply_token and reply_token != "test_token":
                    line_client.reply_flex(reply_token, f"หัวข้อ: {topic}", flex_payload)
                return {
                    "status": "success",
                    "handled_by": "rich_menu_postback",
                    "topic": topic,
                    "response": text_summary
                }

        # Handle satisfaction survey rating
        if action == "rate":
            score = parsed_data.get("score", "5")
            thank_you_text = f"🙏 ขอบคุณสำหรับการให้คะแนนความพึงพอใจ {score} ดาวครับ! ทีมงานจะนำไปพัฒนาบริการต่อไป"
            if reply_token and reply_token != "test_token":
                line_client.reply_text(reply_token, thank_you_text)
            return {
                "status": "success",
                "handled_by": "satisfaction_rating",
                "score": int(score)
            }

        fallback_msg = "ขออภัยครับ ไม่พบข้อมูลที่ต้องการ กรุณาเลือกจากเมนูด้านล่างหรือพิมพ์คำถามได้เลยครับ"
        if reply_token and reply_token != "test_token":
            line_client.reply_text(reply_token, fallback_msg)
        return {"status": "unknown_action", "response": fallback_msg}

dispatcher = Dispatcher()
