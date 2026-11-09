"""
DRAGON: HIDDEN REBIRTH - Master Vertical Webtoon Compositor & Lettering Engine
Formats all 16 key panels into high-resolution vertical mobile webtoon scrolls (800px width),
complete with authentic speech bubbles, narration boxes, sound effects, and atmospheric gutters.
"""

import os
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = Path(r"c:\Users\DESKTOP\Downloads\money\DRAGON_HIDDEN_REBIRTH")
PANELS_DIR = ROOT_DIR / "episodes" / "episode_001" / "panels"
WEBTOON_OUT = ROOT_DIR / "episodes" / "episode_001" / "final_webtoon"
WEBTOON_OUT.mkdir(parents=True, exist_ok=True)

TARGET_WIDTH = 800

def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    font_names = ["impact.ttf" if bold else "arial.ttf", "segoeui.ttf", "tahoma.ttf"]
    for fn in font_names:
        p = Path("C:/Windows/Fonts") / fn
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                pass
    return ImageFont.load_default()

def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.Draw) -> list[str]:
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def draw_speech_bubble(img: Image.Image, text: str, speaker: str = None, pos: tuple[int, int] = (400, 200), max_w: int = 320, is_thought: bool = False):
    draw = ImageDraw.Draw(img)
    font = get_font(20, bold=False)
    lines = wrap_text(text, font, max_w - 40, draw)
    
    line_height = 26
    text_h = len(lines) * line_height
    max_line_w = max([draw.textbbox((0, 0), l, font=font)[2] - draw.textbbox((0, 0), l, font=font)[0] for l in lines] or [100])
    
    pad_x, pad_y = 20, 16
    box_w = max_line_w + pad_x * 2
    box_h = text_h + pad_y * 2
    
    cx, cy = pos
    x0 = max(20, min(TARGET_WIDTH - box_w - 20, cx - box_w // 2))
    y0 = cy - box_h // 2
    x1 = x0 + box_w
    y1 = y0 + box_h
    
    # Shadow
    draw.rounded_rectangle([x0 + 4, y0 + 4, x1 + 4, y1 + 4], radius=16, fill=(10, 10, 15, 120))
    
    # Main bubble
    fill_color = (250, 250, 252) if not is_thought else (235, 238, 245)
    border_color = (20, 20, 25) if not is_thought else (60, 70, 90)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=16, fill=fill_color, outline=border_color, width=3)
    
    # Speaker label if given
    curr_y = y0 + pad_y
    if speaker:
        s_font = get_font(14, bold=True)
        draw.text((x0 + pad_x, y0 - 18), speaker.upper(), font=s_font, fill=(255, 215, 0), stroke_width=2, stroke_fill=(0, 0, 0))
        
    for line in lines:
        l_w = draw.textbbox((0, 0), line, font=font)[2] - draw.textbbox((0, 0), line, font=font)[0]
        text_x = x0 + (box_w - l_w) // 2
        draw.text((text_x, curr_y), line, font=font, fill=(15, 15, 20))
        curr_y += line_height

def draw_narration_box(img: Image.Image, text: str, pos: tuple[int, int] = (400, 100), max_w: int = 500, gold: bool = False):
    draw = ImageDraw.Draw(img)
    font = get_font(18, bold=True)
    lines = wrap_text(text, font, max_w - 30, draw)
    
    line_height = 24
    text_h = len(lines) * line_height
    max_line_w = max([draw.textbbox((0, 0), l, font=font)[2] - draw.textbbox((0, 0), l, font=font)[0] for l in lines] or [120])
    
    pad_x, pad_y = 18, 12
    box_w = max_line_w + pad_x * 2
    box_h = text_h + pad_y * 2
    
    cx, cy = pos
    x0 = max(20, min(TARGET_WIDTH - box_w - 20, cx - box_w // 2))
    y0 = cy - box_h // 2
    x1 = x0 + box_w
    y1 = y0 + box_h
    
    # Cinematic dark narration container
    fill_col = (11, 15, 23)
    outline_col = (212, 175, 55) if gold else (80, 90, 110)
    draw.rectangle([x0, y0, x1, y1], fill=fill_col, outline=outline_col, width=2)
    
    curr_y = y0 + pad_y
    for line in lines:
        l_w = draw.textbbox((0, 0), line, font=font)[2] - draw.textbbox((0, 0), line, font=font)[0]
        text_x = x0 + (box_w - l_w) // 2
        text_col = (255, 225, 120) if gold else (230, 235, 245)
        draw.text((text_x, curr_y), line, font=font, fill=text_col)
        curr_y += line_height

def draw_sfx(img: Image.Image, sfx_text: str, pos: tuple[int, int], color: tuple[int, int, int] = (255, 50, 50), size: int = 40):
    draw = ImageDraw.Draw(img)
    font = get_font(size, bold=True)
    x, y = pos
    # Bold manga sound effect with heavy outline
    draw.text((x, y), sfx_text, font=font, fill=color, stroke_width=4, stroke_fill=(10, 10, 15))

# Screenplay mapping for the 16 key panels across 4 Acts
EPISODE_1_SCRIPT = {
    # ACT 1: THE SOVEREIGN FALL
    "ep01_p01_cosmic_throne": {
        "narrations": [
            {"text": "THE MULTIVERSE WAS NOT DESTROYED IN SILENCE.", "pos": (400, 80), "gold": True},
            {"text": "IT COLLAPSED BENEATH A THRONE OLDER THAN LIGHT.", "pos": (400, 950), "gold": False}
        ],
        "dialogues": [],
        "sfx": [{"text": "*VZZZZT*", "pos": (120, 450), "color": (160, 80, 255), "size": 36}]
    },
    "ep01_p03_four_sovereigns": {
        "narrations": [
            {"text": "FOUR SOVEREIGNS OF THE ANCIENT AEON REMAINED STANDING.", "pos": (400, 70), "gold": True}
        ],
        "dialogues": [],
        "sfx": [{"text": "*KRAAA-SHHH*", "pos": (280, 500), "color": (255, 180, 30), "size": 42}]
    },
    "ep01_p04_hanirwesh_feral": {
        "narrations": [],
        "dialogues": [
            {"speaker": "HANIRWESH KAIVALYA", "text": "Siddhartha... if we carve its crown off, does that count as winning?!", "pos": (400, 850), "thought": False}
        ],
        "sfx": [{"text": "*DRIP*", "pos": (480, 480), "color": (220, 30, 30), "size": 32}]
    },
    "ep01_p07_siddhartha_supernova": {
        "narrations": [],
        "dialogues": [
            {"speaker": "SIDDHARTHA", "text": "No. It counts as buying an eternity.", "pos": (400, 160), "thought": False},
            {"speaker": None, "text": "[20 Memory Reclamation Keys primed into my marrow. We will meet again.]", "pos": (400, 880), "thought": True}
        ],
        "sfx": [{"text": "*IGNITE*", "pos": (500, 420), "color": (255, 215, 0), "size": 38}]
    },
    "ep01_p10_sovereign_annihilation": {
        "narrations": [
            {"text": "FOUR QUASARS MERGED. A FINAL REIGN ENDED.", "pos": (400, 80), "gold": True}
        ],
        "dialogues": [],
        "sfx": [{"text": "*SOVEREIGN ANNIHILATION*", "pos": (150, 480), "color": (255, 240, 100), "size": 44}]
    },
    "ep01_p14_memory_keys_sealed": {
        "narrations": [
            {"text": "THE SOUL SHATTERS INTO 20 CRYSTALLINE KEYS.", "pos": (400, 100), "gold": True},
            {"text": "REBIRTH PROTOCOL: INITIATED.", "pos": (400, 920), "gold": True}
        ],
        "dialogues": [],
        "sfx": [{"text": "*CLANG*", "pos": (480, 450), "color": (255, 215, 0), "size": 36}]
    },

    # ACT 2: JUBILEE HILLS MASSACRE & THE JACKAL
    "ep01_p15_hyderabad_monsoon": {
        "narrations": [
            {"text": "HYDERABAD. JUBILEE HILLS ESTATE. EIGHT YEARS AFTER REBIRTH.", "pos": (400, 90), "gold": True}
        ],
        "dialogues": [],
        "sfx": [{"text": "*THUUU-RUMMM*", "pos": (200, 450), "color": (120, 180, 255), "size": 42}]
    },
    "ep01_p16_ike_reading_trusts": {
        "narrations": [],
        "dialogues": [
            {"speaker": None, "text": "Twelve offshore accounts. Raghav shifted twenty percent to Dubai last Tuesday.", "pos": (380, 180), "thought": True},
            {"speaker": None, "text": "A coup is thirty-six hours away. Father thinks gratitude buys loyalty.", "pos": (400, 880), "thought": True}
        ],
        "sfx": [{"text": "*TAP*", "pos": (520, 500), "color": (200, 200, 220), "size": 28}]
    },
    "ep01_p20_family_dinner": {
        "narrations": [],
        "dialogues": [
            {"speaker": "VIKRAM DRAGON", "text": "Eat something, Ike. You've been staring at ledger sheets since dawn.", "pos": (300, 160), "thought": False},
            {"speaker": "ANANYA DRAGON", "text": "He has your stubborn eyes, Vikram.", "pos": (600, 220), "thought": False},
            {"speaker": None, "text": "[They don't know the perimeter guards were replaced at 8:00 PM.]", "pos": (400, 680), "thought": True}
        ],
        "sfx": []
    },
    "ep01_p28_raghav_pistol_betrayal": {
        "narrations": [],
        "dialogues": [
            {"speaker": "CHIEF RAGHAV", "text": "Forgive me, Vikram sir. The Jackal pays in sovereign debt, not salary.", "pos": (400, 850), "thought": False}
        ],
        "sfx": [{"text": "*CLICK*", "pos": (480, 380), "color": (255, 60, 60), "size": 36}]
    },
    "ep01_p30_devraj_jackal_arrival": {
        "narrations": [],
        "dialogues": [
            {"speaker": "DEVRAJ RATHORE ('THE JACKAL')", "text": "Vikram Dragon. You held fifty-one percent of the Hyderabad corridor for twenty years. The lease has expired.", "pos": (400, 840), "thought": False}
        ],
        "sfx": [{"text": "*TAP... TAP...*", "pos": (200, 480), "color": (220, 180, 60), "size": 34}]
    },
    "ep01_p35_ike_lion_eyes": {
        "narrations": [],
        "dialogues": [
            {"speaker": "DEVRAJ", "text": "The boy... why isn't he trembling?", "pos": (380, 160), "thought": False},
            {"speaker": "IKE DRAGON", "text": "Remember my face, Jackal.", "pos": (400, 870), "thought": False}
        ],
        "sfx": [{"text": "*GLARE*", "pos": (500, 450), "color": (255, 215, 0), "size": 36}]
    },

    # ACT 3: GACHIBOWLI HIGHWAY AMBUSH
    "ep01_p40_maybach_rpg_flip": {
        "narrations": [
            {"text": "GACHIBOWLI EXPRESSWAY. 11:42 PM.", "pos": (400, 80), "gold": True},
            {"text": "A 60-TON ARMORED FORTRESS... REDUCED TO SHREDDED STEEL.", "pos": (400, 940), "gold": False}
        ],
        "dialogues": [],
        "sfx": [{"text": "*KRAAA-BOOOOM!*", "pos": (200, 460), "color": (255, 100, 20), "size": 48}]
    },
    "ep01_p44_narasimha_naidu_execution": {
        "narrations": [],
        "dialogues": [
            {"speaker": "NARASIMHA NAIDU", "text": "Search every inch of the burning metal. Devraj wants the boy's signet ring.", "pos": (400, 850), "thought": False}
        ],
        "sfx": [{"text": "*CH-CHIK*", "pos": (480, 400), "color": (220, 220, 220), "size": 36}]
    },

    # ACT 4: CULVERT SURVIVAL & REBIRTH
    "ep01_p49_ike_in_drainage_sludge": {
        "narrations": [
            {"text": "A SIX-INCH CONCRETE DRAINAGE PIPE. COLD MUD. DIESEL SLUDGE.", "pos": (400, 90), "gold": False}
        ],
        "dialogues": [
            {"speaker": None, "text": "Heart rate: 41 bpm. Suppress body temperature. Do not exhale.", "pos": (380, 250), "thought": True},
            {"speaker": None, "text": "Father's watch... stopped at 11:43 PM.", "pos": (400, 880), "thought": True}
        ],
        "sfx": [{"text": "*DRIP... DRIP...*", "pos": (180, 520), "color": (100, 140, 180), "size": 30}]
    },
    "ep01_p51_sovereign_eye_ignites": {
        "narrations": [
            {"text": "KEY 01: [ABSOLUTE WILL] — UNLOCKED.", "pos": (400, 100), "gold": True}
        ],
        "dialogues": [
            {"speaker": "IKE DRAGON", "text": "I gave you my name, Jackal. In ten years... I will take back this entire city.", "pos": (400, 860), "thought": False}
        ],
        "sfx": [{"text": "*VOOOOOMMM!*", "pos": (220, 450), "color": (255, 215, 0), "size": 52}]
    }
}

ACT_GROUPINGS = {
    "ACT_1_COSMIC_FALL": [
        "ep01_p01_cosmic_throne",
        "ep01_p03_four_sovereigns",
        "ep01_p04_hanirwesh_feral",
        "ep01_p07_siddhartha_supernova",
        "ep01_p10_sovereign_annihilation",
        "ep01_p14_memory_keys_sealed"
    ],
    "ACT_2_JUBILEE_HILLS": [
        "ep01_p15_hyderabad_monsoon",
        "ep01_p16_ike_reading_trusts",
        "ep01_p20_family_dinner",
        "ep01_p28_raghav_pistol_betrayal",
        "ep01_p30_devraj_jackal_arrival",
        "ep01_p35_ike_lion_eyes"
    ],
    "ACT_3_HIGHWAY_AMBUSH": [
        "ep01_p40_maybach_rpg_flip",
        "ep01_p44_narasimha_naidu_execution"
    ],
    "ACT_4_SOVEREIGN_AWAKENING": [
        "ep01_p49_ike_in_drainage_sludge",
        "ep01_p51_sovereign_eye_ignites"
    ]
}

def process_panel(panel_id: str) -> Image.Image:
    panel_file = PANELS_DIR / f"{panel_id}.png"
    if not panel_file.exists():
        raise FileNotFoundError(f"Missing panel: {panel_file}")
    
    img = Image.open(panel_file).convert("RGB")
    # Scale width to TARGET_WIDTH
    w, h = img.size
    target_h = int(h * (TARGET_WIDTH / w))
    img = img.resize((TARGET_WIDTH, target_h), Image.Resampling.LANCZOS)
    
    script = EPISODE_1_SCRIPT.get(panel_id, {})
    
    # 1. Narrations
    for narr in script.get("narrations", []):
        draw_narration_box(img, narr["text"], narr["pos"], max_w=TARGET_WIDTH - 80, gold=narr.get("gold", False))
        
    # 2. SFX
    for sfx in script.get("sfx", []):
        draw_sfx(img, sfx["text"], sfx["pos"], sfx.get("color", (255, 50, 50)), sfx.get("size", 40))
        
    # 3. Dialogues
    for dlg in script.get("dialogues", []):
        draw_speech_bubble(img, dlg["text"], dlg.get("speaker"), dlg["pos"], max_w=340, is_thought=dlg.get("thought", False))
        
    return img

def create_act_scroll(act_name: str, panel_ids: list[str]) -> Path:
    print(f"\n[*] Assembling {act_name} ({len(panel_ids)} panels)...")
    processed_images = [process_panel(pid) for pid in panel_ids]
    
    GUTTER = 60 # Vertical atmospheric gutter between cuts
    total_h = sum([im.size[1] for im in processed_images]) + GUTTER * (len(processed_images) - 1)
    
    scroll = Image.new("RGB", (TARGET_WIDTH, total_h), (11, 15, 23)) # Cosmic Noir background
    
    curr_y = 0
    for idx, im in enumerate(processed_images):
        scroll.paste(im, (0, curr_y))
        curr_y += im.size[1] + GUTTER
        
    out_file = WEBTOON_OUT / f"DRAGON_EP01_{act_name}.png"
    scroll.save(out_file, "PNG", optimize=True)
    print(f"    [+] Saved: {out_file.name} ({TARGET_WIDTH}x{total_h}, {out_file.stat().st_size:,} bytes)")
    return out_file

def main():
    print("==================================================")
    print("   DRAGON: HIDDEN REBIRTH — VERTICAL WEBTOON COMPOSITOR")
    print("   Mobile Standard (800px) Full-Colour Korean Manhwa")
    print("==================================================")
    
    act_files = []
    for act_name, pids in ACT_GROUPINGS.items():
        f = create_act_scroll(act_name, pids)
        act_files.append(f)
        
    print("\n==================================================")
    print(f"[SUCCESS] All 4 Episode 1 Acts Assembled!")
    print(f"Output directory: {WEBTOON_OUT}")
    print("==================================================")

if __name__ == "__main__":
    main()
