"""
Dragon Studios India - Stage 8: Publishing & Multi-Platform Packaging Agent
Generates production-ready distribution bundles for Instagram Reels, YouTube Shorts,
and TikTok, complete with formatted copy, hashtags, and metadata.
"""

import os
import json
import shutil
from typing import Dict, Any, Optional
from pydantic import BaseModel
from dragon_studios.agents.composio_publisher import ComposioPublisherHub

class PlatformMetadata(BaseModel):
    title: str
    caption: str
    hashtags: str
    optimal_time_ist: str
    tags: list[str]

class PublishingBundle(BaseModel):
    project_id: str
    bundle_dir: str
    master_video_path: str
    instagram: PlatformMetadata
    youtube: PlatformMetadata
    tiktok: PlatformMetadata

class PublishingAgent:
    @staticmethod
    def prepare_release_bundle(
        project_id: str,
        title: str,
        pillar: str,
        caption: str,
        hashtags: str,
        master_video_path: str,
        output_dir: str,
        qa_score: float = 90.0
    ) -> Dict[str, Any]:
        """
        Builds a complete multi-platform release bundle.
        """
        bundle_dir = os.path.join(output_dir, project_id, "publish_bundle")
        os.makedirs(bundle_dir, exist_ok=True)

        # Copy master video to bundle
        bundled_video = os.path.join(bundle_dir, "master_vertical_9_16.mp4")
        if os.path.exists(master_video_path):
            shutil.copy2(master_video_path, bundled_video)

        # Platform specific tailoring
        # Instagram
        ig_caption = f"{caption}\n\n{hashtags}"
        ig_metadata = {
            "platform": "INSTAGRAM_REELS",
            "account": "@dragon.studios.india",
            "caption": ig_caption,
            "optimal_posting_window": "7:00 PM - 9:30 PM IST (Peak Engagement)",
            "cover_frame_sec": 1.0,
            "allow_audio_remixing": True
        }

        # YouTube Shorts (Title < 60 chars)
        short_title = (title[:50] + " #shorts") if len(title) > 50 else f"{title} #shorts"
        yt_metadata = {
            "platform": "YOUTUBE_SHORTS",
            "channel": "Dragon Studios India",
            "title": short_title,
            "description": f"{caption}\n\nSubscribe to Dragon Studios India for daily dark anime storytelling & psychology.\n\n#Shorts #Anime #Psychology",
            "tags": ["Shorts", "Anime", "Dark Psychology", "Dragon Studios", "Mindset", "Stoicism"],
            "category_id": "24", # Entertainment
            "privacy_status": "public"
        }

        # TikTok
        tt_metadata = {
            "platform": "TIKTOK",
            "caption": f"{title} ♟️ #anime #stoic #darkpsychology #dragonstudios #fyp",
            "commercial_audio": False
        }

        # Write metadata JSON files
        with open(os.path.join(bundle_dir, "instagram_metadata.json"), "w", encoding="utf-8") as f:
            json.dump(ig_metadata, f, indent=2)

        with open(os.path.join(bundle_dir, "youtube_metadata.json"), "w", encoding="utf-8") as f:
            json.dump(yt_metadata, f, indent=2)

        with open(os.path.join(bundle_dir, "tiktok_metadata.json"), "w", encoding="utf-8") as f:
            json.dump(tt_metadata, f, indent=2)

        # Write clean copy-paste caption text file for mobile phone sharing
        copy_paste_file = os.path.join(bundle_dir, "copy_paste_caption.txt")
        with open(copy_paste_file, "w", encoding="utf-8") as f:
            f.write(ig_caption)

        # Trigger Composio Multi-Platform Syndication (YouTube Shorts, Instagram, Notion, Discord/Slack)
        composio_hub = ComposioPublisherHub()
        syndication_results = composio_hub.syndicate_all(
            project_id=project_id,
            title=title,
            pillar=pillar,
            caption=caption,
            hashtags=hashtags,
            master_video_path=bundled_video,
            qa_score=qa_score,
            output_dir=output_dir
        )

        manifest = {
            "project_id": project_id,
            "status": "PACKAGED_FOR_DISTRIBUTION",
            "bundle_dir": bundle_dir,
            "video_file": bundled_video,
            "copy_paste_file": copy_paste_file,
            "platforms": ["INSTAGRAM_REELS", "YOUTUBE_SHORTS", "TIKTOK", "NOTION", "DISCORD", "SLACK"],
            "composio_syndication": syndication_results
        }

        with open(os.path.join(bundle_dir, "bundle_manifest.json"), "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        return manifest
