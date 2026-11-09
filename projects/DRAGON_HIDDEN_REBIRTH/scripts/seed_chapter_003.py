"""
Seed Chapter 3 into manga_production.db
"""

import sqlite3
import json
from pathlib import Path

DB_PATH = Path(r"C:\Users\DESKTOP\Downloads\money\DRAGON_HIDDEN_REBIRTH\database\manga_production.db")

PANEL_DATA = [
    # Page 1: The Sovereign's Verdict (8 Panels)
    ("ch3_p1_1", "ch3_p1", 1, "Neel armored boots touching down onto cracked sanctum flagstones, purple mist curling outward in concentric ripples, low angle cinematic anime", "THUD... SHHH...", "Neel", None, "WIDE"),
    ("ch3_p1_2", "ch3_p1", 2, "Ananya 15-year-old temple maiden stepping defensively in front of Aarav, holding up glowing bronze prayer talisman, determined expression", "Halt! Who goes there?!", "Ananya", None, "MEDIUM"),
    ("ch3_p1_3", "ch3_p1", 3, "Neel 17-year-old dark prince lowering his glowing violet celestial trishul trident, extinguishing dark flames into wisping smoke", "Lower your talisman, priestess. If I sought your demise, you would already be ash.", "Neel", None, "CLOSE_UP"),
    ("ch3_p1_4", "ch3_p1", 4, "Neel looking down at Aarav with piercing amethyst eyes, calm analytical gaze", "You survived the Void Stalker's venom, boy. The bloodline of the Surya Dragon is unbroken.", "Neel", None, "MEDIUM"),
    ("ch3_p1_5", "ch3_p1", 5, "Aarav teenage warrior youth looking up breathing heavily, left golden eye smoldering with embers, clutching stone dagger", "Who are you? Why do you carry the insignia of the Eclipse?", "Aarav", None, "CLOSE_UP"),
    ("ch3_p1_6", "ch3_p1", 6, "Neel pulls aside midnight cloak showing royal crest on obsidian armor: twin dragons devouring sun and moon", "I am Neel. Last Sentinel of the Twilight Order. And you have just broken the first seal.", "Neel", None, "MEDIUM"),
    ("ch3_p1_7", "ch3_p1", 7, "Ancient Sanskrit lines engraved in granite floor suddenly blazing with intense crimson and gold luminescence", "KRRRR-RUMBLE!", None, None, "WIDE"),
    ("ch3_p1_8", "ch3_p1", 8, "Central stone altar splitting in two with deafening grind, revealing colossal spiral staircase plunging into golden abyss", "The Sanctum cannot hold. The Sunken Spire calls.", "Neel", None, "WIDE"),

    # Page 2: The Collapse of Kashi's Vault (8 Panels)
    ("ch3_p2_1", "ch3_p2", 1, "Massive earthquake tremor shaking subterranean sanctum, colossal stone arches cracking and dropping giant masonry blocks", "CRRR-AAACK!", None, None, "WIDE"),
    ("ch3_p2_2", "ch3_p2", 2, "Aarav lunging forward grabbing Ananya's hand as floor beneath her fractures into yawning chasms", "Ananya, take my hand! Jump!", "Aarav", None, "MEDIUM"),
    ("ch3_p2_3", "ch3_p2", 3, "Swarms of Gilded Specters, dark insectoid shadow drones with glowing golden runes, erupting from fissures into the air", "SKRRR-SKRRR!", None, None, "WIDE"),
    ("ch3_p2_4", "ch3_p2", 4, "Neel twirling glowing violet Trishul in rapid figure-eight overhead, forming kinetic electric vortex barrier pulverizing boulders", "Pestilence of the deep! Return to the void!", "Neel", None, "MEDIUM"),
    ("ch3_p2_5", "ch3_p2", 5, "Aarav's left eye flashing fierce solar radiance, manifesting a crackling golden flame blade over his fist", "I won't let them touch her!", "Aarav", None, "CLOSE_UP"),
    ("ch3_p2_6", "ch3_p2", 6, "Aarav leaping in mid-air cleaving a lunging Gilded Specter in half with fiery horizontal arc, golden sparks raining down", "SHZZZZ-SLASH!", None, None, "ACTION"),
    ("ch3_p2_7", "ch3_p2", 7, "Ananya clasping hands in sacred mudra, invoking glowing amber lotus shield repelling shadow drones with harmonic chime", "Om Shanti... Burn the impurities away!", "Ananya", None, "MEDIUM"),
    ("ch3_p2_8", "ch3_p2", 8, "Entire sanctum floor shattering completely, Aarav Ananya and Neel falling together into endless luminescent abyss", "BOOOOOM!", None, None, "WIDE"),

    # Page 3: The Sunken Spire Revealed (8 Panels)
    ("ch3_p3_1", "ch3_p3", 1, "Trio falling through golden clouds of glowing spore mist and subterranean waterfalls in massive cavern", "WHOOOOSH!", None, None, "WIDE"),
    ("ch3_p3_2", "ch3_p3", 2, "Neel thrusting Trishul downward conjuring circular violet gravitational field with pulsing energy rings cushioning descent", "Hold your breath!", "Neel", None, "MEDIUM"),
    ("ch3_p3_3", "ch3_p3", 3, "Aarav Ananya and Neel landing firmly on colossal ancient bronze suspension bridge spanning subterranean abyss", "CLANGGG!", None, None, "MEDIUM"),
    ("ch3_p3_4", "ch3_p3", 4, "Breathtaking panoramic reveal of subterranean civilization: stepped black basalt Vedic spires, luminous glowing aqueducts, ancient dragon statues", None, None, None, "EXTREME_WIDE"),
    ("ch3_p3_5", "ch3_p3", 5, "Aarav staring in wide-eyed awe at the underground metropolis", "This... this was underneath Kashi the entire time?", "Aarav", None, "CLOSE_UP"),
    ("ch3_p3_6", "ch3_p3", 6, "Neel gripping Trishul, scanning distant black ziggurats with grave apprehension", "The Sunken Spire of Maharishi Agastya. Where the Dragon's primordial heart was buried.", "Neel", None, "CLOSE_UP"),
    ("ch3_p3_7", "ch3_p3", 7, "Miles away atop the apex of tallest black spire, massive golden mechanical eyes ignite inside head of ancient slumbering Titan automaton", "VRRRRR-HUMMM...", None, None, "WIDE"),
    ("ch3_p3_8", "ch3_p3", 8, "Aarav and Neel standing side by side on bridge precipice, solar gold and void purple aura intertwining facing distant Titan", "Then let it wake. We finish this together.", "Aarav", None, "WIDE")
]

def seed():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Insert Chapter 3
    cur.execute("""
        INSERT OR REPLACE INTO chapters (id, chapter_number, title, logline, target_pages, status, reading_direction)
        VALUES ('ch_003', 3, 'The Sunken Spire', 'Aarav, Ananya, and Neel plunge into the ancient subterranean Vedic ziggurat beneath Kashi as an ancient Titan guardian awakens.', 3, 'STORYBOARDING', 'RTL')
    """)

    # 2. Insert Pages
    pages = [
        ("ch3_p1", "ch_003", 1, "DYNAMIC_ACTION", 1024, 1536, 300, "STORYBOARDED"),
        ("ch3_p2", "ch_003", 2, "DYNAMIC_ACTION", 1024, 1536, 300, "STORYBOARDED"),
        ("ch3_p3", "ch_003", 3, "DYNAMIC_ACTION", 1024, 1536, 300, "STORYBOARDED")
    ]
    for p_id, ch_id, p_num, layout, w, h, dpi, status in pages:
        cur.execute("""
            INSERT OR REPLACE INTO pages (id, chapter_id, page_number, layout_type, width_px, height_px, dpi, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (p_id, ch_id, p_num, layout, w, h, dpi, status))

    # 3. Insert Panels
    # Grid bounding box helper for 8 panels (1024 x 1536)
    grid_boxes = [
        # Row 1 (Tier 1: 2 panels)
        (8, 8, 500, 360),
        (516, 8, 500, 360),
        # Row 2 (Tier 2: 2 panels)
        (8, 376, 500, 360),
        (516, 376, 500, 360),
        # Row 3 (Tier 3: 2 panels)
        (8, 744, 500, 360),
        (516, 744, 500, 360),
        # Row 4 (Tier 4: 2 panels)
        (8, 1112, 500, 416),
        (516, 1112, 500, 416)
    ]

    for p_id, page_id, p_idx, prompt, dialogue, speaker, sfx, shot in PANEL_DATA:
        box = grid_boxes[p_idx - 1]
        cur.execute("""
            INSERT OR REPLACE INTO panels (
                id, page_id, panel_index, bbox_x, bbox_y, bbox_w, bbox_h,
                shot_type, visual_prompt, dialogue_text, speaker_name, sfx_text, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING')
        """, (p_id, page_id, p_idx, box[0], box[1], box[2], box[3], shot, prompt, dialogue, speaker, sfx))

    conn.commit()
    conn.close()
    print("[+] Successfully seeded Chapter 3 (3 pages, 24 panels) into manga_production.db!")

if __name__ == "__main__":
    seed()
