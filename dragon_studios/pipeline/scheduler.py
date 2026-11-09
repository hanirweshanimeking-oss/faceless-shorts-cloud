"""
Dragon Studios India - Studio Automation & Production Scheduler
Handles scheduled daily content production, idea generation, automated editing,
and weekly performance digest reporting.
"""

import time
import schedule
from datetime import datetime
from typing import Dict, Any

from dragon_studios.pipeline.orchestrator import StudioOrchestrator
from dragon_studios.database.db_manager import list_projects, save_growth_insight
from dragon_studios.agents.analytics_agent import evaluate_reels_performance

class StudioScheduler:
    def __init__(self, videos_per_day: int = 1):
        self.videos_per_day = videos_per_day
        self.orchestrator = StudioOrchestrator()
        self.current_pillar_idx = 0
        self.pillars = ["DARK_PSYCHOLOGY", "ORIGINAL_MANGA"]

    def run_daily_production_job(self) -> None:
        """Executes the daily automated video creation run."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [SCHEDULER] Starting automated daily video production...")

        for i in range(self.videos_per_day):
            pillar = self.pillars[self.current_pillar_idx % len(self.pillars)]
            self.current_pillar_idx += 1
            
            print(f"[{timestamp}] [SCHEDULER] Producing video #{i+1} under Pillar: {pillar}")
            try:
                result = self.orchestrator.create_production_run(pillar=pillar)
                print(f"[{timestamp}] [SCHEDULER] Video #{i+1} ready for human approval: Project ID '{result['project_id']}'")
            except Exception as e:
                print(f"[{timestamp}] [SCHEDULER] Production failed: {e}")

    def run_analytics_sync_job(self) -> None:
        """Daily sync to fetch engagement signals and update learning database."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [SCHEDULER] Syncing social media analytics...")
        # Simulates fetching latest performance data for active published media
        projects = list_projects(limit=5)
        for p in projects:
            if p["status"] == "PUBLISHED":
                # Evaluate and log performance
                eval_res = evaluate_reels_performance(
                    views=1500,
                    reach=1200,
                    likes=180,
                    comments=24,
                    shares=35,
                    saves=52,
                    watch_time_seconds=22.0,
                    video_duration=25.0
                )
                print(f"[{timestamp}] [SCHEDULER] Evaluated '{p['title']}': Score {eval_res['overall_score']}")

    def start(self, daily_time: str = "18:00") -> None:
        """Starts the scheduling loop."""
        print(f"[SCHEDULER] Initialized. Target: {self.videos_per_day} videos/day at {daily_time}.")
        schedule.every().day.at(daily_time).do(self.run_daily_production_job)
        schedule.every().day.at("23:30").do(self.run_analytics_sync_job)

        # Run one immediate job upon launch if desired
        print("[SCHEDULER] Running background watcher loop. Press Ctrl+C to terminate.")
        try:
            while True:
                schedule.run_pending()
                time.sleep(30)
        except KeyboardInterrupt:
            print("[SCHEDULER] Stopped.")

if __name__ == "__main__":
    scheduler = StudioScheduler(videos_per_day=1)
    scheduler.run_daily_production_job()
