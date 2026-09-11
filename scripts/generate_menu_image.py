"""
Rich Menu Graphic Generator for LINE Agricultural Chatbot.
Generates an official 2500 x 1686 PNG graphic formatted for LINE Rich Menu 2x3 grid.
"""
import os
from PIL import Image, ImageDraw, ImageFont

def generate_rich_menu_image(output_path: str = "data/rich_menu.png"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    width = 2500
    height = 1686
    img = Image.new("RGB", (width, height), "#F3F4F6")
    draw = ImageDraw.Draw(img)

    # 6 Tiles Grid (2 rows x 3 cols)
    cols = 3
    rows = 2
    tile_w = width // cols
    tile_h = height // rows

    tiles = [
        # Row 1
        {
            "col": 0, "row": 0,
            "title": "⚖️ กฎหมายโดรน CAAT",
            "subtitle": "ข้อบังคับ ความสูง และความปลอดภัย",
            "bg": "#1E3A8A", "text_color": "#FFFFFF", "sub_color": "#BFDBFE"
        },
        {
            "col": 1, "row": 0,
            "title": "📋 ขึ้นทะเบียนโดรน",
            "subtitle": "ขั้นตอน กพท. (CAAT) & กสทช.",
            "bg": "#047857", "text_color": "#FFFFFF", "sub_color": "#A7F3D0"
        },
        {
            "col": 2, "row": 0,
            "title": "🌾 เทคนิคพ่นข้าว",
            "subtitle": "ความสูง 2.5-3m / น้ำ 15-20L/ha",
            "bg": "#D97706", "text_color": "#FFFFFF", "sub_color": "#FEF3C7"
        },
        # Row 2
        {
            "col": 0, "row": 1,
            "title": "🧪 ผสมสารเคมีปลอดภัย",
            "subtitle": "ลำดับผสม WALES & อุปกรณ์ PPE",
            "bg": "#B45309", "text_color": "#FFFFFF", "sub_color": "#FDE68A"
        },
        {
            "col": 1, "row": 1,
            "title": "🛠️ การบำรุงรักษาโดรน",
            "subtitle": "ล้างหัวฉีด / แบตเตอรี่ LiPo / GPS",
            "bg": "#374151", "text_color": "#FFFFFF", "sub_color": "#D1D5DB"
        },
        {
            "col": 2, "row": 1,
            "title": "🤖 ถาม AI ผู้เชี่ยวชาญ",
            "subtitle": "พิมพ์ปรึกษาโดรนเกษตรได้ทุกเรื่อง",
            "bg": "#059669", "text_color": "#FFFFFF", "sub_color": "#D1FAE5"
        },
    ]

    # Try to load Arial or default font
    font_large = None
    font_small = None
    try:
        # Common Windows fonts
        font_large = ImageFont.truetype("tahoma.ttf", 64)
        font_small = ImageFont.truetype("tahoma.ttf", 40)
    except Exception:
        try:
            font_large = ImageFont.truetype("arial.ttf", 64)
            font_small = ImageFont.truetype("arial.ttf", 40)
        except Exception:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

    margin = 15
    for t in tiles:
        x0 = t["col"] * tile_w + margin
        y0 = t["row"] * tile_h + margin
        x1 = (t["col"] + 1) * tile_w - margin
        y1 = (t["row"] + 1) * tile_h - margin

        # Draw rounded card
        draw.rounded_rectangle([x0, y0, x1, y1], radius=35, fill=t["bg"])

        # Inner highlight border
        draw.rounded_rectangle([x0, y0, x1, y1], radius=35, outline="#FFFFFF", width=4)

        # Center Text Calculation
        center_x = (x0 + x1) / 2
        center_y = (y0 + y1) / 2

        # Draw Title
        title = t["title"]
        subtitle = t["subtitle"]
        
        draw.text((center_x, center_y - 45), title, fill=t["text_color"], font=font_large, anchor="mm")
        draw.text((center_x, center_y + 45), subtitle, fill=t["sub_color"], font=font_small, anchor="mm")

    img.save(output_path, "PNG")
    print(f"Rich menu image generated successfully at: {output_path}")

if __name__ == "__main__":
    generate_rich_menu_image()
