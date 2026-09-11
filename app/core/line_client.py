"""
LINE Messaging API v3 Client Wrapper.
Handles messaging, interactive loading indicators, and rich menu deployment.
"""
from typing import Optional, Dict, Any
from app.config import settings

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    TextMessage,
    FlexMessage,
    FlexContainer,
    ShowLoadingAnimationRequest,
    RichMenuRequest
)

class LineClientManager:
    def __init__(self):
        self.config = Configuration(access_token=settings.LINE_CHANNEL_ACCESS_TOKEN)

    def get_api(self) -> MessagingApi:
        api_client = ApiClient(self.config)
        return MessagingApi(api_client)

    def get_blob_api(self) -> MessagingApiBlob:
        api_client = ApiClient(self.config)
        return MessagingApiBlob(api_client)

    def show_loading(self, user_id: str, loading_seconds: int = 15):
        """
        Displays the animated typing indicator in LINE chat.
        Satisfies response time UX requirement during RAG query execution.
        """
        try:
            api = self.get_api()
            req = ShowLoadingAnimationRequest(
                chat_id=user_id,
                loading_seconds=loading_seconds
            )
            api.show_loading_animation(req)
        except Exception as e:
            print(f"[LineClient] Warning: Failed to trigger loading animation: {e}")

    def reply_text(self, reply_token: str, text: str):
        """Sends a plain text reply."""
        try:
            api = self.get_api()
            req = ReplyMessageRequest(
                reply_token=reply_token,
                messages=[TextMessage(text=text)]
            )
            api.reply_message(req)
        except Exception as e:
            print(f"[LineClient] Error replying text: {e}")

    def reply_flex(self, reply_token: str, alt_text: str, flex_dict: Dict[str, Any]):
        """Sends an interactive Flex Message."""
        try:
            api = self.get_api()
            container = FlexContainer.from_dict(flex_dict)
            flex_msg = FlexMessage(alt_text=alt_text, contents=container)
            req = ReplyMessageRequest(
                reply_token=reply_token,
                messages=[flex_msg]
            )
            api.reply_message(req)
        except Exception as e:
            print(f"[LineClient] Error replying flex message: {e}")

    def setup_rich_menu(self, menu_config: Dict[str, Any], image_path: Optional[str] = None) -> Optional[str]:
        """
        Creates, uploads image, and activates the default Rich Menu.
        """
        try:
            api = self.get_api()
            blob_api = self.get_blob_api()

            # 1. Create Rich Menu
            rich_menu_req = RichMenuRequest.from_dict(menu_config)
            created = api.create_rich_menu(rich_menu_request=rich_menu_req)
            rich_menu_id = created.rich_menu_id
            print(f"[LineClient] Created Rich Menu with ID: {rich_menu_id}")

            # 2. Upload image if provided
            if image_path:
                with open(image_path, "rb") as f:
                    image_bytes = f.read()
                blob_api.set_rich_menu_image(
                    rich_menu_id=rich_menu_id,
                    body=image_bytes,
                    _headers={"Content-Type": "image/png"}
                )
                print(f"[LineClient] Uploaded image to Rich Menu: {rich_menu_id}")

            # 3. Set as default
            api.set_default_rich_menu(rich_menu_id=rich_menu_id)
            print(f"[LineClient] Rich Menu {rich_menu_id} set as default for all users.")
            return rich_menu_id
        except Exception as e:
            print(f"[LineClient] Failed to setup rich menu: {e}")
            return None

line_client = LineClientManager()
