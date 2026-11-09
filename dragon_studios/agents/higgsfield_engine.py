"""
Dragon Studios India - Higgsfield Video Engineer Local WebGPU Integration
Renders code-based cinematic 3D visual frames directly on local GPU via WebGPU compute,
with procedural AgX tonemapping, depth-of-field, volumetric lighting, and principled shaders.
"""

import os
import sys
import json
import logging
import tempfile
import subprocess
from typing import Dict, Any, Optional
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger("HiggsfieldEngine")

class HiggsfieldWebGPUEngine:
    """
    Interfaces with the local Higgsfield WebGPU path tracer in higgsfield-video-engineer.
    Provides 100% local, zero-cost, photorealistic cinematic rendering for short-form reels.
    """

    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = workspace_root or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )
        self.engine_path = os.path.join(
            self.workspace_root,
            "higgsfield-video-engineer",
            "skills",
            "code-based-films",
            "engine"
        )
        self.render_script = os.path.join(self.engine_path, "bin", "render.mjs")
        self.available = self._detect_engine()

    def _detect_engine(self) -> bool:
        """
        Verifies Node.js, the WebGPU render script, and node_modules exist.
        """
        if not os.path.exists(self.render_script):
            logger.info(f"Higgsfield render script not found at {self.render_script}")
            return False
        node_modules = os.path.join(self.engine_path, "node_modules")
        if not os.path.exists(node_modules):
            logger.info("Higgsfield engine node_modules missing")
            return False
        return True

    def build_cinematic_scene(
        self,
        pillar: str = "DARK_PSYCHOLOGY",
        scene_num: int = 1,
        width: int = 540,
        height: int = 960,
        spp: int = 32
    ) -> Dict[str, Any]:
        """
        Synthesizes a physically-based 3D scene description with camera blocking,
        volumetric atmosphere, principled materials, and dramatic 3-point lighting
        tailored for 9:16 vertical video.
        """
        if pillar == "DARK_PSYCHOLOGY":
            # Obsidian pedestal, deep crimson/purple backlight, glossy reflective sphere
            scene = {
                "version": 1,
                "render": {
                    "width": width,
                    "height": height,
                    "spp": spp,
                    "maxBounces": 6,
                    "post": {"tonemap": "agx", "exposure": 0.25}
                },
                "camera": {
                    "position": [0, 1.4, 4.0],
                    "target": [0, 0.7, 0],
                    "fov": 38,
                    "fstop": 2.8,
                    "focusTarget": [0, 0.75, 0]
                },
                "materials": [
                    # Floor / Monolith: Matte obsidian black
                    {"baseColor": [0.03, 0.03, 0.04], "roughness": 0.65, "metallic": 0.2},
                    # Hero Artifact: Polished metallic dark gold or crimson sheen
                    {"baseColor": [0.85, 0.2, 0.3], "roughness": 0.15, "metallic": 0.85, "clearcoat": 0.8},
                    # Secondary Glass Relic
                    {"baseColor": [0.1, 0.1, 0.12], "transmission": 0.95, "ior": 1.55, "roughness": 0.05}
                ],
                "meshes": [
                    {"name": "pedestal", "primitive": "box", "size": [4.0, 0.2, 4.0], "materials": [0]},
                    {"name": "hero_sphere", "primitive": "sphere", "radius": 0.6, "segments": 96, "rings": 48, "materials": [1]},
                    {"name": "secondary_orb", "primitive": "sphere", "radius": 0.35, "segments": 64, "rings": 32, "materials": [2]}
                ],
                "instances": [
                    {"mesh": 0, "position": [0, 0, 0]},
                    {"mesh": 1, "position": [0, 0.75, 0]},
                    {"mesh": 2, "position": [0.7, 0.45, 0.6]}
                ],
                "lights": [
                    # Rim Key Light (deep violet / neon crimson)
                    {"type": "rect", "position": [-2.2, 3.2, -1.8], "target": [0, 0.7, 0], "size": [1.5, 1.5], "color": [0.95, 0.15, 0.4], "intensity": 14},
                    # Fill Ambient Light (obsidian blue)
                    {"type": "rect", "position": [2.0, 2.0, 2.5], "target": [0, 0.7, 0], "size": [1.0, 1.0], "color": [0.3, 0.4, 0.9], "intensity": 8, "visible": False}
                ],
                "environment": {"type": "color", "color": [0.015, 0.015, 0.025], "intensity": 0.6}
            }
        elif pillar == "AI_TOOLS":
            # Cybernetic architecture, electric cyan rim light, floating transmission crystal
            scene = {
                "version": 1,
                "render": {
                    "width": width,
                    "height": height,
                    "spp": spp,
                    "maxBounces": 6,
                    "post": {"tonemap": "agx", "exposure": 0.35}
                },
                "camera": {
                    "position": [0, 1.2, 3.6],
                    "target": [0, 0.6, 0],
                    "fov": 36,
                    "fstop": 3.2,
                    "focusTarget": [0, 0.65, 0]
                },
                "materials": [
                    # Pedestal: Brushed dark titanium
                    {"baseColor": [0.15, 0.17, 0.22], "roughness": 0.3, "metallic": 0.9},
                    # Hero Core: Refractive glowing cyber crystal
                    {"baseColor": [0.05, 0.75, 0.95], "transmission": 0.98, "ior": 1.48, "roughness": 0.02},
                    # Accent Golden Nodes
                    {"baseColor": [1.0, 0.8, 0.2], "roughness": 0.2, "metallic": 1.0}
                ],
                "meshes": [
                    {"name": "pedestal", "primitive": "box", "size": [3.5, 0.15, 3.5], "materials": [0]},
                    {"name": "core", "primitive": "sphere", "radius": 0.55, "segments": 96, "rings": 48, "materials": [1]},
                    {"name": "node", "primitive": "sphere", "radius": 0.25, "segments": 48, "rings": 24, "materials": [2]}
                ],
                "instances": [
                    {"mesh": 0, "position": [0, -0.05, 0]},
                    {"mesh": 1, "position": [0, 0.65, 0]},
                    {"mesh": 2, "position": [-0.65, 0.35, 0.4]}
                ],
                "lights": [
                    # Cyan Cyber Glow
                    {"type": "rect", "position": [1.8, 2.8, 1.8], "target": [0, 0.65, 0], "size": [1.2, 1.2], "color": [0.1, 0.85, 1.0], "intensity": 15},
                    # Amber Soft Backlight
                    {"type": "rect", "position": [-1.6, 2.0, -2.0], "target": [0, 0.65, 0], "size": [1.0, 1.0], "color": [1.0, 0.6, 0.1], "intensity": 10, "visible": False}
                ],
                "environment": {"type": "color", "color": [0.01, 0.02, 0.04], "intensity": 0.8}
            }
        else: # ORIGINAL_MANGA (Chitran / Anime style)
            # High-contrast dramatic samurai / anime aesthetic, crimson energy
            scene = {
                "version": 1,
                "render": {
                    "width": width,
                    "height": height,
                    "spp": spp,
                    "maxBounces": 5,
                    "post": {"tonemap": "agx", "exposure": 0.2}
                },
                "camera": {
                    "position": [0, 1.3, 3.8],
                    "target": [0, 0.6, 0],
                    "fov": 35,
                    "fstop": 2.5,
                    "focusTarget": [0, 0.6, 0]
                },
                "materials": [
                    # Dark stone arena floor
                    {"baseColor": [0.08, 0.08, 0.1], "roughness": 0.85, "metallic": 0.1},
                    # Dragon Crimson Focus Relic
                    {"baseColor": [0.95, 0.08, 0.15], "roughness": 0.25, "metallic": 0.7, "clearcoat": 0.9},
                    # Metallic blade chrome
                    {"baseColor": [0.9, 0.92, 0.95], "roughness": 0.1, "metallic": 1.0}
                ],
                "meshes": [
                    {"name": "arena", "primitive": "box", "size": [4.0, 0.2, 4.0], "materials": [0]},
                    {"name": "dragon_orb", "primitive": "sphere", "radius": 0.5, "segments": 96, "rings": 48, "materials": [1]},
                    {"name": "blade_pillar", "primitive": "box", "size": [0.2, 1.0, 0.2], "materials": [2]}
                ],
                "instances": [
                    {"mesh": 0, "position": [0, 0, 0]},
                    {"mesh": 1, "position": [0, 0.65, 0]},
                    {"mesh": 2, "position": [0.55, 0.5, -0.3]}
                ],
                "lights": [
                    {"type": "rect", "position": [-2.0, 3.0, 2.0], "target": [0, 0.6, 0], "size": [1.4, 1.4], "color": [1.0, 0.1, 0.2], "intensity": 16},
                    {"type": "rect", "position": [2.0, 1.8, -1.5], "target": [0, 0.6, 0], "size": [0.8, 0.8], "color": [0.8, 0.85, 1.0], "intensity": 7, "visible": False}
                ],
                "environment": {"type": "color", "color": [0.02, 0.015, 0.02], "intensity": 0.5}
            }
        return scene

    def render_scene_webgpu(
        self,
        scene_dict: Dict[str, Any],
        output_png_path: str,
        spp: int = 32,
        max_seconds: int = 35
    ) -> bool:
        """
        Executes local WebGPU path tracing using headless Chrome and Node.
        Returns True on success, False if fallback is needed.
        """
        if not self.available:
            logger.warning("Higgsfield WebGPU engine not available on this system.")
            return False

        os.makedirs(os.path.dirname(os.path.abspath(output_png_path)), exist_ok=True)
        temp_scene = None
        try:
            with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
                json.dump(scene_dict, f, indent=2)
                temp_scene = f.name

            cmd = [
                "node",
                self.render_script,
                temp_scene,
                "--spp", str(spp),
                "--out", output_png_path,
                "--max-seconds", str(max_seconds)
            ]
            logger.info(f"Executing Higgsfield WebGPU render: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                cwd=self.engine_path,
                capture_output=True,
                text=True,
                timeout=max_seconds + 30
            )

            if result.returncode == 0 and os.path.exists(output_png_path) and os.path.getsize(output_png_path) > 1000:
                logger.info(f"WebGPU frame successfully rendered: {output_png_path} ({os.path.getsize(output_png_path)} bytes)")
                return True
            else:
                logger.warning(f"WebGPU render returned code {result.returncode}. Stderr: {result.stderr[:300]}")
                return False

        except Exception as e:
            logger.warning(f"WebGPU render encountered exception: {e}. Gracefully activating fallback.")
            return False
        finally:
            if temp_scene and os.path.exists(temp_scene):
                try:
                    os.remove(temp_scene)
                except Exception:
                    pass

    def render_composite_frame(
        self,
        headline: str,
        subtext: str,
        pillar: str,
        scene_num: int,
        output_path: str,
        width: int = 1080,
        height: int = 1920,
        spp: int = 24,
        allow_webgpu: bool = True
    ) -> str:
        """
        Generates a master 1080x1920 production frame by compositing:
        1. A photorealistic 3D WebGPU path-traced background frame (or high-contrast procedural gradient canvas)
        2. Clean typography, dynamic scene badge, and Dragon Studios India brand watermarks.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        bg_image = None

        if allow_webgpu and self.available:
            # Render a 540x960 WebGPU frame for high-speed local throughput, then upscale smoothly
            temp_gpu_png = output_path.replace(".png", "_webgpu_raw.png")
            scene_data = self.build_cinematic_scene(
                pillar=pillar,
                scene_num=scene_num,
                width=540,
                height=960,
                spp=spp
            )
            success = self.render_scene_webgpu(scene_data, temp_gpu_png, spp=spp, max_seconds=30)
            if success and os.path.exists(temp_gpu_png):
                try:
                    raw_bg = Image.open(temp_gpu_png)
                    bg_image = raw_bg.resize((width, height), Image.Resampling.LANCZOS)
                except Exception as e:
                    logger.warning(f"Failed to load WebGPU raw frame: {e}")
                finally:
                    try:
                        if os.path.exists(temp_gpu_png):
                            os.remove(temp_gpu_png)
                    except Exception:
                        pass

        # If WebGPU didn't run or failed, generate high-contrast procedural studio canvas
        if bg_image is None:
            bg_image = Image.new("RGB", (width, height), color=(11, 12, 16))
            draw = ImageDraw.Draw(bg_image)
            
            if pillar == "DARK_PSYCHOLOGY":
                top_color = (24, 12, 38)
                bottom_color = (5, 5, 8)
                accent_color = (168, 85, 247)
            elif pillar == "AI_TOOLS":
                top_color = (8, 28, 52)
                bottom_color = (3, 7, 18)
                accent_color = (6, 182, 212)
            else:
                top_color = (35, 10, 18)
                bottom_color = (4, 4, 6)
                accent_color = (239, 68, 68)

            for y in range(height):
                ratio = y / height
                r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
                g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
                b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Apply dark vignette overlay to emphasize central typography
        vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        vdraw = ImageDraw.Draw(vignette)
        
        # Determine theme accent colors
        if pillar == "DARK_PSYCHOLOGY":
            accent = (168, 85, 247)
        elif pillar == "AI_TOOLS":
            accent = (6, 182, 212)
        else:
            accent = (239, 68, 68)

        # Draw decorative border
        margin = 40
        vdraw.rectangle([margin, margin, width - margin, height - margin], outline=accent, width=3)
        
        # Dragon Studios Watermark
        vdraw.text((width // 2, 120), "DRAGON STUDIOS INDIA", fill=(180, 180, 200, 230), anchor="mm")
        vdraw.line([(width // 2 - 120, 150), (width // 2 + 120, 150)], fill=accent, width=2)

        # Scene Badge
        badge_text = f"RULE #{scene_num}" if pillar == "DARK_PSYCHOLOGY" else f"PHASE #{scene_num}"
        vdraw.rectangle([width // 2 - 110, 480, width // 2 + 110, 540], fill=accent)
        vdraw.text((width // 2, 510), badge_text, fill=(255, 255, 255, 255), anchor="mm")

        # Word wrap headline
        words = headline.split()
        lines = []
        curr = []
        for w in words:
            curr.append(w)
            if len(" ".join(curr)) > 20:
                lines.append(" ".join(curr[:-1]))
                curr = [w]
        if curr:
            lines.append(" ".join(curr))

        # Draw headline text with dark drop shadow
        start_y = 660
        for i, line in enumerate(lines[:4]):
            y_pos = start_y + (i * 75)
            # Shadow
            vdraw.text((width // 2 + 3, y_pos + 3), line.upper(), fill=(0, 0, 0, 200), anchor="mm")
            # Text
            vdraw.text((width // 2, y_pos), line.upper(), fill=(255, 255, 255, 255), anchor="mm")

        # Composite vignette over background
        bg_rgba = bg_image.convert("RGBA")
        final_img = Image.alpha_composite(bg_rgba, vignette).convert("RGB")
        final_img.save(output_path, quality=95)
        return output_path
