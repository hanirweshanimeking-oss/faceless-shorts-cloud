"""
Script to produce Chapter 2 Pages with Perfect Manga Layout
Calibrated to 1024x1536, ComicNeue typography, tight gutters, and authentic manhwa balloons.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.perfect_compositor import PerfectMangaCompositor

ART_DIR = ROOT_DIR / "generated_art"
FINAL_DIR = ROOT_DIR / "final_pages"
ARTIFACTS_DIR = Path("C:/Users/DESKTOP/.gemini/antigravity/brain/d0e83fc1-b00a-4e33-b50b-cc4e26bfa5c3")

def render_pages():
    compositor = PerfectMangaCompositor(1024, 1536)

    # ==================== PAGE 1 ====================
    page1_panels = [
        {
            "id": "p1_1",
            "bbox": (8, 8, 1008, 420),
            "image_path": str(ART_DIR / "panel_002_01_01.png"),
            "dialogue": "THE SILENCE THAT FOLLOWED WAS NOT PEACE. IT WAS THE WORLD HOLDING ITS BREATH.",
            "speaker": "NARRATOR",
            "balloon_coords": (180, 55),
            "max_width": 290
        },
        {
            "id": "p1_2",
            "bbox": (8, 434, 498, 360),
            "image_path": str(ART_DIR / "panel_002_01_03.png"),
            "dialogue": "THE ELDERS SAID THE FIRST STORIES SHAPED REALITY... BEFORE THE VOID BEGAN ERASING THEM.",
            "speaker": "Ananya",
            "balloon_coords": (150, 495),
            "max_width": 220
        },
        {
            "id": "p1_3",
            "bbox": (512, 434, 504, 360),
            "image_path": str(ART_DIR / "panel_002_01_02.png"),
            "dialogue": "IT FEELS LIKE... IT'S BREATHING. LIKE A HEART SLEEPING FOR THOUSANDS OF YEARS.",
            "speaker": "Aarav",
            "balloon_coords": (850, 495),
            "max_width": 220
        },
        {
            "id": "p1_4",
            "bbox": (8, 800, 498, 320),
            "image_path": str(ROOT_DIR.parent / ".gemini" / "antigravity" / "brain" / "d0e83fc1-b00a-4e33-b50b-cc4e26bfa5c3" / "sdxl_lightning_test.png"),
            "dialogue": "THE FRAGMENT HAS CHOSEN ITS WIELDER.",
            "speaker": "Aarav",
            "is_thought": True,
            "balloon_coords": (160, 855),
            "max_width": 210,
            "sfx": "HUMMM...",
            "sfx_coords": (400, 840),
            "sfx_size": 28
        },
        {
            "id": "p1_5",
            "bbox": (512, 800, 504, 320),
            "image_path": str(ART_DIR / "panel_002_02_01.png"),
            "dialogue": "AARAV! LOOK OUT! THE SHADOWS ARE MOVING!",
            "speaker": "Ananya",
            "balloon_coords": (670, 855),
            "max_width": 220,
            "sfx": "SKRRR...",
            "sfx_coords": (880, 840),
            "sfx_size": 30
        },
        {
            "id": "p1_6",
            "bbox": (8, 1126, 1008, 380),
            "image_path": str(ART_DIR / "panel_002_01_04.png"),
            "dialogue": "ANANYA... GET BEHIND ME. NOW!",
            "speaker": "Aarav",
            "balloon_coords": (512, 1430),
            "max_width": 240,
            "sfx": "BOOOOM!",
            "sfx_coords": (80, 1160),
            "sfx_size": 46
        }
    ]

    out_p1 = FINAL_DIR / "perfect_chapter_002_page_001.png"
    compositor.composite_page(page1_panels, 1, out_p1)
    
    # Copy to artifacts
    import shutil
    shutil.copy(str(out_p1), str(ARTIFACTS_DIR / "perfect_chapter_002_page_001.png"))
    print("[+] Page 1 composite finished and copied to artifacts.")

    # ==================== PAGE 2 ====================
    page2_panels = [
        {
            "id": "p2_1",
            "bbox": (8, 8, 1008, 420),
            "image_path": str(ART_DIR / "panel_002_02_01.png"),
            "dialogue": "THE FRAGMENT... MUST BE ERASED FROM EXISTENCE...",
            "speaker": "Void Stalker",
            "balloon_coords": (780, 65),
            "max_width": 260,
            "sfx": "ROOOAAAR!",
            "sfx_coords": (80, 45),
            "sfx_size": 42
        },
        {
            "id": "p2_2",
            "bbox": (8, 434, 498, 420),
            "image_path": str(ART_DIR / "panel_002_02_02.png"),
            "dialogue": "NOT WHILE I STILL REMEMBER!",
            "speaker": "Aarav",
            "balloon_coords": (180, 490),
            "max_width": 210
        },
        {
            "id": "p2_3",
            "bbox": (512, 434, 504, 420),
            "image_path": str(ART_DIR / "panel_002_02_03.png"),
            "dialogue": "SHIELD OF THE FIRST DAWN!",
            "speaker": "Aarav",
            "balloon_coords": (840, 490),
            "max_width": 210,
            "sfx": "FWOOOOSH!",
            "sfx_coords": (540, 460),
            "sfx_size": 36
        },
        {
            "id": "p2_4",
            "bbox": (8, 860, 1008, 646),
            "image_path": str(ART_DIR / "panel_002_02_04.png"),
            "dialogue": "ENOUGH, VERMIN OF THE VOID.",
            "speaker": "Neel",
            "balloon_coords": (512, 1430),
            "max_width": 240,
            "sfx": "KRAAAACK!",
            "sfx_coords": (80, 890),
            "sfx_size": 46
        }
    ]

    out_p2 = FINAL_DIR / "perfect_chapter_002_page_002.png"
    compositor.composite_page(page2_panels, 2, out_p2)
    shutil.copy(str(out_p2), str(ARTIFACTS_DIR / "perfect_chapter_002_page_002.png"))
    print("[+] Page 2 composite finished and copied to artifacts.")

    # ==================== PAGE 3 ====================
    page3_panels = [
        {
            "id": "p3_1",
            "bbox": (8, 8, 1008, 420),
            "image_path": str(ART_DIR / "panel_002_03_01.png"),
            "dialogue": "RETURN TO NOTHINGNESS.",
            "speaker": "Neel",
            "balloon_coords": (260, 60),
            "max_width": 220,
            "sfx": "SHRRR-BOOM!",
            "sfx_coords": (740, 50),
            "sfx_size": 40
        },
        {
            "id": "p3_2",
            "bbox": (8, 434, 498, 420),
            "image_path": str(ART_DIR / "panel_002_03_02.png"),
            "dialogue": "A SPARK WITHOUT DISCIPLINE WILL ONLY BURN THE WORLD IT SEEKS TO SAVE, AARAV.",
            "speaker": "Neel",
            "balloon_coords": (180, 490),
            "max_width": 220
        },
        {
            "id": "p3_3",
            "bbox": (512, 434, 504, 420),
            "image_path": str(ART_DIR / "panel_002_03_03.png"),
            "dialogue": "THEN TEACH ME. BECAUSE I WON'T LET THEM ERASE ANOTHER STORY.",
            "speaker": "Aarav",
            "balloon_coords": (840, 490),
            "max_width": 220
        },
        {
            "id": "p3_4",
            "bbox": (8, 860, 1008, 646),
            "image_path": str(ART_DIR / "panel_002_03_04.png"),
            "dialogue": "THE FIRST PILLAR HAS FRACTURED AT THE SUNKEN SPIRE. THE HUNT HAS BEGUN.",
            "speaker": "Neel",
            "balloon_coords": (512, 1430),
            "max_width": 260
        }
    ]

    out_p3 = FINAL_DIR / "perfect_chapter_002_page_003.png"
    compositor.composite_page(page3_panels, 3, out_p3)
    shutil.copy(str(out_p3), str(ARTIFACTS_DIR / "perfect_chapter_002_page_003.png"))
    print("[+] Page 3 composite finished and copied to artifacts.")

if __name__ == "__main__":
    render_pages()
