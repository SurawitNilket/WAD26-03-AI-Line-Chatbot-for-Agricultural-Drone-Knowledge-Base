"""
LINE Rich Menu Configuration for AgriDrone Knowledge Base
Dimensions: 2500 x 1686 (Standard high-resolution 2 rows x 3 columns grid)
"""

RICH_MENU_CONFIG = {
    "size": {
        "width": 2500,
        "height": 1686
    },
    "selected": True,
    "name": "AgriDrone Agricultural Knowledge Menu",
    "chatBarText": "เมนูโดรน 🌾",
    "areas": [
        # Tile 1: กฎหมายโดรน CAAT (Row 1, Col 1)
        {
            "bounds": { "x": 0, "y": 0, "width": 833, "height": 843 },
            "action": {
                "type": "postback",
                "label": "กฎหมายโดรน",
                "data": "action=quick_faq&topic=drone_laws",
                "displayText": "ขอดูสรุปกฎหมายและข้อบังคับโดรน CAAT"
            }
        },
        # Tile 2: ขั้นตอนการขึ้นทะเบียน (Row 1, Col 2)
        {
            "bounds": { "x": 833, "y": 0, "width": 834, "height": 843 },
            "action": {
                "type": "postback",
                "label": "ขึ้นทะเบียนโดรน",
                "data": "action=guide&topic=registration_steps",
                "displayText": "ขั้นตอนการขึ้นทะเบียนโดรน CAAT & กสทช."
            }
        },
        # Tile 3: เทคนิคพ่นข้าว (Row 1, Col 3)
        {
            "bounds": { "x": 1667, "y": 0, "width": 833, "height": 843 },
            "action": {
                "type": "postback",
                "label": "เทคนิคพ่นข้าว",
                "data": "action=quick_faq&topic=spraying_rice",
                "displayText": "เทคนิคการบินพ่นยาข้าว"
            }
        },
        # Tile 4: ผสมสารเคมีปลอดภัย (Row 2, Col 1)
        {
            "bounds": { "x": 0, "y": 843, "width": 833, "height": 843 },
            "action": {
                "type": "postback",
                "label": "ผสมสารเคมี",
                "data": "action=quick_faq&topic=chemical_safety",
                "displayText": "วิธีผสมสารเคมีและการป้องกันอันตราย"
            }
        },
        # Tile 5: การบำรุงรักษาโดรน (Row 2, Col 2)
        {
            "bounds": { "x": 833, "y": 843, "width": 834, "height": 843 },
            "action": {
                "type": "postback",
                "label": "การบำรุงรักษา",
                "data": "action=quick_faq&topic=maintenance",
                "displayText": "การบำรุงรักษาและแก้ปัญหาโดรน"
            }
        },
        # Tile 6: ถาม AI ผู้เชี่ยวชาญ (Row 2, Col 3)
        {
            "bounds": { "x": 1667, "y": 843, "width": 833, "height": 843 },
            "action": {
                "type": "message",
                "label": "ถาม AI",
                "text": "ปรึกษาผู้เชี่ยวชาญ AI โดรนเกษตร"
            }
        }
    ]
}
