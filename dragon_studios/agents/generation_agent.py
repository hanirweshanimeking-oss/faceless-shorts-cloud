"""
Dragon Studios India - Stage 5: Asset Generation Engine
Synthesizes studio neural voiceovers, renders procedural high-resolution 1080x1920 visual frames,
and prepares raw scene clips.
"""

import os
import asyncio
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
from typing import Dict, Any, List

from dragon_studios.agents.voice_agent import synthesize_speech
from dragon_studios.agents.script_agent import VideoProductionPlan, SceneBlueprint
from dragon_studios.agents.higgsfield_engine import HiggsfieldWebGPUEngine

class GenerationEngine:
    def __init__(self):
        self.higgsfield_engine = HiggsfieldWebGPUEngine()
    @staticmethod
    def synthesize_scene_audio(text: str, output_path: str, voice: str = "en-US-ChristopherNeural") -> str:
        """
        Synthesizes crystal-clear neural voiceover using Edge-TTS.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        synthesize_speech(text=text, output_path=output_path, voice=voice)
        return output_path

    @staticmethod
    def render_procedural_scene_frame(
        width: int = 1080,
        height: int = 1920,
        headline: str = "",
        subtext: str = "",
        pillar: str = "DARK_PSYCHOLOGY",
        scene_num: int = 1
    ) -> Image.Image:
        """
        Renders a branded, high-contrast vertical 9:16 canvas frame using Pillow.
        """
        img = Image.new("RGB", (width, height), color=(11, 12, 16))
        draw = ImageDraw.Draw(img)

        # Draw dark vertical gradient
        if pillar == "DARK_PSYCHOLOGY":
            top_color = (20, 10, 35)       # deep obsidian purple
            bottom_color = (5, 5, 8)       # midnight black
            accent_color = (147, 51, 234)  # vibrant purple
        elif pillar == "AI_TOOLS":
            top_color = (8, 25, 45)        # tech midnight cyan
            bottom_color = (3, 7, 18)      # obsidian
            accent_color = (6, 182, 212)   # electric cyan
        elif pillar in ["CONVERSATIONAL_PODCAST", "RAJ_SHAMANI"]:
            top_color = (28, 22, 10)       # rich dark amber/gold studio mood
            bottom_color = (6, 5, 4)        # obsidian midnight
            accent_color = (234, 179, 8)   # podcast vibrant yellow/gold
        else: # ORIGINAL_MANGA
            top_color = (30, 8, 15)        # crimson dark
            bottom_color = (4, 4, 6)       # deep void
            accent_color = (239, 68, 68)   # dragon red

        for y in range(height):
            ratio = y / height
            r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Draw decorative glowing border lines
        margin = 40
        draw.rectangle(
            [margin, margin, width - margin, height - margin],
            outline=accent_color,
            width=3
        )

        # Draw Dragon Studios India header watermark
        draw.text((width // 2, 120), "DRAGON STUDIOS INDIA", fill=(160, 160, 180), anchor="mm")
        draw.line([(width // 2 - 120, 150), (width // 2 + 120, 150)], fill=accent_color, width=2)

        # Draw Scene Badge
        if pillar in ["CONVERSATIONAL_PODCAST", "RAJ_SHAMANI"]:
            badge_text = "QUESTION" if scene_num in [1, 5] else "THE INSIGHT"
        elif pillar == "DARK_PSYCHOLOGY":
            badge_text = f"RULE #{scene_num}"
        else:
            badge_text = f"PHASE {scene_num}"
        draw.rectangle([width // 2 - 100, 480, width // 2 + 100, 540], fill=accent_color)
        draw.text((width // 2, 510), badge_text, fill=(255, 255, 255), anchor="mm")

        # Draw Main Headline (word wrapped)
        words = headline.split()
        lines = []
        curr = []
        for w in words:
            curr.append(w)
            if len(" ".join(curr)) > 22:
                lines.append(" ".join(curr[:-1]))
                curr = [w]
        if curr:
            lines.append(" ".join(curr))

        start_y = 660
        for i, line in enumerate(lines[:4]):
            draw.text(
                (width // 2, start_y + (i * 70)),
                line.upper(),
                fill=(255, 255, 255),
                anchor="mm"
            )

        # Draw Subtext / Core Concept
        if subtext:
            draw.text(
                (width // 2, 1200),
                subtext[:60],
                fill=(200, 210, 225),
                anchor="mm"
            )

        # Draw Bottom Engagement Safe Zone
        draw.rectangle([margin + 20, height - 240, width - margin - 20, height - 120], outline=(80, 80, 100), width=1)
        draw.text((width // 2, height - 180), "[SAVE THIS REEL • FOLLOW @DRAGON.STUDIOS.INDIA]", fill=(240, 240, 255), anchor="mm")

        return img

    def render_scene_frame(
        self,
        headline: str,
        subtext: str = "",
        pillar: str = "DARK_PSYCHOLOGY",
        scene_num: int = 1,
        width: int = 1080,
        height: int = 1920,
        use_higgsfield_webgpu: bool = False
    ) -> Image.Image:
        """
        Renders a scene frame using local Higgsfield WebGPU 3D path tracing when requested,
        falling back seamlessly to high-contrast procedural studio canvas.
        """
        if use_higgsfield_webgpu and self.higgsfield_engine.available:
            import tempfile
            with tempfile.NamedTemporaryFile("w", suffix=".png", delete=False) as f:
                temp_png = f.name
            try:
                self.higgsfield_engine.render_composite_frame(
                    headline=headline,
                    subtext=subtext,
                    pillar=pillar,
                    scene_num=scene_num,
                    output_path=temp_png,
                    width=width,
                    height=height,
                    allow_webgpu=True
                )
                if os.path.exists(temp_png) and os.path.getsize(temp_png) > 1000:
                    img = Image.open(temp_png)
                    img.load()
                    return img
            except Exception:
                pass
            finally:
                if os.path.exists(temp_png):
                    try:
                        os.remove(temp_png)
                    except Exception:
                        pass

        return self.render_procedural_scene_frame(
            width=width,
            height=height,
            headline=headline,
            subtext=subtext,
            pillar=pillar,
            scene_num=scene_num
        )

    @staticmethod
    def create_video_clip_from_frame(
        image: Image.Image,
        duration: float,
        output_path: str,
        fps: int = 30
    ) -> str:
        """
        Converts a PIL image frame into a smooth 1080x1920 MP4 video clip.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        height, width, _ = img_np.shape

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        total_frames = max(1, int(duration * fps))
        for _ in range(total_frames):
            out.write(img_np)
        out.release()

        return output_path
