"""
Database Initialization & Seeder for DRAGON: HIDDEN REBIRTH
Creates SQLite tables and seeds canonical story bible, characters, and chapter metadata.
"""

import sqlite3
import json
from pathlib import Path

DB_DIR = Path(__file__).parent
DB_PATH = DB_DIR / "manga_production.db"
SCHEMA_PATH = DB_DIR / "schema.sql"
ROOT_DIR = DB_DIR.parent
STORY_BIBLE_PATH = ROOT_DIR / "story_bible" / "story_bible.md"
CHARACTERS_PATH = ROOT_DIR / "characters" / "characters.json"
WORLD_LORE_PATH = ROOT_DIR / "world" / "world_lore.md"

def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    print(f"[*] Initializing database at {DB_PATH}...")
    conn = get_connection()
    cursor = conn.cursor()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)

    # 1. Seed Story Bible
    if STORY_BIBLE_PATH.exists():
        with open(STORY_BIBLE_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        cursor.execute("""
            INSERT OR REPLACE INTO story_bible (id, category, title, content, version)
            VALUES (?, ?, ?, ?, ?)
        """, ("canon_bible_v1", "PREMISE", "Canonical Story Bible", content, "1.0.0"))

    # 2. Seed Characters
    if CHARACTERS_PATH.exists():
        with open(CHARACTERS_PATH, "r", encoding="utf-8") as f:
            characters_data = json.load(f)
        for c in characters_data:
            eyes_info = c.get('eyes', {})
            eye_desc = eyes_info.get('left') or eyes_info.get('description', 'piercing eyes')
            hair_info = c.get('hair', {})
            hair_desc = hair_info.get('style', 'dark hair')
            clothing_info = c.get('clothing', {})
            clothing_desc = clothing_info.get('main_attire', 'dark attire')
            
            visual_prompt_base = (
                f"masterpiece manga art, dark fantasy style, high contrast ink, screentone shading, "
                f"{c['name']}, {c.get('age', '')}yo, {c.get('build', '')}, {c['facial_structure']}, "
                f"{hair_desc}, {eye_desc}, {clothing_desc}, detailed lineart"
            )
            negative_prompt = "lowres, blurry, extra limbs, bad hands, mutated fingers, color, 3d render, photorealistic, ugly face"
            cursor.execute("""
                INSERT OR REPLACE INTO characters (
                    id, name, alias, age, gender, height_cm, build, 
                    facial_features, hair_details, eye_details, clothing_details, 
                    weapons, personality_traits, visual_prompt_base, negative_prompt, master_seed
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                c["id"], c["name"], c.get("alias", ""), str(c.get("age", "")), c.get("gender", "Male"),
                c.get("height_cm", 175), c.get("build", ""), c.get("facial_structure", ""),
                json.dumps(c.get("hair", {})), json.dumps(c.get("eyes", {})),
                json.dumps(c.get("clothing", {})), json.dumps(c.get("weapons", [])),
                json.dumps(c.get("personality_traits", [])), visual_prompt_base, negative_prompt, 1337
            ))

    # 3. Seed World Locations
    locations = [
        ("loc_obsidian_temple", "The Obsidian Altar of Ignis", "Ruins of Obsidian City", 
         "Ancient subterranean temple of black volcanic stone, cracked altar hovering with dragon runes, shattered stained glass revealing dark violet sky.",
         "dark fantasy manga interior, ancient ruined obsidian temple, floating runic altar, gothic arches, stone pillars, high contrast screentone, ink linework"),
        ("loc_kaelens_reach", "Kaelen's Reach Outpost", "Border Territory", 
         "Desolate frontier settlement built from dragon bone scaffolds and black iron plate, perpetual ash falling like snow.",
         "wide angle manga exterior, dystopian frontier town, dragon bone architecture, iron fortress walls, falling ash atmosphere, detailed inking")
    ]
    for loc_id, name, region, desc, prompt in locations:
        cursor.execute("""
            INSERT OR REPLACE INTO world_locations (id, name, region, description, visual_prompt)
            VALUES (?, ?, ?, ?, ?)
        """, (loc_id, name, region, desc, prompt))

    # 4. Seed Chapter 1 & Page 1
    cursor.execute("""
        INSERT OR REPLACE INTO chapters (id, chapter_number, title, logline, target_pages, status, reading_direction)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "ch_001", 1, "The Broken Seal",
        "In the ruins of the Obsidian City, the ancient seal has fractured. Chitran awakens and unleashes celestial dragon fire upon the imperial hunting party.",
        18, "STORYBOARDING", "RTL"
    ))

    # Page 1 Metadata
    cursor.execute("""
        INSERT OR REPLACE INTO pages (id, chapter_id, page_number, layout_type, width_px, height_px, reading_direction, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "page_001_01", "ch_001", 1, "DYNAMIC_ACTION", 2480, 3508, "RTL", "PLANNED"
    ))

    # Page 1 Panels: 4-Panel Dynamic Manga Layout (Japanese Traditional RTL)
    panels_data = [
        (
            "panel_001_01_01", "page_001_01", 1, 100, 100, 2280, 950, "EXTREME_WIDE",
            json.dumps(["loc_obsidian_temple"]),
            "Extreme wide establishing shot, ruins of the subterranean Obsidian Altar, towering monolithic pillars of black volcanic glass, fractured stone floor with violet smoke rising from deep crevices, intricate dragon runes glowing faintly along ancient walls, dramatic chiaroscuro inking, masterclass manga art, 8k screentone texture",
            "In the ruins of the Obsidian City... the ancient seal has fractured.",
            "NARRATOR", None, "ZHHHHRRRR...", "CRACKLE", "TOP_LEFT", "FINE_TONE"
        ),
        (
            "panel_001_01_02", "page_001_01", 2, 1260, 1100, 1120, 1100, "MEDIUM_CLOSE",
            json.dumps(["char_chitran"]),
            "Medium close-up shot, young male manga protagonist Chitran kneeling on cracked obsidian stone, messy black bangs falling over face, blindfolded with tattered black cloth, dark trench coat collar visible, hands trembling slightly as violet dragon embers begin forming around his fingertips, high tension atmosphere, delicate lineart",
            "This power... it isn't mana. It's...",
            "Chitran", "It's the flame of the ones they slaughtered.", None, None, "TOP_RIGHT", "CROSSHATCH"
        ),
        (
            "panel_001_01_03", "page_001_01", 3, 100, 1100, 1120, 1100, "DUTCH_ANGLE",
            json.dumps(["char_malakor"]),
            "Low angle Dutch tilt, imperial shadow inquisitor with brutal spiked black armor and drawn cleaver sword sneering downward, torchlight casting menacing shadows behind him, ruthless expression, aggressive manga action composition, thick dynamic ink lines",
            "Die like the rest of your cursed vermin!",
            "Inquisitor", None, "SHRRRIIING!", "SLASH", "TOP_LEFT", "SPEED_LINES"
        ),
        (
            "panel_001_01_04", "page_001_01", 4, 100, 2250, 2280, 1150, "WIDE_ACTION",
            json.dumps(["char_chitran"]),
            "Wide dramatic action climax panel, Chitran untying his blindfold in one swift motion, cloth drifting in slow motion into wind, single left eye wide open revealing blazing violet dragon pupil, massive shockwave of celestial purple fire blasting outward in a dome, imperial sword shattering into glowing dust fragments inches from his face, explosive ink splatter and radial speedlines",
            "The hunt begins today.",
            "Chitran", None, "BOOOOOOOM!", "EXPLOSION", "BOTTOM_CENTER", "RADIAL_BURST"
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
    conn.close()
    print("[+] Database initialized and seeded successfully with Chapter 1 Page 1 data!")

if __name__ == "__main__":
    init_database()
