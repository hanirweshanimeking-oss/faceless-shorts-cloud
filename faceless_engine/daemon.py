"""
Faceless Shorts Autonomous Scheduler Daemon
Continuously runs in the background:
1. Monitors the 680-slot master schedule in dragon_studios.db
2. Pre-renders upcoming reels in advance into E:\\faceless_shorts_vault\\
3. Prepares 1-click mobile copy-paste bundles and API triggers for Instagram & YouTube
"""
import os
import sys
import time
import json
import sqlite3
import datetime
from typing import Dict, Any, List

from faceless_engine.scheduler_vault import (
    DB_PATH,
    VAULT_DIR,
    render_scheduled_reel,
    render_batch_for_date
)

def run_scheduler_daemon(poll_interval_sec: int = 60, pre_render_ahead_count: int = 5):
    """
    Main loop for autonomous scheduling & pre-rendering.
    """
    print("=" * 70)
    print("🕒 FACELESS SHORTS AUTONOMOUS SCHEDULER DAEMON ACTIVE")
    print(f"📌 Database: {DB_PATH}")
    print(f"📌 Storage Vault: {VAULT_DIR}")
    print(f"📌 Polling Interval: {poll_interval_sec}s | Pre-render buffer: {pre_render_ahead_count} reels")
    print("=" * 70)

    while True:
        try:
            now = datetime.datetime.now()
            today_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M")
            
            with sqlite3.connect(DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                # 1. Find upcoming unrendered reels
                cursor = conn.cursor()
                unrendered = cursor.execute(
                    """
                    SELECT id, title, scheduled_time FROM scheduled_reels
                    WHERE status = 'SCHEDULED'
                    ORDER BY scheduled_time ASC
                    LIMIT ?
                    """,
                    (pre_render_ahead_count,)
                ).fetchall()
                
            if unrendered:
                print(f"[{time_str}] Found {len(unrendered)} reels awaiting render. Starting pre-render pipeline...")
                for r in unrendered:
                    reel_id = r["id"]
                    print(f"[{time_str}] Pre-rendering: '{r['title']}' (ID: {reel_id}, Scheduled: {r['scheduled_time']})")
                    render_scheduled_reel(reel_id)
            else:
                print(f"[{time_str}] All upcoming reels in buffer are pre-rendered and ready in {VAULT_DIR}.")

            # 2. Check for reels scheduled to be published right now
            current_timestamp = now.strftime("%Y-%m-%d %H:%M")
            with sqlite3.connect(DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                due_reels = conn.execute(
                    """
                    SELECT * FROM scheduled_reels
                    WHERE status = 'READY' AND scheduled_time <= ? AND scheduled_time >= ?
                    """,
                    (current_timestamp + ":59", (now - datetime.timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:00"))
                ).fetchall()

            for d in due_reels:
                print(f"[{time_str}] 🚀 REEL DUE FOR PUBLICATION: '{d['title']}' ({d['id']})")
                # Package distribution bundle
                bundle_dir = os.path.join(VAULT_DIR, "daily_bundles", today_str, f"slot_{d['slot_number']}")
                os.makedirs(bundle_dir, exist_ok=True)
                
                # Copy caption
                with open(os.path.join(bundle_dir, "caption_instagram.txt"), "w", encoding="utf-8") as f:
                    f.write(f"{d['caption']}\n\n{d['hashtags']}")
                    
                with open(os.path.join(bundle_dir, "metadata_youtube.txt"), "w", encoding="utf-8") as f:
                    f.write(f"Title: {d['yt_title']}\n\nDescription:\n{d['yt_description']}\n\nTags: {d['yt_tags']}")

                print(f"[{time_str}] ✓ Packaging bundle ready at: {bundle_dir}")

        except Exception as e:
            print(f"[Daemon Error] {e}")

        time.sleep(poll_interval_sec)

if __name__ == "__main__":
    run_scheduler_daemon()
