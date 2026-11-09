"""
Agent 7: Effects Agent
Synthesizes magical dragon auras, celestial flames, lightning tendrils, speed lines, and sound effects (SFX onomatopoeia).
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math
from pathlib import Path
from typing import Tuple, Optional

class EffectsAgent:
    def __init__(self, effects_dir: Path):
        self.effects_dir = effects_dir
        self.effects_dir.mkdir(parents=True, exist_ok=True)

    def render_sfx(
        self,
        panel_img: Image.Image,
        sfx_text: str,
        style: str = "EXPLOSION",
        position: Optional[Tuple[int, int]] = None
    ) -> Image.Image:
        """
        Overlays dramatic manga katakana/english stylized sound effects onto a panel.
        """
        draw = ImageDraw.Draw(panel_img)
        w, h = panel_img.size
        
        font_size = int(min(w, h) * 0.14)
        try:
            # Try system bold font or default
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()

        # Text bounding box calculation
        bbox = draw.textbbox((0, 0), sfx_text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

        if not position:
            if style == "EXPLOSION":
                x = (w - tw) // 2
                y = int(h * 0.35)
            elif style == "SLASH":
                x = int(w * 0.15)
                y = int(h * 0.25)
            else:
                x = int(w * 0.55)
                y = int(h * 0.15)
        else:
            x, y = position

        # Draw thick black outline with white/screentone interior for classic manga SFX
        outline_thickness = max(4, font_size // 10)
        for ox in range(-outline_thickness, outline_thickness + 1):
            for oy in range(-outline_thickness, outline_thickness + 1):
                draw.text((x + ox, y + oy), sfx_text, font=font, fill=(10, 10, 10))

        # Inner vibrant white/high-contrast text
        draw.text((x, y), sfx_text, font=font, fill=(255, 255, 255))
        return panel_img
