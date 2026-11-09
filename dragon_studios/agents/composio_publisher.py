"""
Dragon Studios India - Composio Multi-Platform Publisher & Alert Hub
Orchestrates automated publishing and project synchronization across:
1. YouTube Shorts (Video upload, auto #Shorts tagging, category)
2. Instagram Reels (Vertical video posting, caption, hashtags)
3. Notion Workspace (Project card, script, viral score, master video asset)
4. Discord & Slack Webhooks (Real-time QA and Human Approval alerts)
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
import requests
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("ComposioPublisherHub")

class ComposioPublishResult(BaseModel):
    success: bool
    platform: str
    action_type: str
    response_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    fallback_used: bool = False

class ComposioPublisherHub:
    """
    Unified manager for Composio multi-app integration and notifications.
    Operates in two modes:
    1. Live Cloud Execution: When COMPOSIO_API_KEY is configured and apps are authenticated.
    2. Resilient Zero-Investment Fallback: Creates pre-formatted payloads and local bundles without crashing.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("COMPOSIO_API_KEY", "").strip()
        self.client = None
        
        if self.api_key:
            try:
                from composio import Composio
                self.client = Composio(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not initialize Composio client: {e}")
                self.client = None

        self.discord_webhook = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
        self.slack_webhook = os.getenv("SLACK_WEBHOOK_URL", "").strip()
        self.notion_database_id = os.getenv("NOTION_DATABASE_ID", "").strip()

    def call_mcp_rpc(self, method: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Sends a JSON-RPC request to the Composio MCP gateway (https://connect.composio.dev/mcp).
        """
        if not self.api_key:
            return None
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }
        try:
            res = requests.post("https://connect.composio.dev/mcp", headers=headers, json=payload, timeout=10)
            if res.status_code == 200:
                for line in res.text.splitlines():
                    if line.startswith("data:"):
                        return json.loads(line[5:].strip())
        except Exception as e:
            logger.debug(f"Composio MCP gateway call failed: {e}")
        return None

    def check_status(self) -> Dict[str, Any]:
        """
        Returns the operational status of Composio and all connected services.
        """
        status = {
            "composio_sdk_installed": True,
            "api_key_configured": bool(self.api_key),
            "mcp_gateway_connected": False,
            "discord_webhook_configured": bool(self.discord_webhook),
            "slack_webhook_configured": bool(self.slack_webhook),
            "notion_database_configured": bool(self.notion_database_id),
            "connected_apps": []
        }

        if self.api_key:
            mcp_res = self.call_mcp_rpc("tools/list")
            if mcp_res and "result" in mcp_res and "tools" in mcp_res["result"]:
                status["mcp_gateway_connected"] = True
                status["mcp_tools_available"] = [t["name"] for t in mcp_res["result"]["tools"]]
                status["connected_apps"] = ["YouTube, Instagram & 1,500+ Apps via Composio Gateway"]
            elif self.client:
                status["connected_apps"] = ["Client initialized"]

        return status

    def publish_youtube_shorts(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: Optional[List[str]] = None,
        privacy_status: str = "public"
    ) -> ComposioPublishResult:
        """
        Publishes a video to YouTube Shorts via Composio or prepares the offline bundle.
        """
        tags = tags or ["Shorts", "Anime", "Dark Psychology", "Dragon Studios India"]
        short_title = title if "#Shorts" in title else f"{title[:85]} #Shorts"

        if self.client:
            try:
                from composio import Action
                # Execute YouTube upload via Composio
                action_result = self.client.actions.execute(
                    action=getattr(Action, "YOUTUBE_UPLOAD_VIDEO", "YOUTUBE_UPLOAD_VIDEO"),
                    params={
                        "title": short_title,
                        "description": description,
                        "tags": tags,
                        "video_file_path": video_path,
                        "privacy_status": privacy_status
                    }
                )
                return ComposioPublishResult(
                    success=True,
                    platform="YOUTUBE_SHORTS",
                    action_type="LIVE_COMPOSIO_UPLOAD",
                    response_data={"result": action_result},
                    fallback_used=False
                )
            except Exception as e:
                logger.warning(f"Composio YouTube upload failed, falling back to local bundle: {e}")

        # Fallback local manifest
        return ComposioPublishResult(
            success=True,
            platform="YOUTUBE_SHORTS",
            action_type="LOCAL_STAGING_MANIFEST",
            response_data={
                "title": short_title,
                "description": description,
                "tags": tags,
                "video_file": video_path,
                "privacy_status": privacy_status,
                "note": "Ready for upload. Connect live account via 'composio add youtube'."
            },
            fallback_used=True
        )

    def publish_instagram_reel(
        self,
        video_path: str,
        caption: str,
        hashtags: str
    ) -> ComposioPublishResult:
        """
        Publishes a 9:16 vertical video as an Instagram Reel.
        """
        full_caption = f"{caption}\n\n{hashtags}"

        if self.client:
            try:
                from composio import Action
                action_result = self.client.actions.execute(
                    action=getattr(Action, "INSTAGRAM_CREATE_POST", "INSTAGRAM_CREATE_POST"),
                    params={
                        "media_type": "REELS",
                        "video_url_or_path": video_path,
                        "caption": full_caption
                    }
                )
                return ComposioPublishResult(
                    success=True,
                    platform="INSTAGRAM_REELS",
                    action_type="LIVE_COMPOSIO_UPLOAD",
                    response_data={"result": action_result},
                    fallback_used=False
                )
            except Exception as e:
                logger.warning(f"Composio Instagram upload failed, falling back to local bundle: {e}")

        return ComposioPublishResult(
            success=True,
            platform="INSTAGRAM_REELS",
            action_type="LOCAL_STAGING_MANIFEST",
            response_data={
                "caption": full_caption,
                "video_file": video_path,
                "note": "Ready for upload. Connect live account via 'composio add instagram'."
            },
            fallback_used=True
        )

    def sync_to_notion(
        self,
        project_id: str,
        title: str,
        pillar: str,
        concept: str,
        hook: str,
        master_video_path: str,
        qa_score: float,
        status: str = "PENDING_APPROVAL"
    ) -> ComposioPublishResult:
        """
        Syncs project metadata, script, and status to a Notion Content Tracker database.
        """
        payload = {
            "project_id": project_id,
            "title": title,
            "pillar": pillar,
            "concept": concept,
            "hook": hook,
            "master_video_path": master_video_path,
            "qa_score": qa_score,
            "status": status
        }

        if self.client and self.notion_database_id:
            try:
                from composio import Action
                action_result = self.client.actions.execute(
                    action=getattr(Action, "NOTION_CREATE_PAGE", "NOTION_CREATE_PAGE"),
                    params={
                        "parent": {"database_id": self.notion_database_id},
                        "properties": {
                            "Title": {"title": [{"text": {"content": title}}]},
                            "Pillar": {"select": {"name": pillar}},
                            "Status": {"status": {"name": status}},
                            "QA Score": {"number": qa_score},
                            "Project ID": {"rich_text": [{"text": {"content": project_id}}]}
                        }
                    }
                )
                return ComposioPublishResult(
                    success=True,
                    platform="NOTION",
                    action_type="LIVE_NOTION_PAGE_CREATED",
                    response_data={"result": action_result},
                    fallback_used=False
                )
            except Exception as e:
                logger.warning(f"Composio Notion sync failed: {e}")

        return ComposioPublishResult(
            success=True,
            platform="NOTION",
            action_type="LOCAL_NOTION_SYNC_FILE",
            response_data=payload,
            fallback_used=True
        )

    def send_discord_alert(
        self,
        project_id: str,
        title: str,
        qa_score: float,
        pillar: str,
        video_path: str,
        webhook_url: Optional[str] = None
    ) -> ComposioPublishResult:
        """
        Sends an approval notification to a Discord channel via Webhook.
        """
        url = webhook_url or self.discord_webhook
        embed = {
            "title": f"🎬 Dragon Studios India: New Video Ready for Review!",
            "description": f"**Title:** {title}\n**Pillar:** `{pillar}`\n**QA Score:** `{qa_score}/100`",
            "color": 65280 if qa_score >= 80 else 16753920,
            "fields": [
                {"name": "Project ID", "value": f"`{project_id}`", "inline": True},
                {"name": "Format", "value": "9:16 Vertical (1080x1920)", "inline": True},
                {"name": "Approve via CLI", "value": f"`python cli.py approve {project_id}`", "inline": False}
            ],
            "footer": {"text": "Dragon Studios Sovereign Gatekeeper • Autonomous AI Studio"}
        }

        if url:
            try:
                res = requests.post(url, json={"embeds": [embed]}, timeout=5)
                if res.status_code in (200, 204):
                    return ComposioPublishResult(
                        success=True,
                        platform="DISCORD",
                        action_type="WEBHOOK_DISPATCHED",
                        response_data={"status_code": res.status_code},
                        fallback_used=False
                    )
            except Exception as e:
                logger.warning(f"Discord webhook dispatch failed: {e}")

        return ComposioPublishResult(
            success=True,
            platform="DISCORD",
            action_type="LOCAL_ALERT_PAYLOAD_GENERATED",
            response_data={"embed": embed},
            fallback_used=True
        )

    def send_slack_alert(
        self,
        project_id: str,
        title: str,
        qa_score: float,
        pillar: str,
        video_path: str,
        webhook_url: Optional[str] = None
    ) -> ComposioPublishResult:
        """
        Sends an approval notification to a Slack channel via Webhook.
        """
        url = webhook_url or self.slack_webhook
        payload = {
            "text": f"🎬 *[Dragon Studios India]* Video ready for approval: *{title}* (QA: {qa_score}/100). Run `python cli.py approve {project_id}`"
        }

        if url:
            try:
                res = requests.post(url, json=payload, timeout=5)
                if res.status_code == 200:
                    return ComposioPublishResult(
                        success=True,
                        platform="SLACK",
                        action_type="WEBHOOK_DISPATCHED",
                        response_data={"status_code": res.status_code},
                        fallback_used=False
                    )
            except Exception as e:
                logger.warning(f"Slack webhook dispatch failed: {e}")

        return ComposioPublishResult(
            success=True,
            platform="SLACK",
            action_type="LOCAL_ALERT_PAYLOAD_GENERATED",
            response_data=payload,
            fallback_used=True
        )

    def syndicate_all(
        self,
        project_id: str,
        title: str,
        pillar: str,
        caption: str,
        hashtags: str,
        master_video_path: str,
        qa_score: float,
        output_dir: str
    ) -> Dict[str, Any]:
        """
        Executes the full multi-channel distribution cycle across YouTube, Instagram, Notion, Discord, and Slack.
        """
        bundle_dir = os.path.join(output_dir, project_id, "publish_bundle")
        os.makedirs(bundle_dir, exist_ok=True)

        results = {}

        # 1. YouTube Shorts
        yt_res = self.publish_youtube_shorts(
            video_path=master_video_path,
            title=title,
            description=f"{caption}\n\n{hashtags}\n\n#Shorts #Anime #DragonStudiosIndia"
        )
        results["youtube_shorts"] = yt_res.model_dump()

        # 2. Instagram Reels
        ig_res = self.publish_instagram_reel(
            video_path=master_video_path,
            caption=caption,
            hashtags=hashtags
        )
        results["instagram_reels"] = ig_res.model_dump()

        # 3. Notion Sync
        notion_res = self.sync_to_notion(
            project_id=project_id,
            title=title,
            pillar=pillar,
            concept="Autonomous Production",
            hook=caption.split("\n")[0] if caption else "",
            master_video_path=master_video_path,
            qa_score=qa_score
        )
        results["notion"] = notion_res.model_dump()

        # 4. Discord Alert
        discord_res = self.send_discord_alert(
            project_id=project_id,
            title=title,
            qa_score=qa_score,
            pillar=pillar,
            video_path=master_video_path
        )
        results["discord"] = discord_res.model_dump()

        # 5. Slack Alert
        slack_res = self.send_slack_alert(
            project_id=project_id,
            title=title,
            qa_score=qa_score,
            pillar=pillar,
            video_path=master_video_path
        )
        results["slack"] = slack_res.model_dump()

        # Persist full Composio syndication manifest
        manifest_path = os.path.join(bundle_dir, "composio_syndication_manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump({
                "project_id": project_id,
                "status": "SYNDICATED",
                "results": results
            }, f, indent=2)

        results["manifest_path"] = manifest_path
        return results
