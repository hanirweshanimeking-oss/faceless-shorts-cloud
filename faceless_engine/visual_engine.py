"""
Faceless Shorts Visual Engine - Adaptive Multi-Style 3D & 2D Animation Director
Supports 6 Distinct Social-Media Styles with 1080x1920 (9:16) 30fps Rendering:
1. "Tall Tale 3D": 2D cartoon characters inside bright 3D miniature worlds (heists, loopholes, crazy history)
2. "Deep Dive 3D": Zack D. Films style medical & human body explainers with x-ray organs and microscopic zoom
3. "Inside Out": Science and engineering cross-sections, blueprint grids, rotating mechanisms
4. "Stick Story": Survival life-hacks, what-if scenarios, dynamic stick figure animations and HUD gauges
5. "Night File 3D": Spooky mysteries, crime dossiers, flashlight cone lighting, evidence pinboards
6. "Paper Atlas": Historic battles, ancient empires, vintage parchment map with animated troop arrows
"""

import os
import math
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from typing import List, Dict, Any, Tuple, Optional
from faceless_engine.config import FONTS_DIR
from faceless_engine.director_agent import DirectorAgent, VisualDirection

# Signature Color Palettes
INK_COLOR = (36, 23, 38)        # Dark plum ink #241726
GOLD_COLOR = (255, 205, 50)     # Hero gold #ffcd32
CYAN_GLOW = (0, 220, 255)       # Bio/tech cyan
RED_ALERT = (240, 45, 55)       # Alarm/danger red
PARCHMENT = (235, 218, 185)     # Antique paper map

class TallTaleRenderer:
    """
    Backwards-compatible Adaptive Visual Renderer capable of orchestrating
    all 6 visual animation styles.
    """
    def __init__(self, width: int = 1080, height: int = 1920):
        self.width = width
        self.height = height
        self._font_cache = {}

    def get_font(self, size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
        key = (size, bold)
        if key not in self._font_cache:
            font_file = "arialbd.ttf" if bold else "arial.ttf"
            font_path = os.path.join(FONTS_DIR, font_file)
            if not os.path.exists(font_path):
                font_path = "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf"
            if not os.path.exists(font_path):
                font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
            if not os.path.exists(font_path):
                font_path = font_file
            try:
                self._font_cache[key] = ImageFont.truetype(font_path, size)
            except Exception:
                self._font_cache[key] = ImageFont.load_default()
        return self._font_cache[key]

    def draw_sky_background(self, draw: ImageDraw.ImageDraw, top_color: Tuple[int, int, int], horizon_color: Tuple[int, int, int]):
        """Renders smooth vertical gradient using fast NumPy broadcasting."""
        h, w = self.height, self.width
        top = np.array(top_color, dtype=np.float32)
        horizon = np.array(horizon_color, dtype=np.float32)
        r = np.linspace(top[0], horizon[0], h)[:, None]
        g = np.linspace(top[1], horizon[1], h)[:, None]
        b = np.linspace(top[2], horizon[2], h)[:, None]
        arr = np.dstack([np.broadcast_to(r, (h, w)), np.broadcast_to(g, (h, w)), np.broadcast_to(b, (h, w))]).astype(np.uint8)
        bg_img = Image.fromarray(arr, mode="RGB")
        draw._image.paste(bg_img, (0, 0))

    # =========================================================================
    # CHARACTER SYSTEM (Supports Cartoon, Anatomical, Stick, Detective)
    # =========================================================================
    def draw_character(
        self,
        draw: ImageDraw.ImageDraw,
        cx: int,
        cy: int,
        scale: float = 1.0,
        archetype: str = "cartoon_hero",
        outfit: str = "suit",
        hair_style: str = "messy",
        expression: str = "smirk",
        action: str = "present_coin",
        bob_y: float = 0.0,
        skin_tone: Tuple[int, int, int] = (255, 226, 194)
    ):
        cy = int(cy + bob_y)

        if archetype == "stick_figure":
            # Dynamic agile stick figure
            head_r = int(50 * scale)
            head_cy = cy - int(240 * scale)
            draw.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], fill=skin_tone, outline=INK_COLOR, width=int(8 * scale))
            # Eyes
            draw.ellipse([cx - 15, head_cy - 10, cx - 5, head_cy], fill=INK_COLOR)
            draw.ellipse([cx + 5, head_cy - 10, cx + 15, head_cy], fill=INK_COLOR)
            # Body spine
            spine_bottom = cy - int(90 * scale)
            draw.line([(cx, head_cy + head_r), (cx, spine_bottom)], fill=INK_COLOR, width=int(12 * scale))
            # Legs
            leg_w = int(10 * scale)
            draw.line([(cx, spine_bottom), (cx - int(45 * scale), cy)], fill=INK_COLOR, width=leg_w)
            draw.line([(cx, spine_bottom), (cx + int(45 * scale), cy)], fill=INK_COLOR, width=leg_w)
            # Arms
            if expression in ["panic", "shock"]:
                # Hands in air
                draw.line([(cx, head_cy + head_r + 20), (cx - int(60 * scale), head_cy - 20)], fill=INK_COLOR, width=leg_w)
                draw.line([(cx, head_cy + head_r + 20), (cx + int(60 * scale), head_cy - 20)], fill=INK_COLOR, width=leg_w)
            else:
                draw.line([(cx, head_cy + head_r + 20), (cx - int(50 * scale), spine_bottom - 20)], fill=INK_COLOR, width=leg_w)
                draw.line([(cx, head_cy + head_r + 20), (cx + int(50 * scale), spine_bottom - 20)], fill=INK_COLOR, width=leg_w)
            return

        elif archetype == "anatomical_figure":
            # Zack D. Films 3D translucent body mannequin
            head_w = int(120 * scale)
            head_h = int(150 * scale)
            head_cy = cy - int(220 * scale)
            # Semi-transparent skin shell
            draw.ellipse([cx - head_w // 2, head_cy - head_h // 2, cx + head_w // 2, head_cy + head_h // 2], fill=(225, 235, 245), outline=CYAN_GLOW, width=int(6 * scale))
            # Glowing X-ray Brain in skull
            draw.ellipse([cx - int(38 * scale), head_cy - int(45 * scale), cx + int(38 * scale), head_cy + int(5 * scale)], fill=(255, 110, 160), outline=(220, 60, 120), width=3)
            # Torso outline with glowing spine
            torso_top = head_cy + head_h // 2
            torso_bottom = cy - int(60 * scale)
            draw.rounded_rectangle([cx - int(75 * scale), torso_top, cx + int(75 * scale), torso_bottom], radius=25, fill=(215, 230, 245), outline=CYAN_GLOW, width=int(6 * scale))
            # Ribcage lines
            for rib_y in range(torso_top + 30, torso_bottom - 20, 28):
                draw.arc([cx - int(60 * scale), rib_y, cx + int(60 * scale), rib_y + 25], 0, 180, fill=CYAN_GLOW, width=4)
            # Glowing heart
            draw.ellipse([cx - 20, torso_top + 45, cx + 25, torso_top + 90], fill=(255, 45, 60), outline=(190, 20, 40), width=3)
            # Spine line
            draw.line([(cx, torso_top), (cx, torso_bottom)], fill=(180, 220, 245), width=8)
            # Legs
            draw.line([(cx - 35, torso_bottom), (cx - 45, cy)], fill=CYAN_GLOW, width=int(14 * scale))
            draw.line([(cx + 35, torso_bottom), (cx + 45, cy)], fill=CYAN_GLOW, width=int(14 * scale))
            return

        # Default: 2D Cartoon Bean-Head Character (Tall Tale / Night File / Inside Out)
        head_w = int(140 * scale)
        head_h = int(160 * scale)
        head_cx = cx
        head_cy = int(cy - 180 * scale)

        # 1. Torso / Outfit
        torso_w = int(130 * scale)
        torso_h = int(180 * scale)
        torso_top = head_cy + int(60 * scale)

        if outfit == "scrubs":
            torso_color = (0, 165, 180)
        elif outfit == "trench_coat":
            torso_color = (45, 40, 35)
        elif outfit == "hoodie":
            torso_color = (225, 80, 45)
        elif outfit == "lab_coat":
            torso_color = (245, 245, 250)
        else:
            torso_color = (35, 55, 95)  # Navy suit

        draw.rounded_rectangle(
            [head_cx - torso_w // 2, torso_top, head_cx + torso_w // 2, torso_top + torso_h],
            radius=int(25 * scale),
            fill=torso_color,
            outline=INK_COLOR,
            width=int(8 * scale)
        )

        # Legs & Shoes
        leg_y_start = torso_top + torso_h - int(10 * scale)
        leg_len = int(140 * scale)
        draw.line([(head_cx - int(35 * scale), leg_y_start), (head_cx - int(35 * scale), leg_y_start + leg_len)], fill=INK_COLOR, width=int(10 * scale))
        draw.line([(head_cx + int(35 * scale), leg_y_start), (head_cx + int(35 * scale), leg_y_start + leg_len)], fill=INK_COLOR, width=int(10 * scale))
        draw.ellipse([head_cx - int(50 * scale), leg_y_start + leg_len - 10, head_cx - int(5 * scale), leg_y_start + leg_len + 20], fill=INK_COLOR)
        draw.ellipse([head_cx + int(5 * scale), leg_y_start + leg_len - 10, head_cx + int(50 * scale), leg_y_start + leg_len + 20], fill=INK_COLOR)

        # Head (Bean shape)
        draw.ellipse(
            [head_cx - head_w // 2, head_cy - head_h // 2, head_cx + head_w // 2, head_cy + head_h // 2],
            fill=skin_tone,
            outline=INK_COLOR,
            width=int(8 * scale)
        )

        # Hair
        hair_color = (40, 25, 20)
        if hair_style == "messy":
            for hx in range(head_cx - 50, head_cx + 50, 20):
                draw.polygon([(hx, head_cy - 75), (hx + 12, head_cy - 100), (hx + 24, head_cy - 70)], fill=hair_color, outline=INK_COLOR, width=2)
        elif hair_style == "parted":
            draw.arc([head_cx - 65, head_cy - 90, head_cx + 65, head_cy - 30], 180, 360, fill=hair_color, width=14)

        # Eyes & Facial Expression
        eye_spacing = int(28 * scale)
        eye_y = head_cy - int(8 * scale)
        eye_r = int(9 * scale)

        if expression == "panic" or expression == "shock":
            # Huge panicked round eyes
            draw.ellipse([head_cx - eye_spacing - eye_r - 4, eye_y - eye_r - 4, head_cx - eye_spacing + eye_r + 4, eye_y + eye_r + 4], fill=(255, 255, 255), outline=INK_COLOR, width=4)
            draw.ellipse([head_cx + eye_spacing - eye_r - 4, eye_y - eye_r - 4, head_cx + eye_spacing + eye_r + 4, eye_y + eye_r + 4], fill=(255, 255, 255), outline=INK_COLOR, width=4)
            draw.ellipse([head_cx - eye_spacing - 3, eye_y - 3, head_cx - eye_spacing + 3, eye_y + 3], fill=INK_COLOR)
            draw.ellipse([head_cx + eye_spacing - 3, eye_y - 3, head_cx + eye_spacing + 3, eye_y + 3], fill=INK_COLOR)
            # O-shaped open mouth
            draw.ellipse([head_cx - 15, head_cy + 25, head_cx + 15, head_cy + 55], fill=(180, 40, 50), outline=INK_COLOR, width=4)
        else:
            # Smirk / confident eyes
            draw.ellipse([head_cx - eye_spacing - eye_r, eye_y - eye_r, head_cx - eye_spacing + eye_r, eye_y + eye_r], fill=INK_COLOR)
            draw.ellipse([head_cx + eye_spacing - eye_r, eye_y - eye_r, head_cx + eye_spacing + eye_r, eye_y + eye_r], fill=INK_COLOR)
            # Confident smile
            draw.arc([head_cx - 24, head_cy + 15, head_cx + 24, head_cy + 45], 0, 180, fill=INK_COLOR, width=int(5 * scale))

    # =========================================================================
    # GENRE SCENE RENDERERS (Deep Dive, Night File, Stick, Inside Out, Paper, Tall Tale)
    # =========================================================================
    def render_deep_dive_scene(self, draw: ImageDraw.ImageDraw, scene: Any, progress: float, bob: float, frame_idx: int):
        """Zack D. Films Medical & Anatomy Deep Dive (x-ray cutaways, cells, biological telemetry)."""
        self.draw_sky_background(draw, (10, 16, 28), (24, 45, 68))
        
        # High-tech Biometric HUD grid in background
        for y in range(250, 1650, 140):
            draw.line([(80, y), (self.width - 80, y)], fill=(20, 55, 80), width=1)
        for x in range(120, self.width - 80, 160):
            draw.line([(x, 250), (x, 1650)], fill=(20, 55, 80), width=1)

        # Pulse wave graph (ECG Monitor)
        ecg_y = 380
        pts = [(100, ecg_y), (350, ecg_y), (380, ecg_y - 80), (410, ecg_y + 60), (440, ecg_y - 30), (460, ecg_y), (980, ecg_y)]
        draw.line(pts, fill=CYAN_GLOW, width=5)

        # Center Anatomical Subject (Zooming into organ/system)
        zoom = 1.0 + progress * 0.18
        self.draw_character(draw, cx=self.width // 2, cy=1450, scale=1.4 * zoom, archetype="anatomical_figure", bob_y=bob)

        # Microscopic cross-section floating window
        win_x = 100
        win_y = 650
        draw.rounded_rectangle([win_x, win_y, win_x + 880, win_y + 440], radius=20, fill=(12, 22, 38), outline=CYAN_GLOW, width=4)
        font_label = self.get_font(28, bold=True)
        draw.text((win_x + 30, win_y + 25), "🔬 MICROSCOPIC MAGNIFICATION (5000X)", fill=CYAN_GLOW, font=font_label)

        # Animated cells / keratin fibers / bacteria
        for i in range(12):
            cell_x = int(win_x + 80 + (i * 70 + progress * 150) % 720)
            cell_y = int(win_y + 120 + (i * 60 + math.sin(frame_idx * 0.1 + i) * 30) % 260)
            # Glowing cell
            draw.ellipse([cell_x - 30, cell_y - 30, cell_x + 30, cell_y + 30], fill=(220, 70, 110), outline=(255, 140, 180), width=4)
            draw.ellipse([cell_x - 10, cell_y - 10, cell_x + 10, cell_y + 10], fill=(120, 20, 50))

        # Warning Biometric Telemetry Callout
        draw.rectangle([win_x + 550, win_y + 340, win_x + 840, win_y + 410], fill=(220, 40, 50))
        font_stat = self.get_font(24, bold=True)
        draw.text((win_x + 695, win_y + 375), "⚠️ CELL DIVISION +84%", fill=(255, 255, 255), font=font_stat, anchor="mm")

    def render_night_file_scene(self, draw: ImageDraw.ImageDraw, scene: Any, progress: float, bob: float, frame_idx: int):
        """Spooky Nocturnal Mystery & Crime Scene (fog, flashlight cone, evidence board, polaroids)."""
        self.draw_sky_background(draw, (6, 8, 14), (18, 22, 34))

        # Glowing full moon with eerie ring
        moon_cx, moon_cy = 840, 320
        draw.ellipse([moon_cx - 100, moon_cy - 100, moon_cx + 100, moon_cy + 100], fill=(240, 245, 255), outline=(100, 120, 150), width=3)
        draw.ellipse([moon_cx - 140, moon_cy - 140, moon_cx + 140, moon_cy + 140], outline=(60, 80, 110), width=2)

        # Evidence Board with red connecting strings
        board_y = 520
        draw.rectangle([80, board_y, self.width - 80, board_y + 600], fill=(35, 28, 24), outline=INK_COLOR, width=6)
        draw.text((self.width // 2, board_y + 40), "CLASSIFIED EVIDENCE DOSSIER", fill=(240, 190, 60), font=self.get_font(32, bold=True), anchor="mm")

        # Polaroid Evidence photos
        for p_i, (px, py, angle) in enumerate([(180, board_y + 140, -5), (460, board_y + 120, 8), (740, board_y + 160, -4)]):
            draw.rectangle([px, py, px + 180, py + 220], fill=(245, 240, 230), outline=INK_COLOR, width=4)
            draw.rectangle([px + 15, py + 15, px + 165, py + 165], fill=(30, 35, 45))
            draw.text((px + 90, py + 195), f"EXHIBIT {chr(65 + p_i)}", fill=INK_COLOR, font=self.get_font(18, bold=True), anchor="mm")

        # Red connecting string
        draw.line([(270, board_y + 250), (550, board_y + 230)], fill=RED_ALERT, width=4)
        draw.line([(550, board_y + 230), (830, board_y + 270)], fill=RED_ALERT, width=4)

        # Huge red rubber stamp
        stamp_font = self.get_font(72, bold=True)
        draw.text((self.width // 2 + 4, board_y + 440 + 4), "UNSOLVED", fill=(20, 0, 0), font=stamp_font, anchor="mm")
        draw.text((self.width // 2, board_y + 440), "UNSOLVED", fill=RED_ALERT, font=stamp_font, anchor="mm")

        # Flashlight beam cone sweeping across bottom
        beam_x = int(self.width // 2 + math.sin(frame_idx * 0.08) * 220)
        draw.polygon([(beam_x, 1150), (beam_x - 320, 1920), (beam_x + 320, 1920)], fill=(255, 255, 200))

        # Detective silhouette on right
        self.draw_character(draw, cx=820, cy=1680, scale=1.35, archetype="cartoon_hero", outfit="trench_coat", expression="focus", bob_y=bob)

    def render_stick_story_scene(self, draw: ImageDraw.ImageDraw, scene: Any, progress: float, bob: float, frame_idx: int):
        """Survival Life-Hacks & What-If Scenarios (stick figure, terrain, survival stats HUD)."""
        # Sunset wilderness gradient
        self.draw_sky_background(draw, (230, 110, 45), (255, 210, 120))

        # Rugged mountain terrain
        pts_mountain = [(0, 1300), (320, 1050), (620, 1220), (880, 980), (self.width, 1260), (self.width, 1920), (0, 1920)]
        draw.polygon(pts_mountain, fill=(75, 45, 30), outline=INK_COLOR, width=6)

        # Survival HUD Gauges
        hud_y = 260
        draw.rounded_rectangle([80, hud_y, self.width - 80, hud_y + 180], radius=16, fill=(20, 25, 35), outline=(255, 140, 20), width=4)
        draw.text((120, hud_y + 35), "SURVIVAL STATS:", fill=(255, 255, 255), font=self.get_font(26, bold=True))

        # Health bar
        draw.text((120, hud_y + 80), "HP: 68%", fill=(255, 60, 60), font=self.get_font(22, bold=True))
        draw.rectangle([250, hud_y + 82, 550, hud_y + 104], fill=(60, 20, 20), outline=INK_COLOR, width=2)
        draw.rectangle([250, hud_y + 82, 250 + int(300 * 0.68), hud_y + 104], fill=(240, 50, 50))

        # Hydration bar
        draw.text((120, hud_y + 120), "WATER: 24%", fill=CYAN_GLOW, font=self.get_font(22, bold=True))
        draw.rectangle([250, hud_y + 122, 550, hud_y + 144], fill=(20, 40, 60), outline=INK_COLOR, width=2)
        draw.rectangle([250, hud_y + 122, 250 + int(300 * 0.24), hud_y + 144], fill=CYAN_GLOW)

        # Danger indicator
        draw.rectangle([620, hud_y + 70, 940, hud_y + 140], fill=(240, 60, 40), outline=INK_COLOR, width=3)
        draw.text((780, hud_y + 105), "⚠️ CRITICAL THREAT", fill=(255, 255, 255), font=self.get_font(22, bold=True), anchor="mm")

        # Campfire flames in middle ground
        fire_x, fire_y = 380, 1420
        flame_h = int(60 + math.sin(frame_idx * 0.4) * 15)
        draw.polygon([(fire_x - 35, fire_y), (fire_x, fire_y - flame_h), (fire_x + 35, fire_y)], fill=(255, 80, 20))
        draw.polygon([(fire_x - 20, fire_y), (fire_x, fire_y - flame_h + 20), (fire_x + 20, fire_y)], fill=(255, 220, 50))

        # Dynamic Stick figure hero acting
        expr = "panic" if (scene and scene.scene_index in [1, 3, 4]) else "smirk"
        self.draw_character(draw, cx=680, cy=1450, scale=1.5, archetype="stick_figure", expression=expr, bob_y=bob)

    def render_inside_out_scene(self, draw: ImageDraw.ImageDraw, scene: Any, progress: float, bob: float, frame_idx: int):
        """Science & Engineering Cross-Sections (blueprint grid, rotating gears, hydraulic cutaway)."""
        self.draw_sky_background(draw, (8, 16, 30), (16, 32, 55))

        # Cyan blueprint isometric grid
        grid_step = 60
        for y in range(0, self.height, grid_step):
            draw.line([(0, y), (self.width, y)], fill=(15, 45, 75), width=1)
        for x in range(0, self.width, grid_step):
            draw.line([(x, 0), (x, self.height)], fill=(15, 45, 75), width=1)

        # Central mechanical assembly (rotating cogwheel)
        gear_cx, gear_cy = self.width // 2, 850
        gear_r = 200
        angle_rot = frame_idx * 0.05
        # Gear teeth
        for a in range(0, 360, 30):
            rad = math.radians(a + math.degrees(angle_rot))
            tx = int(gear_cx + (gear_r + 25) * math.cos(rad))
            ty = int(gear_cy + (gear_r + 25) * math.sin(rad))
            draw.rectangle([tx - 18, ty - 18, tx + 18, ty + 18], fill=(60, 180, 240), outline=(20, 40, 70), width=2)
        draw.ellipse([gear_cx - gear_r, gear_cy - gear_r, gear_cx + gear_r, gear_cy + gear_r], fill=(30, 90, 150), outline=CYAN_GLOW, width=6)
        draw.ellipse([gear_cx - 60, gear_cy - 60, gear_cx + 60, gear_cy + 60], fill=(10, 25, 45), outline=CYAN_GLOW, width=4)

        # Hydraulic piston moving up & down
        piston_h = int(140 + math.sin(frame_idx * 0.15) * 50)
        draw.rectangle([gear_cx - 40, 1150, gear_cx + 40, 1150 + piston_h], fill=(220, 230, 245), outline=INK_COLOR, width=4)
        draw.rectangle([gear_cx - 70, 1150 + piston_h, gear_cx + 70, 1150 + piston_h + 60], fill=(240, 180, 50), outline=INK_COLOR, width=4)

        # Technical Callout lines
        draw.line([(gear_cx + 120, gear_cy - 80), (gear_cx + 340, gear_cy - 160)], fill=(70, 240, 180), width=3)
        draw.rectangle([gear_cx + 340, gear_cy - 190, gear_cx + 500, gear_cy - 130], fill=(12, 28, 48), outline=(70, 240, 180), width=2)
        draw.text((gear_cx + 420, gear_cy - 160), "RPM: 4,800", fill=(70, 240, 180), font=self.get_font(22, bold=True), anchor="mm")

        # Engineer with tablet on left
        self.draw_character(draw, cx=280, cy=1600, scale=1.3, archetype="cartoon_hero", outfit="hoodie", expression="focus", bob_y=bob)

    def render_paper_atlas_scene(self, draw: ImageDraw.ImageDraw, scene: Any, progress: float, bob: float, frame_idx: int):
        """Historical Battles & Maps (antique parchment, marching army arrows, battle markers)."""
        self.draw_sky_background(draw, (225, 205, 170), (245, 230, 205))

        # Vintage map coastline lines
        coast_pts = [(60, 450), (280, 520), (520, 480), (740, 620), (960, 580)]
        draw.line(coast_pts, fill=(160, 140, 110), width=6)
        # Depth wave lines
        for offset in [25, 50]:
            draw.line([(p[0], p[1] + offset) for p in coast_pts], fill=(195, 180, 150), width=2)

        # Ornate Compass Rose on top right
        comp_x, comp_y = 860, 360
        comp_r = 90
        for angle in [0, 90, 180, 270]:
            rad = math.radians(angle)
            draw.line([(comp_x, comp_y), (int(comp_x + comp_r * math.cos(rad)), int(comp_y + comp_r * math.sin(rad)))], fill=(160, 40, 40), width=4)
        for angle in [45, 135, 225, 315]:
            rad = math.radians(angle)
            draw.line([(comp_x, comp_y), (int(comp_x + (comp_r - 25) * math.cos(rad)), int(comp_y + (comp_r - 25) * math.sin(rad)))], fill=(90, 75, 60), width=2)
        draw.ellipse([comp_x - 12, comp_y - 12, comp_x + 12, comp_y + 12], fill=GOLD_COLOR, outline=INK_COLOR, width=2)

        # Marching Troop Arrows
        arrow_start = (220, 1100)
        arrow_end = (int(220 + progress * 520), int(1100 - progress * 240))
        draw.line([arrow_start, arrow_end], fill=(190, 30, 30), width=16)
        draw.polygon([(arrow_end[0] + 25, arrow_end[1]), (arrow_end[0] - 25, arrow_end[1] - 25), (arrow_end[0] - 25, arrow_end[1] + 25)], fill=(190, 30, 30))

        # Crossed swords battle icon
        if progress > 0.5:
            clash_x, clash_y = 740, 860
            draw.line([(clash_x - 40, clash_y - 40), (clash_x + 40, clash_y + 40)], fill=(40, 40, 45), width=8)
            draw.line([(clash_x + 40, clash_y - 40), (clash_x - 40, clash_y + 40)], fill=(40, 40, 45), width=8)
            draw.text((clash_x, clash_y - 65), "CLASH!", fill=(190, 30, 30), font=self.get_font(28, bold=True), anchor="mm")

        # Ancient Commander figure on bottom left
        self.draw_character(draw, cx=320, cy=1620, scale=1.35, archetype="cartoon_hero", outfit="suit", expression="triumph", bob_y=bob)

    def render_tall_tale_scene(self, draw: ImageDraw.ImageDraw, scene: Any, progress: float, bob: float, frame_idx: int, title: str):
        """Crazy Loopholes, Heists & Modern True Stories (dynamic setting, cartoon hero, custom prop)."""
        lower_title = title.lower()
        self.draw_sky_background(draw, (65, 135, 230), (200, 225, 250))
        ground_y = 1580
        draw.rectangle([0, ground_y, self.width, self.height], fill=(110, 105, 100), outline=INK_COLOR, width=6)

        # Dynamic architectural background
        if any(k in lower_title for k in ["bank", "dollar", "money"]):
            # Classic Bank columns
            bw = 640
            bx = (self.width - bw) // 2
            draw.rectangle([bx, 850, bx + bw, ground_y], fill=(235, 230, 220), outline=INK_COLOR, width=6)
            for c_i in range(4):
                cx_col = bx + 50 + c_i * 150
                draw.rectangle([cx_col, 850, cx_col + 50, ground_y], fill=(250, 245, 240), outline=INK_COLOR, width=4)
            # Pediment
            draw.polygon([(bx - 30, 850), (bx + bw // 2, 700), (bx + bw + 30, 850)], fill=(240, 235, 225), outline=INK_COLOR, width=6)
            draw.text((bx + bw // 2, 780), "BANK", fill=INK_COLOR, font=self.get_font(32, bold=True), anchor="mm")
        elif any(k in lower_title for k in ["airport", "plane", "fly"]):
            # Runway & Hangar
            draw.polygon([(self.width // 2 - 40, 800), (self.width // 2 + 40, 800), (self.width - 100, ground_y), (100, ground_y)], fill=(55, 60, 70), outline=INK_COLOR, width=4)
            # Runway center stripes
            for ry in range(850, ground_y, 90):
                draw.line([(self.width // 2, ry), (self.width // 2, ry + 45)], fill=(255, 240, 80), width=6)
            # Airplane in sky
            plane_x = int(150 + progress * 680)
            plane_y = int(450 + math.sin(frame_idx * 0.1) * 20)
            draw.ellipse([plane_x - 70, plane_y - 20, plane_x + 70, plane_y + 20], fill=(245, 245, 255), outline=INK_COLOR, width=4)
            draw.polygon([(plane_x - 10, plane_y), (plane_x - 45, plane_y - 65), (plane_x + 15, plane_y)], fill=(220, 50, 50))
        else:
            # Modern Skyscraper Skyline
            for b_idx in range(5):
                bx = b_idx * 210 - 20
                bw = 180
                bh = 450 + (b_idx % 3) * 160
                draw.rectangle([bx, ground_y - bh, bx + bw, ground_y], fill=(70 + b_idx * 15, 110 + b_idx * 12, 160), outline=INK_COLOR, width=5)
                for wy in range(ground_y - bh + 30, ground_y - 30, 50):
                    for wx in range(bx + 20, bx + bw - 20, 40):
                        draw.rectangle([wx, wy, wx + 20, wy + 25], fill=(255, 250, 190), outline=INK_COLOR, width=2)

        # Dynamic Hero Cartoon Character
        expr = "panic" if (scene and scene.scene_index in [3, 4]) else "smirk"
        outfit = "hoodie" if "student" in lower_title else "suit"
        self.draw_character(draw, cx=360, cy=ground_y, scale=1.35, archetype="cartoon_hero", outfit=outfit, expression=expr, bob_y=bob)

        # Floating dynamic prop (Gold Coin, Golden Key, or Trophy)
        prop_x = 740
        prop_y = 1050 + int(bob * 1.2)
        prop_r = 140
        draw.ellipse([prop_x - prop_r, prop_y - prop_r, prop_x + prop_r, prop_y + prop_r], fill=GOLD_COLOR, outline=INK_COLOR, width=8)
        draw.ellipse([prop_x - prop_r + 20, prop_y - prop_r + 20, prop_x + prop_r - 20, prop_y + prop_r - 20], outline=(225, 175, 40), width=4)
        draw.text((prop_x, prop_y - 5), "$", fill=(60, 40, 10), font=self.get_font(120, bold=True), anchor="mm")

    # =========================================================================
    # MASTER FRAME DISPATCHER
    # =========================================================================
    def render_scene_frame(
        self,
        scene_idx: int,
        frame_in_scene: int,
        total_scene_frames: int,
        scene_beat: Optional[Any] = None,
        style: str = "Tall Tale 3D",
        title: str = "Faceless Short"
    ) -> Image.Image:
        """
        Renders a single 1080x1920 animation frame dynamically tailored to
        the active style, scene narration, and character direction.
        """
        img = Image.new("RGB", (self.width, self.height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        progress = frame_in_scene / max(1, total_scene_frames)
        bob = math.sin(frame_in_scene * 0.18) * 8.0

        # Dispatch to style renderer
        if style == "Deep Dive 3D":
            self.render_deep_dive_scene(draw, scene_beat, progress, bob, frame_in_scene)
        elif style == "Night File 3D":
            self.render_night_file_scene(draw, scene_beat, progress, bob, frame_in_scene)
        elif style == "Stick Story":
            self.render_stick_story_scene(draw, scene_beat, progress, bob, frame_in_scene)
        elif style == "Inside Out":
            self.render_inside_out_scene(draw, scene_beat, progress, bob, frame_in_scene)
        elif style == "Paper Atlas":
            self.render_paper_atlas_scene(draw, scene_beat, progress, bob, frame_in_scene)
        else: # Tall Tale 3D
            self.render_tall_tale_scene(draw, scene_beat, progress, bob, frame_in_scene, title)

        # Contextual Scene Header Badge
        badge_text = f"SCENE #{scene_idx}"
        if scene_beat and hasattr(scene_beat, "name") and scene_beat.name:
            badge_text = scene_beat.name.upper()

        badge_w = 480
        badge_h = 60
        bx = (self.width - badge_w) // 2
        by = 140
        draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=15, fill=(20, 24, 35), outline=GOLD_COLOR, width=3)
        draw.text((self.width // 2, by + badge_h // 2), badge_text[:28], fill=(255, 255, 255), font=self.get_font(24, bold=True), anchor="mm")

        return img

    def render_scene_video(
        self,
        scene_idx: int,
        duration_sec: float,
        output_mp4_path: str,
        scene_beat: Optional[Any] = None,
        style: str = "Tall Tale 3D",
        title: str = "Faceless Short",
        fps: int = 30
    ) -> str:
        """
        Renders a full 30fps scene video clip to MP4 using OpenCV and FFmpeg.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_mp4_path)), exist_ok=True)
        total_frames = int(round(duration_sec * fps))
        raw_avi = output_mp4_path.replace(".mp4", "_raw.mp4")

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(raw_avi, fourcc, fps, (self.width, self.height))

        for f in range(total_frames):
            pil_img = self.render_scene_frame(
                scene_idx=scene_idx,
                frame_in_scene=f,
                total_scene_frames=total_frames,
                scene_beat=scene_beat,
                style=style,
                title=title
            )
            # Convert RGB PIL to BGR OpenCV
            bgr_frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            writer.write(bgr_frame)

        writer.release()

        # Re-encode with FFmpeg H.264 yuv420p for universal social media compatibility
        from faceless_engine.config import FFMPEG_BIN
        import subprocess
        cmd = [
            FFMPEG_BIN, "-y",
            "-i", raw_avi,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "veryfast",
            "-crf", "18",
            output_mp4_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        if os.path.exists(raw_avi) and raw_avi != output_mp4_path:
            os.remove(raw_avi)

        return output_mp4_path
