"""
Faceless Shorts Automation - Cloud Publisher & Telegram Delivery Engine
Publishes to YouTube Shorts, Instagram Reels, and delivers video directly to Telegram.
"""
import os
import sys
import argparse
import json
import logging
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CloudPublisher")

def deliver_to_telegram(video_path: str, prompt: str, style: str, bot_token: str, chat_id: str) -> bool:
    """Delivers the master 1080x1920 MP4 directly to Hanirwesh on Telegram."""
    if not bot_token or not chat_id:
        logger.warning("Telegram credentials missing, skipping direct video delivery.")
        return False
        
    logger.info(f"Uploading {video_path} ({os.path.getsize(video_path):,} bytes) to Telegram chat {chat_id}...")
    url = f"https://api.telegram.org/bot{bot_token}/sendVideo"
    caption = (
        f"🎬 *YOUR VIRAL REEL IS READY!*\n\n"
        f"📌 *Topic:* {prompt}\n"
        f"🎨 *Style:* {style}\n"
        f"⚡ *Rendered 100% in Cloud (PC Off Mode)*\n"
        f"📱 *1080x1920 (9:16) with Yellow Captions & Foley*\n\n"
        f"#FacelessShorts #AIReels #TallTale3D #Animation"
    )
    try:
        with open(video_path, "rb") as f:
            files = {"video": (os.path.basename(video_path), f, "video/mp4")}
            data = {
                "chat_id": chat_id,
                "caption": caption,
                "parse_mode": "Markdown",
                "supports_streaming": True
            }
            res = requests.post(url, data=data, files=files, timeout=180)
            if res.status_code == 200:
                logger.info("✓ Video successfully delivered to Telegram!")
                return True
            else:
                logger.error(f"Telegram API error {res.status_code}: {res.text}")
                return False
    except Exception as e:
        logger.error(f"Failed to deliver video to Telegram: {e}")
        return False

def publish_to_composio(video_path: str, prompt: str, platforms: str, composio_key: str) -> dict:
    """Attempts live multi-platform publishing via Composio Gateway."""
    report = {"youtube": "SKIPPED", "instagram": "SKIPPED"}
    if not composio_key:
        logger.info("COMPOSIO_API_KEY not configured. Generating publication manifests.")
        return report

    try:
        from composio import Composio, Action
        client = Composio(api_key=composio_key)
        
        # 1. YouTube Shorts
        if "ALL" in platforms.upper() or "YOUTUBE" in platforms.upper():
            try:
                logger.info("Publishing to YouTube Shorts via Composio...")
                yt_res = client.actions.execute(
                    action=getattr(Action, "YOUTUBE_UPLOAD_VIDEO", "YOUTUBE_UPLOAD_VIDEO"),
                    params={
                        "title": f"{prompt[:80]} #Shorts",
                        "description": f"{prompt}\n\n#Shorts #Viral #Story #Animation",
                        "tags": ["Shorts", "Viral", "Story", "Tall Tale 3D"],
                        "video_file_path": video_path,
                        "privacy_status": "public"
                    }
                )
                report["youtube"] = "PUBLISHED"
                logger.info(f"✓ YouTube Shorts publish result: {yt_res}")
            except Exception as e:
                logger.warning(f"YouTube Shorts upload via Composio notice: {e}")
                report["youtube"] = f"PENDING_CONNECTION ({e})"

        # 2. Instagram Reels
        if "ALL" in platforms.upper() or "INSTAGRAM" in platforms.upper():
            try:
                logger.info("Publishing to Instagram Reels via Composio...")
                ig_res = client.actions.execute(
                    action=getattr(Action, "INSTAGRAM_CREATE_POST", "INSTAGRAM_CREATE_POST"),
                    params={
                        "media_type": "REELS",
                        "video_url_or_path": video_path,
                        "caption": f"{prompt}\n.\n.\n#reels #viral #explorepage #animation #story"
                    }
                )
                report["instagram"] = "PUBLISHED"
                logger.info(f"✓ Instagram Reels publish result: {ig_res}")
            except Exception as e:
                logger.warning(f"Instagram Reels upload via Composio notice: {e}")
                report["instagram"] = f"PENDING_CONNECTION ({e})"

    except Exception as e:
        logger.warning(f"Composio client init or action error: {e}")
        
    return report

def send_telegram_alert(bot_token: str, chat_id: str, message: str):
    """Sends a text status message to Telegram."""
    if not bot_token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        logger.warning(f"Telegram alert error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Cloud Reel Publisher & Telegram Delivery")
    parser.add_argument("--video", type=str, required=True, help="Path to final .mp4 video")
    parser.add_argument("--prompt", type=str, required=True, help="Video title / topic")
    parser.add_argument("--style", type=str, default="Tall Tale 3D", help="Visual style")
    parser.add_argument("--platforms", type=str, default="ALL", help="ALL, YOUTUBE, INSTAGRAM, TELEGRAM")
    parser.add_argument("--slug", type=str, default="reel_out", help="Project slug")
    args = parser.parse_args()

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    composio_key = os.getenv("COMPOSIO_API_KEY", "").strip()

    if not os.path.exists(args.video):
        logger.error(f"Video file not found: {args.video}")
        send_telegram_alert(bot_token, chat_id, f"❌ *Cloud Render Error:* Video output missing for `{args.prompt}`.")
        sys.exit(1)

    # 1. Deliver to Telegram
    delivered = deliver_to_telegram(args.video, args.prompt, args.style, bot_token, chat_id)

    # 2. Publish to YouTube & Instagram
    pub_report = publish_to_composio(args.video, args.prompt, args.platforms, composio_key)

    # 3. Status summary notification
    summary_msg = (
        f"📊 *CLOUD DISTRIBUTION REPORT*\n\n"
        f"📌 *Project:* `{args.slug}`\n"
        f"📱 *Telegram Delivery:* {'✓ Sent to phone' if delivered else '⚠️ Failed'}\n"
        f"🔴 *YouTube Shorts:* {pub_report.get('youtube')}\n"
        f"📸 *Instagram Reels:* {pub_report.get('instagram')}\n\n"
        f"💡 _Everything ran autonomously on GitHub Actions with zero local PC compute!_"
    )
    send_telegram_alert(bot_token, chat_id, summary_msg)
    
    # Save report
    out_dir = os.path.dirname(args.video)
    with open(os.path.join(out_dir, "publish_report.json"), "w", encoding="utf-8") as f:
        json.dump({"prompt": args.prompt, "style": args.style, "telegram_delivered": delivered, "publishing": pub_report}, f, indent=2)

    logger.info("Publishing and delivery workflow completed successfully.")

if __name__ == "__main__":
    main()
