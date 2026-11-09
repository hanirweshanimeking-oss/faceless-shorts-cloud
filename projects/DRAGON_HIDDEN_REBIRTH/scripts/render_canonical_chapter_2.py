"""
Canonical Master Compositor for CHITRAN Chapter 2: THE VEIL OF SHADOWS
Calibrated 100% to Hanirwesh's Master Reference Specification (chitran_page_001 - 007):
- Dimensions: 1024 x 1536
- Margins: 8px white trim, 5px gutters, 2px crisp black panel frames
- Aspect-ratio preserving smart cropping for all panels
- Official CHITRAN brush logo + orange flame + chapter subtitle banner on Page 1
- Official ending brush slogan banner ("STORIES WILL LIVE... OR THE WORLD WILL DIE.") on Page 3
- Snug comic-style dialogue balloons, jagged scream balloons, and rectangular narration boxes
- ComicNeue-BoldItalic lettering and Bangers glowing sound effects
"""

import os
import sys
import textwrap
import shutil
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = Path(__file__).parent.parent
FONTS_DIR = ROOT_DIR / "fonts"
COMIC_FONT_PATH = FONTS_DIR / "ComicNeue-BoldItalic.ttf"
SFX_FONT_PATH = FONTS_DIR / "Bangers-Regular.ttf"
LOGO_PATH = ROOT_DIR / "reference_standards" / "chitran_logo_perfect.png"
BANNER_PATH = Path("C:/Users/DESKTOP/.gemini/antigravity/brain/d0e83fc1-b00a-4e33-b50b-cc4e26bfa5c3/banner_crop.png")
ART_DIR = ROOT_DIR / "generated_art" / "chapter_002_hd"
FINAL_DIR = ROOT_DIR / "final_pages"
ARTIFACTS_DIR = Path("C:/Users/DESKTOP/.gemini/antigravity/brain/d0e83fc1-b00a-4e33-b50b-cc4e26bfa5c3")

class CanonicalMangaCompositor:
    def __init__(self, canvas_w: int = 1024, canvas_h: int = 1536):
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h

    def _get_font(self, size: int) -> ImageFont.FreeTypeFont:
        if COMIC_FONT_PATH.exists():
            return ImageFont.truetype(str(COMIC_FONT_PATH), size)
        return ImageFont.load_default()

    def _get_sfx_font(self, size: int) -> ImageFont.FreeTypeFont:
        if SFX_FONT_PATH.exists():
            return ImageFont.truetype(str(SFX_FONT_PATH), size)
        return ImageFont.load_default()

    def crop_and_fit(self, img: Image.Image, target_w: int, target_h: int) -> Image.Image:
        """Smart center-crop and resize preserving aspect ratio without distortion."""
        img_w, img_h = img.size
        target_ratio = target_w / target_h
        img_ratio = img_w / img_h

        if img_ratio > target_ratio:
            # Source is wider: crop width
            new_w = int(img_h * target_ratio)
            left = (img_w - new_w) // 2
            img_cropped = img.crop((left, 0, left + new_w, img_h))
        else:
            # Source is taller: crop height
            new_h = int(img_w / target_ratio)
            top = (img_h - new_h) // 2
            img_cropped = img.crop((0, top, img_w, top + new_h))

        return img_cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)

    def draw_dialogue_balloon(
        self,
        draw: ImageDraw.Draw,
        text: str,
        speaker: str,
        center_x: int,
        center_y: int,
        max_width: int = 210,
        is_thought: bool = False,
        is_shout: bool = False,
        font_size: int = 16
    ):
        """Draws clean, snug authentic comic dialogue balloons, thought bubbles, or narration boxes."""
        font = self._get_font(font_size)
        text_caps = text.upper()

        avg_char_w = int(font_size * 0.55)
        wrap_width = max(8, max_width // avg_char_w)
        lines = textwrap.wrap(text_caps, width=wrap_width)
        if not lines:
            return

        line_height = int(font_size * 1.25)
        text_block_h = len(lines) * line_height
        max_line_w = max(draw.textbbox((0, 0), line, font=font)[2] for line in lines)

        padding_x = 16
        padding_y = 10
        bw = max_line_w + (padding_x * 2)
        bh = text_block_h + (padding_y * 2)

        x0 = center_x - bw // 2
        y0 = center_y - bh // 2
        x1 = x0 + bw
        y1 = y0 + bh

        # Keep inside canvas boundaries
        if x0 < 14:
            x0, x1 = 14, 14 + bw
        if x1 > self.canvas_w - 14:
            x1, x0 = self.canvas_w - 14, self.canvas_w - 14 - bw

        if speaker.upper() == "NARRATOR":
            # Rectangular Narration Box (white with 2px solid black outline)
            draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=(10, 10, 15), width=2)
        elif is_thought:
            # Elliptical Thought Balloon with trailing circles
            draw.ellipse([x0, y0, x1, y1], fill=(255, 255, 255), outline=(10, 10, 15), width=2)
            cx = (x0 + x1) // 2
            draw.ellipse([cx - 8, y1 + 3, cx + 2, y1 + 13], fill=(255, 255, 255), outline=(10, 10, 15), width=2)
            draw.ellipse([cx - 14, y1 + 15, cx - 8, y1 + 21], fill=(255, 255, 255), outline=(10, 10, 15), width=2)
        elif is_shout:
            # Spiky shout balloon
            rad = min(20, bh // 2)
            draw.rounded_rectangle([x0, y0, x1, y1], radius=rad, fill=(255, 255, 255), outline=(10, 10, 15), width=2)
            # Small sharp burst tail
            cx = (x0 + x1) // 2
            tail_x = cx - 8
            tail_y = y1
            draw.polygon([(tail_x, tail_y - 1), (tail_x + 16, tail_y - 1), (tail_x + 20, tail_y + 14)], fill=(255, 255, 255), outline=(10, 10, 15))
            draw.line([(tail_x + 1, tail_y), (tail_x + 15, tail_y)], fill=(255, 255, 255), width=3)
        else:
            # Authentic Manhwa Elliptical Balloon with smooth rounded corners and clean tail
            rad = min(22, bh // 2)
            draw.rounded_rectangle([x0, y0, x1, y1], radius=rad, fill=(255, 255, 255), outline=(10, 10, 15), width=2)
            
            # Smooth tail pointer
            cx = (x0 + x1) // 2
            tail_x = cx - 8
            tail_y = y1
            draw.polygon([(tail_x, tail_y - 1), (tail_x + 16, tail_y - 1), (tail_x + 6, tail_y + 13)], fill=(255, 255, 255), outline=(10, 10, 15))
            draw.line([(tail_x + 1, tail_y), (tail_x + 15, tail_y)], fill=(255, 255, 255), width=3)

        # Draw centered text lines
        cur_y = y0 + padding_y
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            lw = bbox[2] - bbox[0]
            lx = x0 + (bw - lw) // 2
            draw.text((lx, cur_y), line, font=font, fill=(10, 10, 15))
            cur_y += line_height

    def draw_sfx(self, draw: ImageDraw.Draw, text: str, x: int, y: int, size: int = 34, color: Tuple[int, int, int] = (255, 180, 20)):
        """Draws dynamic stylized manga sound effects with heavy outline and glowing color."""
        font = self._get_sfx_font(size)
        text_caps = text.upper()
        
        # Black outline / shadow
        for ox, oy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2), (-2, 2), (2, -2), (3, 3)]:
            draw.text((x + ox, y + oy), text_caps, font=font, fill=(10, 10, 15))
            
        # Glowing inner text
        draw.text((x, y), text_caps, font=font, fill=color)

    def draw_chapter_1_header(self, canvas: Image.Image, draw: ImageDraw.Draw, panel_x: int, panel_y: int):
        """Draws official CHITRAN brush logo, motto, and chapter title badge on Page 1."""
        if LOGO_PATH.exists():
            logo = Image.open(LOGO_PATH).convert("RGBA")
            # Resize logo to fit upper left: ~320px wide
            logo_w = 320
            logo_h = int(logo.size[1] * (logo_w / logo.size[0]))
            logo_resized = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
            canvas.paste(logo_resized, (panel_x + 20, panel_y + 15), logo_resized)
            
            # Motto under logo with crisp white halo outline for contrast
            motto_font = self._get_font(13)
            motto_text = "OUR STORIES. OUR ROOTS. OUR WORLD."
            mx = panel_x + 35
            my = panel_y + 15 + logo_h + 6
            for ox, oy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
                draw.text((mx + ox, my + oy), motto_text, font=motto_font, fill=(255, 255, 255))
            draw.text((mx, my), motto_text, font=motto_font, fill=(15, 15, 20))
            
            # Chapter 2 Subtitle badge with crisp white halo outline
            sub_font = self._get_font(14)
            badge_text = "— CHAPTER 2: THE VEIL OF SHADOWS —"
            bx = panel_x + 30
            by = my + 22
            for ox, oy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
                draw.text((bx + ox, by + oy), badge_text, font=sub_font, fill=(255, 255, 255))
            draw.text((bx, by), badge_text, font=sub_font, fill=(20, 20, 25))

    def composite_page(
        self,
        panels_data: List[Dict[str, Any]],
        page_num: int,
        out_path: Path,
        has_header: bool = False,
        has_ending_banner: bool = False
    ) -> Path:
        canvas = Image.new("RGB", (self.canvas_w, self.canvas_h), (255, 255, 255))
        draw = ImageDraw.Draw(canvas)

        # 1. Paste all cropped panels
        for p in panels_data:
            x, y, w, h = p["bbox"]
            img_path = Path(p["image_path"])
            if img_path.exists():
                panel_img = Image.open(img_path).convert("RGB")
                panel_fitted = self.crop_and_fit(panel_img, w, h)
                
                # Draw crisp 2px solid black border around panel image
                panel_draw = ImageDraw.Draw(panel_fitted)
                panel_draw.rectangle([0, 0, w - 1, h - 1], outline=(8, 8, 12), width=2)
                
                canvas.paste(panel_fitted, (x, y))

        # 2. Header overlay for Page 1
        if has_header and len(panels_data) > 0:
            p1_x, p1_y, _, _ = panels_data[0]["bbox"]
            self.draw_chapter_1_header(canvas, draw, p1_x, p1_y)

        # 3. Draw Speech Balloons, Narration, and SFX
        for p in panels_data:
            x, y, w, h = p["bbox"]
            dialogue = p.get("dialogue")
            speaker = p.get("speaker", "")
            is_thought = p.get("is_thought", False)
            is_shout = p.get("is_shout", False)
            sfx = p.get("sfx")

            if dialogue:
                bx, by = p.get("balloon_coords", (x + w // 2, y + int(h * 0.3)))
                max_w = p.get("max_width", 210)
                font_sz = p.get("font_size", 16)
                self.draw_dialogue_balloon(draw, dialogue, speaker, bx, by, max_width=max_w, is_thought=is_thought, is_shout=is_shout, font_size=font_sz)

            if sfx:
                sfx_x, sfx_y = p.get("sfx_coords", (x + 25, y + 25))
                sfx_color = p.get("sfx_color", (255, 180, 20))
                self.draw_sfx(draw, sfx, sfx_x, sfx_y, size=p.get("sfx_size", 34), color=sfx_color)

        # 4. Ending Slogan Banner for Page 3
        if has_ending_banner:
            if BANNER_PATH.exists():
                banner_img = Image.open(BANNER_PATH).convert("RGBA")
                # Resize banner to width ~740px
                bw = 720
                bh = int(banner_img.size[1] * (bw / banner_img.size[0]))
                banner_resized = banner_img.resize((bw, bh), Image.Resampling.LANCZOS)
                canvas.paste(banner_resized, (15, self.canvas_h - 110), banner_resized)

            # Bottom Right "END OF CHAPTER 2 / TO BE CONTINUED..." box
            end_font = self._get_font(13)
            box_x0 = self.canvas_w - 275
            box_y0 = self.canvas_h - 100
            box_x1 = self.canvas_w - 15
            box_y1 = self.canvas_h - 58
            draw.rectangle([box_x0, box_y0, box_x1, box_y1], fill=(255, 255, 255), outline=(10, 10, 15), width=2)
            draw.text((box_x0 + 12, box_y0 + 7), "END OF CHAPTER 2", font=self._get_font(14), fill=(10, 10, 15))
            draw.text((box_x0 + 12, box_y0 + 24), "TO BE CONTINUED IN CH. 3...", font=end_font, fill=(50, 50, 55))

        # 5. Bottom Folio / Page Number
        page_font = self._get_font(18)
        p_str = f"{page_num}"
        bbox = draw.textbbox((0, 0), p_str, font=page_font)
        pw = bbox[2] - bbox[0]
        draw.text(((self.canvas_w - pw) // 2, self.canvas_h - 22), p_str, font=page_font, fill=(90, 90, 95))

        out_path.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(out_path, "PNG", dpi=(300, 300))
        print(f"[+] Master Page exported to: {out_path} ({self.canvas_w}x{self.canvas_h})")
        return out_path

def render_chapter_2():
    compositor = CanonicalMangaCompositor(1024, 1536)

    # =========================================================================
    # PAGE 1: THE SANCTUARY AT MIDNIGHT (8 PANELS)
    # =========================================================================
    p1_panels = [
        # Tier 1: Wide establishing shot with Title Header (1008 x 380)
        {
            "id": "p1_1",
            "bbox": (8, 8, 1008, 380),
            "image_path": str(ART_DIR / "p1_1_sanctum_wide.png"),
            "dialogue": "THE SILENCE THAT FOLLOWED WAS NOT PEACE... IT WAS THE WORLD HOLDING ITS BREATH.",
            "speaker": "NARRATOR",
            "balloon_coords": (780, 50),
            "max_width": 260
        },
        # Tier 2: 2 Panels (altar + Ananya concern) (501 x 280 each, y: 393)
        {
            "id": "p1_2",
            "bbox": (8, 393, 501, 280),
            "image_path": str(ART_DIR / "p1_2_aarav_ananya_altar.png"),
            "dialogue": "THE TOME BROUGHT US TO THE SUBTERRANEAN GHATS. IT FEELS... AWAKE.",
            "speaker": "Aarav",
            "balloon_coords": (250, 440),
            "max_width": 230
        },
        {
            "id": "p1_3",
            "bbox": (514, 393, 502, 280),
            "image_path": str(ART_DIR / "p1_3_ananya_concern.png"),
            "dialogue": "AARAV... THE ELDERS WARNED THAT DIGGING INTO ERASURES SUMMONS THE OBSCURITY.",
            "speaker": "Ananya",
            "balloon_coords": (760, 440),
            "max_width": 230
        },
        # Tier 3: 2 Panels (Aarav determined + Sanskrit scroll) (501 x 280 each, y: 678)
        {
            "id": "p1_4",
            "bbox": (8, 678, 501, 280),
            "image_path": str(ART_DIR / "p1_4_aarav_determined.png"),
            "dialogue": "IF WE DON'T READ THEM, WHO WILL REMEMBER OUR ROOTS?",
            "speaker": "Aarav",
            "balloon_coords": (260, 725),
            "max_width": 220
        },
        {
            "id": "p1_5",
            "bbox": (514, 678, 502, 280),
            "image_path": str(ART_DIR / "p1_5_sanskrit_scroll.png"),
            "dialogue": "LOOK... THE GOLDEN SCRIPT... IT RESPONDS TO YOUR BLOOD!",
            "speaker": "Ananya",
            "balloon_coords": (760, 725),
            "max_width": 220
        },
        # Tier 4: 3 Panels (Fragment hover + Macro eye + Shadows creeping) (332 x 520 each, y: 963)
        {
            "id": "p1_6",
            "bbox": (8, 963, 332, 535),
            "image_path": str(ART_DIR / "p1_6_fragment_hover.png"),
            "dialogue": "IT FEELS LIKE A HEART THAT HAS SLEPT FOR AGES.",
            "speaker": "Aarav",
            "is_thought": True,
            "balloon_coords": (170, 1020),
            "max_width": 190,
            "sfx": "HUMMM...",
            "sfx_coords": (30, 1380),
            "sfx_size": 32,
            "sfx_color": (255, 190, 30)
        },
        {
            "id": "p1_7",
            "bbox": (345, 963, 334, 535),
            "image_path": str(ART_DIR / "p1_7_aarav_macro_eye.png"),
            "dialogue": "THE SPARK...",
            "speaker": "Aarav",
            "is_thought": True,
            "balloon_coords": (512, 1020),
            "max_width": 160
        },
        {
            "id": "p1_8",
            "bbox": (684, 963, 332, 535),
            "image_path": str(ART_DIR / "p1_8_shadows_creeping.png"),
            "dialogue": "AARAV! LOOK OUT! THE SHADOWS ARE MOVING!",
            "speaker": "Ananya",
            "is_shout": True,
            "balloon_coords": (850, 1030),
            "max_width": 200,
            "sfx": "SKRRR...",
            "sfx_coords": (710, 1380),
            "sfx_size": 32,
            "sfx_color": (230, 40, 40)
        }
    ]

    out_p1 = FINAL_DIR / "perfect_chapter_002_page_001.png"
    compositor.composite_page(p1_panels, 1, out_p1, has_header=True)
    shutil.copy(str(out_p1), str(ARTIFACTS_DIR / "perfect_chapter_002_page_001.png"))

    # =========================================================================
    # PAGE 2: THE DEVOURER OF STORIES (8 PANELS)
    # =========================================================================
    p2_panels = [
        # Tier 1: 2 Panels (Void erupt + Void fangs) (y: 8 to 380)
        {
            "id": "p2_1",
            "bbox": (8, 8, 590, 375),
            "image_path": str(ART_DIR / "p2_1_void_erupt.png"),
            "sfx": "ROOOAAAR!",
            "sfx_coords": (40, 35),
            "sfx_size": 42,
            "sfx_color": (255, 50, 50)
        },
        {
            "id": "p2_2",
            "bbox": (603, 8, 413, 375),
            "image_path": str(ART_DIR / "p2_2_void_fangs.png"),
            "dialogue": "THE BEARER OF STORIES... MUST BE EXTINGUISHED FROM EXISTENCE!",
            "speaker": "Void Stalker",
            "balloon_coords": (810, 70),
            "max_width": 230
        },
        # Tier 2: 2 Panels (Ananya fear + Aarav protect) (y: 388 to 680)
        {
            "id": "p2_3",
            "bbox": (8, 388, 440, 290),
            "image_path": str(ART_DIR / "p2_3_ananya_fear.png"),
            "dialogue": "WHAT IS THAT HORROR?! IT DEVOURS THE WRITING ON THE STONE!",
            "speaker": "Ananya",
            "balloon_coords": (220, 435),
            "max_width": 210
        },
        {
            "id": "p2_4",
            "bbox": (453, 388, 563, 290),
            "image_path": str(ART_DIR / "p2_4_aarav_protect.png"),
            "dialogue": "ANANYA... GET BEHIND ME! NOW!",
            "speaker": "Aarav",
            "is_shout": True,
            "balloon_coords": (735, 435),
            "max_width": 230
        },
        # Tier 3: 2 Panels (Eyes ignite + Celestial flame burst) (y: 683 to 1030)
        {
            "id": "p2_5",
            "bbox": (8, 683, 440, 350),
            "image_path": str(ART_DIR / "p2_5_aarav_eyes_ignite.png"),
            "dialogue": "NOT WHILE I STILL REMEMBER!",
            "speaker": "Aarav",
            "is_shout": True,
            "balloon_coords": (220, 735),
            "max_width": 200
        },
        {
            "id": "p2_6",
            "bbox": (453, 683, 563, 350),
            "image_path": str(ART_DIR / "p2_6_celestial_flame_burst.png"),
            "dialogue": "SHIELD OF THE FIRST DAWN!",
            "speaker": "Aarav",
            "is_shout": True,
            "balloon_coords": (735, 735),
            "max_width": 230,
            "sfx": "BOOOOM!",
            "sfx_coords": (480, 710),
            "sfx_size": 40,
            "sfx_color": (255, 200, 30)
        },
        # Tier 4: 2 Panels (Fire vs Shadow + Shadow overwhelm) (y: 1038 to 1498)
        {
            "id": "p2_7",
            "bbox": (8, 1038, 501, 460),
            "image_path": str(ART_DIR / "p2_7_fire_vs_shadow.png"),
            "sfx": "KRRR-SHHH!",
            "sfx_coords": (30, 1060),
            "sfx_size": 36,
            "sfx_color": (255, 140, 20)
        },
        {
            "id": "p2_8",
            "bbox": (514, 1038, 502, 460),
            "image_path": str(ART_DIR / "p2_8_shadow_overwhelm.png"),
            "dialogue": "THE FLAME... IT'S TOO UNSTABLE! THE SHADOWS ARE CRACKING THE BARRIER!",
            "speaker": "Aarav",
            "balloon_coords": (765, 1090),
            "max_width": 230
        }
    ]

    out_p2 = FINAL_DIR / "perfect_chapter_002_page_002.png"
    compositor.composite_page(p2_panels, 2, out_p2)
    shutil.copy(str(out_p2), str(ARTIFACTS_DIR / "perfect_chapter_002_page_002.png"))

    # =========================================================================
    # PAGE 3: THE SOVEREIGN'S JUDGMENT (8 PANELS)
    # =========================================================================
    p3_panels = [
        # Tier 1: 2 Panels (Lightning crash + Neel arrival) (y: 8 to 360)
        {
            "id": "p3_1",
            "bbox": (8, 8, 440, 355),
            "image_path": str(ART_DIR / "p3_1_lightning_crash.png"),
            "sfx": "ZAPPPP-KRAAAACK!",
            "sfx_coords": (25, 30),
            "sfx_size": 34,
            "sfx_color": (40, 210, 255)
        },
        {
            "id": "p3_2",
            "bbox": (453, 8, 563, 355),
            "image_path": str(ART_DIR / "p3_2_neel_arrival.png"),
            "dialogue": "ENOUGH, VERMIN OF THE VOID.",
            "speaker": "Neel",
            "balloon_coords": (735, 60),
            "max_width": 230
        },
        # Tier 2: 2 Panels (Neel vortex hand + Vortex shockwave) (y: 368 to 660)
        {
            "id": "p3_3",
            "bbox": (8, 368, 440, 290),
            "image_path": str(ART_DIR / "p3_3_neel_vortex_hand.png"),
            "sfx": "WHOOOSH...",
            "sfx_coords": (30, 390),
            "sfx_size": 34,
            "sfx_color": (60, 220, 255)
        },
        {
            "id": "p3_4",
            "bbox": (453, 368, 563, 290),
            "image_path": str(ART_DIR / "p3_4_vortex_shockwave.png"),
            "dialogue": "RETURN TO NOTHINGNESS.",
            "speaker": "Neel",
            "balloon_coords": (735, 410),
            "max_width": 220,
            "sfx": "SHRRR-BOOM!",
            "sfx_coords": (480, 600),
            "sfx_size": 36,
            "sfx_color": (80, 200, 255)
        },
        # Tier 3: 2 Panels (Aarav shocked + Neel close) (y: 663 to 960)
        {
            "id": "p3_5",
            "bbox": (8, 663, 501, 295),
            "image_path": str(ART_DIR / "p3_5_aarav_shocked.png"),
            "dialogue": "YOU... YOU'RE THE SOVEREIGN FROM THE MOONLIT CORRIDOR...",
            "speaker": "Aarav",
            "balloon_coords": (260, 710),
            "max_width": 220
        },
        {
            "id": "p3_6",
            "bbox": (514, 663, 502, 295),
            "image_path": str(ART_DIR / "p3_6_neel_close.png"),
            "dialogue": "A SPARK WITHOUT DISCIPLINE WILL ONLY BURN THE WORLD IT SEEKS TO SAVE, AARAV.",
            "speaker": "Neel",
            "balloon_coords": (765, 710),
            "max_width": 230
        },
        # Tier 4: 2 Panels (Aarav resolve + Temple roof constellation) (y: 963 to 1395)
        {
            "id": "p3_7",
            "bbox": (8, 963, 440, 420),
            "image_path": str(ART_DIR / "p3_7_aarav_resolve.png"),
            "dialogue": "THEN TEACH ME. BECAUSE I WON'T LET THEM ERASE ANOTHER STORY.",
            "speaker": "Aarav",
            "balloon_coords": (225, 1020),
            "max_width": 210
        },
        {
            "id": "p3_8",
            "bbox": (453, 963, 563, 420),
            "image_path": str(ART_DIR / "p3_8_temple_roof_constellation.png"),
            "dialogue": "THE FIRST PILLAR HAS FRACTURED AT THE SUNKEN SPIRE. THE HUNT HAS BEGUN.",
            "speaker": "Neel",
            "balloon_coords": (735, 1020),
            "max_width": 240
        }
    ]

    out_p3 = FINAL_DIR / "perfect_chapter_002_page_003.png"
    compositor.composite_page(p3_panels, 3, out_p3, has_ending_banner=True)
    shutil.copy(str(out_p3), str(ARTIFACTS_DIR / "perfect_chapter_002_page_003.png"))

    print("\n[=== CHAPTER 2 MASTER PAGES RENDERED AND VERIFIED ===]")

if __name__ == "__main__":
    render_chapter_2()
