"""
Deterministic Rule-Based Engine.
Handles high-frequency predefined queries and rich menu postbacks instantly without calling the LLM.
Saves token costs, avoids hallucinations, and guarantees 0ms response latency.
"""
from typing import Optional, Dict, Any, Tuple
from app.config import settings
from app.templates.flex_messages import (
    create_drone_laws_flex,
    create_registration_steps_flex,
    create_crop_spraying_flex,
    create_chemical_safety_flex,
    create_maintenance_flex
)

class RuleEngine:
    def __init__(self):
        self.rules = {
            "drone_laws": {
                "keywords": ["กฎหมาย", "ข้อบังคับ", "caat", "กพท", "ความสูงบิน", "บินได้กี่เมตร", "โทษ", "ปรับโดรน"],
                "flex_builder": lambda: create_drone_laws_flex(settings.CAAT_INFOGRAPHIC_URL),
                "text_summary": (
                    "⚖️ สรุปกฎหมายโดรน (CAAT):\n"
                    "1. บินสูงไม่เกิน 90 เมตร (300 ฟุต)\n"
                    "2. ห่างจากคน ยานพาหนะ อาคาร 30-50 เมตร\n"
                    "3. ห้ามบินกลางคืน (เฉพาะพระอาทิตย์ขึ้น-ตก)\n"
                    "4. ห้ามบินใกล้สนามบิน 9 กม. (5 ไมล์ทะเล)\n"
                    "⚠️ ฝ่าฝืนมีโทษจำคุกสูงสุด 1 ปี หรือปรับสูงสุด 40,000 บาท\n"
                    f"ศึกษาเพิ่มเติม: {settings.CAAT_INFOGRAPHIC_URL}"
                )
            },
            "registration_steps": {
                "keywords": ["ขึ้นทะเบียน", "ลงทะเบียน", "anyregis", "uas portal", "ขั้นตอนการขึ้นทะเบียน", "ขออนุญาตบิน", "ทำประกัน"],
                "flex_builder": lambda: create_registration_steps_flex(settings.NBTC_REGIS_URL, settings.CAAT_UAS_PORTAL_URL),
                "text_summary": (
                    "📋 3 ขั้นตอนขึ้นทะเบียนโดรนเกษตร:\n"
                    "1. ทำประกันภัยโดรน (วงเงินบุคคลภายนอก 1 ล้านบาทขึ้นไป)\n"
                    f"2. ขึ้นทะเบียนวิทยุ กสทช. ภายใน 30 วันที่ {settings.NBTC_REGIS_URL}\n"
                    f"3. ขึ้นทะเบียนผู้บังคับโดรนและเครื่องที่ CAAT: {settings.CAAT_UAS_PORTAL_URL}"
                )
            },
            "spraying_rice": {
                "keywords": ["พ่นข้าว", "นาข้าว", "ฉีดข้าว", "ความสูงพ่นข้าว", "ความเร็วพ่นข้าว", "น้ำกี่ลิตรต่อไร่"],
                "flex_builder": lambda: create_crop_spraying_flex("rice", settings.DOAE_DRONE_MANUAL_URL),
                "text_summary": (
                    "🌾 เทคนิคการบินพ่นยาในนาข้าว:\n"
                    "• ความสูง: 2.5 - 3.0 เมตร เหนือยอดรวงข้าว\n"
                    "• ความเร็ว: 4.0 - 5.0 เมตร/วินาที\n"
                    "• ปริมาณน้ำ: 15 - 20 ลิตร/เฮกตาร์ (2.5 - 3.5 ลิตร/ไร่)\n"
                    "• เวลาพ่น: เช้า 06.00-09.00 น. หรือเย็น 16.00-18.00 น. (เลี่ยงลมแรง >3 m/s)\n"
                    f"อ้างอิง: คู่มือโดรนเพื่อการเกษตร กรมส่งเสริมการเกษตร"
                )
            },
            "chemical_safety": {
                "keywords": ["ผสมสาร", "ผสมปุ๋ย", "สารเคมี", "wales", "ลำดับผสม", "สารจับใบ", "หัวฉีดตันจากยา"],
                "flex_builder": lambda: create_chemical_safety_flex(),
                "text_summary": (
                    "🧪 ลำดับการผสมสารเคมีในถังโดรน (WALES Rule):\n"
                    "1. น้ำสะอาดครึ่งถัง\n"
                    "2. สารผง WP / WDG\n"
                    "3. สารแขวนลอย SC\n"
                    "4. สารละลายน้ำ SL\n"
                    "5. สารน้ำมัน EC\n"
                    "6. สารจับใบ เติมน้ำเต็มถังแล้วกวนให้เข้ากัน\n"
                    "⚠️ สวมชุด PPE และแว่นตานิรภัยทุกครั้ง ห้ามพ่นเมื่อลมแรงเกิน 3 m/s"
                )
            },
            "maintenance": {
                "keywords": ["บำรุงรักษา", "ดูแลโดรน", "ล้างหัวฉีด", "แบตเตอรี่", "lipo", "ชาร์จแบต", "เข็มทิศ", "calibrate"],
                "flex_builder": lambda: create_maintenance_flex(),
                "text_summary": (
                    "🛠️ การบำรุงรักษาโดรนเกษตร:\n"
                    "1. หัวฉีดตัน: แช่น้ำอุ่น ใช้แปรงสีฟันขนอ่อนขัด ห้ามใช้ลวดแยง\n"
                    "2. แบต LiPo: พักให้เย็นก่อนชาร์จเสมอ, เก็บรักษาที่ 3.80 - 3.85V/cell\n"
                    "3. เข็มทิศ: Calibrate ใหม่ทุกครั้งที่ย้ายแปลงบินข้ามอำเภอ"
                )
            }
        }

    def match(self, text: str) -> Optional[Tuple[str, Dict[str, Any], str]]:
        """
        Matches user text against predefined rules.
        Returns (topic_key, flex_payload, text_summary) if matched, else None.
        """
        normalized = text.strip().lower()
        for topic, data in self.rules.items():
            for kw in data["keywords"]:
                if kw in normalized:
                    return topic, data["flex_builder"](), data["text_summary"]
        return None

    def get_by_topic(self, topic: str) -> Optional[Tuple[Dict[str, Any], str]]:
        """Retrieves rule response directly by topic key (used by Rich Menu postbacks)."""
        if topic in self.rules:
            data = self.rules[topic]
            return data["flex_builder"](), data["text_summary"]
        return None

rule_engine = RuleEngine()
