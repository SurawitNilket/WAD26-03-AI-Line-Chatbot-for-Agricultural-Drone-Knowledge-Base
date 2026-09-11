"""
Comprehensive API and Pipeline Unit Tests for AgriDrone Chatbot.
Course: 2026 EN813701 Web Application Development
"""
import pytest
from starlette.testclient import TestClient
from app.main import app
from app.core.dispatcher import dispatcher
from app.services.rule_engine import rule_engine

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "AgriDrone" in data["service"]
    assert data["status"] == "online"
    assert "endpoints" in data

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_richmenu_config_format():
    response = client.get("/api/v1/richmenu/config")
    assert response.status_code == 200
    data = response.json()
    assert data["size"]["width"] == 2500
    assert data["size"]["height"] == 1686
    assert len(data["areas"]) == 6

def test_rule_engine_matching():
    # Test law keyword
    match_law = rule_engine.match("อยากรู้กฎหมายโดรนบินได้กี่เมตรครับ")
    assert match_law is not None
    topic, flex, summary = match_law
    assert topic == "drone_laws"
    assert "90 เมตร" in summary

    # Test rice spraying
    match_rice = rule_engine.match("การพ่นข้าวต้องใช้น้ำกี่ลิตรต่อไร่")
    assert match_rice is not None
    topic, flex, summary = match_rice
    assert topic == "spraying_rice"
    assert "2.5 – 3.0 เมตร" in summary or "2.5 - 3.0 เมตร" in summary

def test_query_endpoint_rule_based():
    payload = {
        "user_id": "test_user_01",
        "question": "ขั้นตอนการขึ้นทะเบียนโดรนเกษตรมีอะไรบ้าง",
        "stream": False
    }
    response = client.post("/api/v1/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_rule_based"] is True
    assert "ขึ้นทะเบียน" in data["answer"]
    assert "anyregis.nbtc.go.th" in data["answer"] or "กสทช" in data["answer"]

def test_query_endpoint_rag():
    payload = {
        "user_id": "test_user_02",
        "question": "การพ่นในไร่มันสำปะหลังต้องบินสูงเท่าไหร่และระวังศัตรูพืชอะไร",
        "stream": False
    }
    response = client.post("/api/v1/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["sources"]) > 0
    assert "มันสำปะหลัง" in data["answer"]
    # Check that official DOAE source is cited
    assert any("กรมส่งเสริมการเกษตร" in s["source_name"] or "DOAE" in s["source_name"] for s in data["sources"])

def test_query_endpoint_out_of_scope():
    payload = {
        "user_id": "test_user_03",
        "question": "วิธีเขียนโปรแกรม React เบื้องต้นทำอย่างไร",
        "stream": False
    }
    response = client.post("/api/v1/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "นอกเหนือขอบเขต" in data["answer"]

def test_feedback_flow():
    # Submit rating 5
    fb_payload = {
        "user_id": "pilot_01",
        "query": "เทคนิคการพ่นข้าว",
        "score": 5,
        "comment": "คำตอบชัดเจน มีแหล่งอ้างอิงกรมส่งเสริมการเกษตร"
    }
    res = client.post("/api/v1/feedback", json=fb_payload)
    assert res.status_code == 200
    assert res.json()["status"] == "success"

    # Check stats
    stats_res = client.get("/api/v1/feedback/stats")
    assert stats_res.status_code == 200
    stats = stats_res.json()
    assert stats["total_responses"] >= 1
    assert stats["average_score"] >= 4.0

def test_dispatcher_postback_actions():
    # Test Rich menu postback for maintenance
    result = dispatcher.handle_postback("pilot_01", "test_token", "action=quick_faq&topic=maintenance")
    assert result["status"] == "success"
    assert result["handled_by"] == "rich_menu_postback"
    assert "บำรุงรักษา" in result["response"]

    # Test star rating postback
    rate_res = dispatcher.handle_postback("pilot_01", "test_token", "action=rate&score=5")
    assert rate_res["status"] == "success"
    assert rate_res["score"] == 5
