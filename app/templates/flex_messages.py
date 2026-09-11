"""
LINE Flex Message builders for rich UI responses.
Generates structured JSON payloads conforming to the LINE Flex Message specification.
"""
from typing import List, Dict, Any, Optional

def create_drone_laws_flex(caat_url: str) -> Dict[str, Any]:
    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#1E3A8A",
            "contents": [
                {
                    "type": "text",
                    "text": "⚖️ สรุปกฎหมายโดรน (CAAT)",
                    "weight": "bold",
                    "color": "#FFFFFF",
                    "size": "lg"
                },
                {
                    "type": "text",
                    "text": "ข้อบังคับหลักสำหรับการบินโดรนในไทย",
                    "color": "#BFDBFE",
                    "size": "xs",
                    "margin": "sm"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": "• ความสูงเพดานบิน: ห้ามบินเกิน 90 เมตร (300 ฟุต)",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": "• ระยะห่างปลอดภัย: ห่างจากคน ยานพาหนะ หรือสิ่งปลูกสร้างอย่างน้อย 30 - 50 เมตร",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": "• เวลาทำการบิน: เฉพาะเวลากลางวัน (พระอาทิตย์ขึ้น - ตก)",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": "• ละเมิดสิทธิ: ห้ามละเมิดสิทธิความเป็นส่วนตัวผู้อื่น",
                            "size": "sm",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": "⚠️ โทษฝ่าฝืน: จำคุกไม่เกิน 1 ปี หรือปรับไม่เกิน 40,000 บาท หรือทั้งจำทั้งปรับ",
                            "size": "xs",
                            "color": "#DC2626",
                            "weight": "bold",
                            "wrap": True,
                            "margin": "md"
                        }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#2563EB",
                    "action": {
                        "type": "uri",
                        "label": "เปิดดู Infographic CAAT ทางการ",
                        "uri": caat_url
                    }
                }
            ]
        }
    }

def create_registration_steps_flex(nbtc_url: str, caat_url: str) -> Dict[str, Any]:
    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#047857",
            "contents": [
                {
                    "type": "text",
                    "text": "📋 ขั้นตอนการขึ้นทะเบียนโดรนเกษตร",
                    "weight": "bold",
                    "color": "#FFFFFF",
                    "size": "md"
                },
                {
                    "type": "text",
                    "text": "ต้องทำให้ครบทั้ง 3 ขั้นตอนก่อนขึ้นบิน",
                    "color": "#A7F3D0",
                    "size": "xs",
                    "margin": "xs"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        { "type": "text", "text": "ขั้นที่ 1: ทำประกันภัยโดรน", "weight": "bold", "size": "sm", "color": "#065F46" },
                        { "type": "text", "text": "วงเงินคุ้มครองบุคคลภายนอกไม่น้อยกว่า 1 ล้านบาท/ครั้ง", "size": "xs", "color": "#4B5563", "wrap": True }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        { "type": "text", "text": "ขั้นที่ 2: ขึ้นทะเบียนคลื่นความถี่ (กสทช.)", "weight": "bold", "size": "sm", "color": "#065F46" },
                        { "type": "text", "text": "ภายใน 30 วันหลังซื้อโดรน ผ่านระบบ Anyregis", "size": "xs", "color": "#4B5563", "wrap": True }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        { "type": "text", "text": "ขั้นที่ 3: ขึ้นทะเบียนผู้บังคับโดรน (กพท./CAAT)", "weight": "bold", "size": "sm", "color": "#065F46" },
                        { "type": "text", "text": "ผ่านระบบออนไลน์ CAAT UAS Portal", "size": "xs", "color": "#4B5563", "wrap": True }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "secondary",
                    "action": {
                        "type": "uri",
                        "label": "1. เว็บไซต์ Anyregis (กสทช.)",
                        "uri": nbtc_url
                    }
                },
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#059669",
                    "action": {
                        "type": "uri",
                        "label": "2. CAAT UAS Portal (กพท.)",
                        "uri": caat_url
                    }
                }
            ]
        }
    }

def create_crop_spraying_flex(crop: str, doae_url: str) -> Dict[str, Any]:
    if crop == "rice":
        title = "🌾 เทคนิคการบินพ่นยาในนาข้าว"
        height = "2.5 – 3.0 เมตร เหนือยอดรวงข้าว"
        speed = "4.0 – 5.0 เมตร/วินาที"
        volume = "15 – 20 ลิตร/เฮกตาร์ (2.5 – 3.5 ลิตร/ไร่)"
        notes = "ช่วงเวลาเหมาะสม: 06.00-09.00 น. หรือ 16.00-18.00 น. เลี่ยงแดดจัดและลมแรง"
    else:
        title = f"🌱 เทคนิคการบินพ่นพืช: {crop}"
        height = "2.0 – 3.0 เมตร เหนือยอดทรงพุ่ม"
        speed = "3.5 – 4.5 เมตร/วินาที"
        volume = "20 – 30 ลิตร/เฮกตาร์"
        notes = "ควรตรวจทิศทางลมสม่ำเสมอเพื่อควบคุมละอองสารเคมี"

    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#D97706",
            "contents": [
                { "type": "text", "text": title, "weight": "bold", "color": "#FFFFFF", "size": "md" }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                { "type": "text", "text": f"• ความสูงการบิน: {height}", "size": "sm", "wrap": True },
                { "type": "text", "text": f"• ความเร็วการบิน: {speed}", "size": "sm", "wrap": True },
                { "type": "text", "text": f"• ปริมาณน้ำฉีดพ่น: {volume}", "size": "sm", "wrap": True },
                { "type": "text", "text": f"• คำแนะนำ: {notes}", "size": "xs", "color": "#6B7280", "wrap": True, "margin": "md" }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "action": {
                        "type": "uri",
                        "label": "อ้างอิง: คู่มือโดรนเกษตร กรมส่งเสริมการเกษตร",
                        "uri": doae_url
                    }
                }
            ]
        }
    }

def create_chemical_safety_flex() -> Dict[str, Any]:
    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#B45309",
            "contents": [
                { "type": "text", "text": "🧪 การผสมสารเคมี & ความปลอดภัย", "weight": "bold", "color": "#FFFFFF", "size": "md" }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                { "type": "text", "text": "ลำดับการผสมสารในถัง (WALES Rule):", "weight": "bold", "size": "sm" },
                { "type": "text", "text": "1. น้ำสะอาดครึ่งถัง\n2. สารชนิดผง (WP, WDG)\n3. สารแขวนลอย (SC)\n4. สารละลายน้ำ (SL, SP)\n5. สารน้ำมันสูตรเข้มข้น (EC)\n6. สารจับใบ เติมน้ำให้เต็มแล้วกวนผสม", "size": "xs", "wrap": True, "color": "#374151" },
                { "type": "separator", "margin": "md" },
                { "type": "text", "text": "⚠️ ข้อห้าม: ห้ามพ่นเมื่อลมแรงเกิน 3 เมตร/วินาที สวมหน้ากาก ถุงมือ และแว่นตานิรภัยเสมอ", "size": "xs", "color": "#DC2626", "wrap": True, "margin": "sm" }
            ]
        }
    }

def create_maintenance_flex() -> Dict[str, Any]:
    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#4B5563",
            "contents": [
                { "type": "text", "text": "🛠️ การบำรุงรักษา & แก้ไขปัญหาโดรน", "weight": "bold", "color": "#FFFFFF", "size": "md" }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                { "type": "text", "text": "1. หัวฉีดตัน / พ่นไม่สม่ำเสมอ:", "weight": "bold", "size": "xs", "color": "#111827" },
                { "type": "text", "text": "ถอดล้างด้วยน้ำสะอาดและแปรงขนนุ่ม ห้ามใช้ลวดแยงเพราะรูจะเสียทรง", "size": "xs", "color": "#4B5563", "wrap": True },
                { "type": "text", "text": "2. การดูแลแบตเตอรี่อัจฉริยะ (LiPo):", "weight": "bold", "size": "xs", "color": "#111827", "margin": "sm" },
                { "type": "text", "text": "อย่าชาร์จทันทีหลังบิน (รอให้เย็นก่อน), เก็บรักษาที่ 3.8 - 3.85V/Cell", "size": "xs", "color": "#4B5563", "wrap": True },
                { "type": "text", "text": "3. ปัญหาสัญญาณดาวเทียม / Compass:", "weight": "bold", "size": "xs", "color": "#111827", "margin": "sm" },
                { "type": "text", "text": "หมั่น Calibrate เข็มทิศเมื่อย้ายแปลง และห่างจากเสาไฟฟ้าแรงสูงหรือโครงเหล็ก", "size": "xs", "color": "#4B5563", "wrap": True }
            ]
        }
    }

def create_rag_answer_flex(answer: str, citations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generates a LINE Flex Message wrapping RAG answer with verified source citations."""
    citation_elements = []
    if citations:
        citation_elements.append({ "type": "separator", "margin": "lg" })
        citation_elements.append({
            "type": "text",
            "text": "📚 แหล่งอ้างอิงข้อมูลทางการ:",
            "size": "xs",
            "weight": "bold",
            "color": "#1E40AF",
            "margin": "md"
        })
        for item in citations[:3]:
            btn_title = item.get("title", "เอกสารอ้างอิง")
            url = item.get("url")
            if url:
                citation_elements.append({
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": f"🔗 {btn_title[:35]}",
                        "uri": url
                    }
                })
            else:
                citation_elements.append({
                    "type": "text",
                    "text": f"• {btn_title}",
                    "size": "xxs",
                    "color": "#6B7280",
                    "wrap": True
                })

    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "horizontal",
            "backgroundColor": "#059669",
            "contents": [
                {
                    "type": "text",
                    "text": "🌾 คำตอบจากผู้เชี่ยวชาญโดรนเกษตร",
                    "color": "#FFFFFF",
                    "weight": "bold",
                    "size": "sm"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": answer,
                    "wrap": True,
                    "size": "sm",
                    "color": "#1F2937"
                },
                *citation_elements
            ]
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": "ให้คะแนนคำตอบนี้:",
                    "size": "xxs",
                    "color": "#9CA3AF",
                    "gravity": "center"
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": { "type": "postback", "label": "⭐⭐⭐⭐⭐", "data": "action=rate&score=5" }
                }
            ]
        }
    }
