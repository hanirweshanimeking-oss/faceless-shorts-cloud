"""
Dragon Studios India - Thumbnail & Cover Design Agent
Generates branded, high-contrast, atmospheric anime covers and thumbnails
for Instagram Reels (9:16) and YouTube Shorts / Long-form (16:9 & 9:16).
"""

import os
import subprocess
from typing import Dict, Any, Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FFMPEG_BIN = "C:\\Users\\DESKTOP\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-9.0.2-full_build\\bin\\ffmpeg.exe"
if not os.path.exists(FFMPEG_BIN):
    FFMPEG_BIN = "ffmpeg"

FONT_PATH = "C:\\Windows\\Fonts\\arialbd.ttf"
IMPACT_FONT_PATH = "C:\\Windows\\Fonts\\impact.ttf"

def extract_frame_from_video(
    video_path: str,
    output_image_path: str,
    timestamp_seconds: float = 1.5
) -> str:
    """Extracts a high-quality keyframe from a video at the specified timestamp."""
    os.makedirs(os.path.dirname(os.path.abspath(output_image_path)), exist_ok=True)
    cmd = [
        FFMPEG_BIN, "-y",
        "-ss", str(timestamp_seconds),
        "-i", video_path,
        "-vframes", "1",
        "-q:v", "2",
        output_image_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_image_path

def generate_reels_cover(
    background_image_path: str,
    output_cover_path: str,
    title_text: str,
    badge_text: str = "DRAGON STUDIOS",
    width: int = 1080,
    height: int = 1920
) -> str:
    """
    Creates a styled 9:16 vertical cover for Instagram Reels.
    Adds dark anime gradient overlay, bold high-contrast text, and branding.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_cover_path)), exist_ok=True)

    if os.path.exists(background_image_path):
        base_img = Image.open(background_image_path).convert("RGBA")
        base_img = base_img.resize((width, height), Image.Resampling.LANCZOS)
    else:
        # Fallback dark background
        base_img = Image.new("RGBA", (width, height), (11, 12, 16, 255))

    # Create dark gradient overlay for top & bottom readability
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)

    # Top dark gradient (for badge)
    for y in range(400):
        alpha = int(220 * (1.0 - (y / 400.0)))
        draw_overlay.line([(0, y), (width, y)], fill=(8, 8, 12, alpha))

    # Bottom dark gradient (for title text)
    for y in range(height - 800, height):
        progress = (y - (height - 800)) / 800.0
        alpha = int(240 * progress)
        draw_overlay.line([(0, y), (width, y)], fill=(8, 8, 12, alpha))

    # Merge base with gradient overlay
    composite = Image.alpha_composite(base_img, overlay)
    draw = ImageDraw.Draw(composite)

    # Load fonts
    try:
        badge_font = ImageFont.truetype(FONT_PATH, size=36)
        title_font = ImageFont.truetype(IMPACT_FONT_PATH, size=72)
    except Exception:
        badge_font = ImageFont.load_default()
        title_font = ImageFont.load_default()

    # Draw Dragon Studios branding badge at top
    badge_box = draw.textbbox((0, 0), badge_text, font=badge_font)
    badge_w = badge_box[2] - badge_box[0]
    badge_x = (width - badge_w) // 2
    badge_y = 120

    # Draw badge background pill
    draw.rounded_rectangle(
        [badge_x - 20, badge_y - 10, badge_x + badge_w + 20, badge_y + 45],
        radius=15,
        fill=(147, 51, 234, 180),  # Royal anime purple
        outline=(255, 255, 255, 200),
        width=2
    )
    draw.text((badge_x, badge_y), badge_text, font=badge_font, fill=(255, 255, 255, 255))

    # Draw title text at bottom (with drop shadow & border)
    # Split title if too long
    words = title_text.upper().split()
    lines = []
    current_line = []
    for w in words:
        current_line.append(w)
        test_line = " ".join(current_line)
        bbox = draw.textbbox((0, 0), test_line, font=title_font)
        if (bbox[2] - bbox[0]) > (width - 120):
            current_line.pop()
            lines.append(" ".join(current_line))
            current_line = [w]
    if current_line:
        lines.append(" ".join(current_line))

    # Render lines from bottom upward
    line_height = 85
    start_y = height - 500 - (len(lines) * line_height)

    for idx, line in enumerate(lines):
        line_bbox = draw.textbbox((0, 0), line, font=title_font)
        line_w = line_bbox[2] - line_bbox[0]
        line_x = (width - line_w) // 2
        line_y = start_y + (idx * line_height)

        # Drop shadow
        draw.text((line_x + 4, line_y + 4), line, font=title_font, fill=(0, 0, 0, 255))
        # Main text (Gold / White)
        text_color = (255, 215, 0, 255) if idx == 0 else (255, 255, 255, 255)
        draw.text((line_x, line_y), line, font=title_font, fill=text_color)

    # Save final JPG cover
    rgb_img = composite.convert("RGB")
    rgb_img.save(output_cover_path, "JPEG", quality=95)
    return output_cover_path
