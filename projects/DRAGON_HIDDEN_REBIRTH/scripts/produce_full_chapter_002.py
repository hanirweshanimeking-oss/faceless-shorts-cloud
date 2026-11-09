"""
Production script for Chapter 2: Pages 2 and 3
Executes FLUX.1-schnell AI generation, compositing, lettering, and QA inspection.
"""

import sqlite3
import json
import sys
import os
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from agents.production_manager import ProductionManager

DB_PATH = ROOT_DIR / "database" / "manga_production.db"

def seed_and_produce_page_2_and_3():
    with sqlite3.connect(str(DB_PATH)) as conn:
        cursor = conn.cursor()

        # ================= PAGE 2 =================
        cursor.execute("""
            INSERT OR REPLACE INTO pages (id, chapter_id, page_number, layout_type, width_px, height_px, reading_direction, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "page_002_02", "ch_002", 2, "DYNAMIC_ACTION", 2480, 3508, "VERTICAL_WEBTOON", "PLANNED"
        ))

        panels_page_2 = [
            (
                "panel_002_02_01", "page_002_02", 1, 100, 100, 2280, 950, "WIDE_ACTION",
                json.dumps(["char_void_stalker"]),
                "Terrifying towering Void Stalker shadow demon erupting from stone floor, nightmarish black smoke silhouette with razor sharp claws, burning slit crimson eyes, dark smoke tendrils, crumbling ancient Sanskrit library, dynamic perspective, cinematic full color manhwa",
                "THE FRAGMENT... MUST BE ERASED FROM EXISTENCE...",
                "Void Stalker", None, "ROOOAAAR!", "EXPLOSION", "TOP_RIGHT", "SPEED_LINES"
            ),
            (
                "panel_002_02_02", "page_002_02", 2, 100, 1100, 1120, 1100, "EXTREME_CLOSE",
                json.dumps(["char_aarav"]),
                "Extreme close up of Indian teenage anime boy Aarav, blazing golden amber eyes with intense solar flame reflections, grit teeth, messy black hair, flowing crimson scarf whipped by heat, dramatic anime combat expression, 8k manhwa",
                "Not while I still remember!",
                "Aarav", None, None, None, "TOP_LEFT", "FINE_TONE"
            ),
            (
                "panel_002_02_03", "page_002_02", 3, 1260, 1100, 1120, 1100, "DYNAMIC_ACTION",
                json.dumps(["char_aarav"]),
                "Aarav thrusting both palms forward, explosive concentric rings of celestial golden solar fire bursting outward, swirling mandala fire barrier repelling shadowy black claws, blinding radiant yellow sparks, cinematic manhwa action",
                "SHIELD OF THE FIRST DAWN!",
                "Aarav", None, "FWOOOOOSH!", "SLASH", "TOP_RIGHT", "SPEED_LINES"
            ),
            (
                "panel_002_02_04", "page_002_02", 4, 100, 2250, 2280, 1150, "SPLASH_HERO",
                json.dumps(["char_neel"]),
                "Epic entrance of celestial Hindu god Neel The Blue Sovereign descending from moonlit sky through cracked stone dome, ethereal blue skin, glowing cyan trishul insignia burning on forehead, cosmic cobalt eyes, royal gold armlets, floating in air with spinning miniature blue galaxy vortex in hand, cinematic lighting, 8k manhwa",
                "Enough, vermin of the Void.",
                "Neel", None, "KRAAAACK!", "LIGHTNING", "BOTTOM_CENTER", "FINE_TONE"
            )
        ]

        for p in panels_page_2:
            cursor.execute("""
                INSERT OR REPLACE INTO panels (
                    id, page_id, panel_index, bbox_x, bbox_y, bbox_w, bbox_h, shot_type,
                    character_ids, visual_prompt, dialogue_text, speaker_name, thought_text,
                    sfx_text, sfx_style, balloon_position, screentone_style
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, p)

        # ================= PAGE 3 =================
        cursor.execute("""
            INSERT OR REPLACE INTO pages (id, chapter_id, page_number, layout_type, width_px, height_px, reading_direction, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "page_002_03", "ch_002", 3, "DYNAMIC_ACTION", 2480, 3508, "VERTICAL_WEBTOON", "PLANNED"
        ))

        panels_page_3 = [
            (
                "panel_002_03_01", "page_002_03", 1, 100, 100, 2280, 950, "WIDE_ACTION",
                json.dumps(["char_neel"]),
                "Neel clenching glowing fist, massive cosmic blue shockwave vortex expanding across the stone temple, disintegrating shadowy void demons into sparkling blue cosmic stardust and light particles, cinematic wide angle, 8k manhwa",
                "Return to nothingness.",
                "Neel", None, "SHRRR-BOOOOM!", "EXPLOSION", "TOP_LEFT", "SPEED_LINES"
            ),
            (
                "panel_002_03_02", "page_002_03", 2, 100, 1100, 1120, 1100, "MEDIUM_CLOSE",
                json.dumps(["char_neel"]),
                "Handsome divine deity Neel looking down calmly with ancient wisdom, deep blue skin, glowing cobalt eyes, intricate Indian gold jewelry, dark hair blowing gently, moonlit temple background, cinematic manhwa",
                "A spark without discipline will only burn the world it seeks to save, Aarav.",
                "Neel", None, None, None, "TOP_LEFT", "FINE_TONE"
            ),
            (
                "panel_002_03_03", "page_002_03", 3, 1260, 1100, 1120, 1100, "MEDIUM_CLOSE",
                json.dumps(["char_aarav"]),
                "Teenage hero Aarav standing resolute, messy black hair and red scarf, amber eyes glowing with determination, golden solar fire swirling gently around his forearm, looking up bravely, cinematic lighting, 8k manhwa",
                "Then teach me. Because I won't let them erase another story.",
                "Aarav", None, None, None, "TOP_RIGHT", "FINE_TONE"
            ),
            (
                "panel_002_03_04", "page_002_03", 4, 100, 2250, 2280, 1150, "EXTREME_WIDE",
                json.dumps(["char_aarav", "char_neel", "char_ananya"]),
                "Cinematic wide panoramic rooftop silhouette shot, Aarav with fluttering red scarf, Ananya in saree, and tall majestic Neel standing at ancient stone temple ledge looking out over glowing mythological Indian kingdom, star filled night sky where glowing cosmic celestial dragon constellation shines brilliantly, 8k digital painting manhwa",
                "The First Pillar has fractured at the Sunken Spire. The hunt has begun.",
                "Neel", None, None, None, "BOTTOM_CENTER", "FINE_TONE"
            )
        ]

        for p in panels_page_3:
            cursor.execute("""
                INSERT OR REPLACE INTO panels (
                    id, page_id, panel_index, bbox_x, bbox_y, bbox_w, bbox_h, shot_type,
                    character_ids, visual_prompt, dialogue_text, speaker_name, thought_text,
                    sfx_text, sfx_style, balloon_position, screentone_style
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, p)

        conn.commit()
    print("[+] Database seeded for Page 2 and Page 3.")

    manager = ProductionManager(ROOT_DIR)

    print("\n[*] Producing Chapter 2 Page 2...")
    res2 = manager.produce_page("page_002_02", prefer_cloud=True)
    print(f"[+] Page 2 Done: {res2['master_page_path']} (QA: {res2['qa_result']['verdict']}, Score: {res2['qa_result']['overall_score']:.2f})")

    print("\n[*] Producing Chapter 2 Page 3...")
    res3 = manager.produce_page("page_002_03", prefer_cloud=True)
    print(f"[+] Page 3 Done: {res3['master_page_path']} (QA: {res3['qa_result']['verdict']}, Score: {res3['qa_result']['overall_score']:.2f})")

if __name__ == "__main__":
    seed_and_produce_page_2_and_3()
