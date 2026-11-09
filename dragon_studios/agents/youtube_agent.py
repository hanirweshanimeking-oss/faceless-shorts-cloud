"""
Dragon Studios India - YouTube Publishing & Management Agent
Operates via official Google YouTube Data API v3.
Supports YouTube Shorts and long-form uploads with resumable chunking.
Strictly enforces human approval gate before publishing.
"""

import os
import json
from typing import Dict, Any, Optional

class YouTubeManager:
    def __init__(
        self,
        client_secret_file: Optional[str] = None,
        credentials_pickle: Optional[str] = None
    ):
        self.client_secret_file = client_secret_file or os.getenv("YOUTUBE_CLIENT_SECRET_FILE", "config/client_secret.json")
        self.credentials_pickle = credentials_pickle or os.getenv("YOUTUBE_TOKEN_PICKLE", "config/youtube_token.pickle")

    def check_approval_gate(self, is_approved: bool) -> None:
        """Enforces mandatory human confirmation before upload."""
        if not is_approved:
            raise PermissionError(
                "SECURITY GATEWAY: Cannot publish to YouTube without explicit user approval in chat!"
            )

    def prepare_metadata(
        self,
        title: str,
        description: str,
        tags: list,
        is_short: bool = True
    ) -> Dict[str, Any]:
        """Prepares standard YouTube snippet and status payload."""
        final_title = title
        if is_short and "#Shorts" not in title:
            final_title = f"{title} #Shorts"
            
        final_tags = list(set(tags + ["Shorts", "Anime", "Dragon Studios India", "Chitran"]))
        
        return {
            "snippet": {
                "title": final_title[:100],
                "description": description,
                "tags": final_tags[:20],
                "categoryId": "1"  # Film & Animation
            },
            "status": {
                "privacyStatus": "public",  # or 'unlisted' for preview
                "selfDeclaredMadeForKids": False
            }
        }

    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: list,
        is_approved: bool = False,
        privacy_status: str = "public"
    ) -> Dict[str, Any]:
        """
        Executes a resumable upload to YouTube via official API.
        Enforces human approval check.
        """
        self.check_approval_gate(is_approved)

        if not os.path.exists(self.client_secret_file):
            # Safe Fallback: Return pre-upload preview package
            return {
                "status": "MOCK_PUBLISHED",
                "message": "client_secret.json not found in config/. Ready to publish once OAuth credentials are saved.",
                "video_id": "mock_yt_vid_101",
                "video_url": "https://youtube.com/shorts/mock_yt_vid_101",
                "title": title
            }

        # Real Google API upload workflow (when client_secret.json is provided)
        try:
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
            import pickle

            with open(self.credentials_pickle, "rb") as token:
                credentials = pickle.load(token)

            youtube = build("youtube", "v3", credentials=credentials)
            
            body = self.prepare_metadata(title, description, tags, is_short=True)
            body["status"]["privacyStatus"] = privacy_status
            
            media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
            request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
            
            response = request.execute()
            video_id = response.get("id")
            
            return {
                "status": "PUBLISHED",
                "video_id": video_id,
                "video_url": f"https://youtube.com/shorts/{video_id}",
                "title": title
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e)
            }
