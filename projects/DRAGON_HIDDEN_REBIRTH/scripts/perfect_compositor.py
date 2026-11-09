"""
DRAGON: HIDDEN REBIRTH - SSS+ Master Manga Page Compositor
Exact calibration to Hanirwesh's canonical CHITRAN specification:
- Dimensions: 1024 x 1536 (2:3 aspect ratio matching Pages 1-7)
- Margins: 8px white trim, 5px inter-panel gutters, 2px solid black panel frames
- Lettering: ComicNeue-BoldItalic all-caps typography
- Speech balloons: Tight padding (14px/10px), smooth oval contours, 2px crisp outlines
- Narration boxes: Crisp rectangular caption boxes with thin 2px borders
- Sound effects: Bangers dynamic manga lettering with fiery colored drop shadows
"""

import os
import sys
import textwrap
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = Path(__file__).parent.parent
FONTS_DIR = ROOT_DIR / "fonts"
COMIC_FONT = FONTS_DIR / "ComicNeue-BoldItalic.ttf"
SFX_FONT = FONTS_DIR / "Bangers-Regular.ttf"

class PerfectMangaCompositor:
    def __init__(self, canvas_w: int = 1024, canvas_h: int = 1536):
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h

    def _get_font(self, size: int) -> ImageFont.FreeTypeFont:
        if COMIC_FONT.exists():
            return ImageFont.truetype(str(COMIC_FONT), size)
        return ImageFont.load_default()

    def _get_sfx_font(self, size: int) -> ImageFont.FreeTypeFont:
        if SFX_FONT.exists():
            return ImageFont.truetype(str(SFX_FONT), size)
        return ImageFont.load_default()

    def draw_dialogue_balloon(
        self,
        draw: ImageDraw.Draw,
        text: str,
        speaker: str,
        center_x: int,
        center_y: int,
        max_width: int = 240,
        is_thought: bool = False,
        tail_target: Optional[Tuple[int, int]] = None
    ):
        """Draws a snug, authentic manhwa dialogue balloon or rectangular narration box."""
        font_size = 17
        font = self._get_font(font_size)
        text_caps = text.upper()

        avg_char_w = 9
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

        # Keep inside canvas
        if x0 < 15:
            x0, x1 = 15, 15 + bw
        if x1 > self.canvas_w - 15:
            x1, x0 = self.canvas_w - 15, self.canvas_w - 15 - bw

        if speaker.upper() == "NARRATOR":
            # Rectangular Narration Box
            draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=(10, 10, 15), width=2)
        elif is_thought:
            # Oval Thought Balloon
            draw.ellipse([x0, y0, x1, y1], fill=(255, 255, 255), outline=(10, 10, 15), width=2)
            # Trailing thought circles
            cx = (x0 + x1) // 2
            draw.ellipse([cx - 8, y1 + 3, cx + 2, y1 + 13], fill=(255, 255, 255), outline=(10, 10, 15), width=2)
            draw.ellipse([cx - 14, y1 + 15, cx - 8, y1 + 21], fill=(255, 255, 255), outline=(10, 10, 15), width=2)
        else:
            # Authentic Manhwa Elliptical Balloon with smooth rounded corners
            rad = min(22, bh // 2)
            draw.rounded_rectangle([x0, y0, x1, y1], radius=rad, fill=(255, 255, 255), outline=(10, 10, 15), width=2)
            
            # Tail pointer
            cx = (x0 + x1) // 2
            tail_x = cx - 10
            tail_y = y1
            draw.polygon([(tail_x, tail_y - 1), (tail_x + 18, tail_y - 1), (tail_x + 6, tail_y + 14)], fill=(255, 255, 255), outline=(10, 10, 15))
            # Clear seam line
            draw.line([(tail_x + 1, tail_y), (tail_x + 17, tail_y)], fill=(255, 255, 255), width=3)

        # Draw centered text lines
        cur_y = y0 + padding_y
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            lw = bbox[2] - bbox[0]
            lx = x0 + (bw - lw) // 2
            draw.text((lx, cur_y), line, font=font, fill=(10, 10, 15))
            cur_y += line_height

    def draw_sfx(self, draw: ImageDraw.Draw, text: str, x: int, y: int, size: int = 34):
        """Draws dynamic stylized manga sound effects with black outline and glowing color."""
        font = self._get_sfx_font(size)
        text_caps = text.upper()
        
        # Black outline / drop shadow
        for ox, oy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2), (-2, 2), (2, -2), (3, 3)]:
            draw.text((x + ox, y + oy), text_caps, font=font, fill=(10, 10, 15))
            
        # Glowing inner text
        draw.text((x, y), text_caps, font=font, fill=(255, 180, 20))

    def composite_page(
        self,
        panels_data: List[Dict[str, Any]],
        page_num: int,
        out_path: Path,
        chapter_title: Optional[str] = None
    ) -> Path:
        """
        Composites an authentic multi-panel manga page with tight gutters and proper lettering.
        """
        canvas = Image.new("RGB", (self.canvas_w, self.canvas_h), (252, 252, 252))
        draw = ImageDraw.Draw(canvas)

        # 1. Paste all panels
        for p in panels_data:
            x, y, w, h = p["bbox"]
            img_path = Path(p["image_path"])
            if img_path.exists():
                panel_img = Image.open(img_path).convert("RGB")
                panel_resized = panel_img.resize((w, h), Image.Resampling.LANCZOS)
                
                # Draw crisp 2px solid black border around panel image
                panel_draw = ImageDraw.Draw(panel_resized)
                panel_draw.rectangle([0, 0, w - 1, h - 1], outline=(8, 8, 12), width=2)
                
                canvas.paste(panel_resized, (x, y))

        # 2. Draw Speech Balloons, Narration, and SFX
        for p in panels_data:
            x, y, w, h = p["bbox"]
            dialogue = p.get("dialogue")
            speaker = p.get("speaker", "")
            balloon_pos = p.get("balloon_pos", "TOP_LEFT")
            is_thought = p.get("is_thought", False)
            sfx = p.get("sfx")

            if dialogue:
                bx, by = p.get("balloon_coords", (0, 0))
                if bx == 0 and by == 0:
                    if "TOP_LEFT" in balloon_pos:
                        bx = x + int(w * 0.28)
                        by = y + int(h * 0.22)
                    elif "TOP_RIGHT" in balloon_pos:
                        bx = x + int(w * 0.72)
                        by = y + int(h * 0.22)
                    elif "BOTTOM_CENTER" in balloon_pos:
                        bx = x + int(w * 0.5)
                        by = y + int(h * 0.78)
                    else:
                        bx = x + int(w * 0.5)
                        by = y + int(h * 0.3)
                
                max_w = p.get("max_width", 220)
                self.draw_dialogue_balloon(draw, dialogue, speaker, bx, by, max_width=max_w, is_thought=is_thought)

            if sfx:
                sfx_x, sfx_y = p.get("sfx_coords", (x + 25, y + 25))
                self.draw_sfx(draw, sfx, sfx_x, sfx_y, size=p.get("sfx_size", 34))

        # 3. Draw Bottom Folio / Page Number
        page_font = self._get_font(18)
        p_str = f"{page_num}"
        bbox = draw.textbbox((0, 0), p_str, font=page_font)
        pw = bbox[2] - bbox[0]
        draw.text(((self.canvas_w - pw) // 2, self.canvas_h - 22), p_str, font=page_font, fill=(100, 100, 100))

        out_path.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(out_path, "PNG", dpi=(300, 300))
        print(f"[+] Master Page exported to: {out_path} ({self.canvas_w}x{self.canvas_h})")
        return out_path
