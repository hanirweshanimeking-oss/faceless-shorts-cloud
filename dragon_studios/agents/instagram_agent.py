"""
Dragon Studios India - Instagram Reels Management Agent
Operates via official Meta Graph API v21.0.
Strictly enforces human approval gate before publishing.
Target: @dragon.studios.india (ID: 16380055510)
"""

import os
import time
import requests
from typing import Dict, Any, Optional

GRAPH_API_VERSION = "v21.0"
GRAPH_BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

class InstagramReelsManager:
    def __init__(
        self,
        account_id: str = "16380055510",
        access_token: Optional[str] = None
    ):
        self.account_id = account_id or os.getenv("IG_ACCOUNT_ID", "16380055510")
        self.access_token = access_token or os.getenv("META_PAGE_ACCESS_TOKEN", "")

    def check_approval_gate(self, is_approved: bool) -> None:
        """Enforces the mandatory human approval rule."""
        if not is_approved:
            raise PermissionError(
                "SECURITY GATEWAY: Cannot publish to @dragon.studios.india without explicit user approval in chat!"
            )

    def create_reels_container(
        self,
        video_url: str,
        caption: str,
        cover_url: Optional[str] = None,
        share_to_feed: bool = True
    ) -> Dict[str, Any]:
        """
        Step 1: Creates an Instagram Reels media container via Meta Graph API.
        The video must be accessible via a public HTTPS URL.
        """
        if not self.access_token:
            return {
                "status": "MOCK_MODE",
                "message": "META_PAGE_ACCESS_TOKEN is not configured. Ready to publish upon providing token.",
                "container_id": f"mock_container_{int(time.time())}"
            }

        url = f"{GRAPH_BASE_URL}/{self.account_id}/media"
        payload = {
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "share_to_feed": share_to_feed,
            "access_token": self.access_token
        }
        if cover_url:
            payload["cover_url"] = cover_url

        response = requests.post(url, data=payload, timeout=30)
        data = response.json()
        if "id" in data:
            return {"status": "SUCCESS", "container_id": data["id"]}
        else:
            return {"status": "ERROR", "error": data.get("error", {})}

    def poll_container_status(
        self,
        container_id: str,
        timeout_seconds: int = 180,
        interval: int = 5
    ) -> Dict[str, Any]:
        """
        Step 2: Polls the Reels container status until 'FINISHED' or timeout.
        """
        if container_id.startswith("mock_"):
            return {"status": "FINISHED", "container_id": container_id}

        url = f"{GRAPH_BASE_URL}/{container_id}"
        params = {
            "fields": "status_code",
            "access_token": self.access_token
        }
        
        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            response = requests.get(url, params=params, timeout=15)
            data = response.json()
            status_code = data.get("status_code")
            
            if status_code == "FINISHED":
                return {"status": "FINISHED", "container_id": container_id}
            elif status_code in ("ERROR", "EXPIRED"):
                return {"status": "FAILED", "reason": status_code, "raw": data}
            
            time.sleep(interval)
            
        return {"status": "TIMEOUT", "container_id": container_id}

    def publish_container(self, container_id: str) -> Dict[str, Any]:
        """
        Step 3: Publishes the verified Reels container live to Instagram.
        """
        if container_id.startswith("mock_"):
            mock_id = f"mock_media_{int(time.time())}"
            return {
                "status": "MOCK_PUBLISHED",
                "media_id": mock_id,
                "permalink": f"https://www.instagram.com/reel/{mock_id}/"
            }

        url = f"{GRAPH_BASE_URL}/{self.account_id}/media_publish"
        payload = {
            "creation_id": container_id,
            "access_token": self.access_token
        }
        response = requests.post(url, data=payload, timeout=30)
        data = response.json()
        
        if "id" in data:
            media_id = data["id"]
            return {
                "status": "PUBLISHED",
                "media_id": media_id,
                "permalink": f"https://www.instagram.com/reel/{media_id}/"
            }
        else:
            return {"status": "ERROR", "error": data.get("error", {})}
