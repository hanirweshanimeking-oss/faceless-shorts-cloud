"""
Agent 8: Composition Agent
Assembles panels onto the 300 DPI master canvas, formats speech balloons, dialogue text, and sound effects.
"""

import sqlite3
import textwrap
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import Dict, Any, List, Tuple

class CompositionAgent:
    def __init__(self, db_path: Path, final_pages_dir: Path):
        self.db_path = db_path
        self.final_pages_dir = final_pages_dir
        self.final_pages_dir.mkdir(parents=True, exist_ok=True)

    def draw_speech_balloon(
        self,
        draw: ImageDraw.Draw,
        text: str,
        speaker: str,
        center_x: int,
        center_y: int,
        max_width: int = 450,
        is_thought: bool = False
    ) -> Tuple[int, int, int, int]:
        """
        Draws an authentic manga oval speech balloon with clean word-wrapping and tail pointer.
        """
        font_size = 32
        try:
            font = ImageFont.truetype("arialbd.ttf" if speaker == "Inquisitor" else "arial.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()

        # Word wrap text
        avg_char_w = 16
        wrap_width = max(12, max_width // avg_char_w)
        lines = textwrap.wrap(text, width=wrap_width)
        
        # Calculate text block dimensions
        line_height = int(font_size * 1.35)
        text_block_h = len(lines) * line_height
        max_line_w = max(draw.textbbox((0, 0), line, font=font)[2] for line in lines) if lines else 100
        
        padding_x = 36
        padding_y = 28
        bw = max_line_w + (padding_x * 2)
        bh = text_block_h + (padding_y * 2)
        
        x0 = center_x - bw // 2
        y0 = center_y - bh // 2
        x1 = x0 + bw
        y1 = y0 + bh

        # Draw balloon background with border
        if speaker.upper() == "NARRATOR":
            # Authentic rectangular manhwa narration box
            draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=(15, 15, 20), width=4)
        elif is_thought:
            # Cloud/thought style
            draw.ellipse([x0, y0, x1, y1], fill=(255, 255, 255), outline=(10, 10, 10), width=4)
            # Small thought bubbles leading down
            draw.ellipse([center_x - 25, y1 + 6, center_x - 11, y1 + 20], fill=(255, 255, 255), outline=(10, 10, 10), width=3)
            draw.ellipse([center_x - 38, y1 + 24, center_x - 30, y1 + 32], fill=(255, 255, 255), outline=(10, 10, 10), width=2)
        else:
            # Elliptical dialogue balloon
            draw.rounded_rectangle([x0, y0, x1, y1], radius=28, fill=(255, 255, 255), outline=(10, 10, 10), width=4)
            # Tail pointer
            tail_x = center_x - 20
            tail_y = y1
            draw.polygon([(tail_x, tail_y - 2), (tail_x + 35, tail_y - 2), (tail_x + 15, tail_y + 35)], fill=(255, 255, 255), outline=(10, 10, 10))
            # Clear seam
            draw.line([(tail_x + 2, tail_y), (tail_x + 33, tail_y)], fill=(255, 255, 255), width=6)

        # Draw centered text lines
        cur_y = y0 + padding_y
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            lw = bbox[2] - bbox[0]
            lx = center_x - (lw // 2)
            draw.text((lx, cur_y), line, font=font, fill=(10, 10, 10))
            cur_y += line_height

        return (x0, y0, x1, y1)

    def composite_page(self, page_id: str) -> Path:
        """
        Gathers all panels for a page from DB and composites them into the 300 DPI master canvas.
        """
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pages WHERE id = ?", (page_id,))
            page_rec = cursor.fetchone()
            if not page_rec:
                raise ValueError(f"Page {page_id} not found.")

            cursor.execute("SELECT c.chapter_number FROM chapters c WHERE c.id = ?", (page_rec["chapter_id"],))
            ch_row = cursor.fetchone()
            chapter_num = ch_row["chapter_number"] if ch_row else 1

            cursor.execute("SELECT * FROM panels WHERE page_id = ? ORDER BY panel_index ASC", (page_id,))
            panels = [dict(p) for p in cursor.fetchall()]

        # Master page canvas (2480 x 3508 B5 standard 300 DPI)
        pw = page_rec["width_px"]
        ph = page_rec["height_px"]
        canvas = Image.new("RGB", (pw, ph), (255, 255, 255))
        draw = ImageDraw.Draw(canvas)

        # Draw page trim guide / margin boundary
        margin = 60
        draw.rectangle([margin, margin, pw - margin, ph - margin], outline=(230, 230, 230), width=1)

        # Composite each panel
        for p in panels:
            raw_path = p.get("raw_panel_path")
            if raw_path and Path(raw_path).exists():
                panel_img = Image.open(raw_path)
                canvas.paste(panel_img, (p["bbox_x"], p["bbox_y"]))
            else:
                # Placeholder frame
                draw.rectangle([p["bbox_x"], p["bbox_y"], p["bbox_x"] + p["bbox_w"], p["bbox_y"] + p["bbox_h"]], outline=(15, 15, 15), width=6)

            # Draw Speech Balloons & Dialogue
            dialogue = p.get("dialogue_text")
            speaker = p.get("speaker_name") or ""
            thought = p.get("thought_text")
            
            if dialogue:
                pos = p.get("balloon_position", "TOP_LEFT")
                px, py = p["bbox_x"], p["bbox_y"]
                pw_p, ph_p = p["bbox_w"], p["bbox_h"]
                
                if "TOP_RIGHT" in pos:
                    bx = px + int(pw_p * 0.72)
                    by = py + int(ph_p * 0.22)
                elif "TOP_LEFT" in pos:
                    bx = px + int(pw_p * 0.28)
                    by = py + int(ph_p * 0.22)
                elif "BOTTOM_CENTER" in pos:
                    bx = px + int(pw_p * 0.5)
                    by = py + int(ph_p * 0.78)
                else:
                    bx = px + int(pw_p * 0.35)
                    by = py + int(ph_p * 0.25)
                
                self.draw_speech_balloon(draw, dialogue, speaker, bx, by)

            if thought:
                # Thought balloon
                th_x = p["bbox_x"] + int(p["bbox_w"] * 0.3)
                th_y = p["bbox_y"] + int(p["bbox_h"] * 0.65)
                self.draw_speech_balloon(draw, thought, speaker, th_x, th_y, is_thought=True)

        # Draw Bottom Chapter/Page Folio
        page_num = page_rec["page_number"]
        folio_text = f"CHITRAN: THE MANGA  |  CHAPTER {chapter_num}  |  PAGE {page_num}"
        try:
            folio_font = ImageFont.truetype("arial.ttf", 22)
        except Exception:
            folio_font = ImageFont.load_default()
            
        draw.text((margin + 20, ph - margin + 15), folio_text, font=folio_font, fill=(120, 120, 120))
        draw.text((pw - margin - 80, ph - margin + 15), f"{page_num}", font=folio_font, fill=(100, 100, 100))

        # Save Final Page
        out_page_path = self.final_pages_dir / f"chapter_{chapter_num:03d}_page_{page_num:03d}.png"
        canvas.save(out_page_path, "PNG", dpi=(300, 300))

        # Update DB
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE pages 
                SET master_image_path = ?, status = 'COMPOSITED', updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (str(out_page_path), page_id))
            conn.commit()

        return out_page_path
