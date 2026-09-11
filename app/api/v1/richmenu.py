"""
Rich Menu Management Endpoints.
Allows programmatic triggering of Rich Menu creation, image generation, and association.
"""
import os
from fastapi import APIRouter
from app.models.schemas import RichMenuSetupResponse
from app.templates.rich_menu_config import RICH_MENU_CONFIG
from app.core.line_client import line_client

router = APIRouter()

@router.get("/richmenu/config")
async def get_rich_menu_config():
    """Returns the current 2x3 Rich Menu configuration JSON."""
    return RICH_MENU_CONFIG

@router.post("/richmenu/setup", response_model=RichMenuSetupResponse)
async def setup_rich_menu_endpoint():
    """
    Creates and sets the default rich menu using the LINE Messaging API.
    """
    from scripts.generate_menu_image import generate_rich_menu_image
    
    image_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "rich_menu.png")
    image_path = os.path.abspath(image_path)
    if not os.path.exists(image_path):
        generate_rich_menu_image(image_path)

    rich_menu_id = line_client.setup_rich_menu(RICH_MENU_CONFIG, image_path=image_path)
    if rich_menu_id:
        return RichMenuSetupResponse(
            status="success",
            rich_menu_id=rich_menu_id,
            message="Rich menu created and set as default successfully."
        )
    else:
        return RichMenuSetupResponse(
            status="skipped_or_failed",
            rich_menu_id=None,
            message="Rich menu deployment skipped (check LINE_CHANNEL_ACCESS_TOKEN in .env) or error occurred."
        )
