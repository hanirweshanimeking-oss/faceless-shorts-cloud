"""
Faceless Shorts Mass Production Engine
Renders the complete queue of scheduled reels autonomously into E:\\faceless_shorts_vault\\
Supports multi-worker parallel execution, progress tracking, and self-healing error recovery.
"""
import os
import sys
import time
import sqlite3
import datetime
import concurrent.futures
from typing import List, Dict, Any, Optional

from faceless_engine.scheduler_vault import (
    DB_PATH,
    VAULT_DIR,
    render_scheduled_reel
)

def get_pending_reels() -> List[Dict[str, Any]]:
    """Fetches all scheduled reels awaiting render from SQLite."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT id, date_str, slot_number, scheduled_time, title, pillar, style
            FROM scheduled_reels
            WHERE status = 'SCHEDULED'
            ORDER BY date_str ASC, slot_number ASC
            """
        ).fetchall()
        return [dict(r) for r in rows]

def get_stats() -> Dict[str, int]:
    """Returns database counts by status."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        total = cursor.execute("SELECT COUNT(*) FROM scheduled_reels").fetchone()[0]
        ready = cursor.execute("SELECT COUNT(*) FROM scheduled_reels WHERE status = 'READY'").fetchone()[0]
        rendering = cursor.execute("SELECT COUNT(*) FROM scheduled_reels WHERE status = 'RENDERING'").fetchone()[0]
        failed = cursor.execute("SELECT COUNT(*) FROM scheduled_reels WHERE status = 'FAILED'").fetchone()[0]
        scheduled = cursor.execute("SELECT COUNT(*) FROM scheduled_reels WHERE status = 'SCHEDULED'").fetchone()[0]
        return {
            "total": total,
            "ready": ready,
            "rendering": rendering,
            "failed": failed,
            "scheduled": scheduled
        }

def run_mass_production(workers: int = 2, max_reels: Optional[int] = None):
    """
    Mass production runner:
    Processes the entire queue using parallel workers until all scheduled reels are created.
    """
    t0 = time.time()
    stats = get_stats()
    
    print("=" * 75)
    print("🚀 STARTING MASS FACELESS SHORTS PRODUCTION ENGINE")
    print(f"📊 Total Calendar Slots: {stats['total']} reels (Nov 8, 2026 ➔ Jan 14, 2027)")
    print(f"✅ Already in Vault: {stats['ready']} reels | ⏳ Remaining to render: {stats['scheduled']}")
    print(f"⚙️ Parallel CPU Workers: {workers} | 📁 Vault: {VAULT_DIR}")
    print("=" * 75)

    pending = get_pending_reels()
    if max_reels:
        pending = pending[:max_reels]

    if not pending:
        print("[MassProduction] All reels are already rendered and ready in the vault!")
        return

    print(f"[MassProduction] Queued {len(pending)} reels for continuous production.\n")

    completed = 0
    failed_count = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        # Submit pending reels
        future_to_reel = {
            executor.submit(render_scheduled_reel, r["id"]): r
            for r in pending
        }

        for future in concurrent.futures.as_completed(future_to_reel):
            reel = future_to_reel[future]
            rid = reel["id"]
            try:
                out_path = future.result()
                if out_path and os.path.exists(out_path):
                    completed += 1
                    current_stats = get_stats()
                    pct = round((current_stats["ready"] / current_stats["total"]) * 100, 1)
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ✅ [PROGRESS {current_stats['ready']}/{current_stats['total']} ({pct}%)] Done: '{reel['title']}' -> {os.path.basename(out_path)}")
                else:
                    failed_count += 1
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ⚠️ Failed: '{reel['title']}' ({rid})")
            except Exception as e:
                failed_count += 1
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ❌ Error on '{reel['title']}': {e}")

    elapsed_min = round((time.time() - t0) / 60, 1)
    final_stats = get_stats()
    print("\n" + "=" * 75)
    print(f"🏁 MASS BATCH COMPLETE IN {elapsed_min} MINUTES!")
    print(f"✅ Total Ready in Vault: {final_stats['ready']} / {final_stats['total']}")
    print(f"📁 Vault Path: {VAULT_DIR}")
    print("=" * 75)

if __name__ == "__main__":
    workers = 2
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        workers = int(sys.argv[1])
    run_mass_production(workers=workers)
