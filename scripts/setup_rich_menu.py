"""
Standalone setup script for LINE Rich Menu.
Run this script after configuring LINE_CHANNEL_ACCESS_TOKEN in .env
"""
import os
import sys

# Ensure root project directory is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings
from app.templates.rich_menu_config import RICH_MENU_CONFIG
from app.core.line_client import line_client
from scripts.generate_menu_image import generate_rich_menu_image

def main():
    print("=== LINE Agricultural Drone Chatbot: Rich Menu Deployment ===")
    if not settings.LINE_CHANNEL_ACCESS_TOKEN or settings.LINE_CHANNEL_ACCESS_TOKEN == "dummy_line_channel_access_token":
        print("ERROR: LINE_CHANNEL_ACCESS_TOKEN is not configured in .env file.")
        print("Please obtain a Channel Access Token from LINE Developers Console and save it to .env.")
        return

    image_path = "data/rich_menu.png"
    if not os.path.exists(image_path):
        print("Generating rich menu image...")
        generate_rich_menu_image(image_path)

    print("Uploading rich menu and setting as default...")
    menu_id = line_client.setup_rich_menu(RICH_MENU_CONFIG, image_path=image_path)
    if menu_id:
        print(f"SUCCESS: Rich menu configured and linked with ID: {menu_id}")
    else:
        print("FAILED: Could not configure rich menu on LINE.")

if __name__ == "__main__":
    main()
