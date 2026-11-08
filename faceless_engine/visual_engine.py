"""
Faceless Shorts Visual Engine - Tall Tale 3D Style
Renders 1080x1920 vertical 9:16 animations featuring:
- Expressive 2D cartoon characters (bean heads, stick limbs, ink outlines, rich facial expressions)
- 3D miniature architectural worlds (bank facades, vaults, trading floors, skyscrapers, gold coins)
- Camera glides, zooms, impact shakes, and depth layering
- Ink outlines and vibrant storybook color palette
"""
import os
import math
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from typing import List, Dict, Any, Tuple
from faceless_engine.config import FONTS_DIR

# Styling constants matching Nafay3D / "The Bridge" look
INK_COLOR = (36, 23, 38)        # Dark plum ink #241726
SKIN_COLOR = (255, 226, 194)    # Warm skin #ffe2c2
GOLD_COLOR = (255, 205, 60)     # Gold coin / accent #ffcd3c
NAVY_SUIT = (35, 55, 95)        # Classic banker navy suit
CRIMSON_RED = (220, 45, 55)     # Crisis red
ALERT_ORANGE = (245, 135, 35)   # Energy orange

class TallTaleRenderer:
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
        """Renders the signature storybook sky gradient using fast NumPy broadcasting."""
        # Fast vectorized gradient
        h, w = self.height, self.width
        top = np.array(top_color, dtype=np.float32)
        horizon = np.array(horizon_color, dtype=np.float32)
        r = np.linspace(top[0], horizon[0], h)[:, None]
        g = np.linspace(top[1], horizon[1], h)[:, None]
        b = np.linspace(top[2], horizon[2], h)[:, None]
        arr = np.dstack([np.broadcast_to(r, (h, w)), np.broadcast_to(g, (h, w)), np.broadcast_to(b, (h, w))]).astype(np.uint8)
        bg_img = Image.fromarray(arr, mode="RGB")
        draw._image.paste(bg_img, (0, 0))

    def draw_bean_character(
        self,
        draw: ImageDraw.ImageDraw,
        cx: int,
        cy: int,
        scale: float = 1.0,
        expression: str = "smirk",
        outfit: str = "navy_suit",
        arm_gesture: str = "present_coin",
        bob_y: float = 0.0
    ):
        """
        Draws the signature flat 2D cartoon character:
        - Superellipse bean head
        - Stick limbs with ink-dot hands
        - Dark plum ink outlines
        - Expressive eyes and mouth
        """
        cy = int(cy + bob_y)
        head_w = int(140 * scale)
        head_h = int(160 * scale)
        head_cx = cx
        head_cy = int(cy - 180 * scale)

        # 1. Torso / Outfit
        torso_w = int(130 * scale)
        torso_h = int(180 * scale)
        torso_top = head_cy + int(60 * scale)
        
        torso_color = NAVY_SUIT if outfit == "navy_suit" else (210, 60, 60)
        # Draw torso with ink outline
        draw.rounded_rectangle(
            [head_cx - torso_w // 2, torso_top, head_cx + torso_w // 2, torso_top + torso_h],
            radius=int(25 * scale),
            fill=torso_color,
            outline=INK_COLOR,
            width=int(8 * scale)
        )

        # White shirt & tie
        tie_color = (200, 30, 40) if outfit == "navy_suit" else (40, 40, 40)
        draw.polygon([
            (head_cx - int(20 * scale), torso_top + int(8 * scale)),
            (head_cx + int(20 * scale), torso_top + int(8 * scale)),
            (head_cx, torso_top + int(35 * scale))
        ], fill=(245, 245, 250), outline=INK_COLOR, width=int(3 * scale))
        
        draw.polygon([
            (head_cx - int(10 * scale), torso_top + int(35 * scale)),
            (head_cx + int(10 * scale), torso_top + int(35 * scale)),
            (head_cx, torso_top + int(110 * scale))
        ], fill=tie_color, outline=INK_COLOR, width=int(3 * scale))

        # 2. Stick Legs & Shoes
        leg_y_start = torso_top + torso_h - int(10 * scale)
        leg_len = int(140 * scale)
        leg_w = int(10 * scale)
        
        # Left leg
        draw.line([(head_cx - int(35 * scale), leg_y_start), (head_cx - int(35 * scale), leg_y_start + leg_len)], fill=INK_COLOR, width=leg_w)
        # Right leg
        draw.line([(head_cx + int(35 * scale), leg_y_start), (head_cx + int(35 * scale), leg_y_start + leg_len)], fill=INK_COLOR, width=leg_w)
        
        # Shoes (ink boots)
        boot_w = int(45 * scale)
        boot_h = int(22 * scale)
        draw.ellipse([head_cx - int(50 * scale), leg_y_start + leg_len - int(10 * scale), head_cx - int(50 * scale) + boot_w, leg_y_start + leg_len + boot_h], fill=INK_COLOR)
        draw.ellipse([head_cx + int(20 * scale), leg_y_start + leg_len - int(10 * scale), head_cx + int(20 * scale) + boot_w, leg_y_start + leg_len + boot_h], fill=INK_COLOR)

        # 3. Stick Arms
        arm_w = int(9 * scale)
        shoulder_y = torso_top + int(25 * scale)
        
        if arm_gesture == "present_coin":
            # Right arm bends up holding a shiny coin
            draw.line([(head_cx + int(60 * scale), shoulder_y), (head_cx + int(110 * scale), shoulder_y - int(30 * scale))], fill=INK_COLOR, width=arm_w)
            draw.line([(head_cx + int(110 * scale), shoulder_y - int(30 * scale)), (head_cx + int(145 * scale), shoulder_y - int(80 * scale))], fill=INK_COLOR, width=arm_w)
            # Hand ink dot
            draw.ellipse([head_cx + int(135 * scale), shoulder_y - int(92 * scale), head_cx + int(155 * scale), shoulder_y - int(72 * scale)], fill=INK_COLOR)
            # Left arm relaxed at side
            draw.line([(head_cx - int(60 * scale), shoulder_y), (head_cx - int(85 * scale), shoulder_y + int(90 * scale))], fill=INK_COLOR, width=arm_w)
            draw.ellipse([head_cx - int(95 * scale), shoulder_y + int(85 * scale), head_cx - int(75 * scale), shoulder_y + int(105 * scale)], fill=INK_COLOR)
            
        elif arm_gesture == "panic_head":
            # Both hands clutching head
            draw.line([(head_cx - int(60 * scale), shoulder_y), (head_cx - int(95 * scale), head_cy + int(20 * scale))], fill=INK_COLOR, width=arm_w)
            draw.line([(head_cx - int(95 * scale), head_cy + int(20 * scale)), (head_cx - int(65 * scale), head_cy - int(30 * scale))], fill=INK_COLOR, width=arm_w)
            draw.line([(head_cx + int(60 * scale), shoulder_y), (head_cx + int(95 * scale), head_cy + int(20 * scale))], fill=INK_COLOR, width=arm_w)
            draw.line([(head_cx + int(95 * scale), head_cy + int(20 * scale)), (head_cx + int(65 * scale), head_cy - int(30 * scale))], fill=INK_COLOR, width=arm_w)
        else: # triumph
            # Both arms thrown in the air
            draw.line([(head_cx - int(60 * scale), shoulder_y), (head_cx - int(120 * scale), shoulder_y - int(110 * scale))], fill=INK_COLOR, width=arm_w)
            draw.line([(head_cx + int(60 * scale), shoulder_y), (head_cx + int(120 * scale), shoulder_y - int(110 * scale))], fill=INK_COLOR, width=arm_w)
            draw.ellipse([head_cx - int(130 * scale), shoulder_y - int(120 * scale), head_cx - int(110 * scale), shoulder_y - int(100 * scale)], fill=INK_COLOR)
            draw.ellipse([head_cx + int(110 * scale), shoulder_y - int(120 * scale), head_cx + int(130 * scale), shoulder_y - int(100 * scale)], fill=INK_COLOR)

        # 4. Bean Head (pointed crown, fuller jaw)
        head_box = [head_cx - head_w // 2, head_cy - head_h // 2, head_cx + head_w // 2, head_cy + head_h // 2]
        draw.ellipse(head_box, fill=SKIN_COLOR, outline=INK_COLOR, width=int(8 * scale))

        # Hair / Style
        if outfit == "navy_suit":
            # Neat side-part hair
            draw.chord([head_box[0] - int(5 * scale), head_box[1] - int(10 * scale), head_box[2] + int(5 * scale), head_box[1] + int(60 * scale)], 180, 360, fill=(45, 30, 20), outline=INK_COLOR, width=int(5 * scale))
        else:
            # Messy panicked hair
            draw.arc([head_box[0] - int(10 * scale), head_box[1] - int(15 * scale), head_box[2] + int(10 * scale), head_box[1] + int(50 * scale)], 170, 370, fill=(35, 25, 20), width=int(14 * scale))

        # 5. Facial Expressions
        eye_y = head_cy - int(10 * scale)
        eye_spacing = int(32 * scale)
        eye_r = int(9 * scale)
        
        if expression == "smirk":
            # Confident, slightly lidded eyes
            draw.ellipse([head_cx - eye_spacing - eye_r, eye_y - eye_r, head_cx - eye_spacing + eye_r, eye_y + eye_r], fill=INK_COLOR)
            draw.ellipse([head_cx + eye_spacing - eye_r, eye_y - eye_r, head_cx + eye_spacing + eye_r, eye_y + eye_r], fill=INK_COLOR)
            # Smirking eyebrow arched
            draw.line([(head_cx - eye_spacing - int(14 * scale), eye_y - int(18 * scale)), (head_cx - eye_spacing + int(14 * scale), eye_y - int(16 * scale))], fill=INK_COLOR, width=int(4 * scale))
            draw.line([(head_cx + eye_spacing - int(14 * scale), eye_y - int(22 * scale)), (head_cx + eye_spacing + int(16 * scale), eye_y - int(14 * scale))], fill=INK_COLOR, width=int(5 * scale))
            # Cocky smirk mouth
            draw.arc([head_cx - int(10 * scale), head_cy + int(15 * scale), head_cx + int(35 * scale), head_cy + int(45 * scale)], 20, 160, fill=INK_COLOR, width=int(5 * scale))
            
        elif expression == "panic":
            # Huge wide shocked eyes with tiny pupils
            big_r = int(18 * scale)
            draw.ellipse([head_cx - eye_spacing - big_r, eye_y - big_r, head_cx - eye_spacing + big_r, eye_y + big_r], fill=(255, 255, 255), outline=INK_COLOR, width=int(4 * scale))
            draw.ellipse([head_cx + eye_spacing - big_r, eye_y - big_r, head_cx + eye_spacing + big_r, eye_y + big_r], fill=(255, 255, 255), outline=INK_COLOR, width=int(4 * scale))
            # Tiny frantic pupils
            draw.ellipse([head_cx - eye_spacing - int(4 * scale), eye_y - int(4 * scale), head_cx - eye_spacing + int(4 * scale), eye_y + int(4 * scale)], fill=INK_COLOR)
            draw.ellipse([head_cx + eye_spacing - int(4 * scale), eye_y - int(4 * scale), head_cx + eye_spacing + int(4 * scale), eye_y + int(4 * scale)], fill=INK_COLOR)
            # Angled panicked eyebrows
            draw.line([(head_cx - eye_spacing - int(15 * scale), eye_y - int(24 * scale)), (head_cx - eye_spacing + int(15 * scale), eye_y - int(32 * scale))], fill=INK_COLOR, width=int(5 * scale))
            draw.line([(head_cx + eye_spacing - int(15 * scale), eye_y - int(32 * scale)), (head_cx + eye_spacing + int(15 * scale), eye_y - int(24 * scale))], fill=INK_COLOR, width=int(5 * scale))
            # Open screaming mouth
            draw.ellipse([head_cx - int(18 * scale), head_cy + int(20 * scale), head_cx + int(18 * scale), head_cy + int(50 * scale)], fill=(90, 30, 40), outline=INK_COLOR, width=int(4 * scale))
            # Sweat drop
            draw.polygon([(head_cx + int(50 * scale), head_cy - int(40 * scale)), (head_cx + int(56 * scale), head_cy - int(25 * scale)), (head_cx + int(44 * scale), head_cy - int(25 * scale))], fill=(100, 200, 255))
            draw.ellipse([head_cx + int(44 * scale), head_cy - int(27 * scale), head_cx + int(56 * scale), head_cy - int(15 * scale)], fill=(100, 200, 255))
        else: # triumph / smile
            draw.arc([head_cx - eye_spacing - eye_r, eye_y - eye_r, head_cx - eye_spacing + eye_r, eye_y + eye_r], 180, 360, fill=INK_COLOR, width=int(5 * scale))
            draw.arc([head_cx + eye_spacing - eye_r, eye_y + eye_r, head_cx + eye_spacing + eye_r, eye_y + eye_r], 180, 360, fill=INK_COLOR, width=int(5 * scale))
            # Huge open smile
            draw.chord([head_cx - int(28 * scale), head_cy + int(15 * scale), head_cx + int(28 * scale), head_cy + int(52 * scale)], 0, 180, fill=(180, 40, 50), outline=INK_COLOR, width=int(4 * scale))

    def draw_giant_gold_dollar_coin(self, draw: ImageDraw.ImageDraw, cx: int, cy: int, radius: int = 160, tilt_angle: float = 0.0):
        """Draws the hero shiny 3D gold $1 coin with engraved rim and bold '$1'."""
        # Rim shadow / 3D extrusion
        ext_y = int(24 * math.cos(tilt_angle))
        draw.ellipse([cx - radius, cy - radius + ext_y, cx + radius, cy + radius + ext_y], fill=(180, 130, 20), outline=INK_COLOR, width=8)
        
        # Front face
        draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=GOLD_COLOR, outline=INK_COLOR, width=9)
        # Inner coin ridge
        draw.ellipse([cx - radius + 22, cy - radius + 22, cx + radius - 22, cy + radius - 22], outline=(225, 175, 40), width=5)
        
        # Big bold "$1" in center
        font = self.get_font(int(radius * 0.95), bold=True)
        draw.text((cx, cy - 8), "$1", fill=(60, 40, 10), font=font, anchor="mm")
        
        # Star accents on rim
        for angle in [0, 90, 180, 270]:
            rad = math.radians(angle)
            sx = int(cx + (radius - 12) * math.cos(rad))
            sy = int(cy + (radius - 12) * math.sin(rad))
            draw.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=INK_COLOR)

    def draw_historic_bank_facade(self, draw: ImageDraw.ImageDraw, ground_y: int, zoom: float = 1.0):
        """Renders 3D miniature neoclassical bank with triangular pediment and columns."""
        bw = int(720 * zoom)
        bh = int(680 * zoom)
        bx = (self.width - bw) // 2
        by = ground_y - bh

        # Bank steps (stacked trapezoids)
        for i in range(4):
            sw = bw + (4 - i) * 35
            sx = (self.width - sw) // 2
            sy = ground_y - (4 - i) * 16
            draw.rectangle([sx, sy, sx + sw, sy + 16], fill=(215, 210, 200), outline=INK_COLOR, width=4)

        # Main building block (warm sandstone with black ink)
        draw.rectangle([bx, by + 180, bx + bw, ground_y - 64], fill=(235, 230, 220), outline=INK_COLOR, width=6)

        # 4 Classical Neoclassical Columns
        col_w = int(58 * zoom)
        col_spacing = (bw - col_w * 4) // 5
        for i in range(4):
            cx = bx + col_spacing * (i + 1) + col_w * i
            # Column shaft
            draw.rectangle([cx, by + 180, cx + col_w, ground_y - 64], fill=(248, 245, 240), outline=INK_COLOR, width=5)
            # Column capital (top & bottom flare)
            draw.rectangle([cx - 8, by + 172, cx + col_w + 8, by + 186], fill=(220, 215, 205), outline=INK_COLOR, width=4)
            draw.rectangle([cx - 8, ground_y - 74, cx + col_w + 8, ground_y - 60], fill=(220, 215, 205), outline=INK_COLOR, width=4)

        # Architrave / Cornice
        draw.rectangle([bx - 20, by + 140, bx + bw + 20, by + 180], fill=(220, 215, 205), outline=INK_COLOR, width=6)

        # Triangular Pediment (The roof gable)
        draw.polygon([
            (bx - 30, by + 140),
            (bx + bw // 2, by),
            (bx + bw + 30, by + 140)
        ], fill=(240, 235, 225), outline=INK_COLOR, width=7)

        # Royal Crest inside pediment
        crown_cx = bx + bw // 2
        crown_cy = by + 90
        draw.ellipse([crown_cx - 40, crown_cy - 25, crown_cx + 40, crown_cy + 25], fill=GOLD_COLOR, outline=INK_COLOR, width=4)
        font_crest = self.get_font(24, bold=True)
        draw.text((crown_cx, crown_cy), "1762", fill=INK_COLOR, font=font_crest, anchor="mm")

        # Big Engraved Signboard: "BARINGS BANK"
        draw.rectangle([bx + 110, by + 144, bx + bw - 110, by + 176], fill=(30, 45, 65), outline=INK_COLOR, width=3)
        font_sign = self.get_font(26, bold=True)
        draw.text((bx + bw // 2, by + 160), "BARINGS BANK", fill=(255, 220, 100), font=font_sign, anchor="mm")

        # Huge Golden Bank Vault Door visible in center portal
        portal_w = int(180 * zoom)
        portal_h = int(240 * zoom)
        px = bx + (bw - portal_w) // 2
        py = ground_y - 64 - portal_h
        draw.rounded_rectangle([px, py, px + portal_w, py + portal_h], radius=15, fill=(18, 22, 30), outline=INK_COLOR, width=5)
        # Vault circular steel door
        draw.ellipse([px + 20, py + 40, px + portal_w - 20, py + portal_h - 20], fill=(160, 170, 185), outline=INK_COLOR, width=6)
        draw.ellipse([px + 50, py + 70, px + portal_w - 50, py + portal_h - 50], fill=GOLD_COLOR, outline=INK_COLOR, width=4)
        draw.line([(px + portal_w // 2, py + 55), (px + portal_w // 2, py + portal_h - 35)], fill=INK_COLOR, width=6)
        draw.line([(px + 35, py + (portal_h + 20) // 2), (px + portal_w - 35, py + (portal_h + 20) // 2)], fill=INK_COLOR, width=6)

    def draw_trading_crash_environment(self, draw: ImageDraw.ImageDraw, progress: float):
        """Renders the catastrophic 1995 trading floor crash with plummeting graph and alarm glow."""
        # Deep dim trading room via fast NumPy
        self.draw_sky_background(draw, (10, 8, 12), (45, 18, 27))

        # Big neon red trading board header
        draw.rectangle([60, 180, self.width - 60, 360], fill=(15, 12, 18), outline=(220, 40, 50), width=6)
        font_ticker = self.get_font(42, bold=True)
        draw.text((self.width // 2, 230), "NIKKEI FUTURES - ACC #88888", fill=(255, 60, 60), font=font_ticker, anchor="mm")
        
        # Plunging loss number
        loss_text = "-$1,400,000,000"
        font_loss = self.get_font(64, bold=True)
        draw.text((self.width // 2, 305), loss_text, fill=(255, 30, 30), font=font_loss, anchor="mm")

        # The crashing zigzag stock line
        chart_top = 440
        chart_bottom = 1200
        chart_left = 80
        chart_right = self.width - 80
        
        pts = [
            (chart_left, chart_top + 100),
            (chart_left + 150, chart_top + 60),
            (chart_left + 300, chart_top + 160),
            (chart_left + 450, chart_top + 120),
            (chart_left + 600, chart_top + 320),
            (chart_left + 750, chart_bottom - 120),
            (chart_right, chart_bottom + int(80 * progress))
        ]
        
        # Red neon shadow / line
        draw.line(pts, fill=(255, 30, 30), width=16)
        # Giant red arrow head piercing down
        last_pt = pts[-1]
        draw.polygon([
            (last_pt[0], last_pt[1] + 35),
            (last_pt[0] - 25, last_pt[1] - 25),
            (last_pt[0] + 25, last_pt[1] - 25)
        ], fill=(255, 30, 30))

        # Floating panicked paper receipts
        for k in range(8):
            px = int(120 + (k * 125 + progress * 60) % 800)
            py = int(500 + (k * 110 + progress * 150) % 650)
            draw.rectangle([px, py, px + 75, py + 50], fill=(240, 240, 245), outline=INK_COLOR, width=3)
            draw.line([(px + 10, py + 15), (px + 65, py + 15)], fill=(150, 150, 160), width=2)
            draw.line([(px + 10, py + 30), (px + 50, py + 30)], fill=(220, 60, 60), width=2)

    def draw_the_deal_table(self, draw: ImageDraw.ImageDraw, progress: float):
        """Renders the executive boardroom table where the $1 coin contract is signed."""
        # Warm golden wood panel background via fast NumPy
        self.draw_sky_background(draw, (30, 20, 15), (75, 50, 35))

        # Boardroom mahogany table in 3D perspective
        table_top_y = 1100
        draw.polygon([
            (100, table_top_y),
            (self.width - 100, table_top_y),
            (self.width + 100, self.height),
            (-100, self.height)
        ], fill=(95, 45, 25), outline=INK_COLOR, width=8)

        # Official Acquisition Contract on table
        doc_x = self.width // 2 - 180
        doc_y = table_top_y + 120
        draw.rectangle([doc_x, doc_y, doc_x + 360, doc_y + 440], fill=(250, 246, 235), outline=INK_COLOR, width=6)
        
        font_contract = self.get_font(28, bold=True)
        draw.text((self.width // 2, doc_y + 45), "DEED OF PURCHASE", fill=INK_COLOR, font=font_contract, anchor="mm")
        font_sub = self.get_font(20, bold=False)
        draw.text((self.width // 2, doc_y + 85), "Barings Bank PLC -> Aad Jacobs", fill=(80, 80, 90), font=font_sub, anchor="mm")
        
        # Golden Seal
        draw.ellipse([self.width // 2 - 40, doc_y + 320, self.width // 2 + 40, doc_y + 400], fill=CRIMSON_RED, outline=INK_COLOR, width=4)
        
        # The $1 coin sliding onto the contract
        coin_slide_x = int(doc_x + 180 + (1.0 - progress) * 220)
        coin_slide_y = doc_y + 200
        self.draw_giant_gold_dollar_coin(draw, coin_slide_x, coin_slide_y, radius=70)

    def render_scene_frame(
        self,
        scene_idx: int,
        frame_in_scene: int,
        total_scene_frames: int
    ) -> Image.Image:
        """
        Renders a single pristine 1080x1920 animation frame for the requested scene.
        """
        img = Image.new("RGB", (self.width, self.height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        progress = frame_in_scene / max(1, total_scene_frames)
        bob = math.sin(frame_in_scene * 0.18) * 8.0

        if scene_idx == 1:
            # SCENE 1: The $1 Hook
            # Saturated English morning sky
            self.draw_sky_background(draw, (75, 140, 225), (195, 215, 240))
            # Pavement / Cobblestones
            ground_y = 1580
            draw.rectangle([0, ground_y, self.width, self.height], fill=(120, 115, 110), outline=INK_COLOR, width=6)
            # Neoclassical bank in background with smooth push-in
            zoom = 1.0 + progress * 0.08
            self.draw_historic_bank_facade(draw, ground_y, zoom=zoom)
            # Hero Aad Jacobs character holding the giant gold coin
            self.draw_bean_character(draw, cx=360, cy=ground_y, scale=1.35, expression="smirk", outfit="navy_suit", arm_gesture="present_coin", bob_y=bob)
            # Hero $1 Coin floating with sparkling aura
            coin_scale = 145 + int(math.sin(frame_in_scene * 0.22) * 8)
            self.draw_giant_gold_dollar_coin(draw, cx=740, cy=1050 + int(bob * 1.2), radius=coin_scale)

        elif scene_idx == 2:
            # SCENE 2: The 200-Year Empire (Barings Bank Grand Vault & Royal Guards)
            self.draw_sky_background(draw, (55, 105, 185), (180, 200, 225))
            ground_y = 1600
            draw.rectangle([0, ground_y, self.width, self.height], fill=(95, 90, 85), outline=INK_COLOR, width=6)
            self.draw_historic_bank_facade(draw, ground_y, zoom=1.15)
            # Royal Bearskin Guard on left & right
            self.draw_bean_character(draw, cx=200, cy=ground_y, scale=1.2, expression="smirk", outfit="royal", arm_gesture="panic_head", bob_y=bob * 0.5)
            self.draw_bean_character(draw, cx=880, cy=ground_y, scale=1.2, expression="smirk", outfit="royal", arm_gesture="panic_head", bob_y=-bob * 0.5)
            # Stacked gold ingots in foreground
            for row in range(3):
                for col in range(5 - row):
                    gx = 340 + row * 45 + col * 90
                    gy = ground_y - 40 - row * 35
                    draw.rectangle([gx, gy, gx + 80, gy + 30], fill=GOLD_COLOR, outline=INK_COLOR, width=4)

        elif scene_idx == 3:
            # SCENE 3: The Rogue Bet (Nick Leeson sweating over glowing computer terminal)
            self.draw_trading_crash_environment(draw, progress)
            # Panicked young trader
            self.draw_bean_character(draw, cx=self.width // 2, cy=1580, scale=1.4, expression="panic", outfit="trader", arm_gesture="panic_head", bob_y=bob * 1.5)

        elif scene_idx == 4:
            # SCENE 4: The 1.4 Billion Crash & Shock
            self.draw_trading_crash_environment(draw, 1.0)
            # Impact screen shake
            shake_x = int(math.sin(frame_in_scene * 0.8) * 12 * (1.0 - progress))
            shake_y = int(math.cos(frame_in_scene * 0.9) * 12 * (1.0 - progress))
            self.draw_bean_character(draw, cx=self.width // 2 + shake_x, cy=1580 + shake_y, scale=1.45, expression="panic", outfit="trader", arm_gesture="panic_head", bob_y=bob * 2.0)
            # Giant red stamp: "BANKRUPT!"
            font_bankrupt = self.get_font(95, bold=True)
            draw.text((self.width // 2 + 5, 820 + 5), "BANKRUPT!", fill=(30, 0, 0), font=font_bankrupt, anchor="mm")
            draw.text((self.width // 2, 820), "BANKRUPT!", fill=(255, 240, 240), font=font_bankrupt, anchor="mm")

        elif scene_idx == 5:
            # SCENE 5: The Historic Deal ($1 Purchase Contract)
            self.draw_the_deal_table(draw, progress)
            # Aad Jacobs calmly on the left
            self.draw_bean_character(draw, cx=260, cy=1250, scale=1.2, expression="smirk", outfit="navy_suit", arm_gesture="present_coin", bob_y=bob)

        else:
            # SCENE 6: The 50-Billion Empire & Seamless Loop
            # Sunny triumphant sky
            self.draw_sky_background(draw, (45, 130, 240), (220, 235, 255))
            ground_y = 1620
            # Modern skyscraper skyline
            for b_idx in range(6):
                bx = b_idx * 190 - 40
                bw = 160
                bh = 500 + (b_idx % 3) * 180
                draw.rectangle([bx, ground_y - bh, bx + bw, ground_y], fill=(70 + b_idx * 15, 110 + b_idx * 12, 160), outline=INK_COLOR, width=5)
                # Windows
                for wy in range(ground_y - bh + 30, ground_y - 30, 45):
                    for wx in range(bx + 20, bx + bw - 20, 35):
                        draw.rectangle([wx, wy, wx + 20, wy + 25], fill=(255, 250, 190), outline=INK_COLOR, width=2)
            
            # Ground street
            draw.rectangle([0, ground_y, self.width, self.height], fill=(90, 85, 80), outline=INK_COLOR, width=6)
            # Triumphant Aad Jacobs atop the empire
            self.draw_bean_character(draw, cx=self.width // 2, cy=ground_y - 80, scale=1.4, expression="triumph", outfit="navy_suit", arm_gesture="triumph", bob_y=bob)
            # Floating dollar bills / confetti
            for c_i in range(16):
                cx_c = int((c_i * 75 + progress * 240) % self.width)
                cy_c = int((c_i * 95 + frame_in_scene * 7) % ground_y)
                draw.rectangle([cx_c, cy_c, cx_c + 45, cy_c + 24], fill=(130, 215, 130), outline=INK_COLOR, width=3)
                draw.text((cx_c + 22, cy_c + 12), "$", fill=INK_COLOR, font=self.get_font(18, bold=True), anchor="mm")

        return img

    def render_scene_video(
        self,
        scene_idx: int,
        duration_sec: float,
        output_mp4_path: str,
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
            pil_img = self.render_scene_frame(scene_idx, f, total_frames)
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
