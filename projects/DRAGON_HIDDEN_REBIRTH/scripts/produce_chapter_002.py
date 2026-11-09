"""
Chapter 2 Production Pipeline Execution Script
Seeds Chapter 2: The Veil of Shadows into manga_production.db and executes end-to-end production.
"""

import sqlite3
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from agents.production_manager import ProductionManager

DB_PATH = ROOT_DIR / "database" / "manga_production.db"

def seed_and_produce_chapter_002():
    print("[*] Seeding Chapter 2 into manga_production.db...")
    with sqlite3.connect(str(DB_PATH)) as conn:
        cursor = conn.cursor()

        # 1. Seed Chapter 2 Record
        cursor.execute("""
            INSERT OR REPLACE INTO chapters (id, chapter_number, title, logline, target_pages, status, reading_direction)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "ch_002", 2, "The Veil of Shadows",
            "In the subterranean library beneath the temple ghats, Aarav and Ananya decipher the ancient Fragment of Creation. As the Void stalks them, the Blue Sovereign Neel intervenes.",
            7, "GENERATING", "VERTICAL_WEBTOON"
        ))

        # 2. Seed Chapter 2 Page 1
        cursor.execute("""
            INSERT OR REPLACE INTO pages (id, chapter_id, page_number, layout_type, width_px, height_px, reading_direction, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "page_002_01", "ch_002", 1, "DYNAMIC_ACTION", 2480, 3508, "VERTICAL_WEBTOON", "PLANNED"
        ))

        # 3. Seed Page 1 Panels
        panels_data = [
            (
                "panel_002_01_01", "page_002_01", 1, 100, 100, 2280, 950, "EXTREME_WIDE",
                json.dumps(["loc_obsidian_temple"]),
                "Vast subterranean hall of carved stone temple arches, ancient Sanskrit inscriptions, moonlight streaming through high stone jali lattice, oil lamps casting golden reflections, midnight atmosphere, full color cinematic anime manhwa",
                "The silence that followed was not peace. It was the world holding its breath.",
                "NARRATOR", None, "HUMMM...", "CRACKLE", "TOP_LEFT", "FINE_TONE"
            ),
            (
                "panel_002_01_02", "page_002_01", 2, 1260, 1100, 1120, 1100, "MEDIUM_CLOSE",
                json.dumps(["char_aarav"]),
                "Aarav standing in library, messy black hair and red scarf, glowing amber eyes reflecting hovering golden diamond relic fragment with Sanskrit runes, warm atmospheric lighting, full color anime manhwa",
                "It feels like... it's breathing. Like a heart sleeping for thousands of years.",
                "Aarav", "The Fragment has chosen its wielder.", None, None, "TOP_RIGHT", "FINE_TONE"
            ),
            (
                "panel_002_01_03", "page_002_01", 3, 100, 1100, 1120, 1100, "MEDIUM_CLOSE",
                json.dumps(["char_ananya"]),
                "Ananya leaning forward with concern, violet silk saree and gold temple jewelry, white jasmine flowers in hair, warm golden lamp glow on face, full color anime manhwa",
                "The elders said the First Stories shaped reality... before the Void began erasing them.",
                "Ananya", None, None, None, "TOP_LEFT", "FINE_TONE"
            ),
            (
                "panel_002_01_04", "page_002_01", 4, 100, 2250, 2280, 1150, "WIDE_ACTION",
                json.dumps(["char_aarav"]),
                "Shifting void shadows detaching from stone walls with burning crimson eyes, Aarav thrusting hand forward igniting swirling golden fire barrier, dynamic action composition, cinematic full color",
                "Ananya... get behind me. Now!",
                "Aarav", None, "SKRRR... SKRRR...", "SLASH", "BOTTOM_CENTER", "SPEED_LINES"
            )
        ]

        for p in panels_data:
            cursor.execute("""
                INSERT OR REPLACE INTO panels (
                    id, page_id, panel_index, bbox_x, bbox_y, bbox_w, bbox_h, shot_type,
                    character_ids, visual_prompt, dialogue_text, speaker_name, thought_text,
                    sfx_text, sfx_style, balloon_position, screentone_style
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, p)

        conn.commit()
    print("[+] Chapter 2 Page 1 seeded successfully.")

    # 4. Produce Page using ProductionManager
    manager = ProductionManager(ROOT_DIR)
    result = manager.produce_page("page_002_01", prefer_cloud=True)
    
    print("\n" + "=" * 55)
    print(f"[+] CHAPTER 2 PRODUCTION COMPLETE: {result['page_id']}")
    print(f"[+] Master Page: {result['master_page_path']}")
    print(f"[+] QA Verdict: {result['qa_result']['verdict']} (Score: {result['qa_result']['overall_score']:.2f}/10)")
    print(f"[+] Elapsed: {result['elapsed_seconds']}s | Cost: INR {result['budget_spent_inr']}")
    print("=" * 55)

if __name__ == "__main__":
    seed_and_produce_chapter_002()
