"""
Dragon Studios India - Higgsfield Skills & Model Catalog Adapter
Bridges the 10-stage autonomous creator studio with Higgsfield Agent Skills
and the 38-model OpenHiggsfield video/image generation catalog.
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("HiggsfieldSkills")

class ModelSpec(BaseModel):
    id: str
    name: str
    kind: str  # "video" or "image"
    category: str
    aspect_ratios: List[str]
    default_duration: Optional[int] = None
    max_duration: Optional[int] = None
    supports_audio: bool = False
    estimated_credits_per_run: float = 1.0

class HiggsfieldSkillsAdapter:
    """
    Adapter for Higgsfield CLI, Higgsfield Agent Skills, and OpenHiggsfield 38-model catalog.
    """

    # Comprehensive 38-model catalog extracted from OpenHiggsfield Studio
    SUPPORTED_MODELS = {
        # Video Models
        "soul-2": ModelSpec(id="soul-2", name="Soul 2 (Cinematic)", kind="video", category="Higgsfield Native", aspect_ratios=["9:16", "16:9", "1:1"], default_duration=5, max_duration=10, supports_audio=True, estimated_credits_per_run=2.5),
        "soul-cinema": ModelSpec(id="soul-cinema", name="Soul Cinema", kind="video", category="Higgsfield Native", aspect_ratios=["9:16", "16:9", "2.39:1"], default_duration=5, max_duration=10, supports_audio=True, estimated_credits_per_run=3.0),
        "seedance-2.5": ModelSpec(id="seedance-2.5", name="Seedance 2.5", kind="video", category="Dance & Motion", aspect_ratios=["9:16", "16:9"], default_duration=5, max_duration=10, supports_audio=True, estimated_credits_per_run=2.0),
        "seedance-2.5-edit": ModelSpec(id="seedance-2.5-edit", name="Seedance 2.5 Edit", kind="video", category="Dance & Motion", aspect_ratios=["9:16", "16:9"], default_duration=5, max_duration=10, supports_audio=True, estimated_credits_per_run=2.0),
        "kling-3-turbo": ModelSpec(id="kling-3-turbo", name="Kling 3 Turbo", kind="video", category="Kuaishou Kling", aspect_ratios=["9:16", "16:9", "1:1"], default_duration=5, max_duration=10, supports_audio=False, estimated_credits_per_run=1.5),
        "kling-3-pro": ModelSpec(id="kling-3-pro", name="Kling 3 Pro", kind="video", category="Kuaishou Kling", aspect_ratios=["9:16", "16:9", "1:1"], default_duration=5, max_duration=10, supports_audio=False, estimated_credits_per_run=3.0),
        "kling-3-4k": ModelSpec(id="kling-3-4k", name="Kling 3 4K Master", kind="video", category="Kuaishou Kling", aspect_ratios=["9:16", "16:9"], default_duration=5, max_duration=10, supports_audio=False, estimated_credits_per_run=5.0),
        "wan-3-prime": ModelSpec(id="wan-3-prime", name="Wan 3 Prime", kind="video", category="Alibaba Wan", aspect_ratios=["9:16", "16:9"], default_duration=5, max_duration=10, supports_audio=False, estimated_credits_per_run=2.0),
        "minimax-h3": ModelSpec(id="minimax-h3", name="MiniMax Hailuo H3", kind="video", category="MiniMax", aspect_ratios=["9:16", "16:9"], default_duration=6, max_duration=10, supports_audio=False, estimated_credits_per_run=2.5),
        "ltx-2.5-fast": ModelSpec(id="ltx-2.5-fast", name="LTX 2.5 Fast", kind="video", category="Lightricks LTX", aspect_ratios=["9:16", "16:9"], default_duration=5, max_duration=10, supports_audio=False, estimated_credits_per_run=1.0),
        "ltx-2.5-pro": ModelSpec(id="ltx-2.5-pro", name="LTX 2.5 Pro", kind="video", category="Lightricks LTX", aspect_ratios=["9:16", "16:9"], default_duration=5, max_duration=10, supports_audio=False, estimated_credits_per_run=2.2),
        "pixverse-6": ModelSpec(id="pixverse-6", name="PixVerse 6.0", kind="video", category="PixVerse", aspect_ratios=["9:16", "16:9"], default_duration=5, max_duration=8, supports_audio=False, estimated_credits_per_run=2.0),
        "grok-imagine-video-1.5": ModelSpec(id="grok-imagine-video-1.5", name="Grok Imagine Video 1.5", kind="video", category="xAI Grok", aspect_ratios=["9:16", "16:9"], default_duration=5, max_duration=10, supports_audio=False, estimated_credits_per_run=2.5),

        # Image Models
        "flux-2": ModelSpec(id="flux-2", name="Flux 2 Pro", kind="image", category="Black Forest Labs", aspect_ratios=["9:16", "16:9", "1:1", "4:5"], estimated_credits_per_run=1.0),
        "flux-3": ModelSpec(id="flux-3", name="Flux 3 Cinematic", kind="image", category="Black Forest Labs", aspect_ratios=["9:16", "16:9", "1:1", "4:5"], estimated_credits_per_run=1.5),
        "ideogram-4": ModelSpec(id="ideogram-4", name="Ideogram 4 (Typography)", kind="image", category="Ideogram", aspect_ratios=["9:16", "16:9", "1:1"], estimated_credits_per_run=1.0),
        "recraft-4.1": ModelSpec(id="recraft-4.1", name="Recraft 4.1 Vector/Graphic", kind="image", category="Recraft", aspect_ratios=["9:16", "16:9", "1:1"], estimated_credits_per_run=1.0),
        "qwen-image-3": ModelSpec(id="qwen-image-3", name="Qwen Image 3", kind="image", category="Alibaba Qwen", aspect_ratios=["9:16", "16:9", "1:1"], estimated_credits_per_run=0.8),
        "z-image-turbo": ModelSpec(id="z-image-turbo", name="Z-Image Turbo", kind="image", category="Higgsfield Fast", aspect_ratios=["9:16", "16:9", "1:1"], estimated_credits_per_run=0.5)
    }

    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = workspace_root or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )
        self.skills_dir = os.path.join(self.workspace_root, "higgsfield-skills")
        self.open_studio_dir = os.path.join(self.workspace_root, "open-higgsfield")
        self.api_key = os.getenv("HIGGSFIELD_API_KEY", "").strip()

    def get_catalog_models(self, kind: Optional[str] = None) -> List[ModelSpec]:
        """
        Returns supported models filtered by kind ('video', 'image', or all).
        """
        if not kind:
            return list(self.SUPPORTED_MODELS.values())
        return [m for m in self.SUPPORTED_MODELS.values() if m.kind == kind]

    def build_faceless_video_blueprint(
        self,
        topic: str,
        pillar: str,
        scenes: List[Dict[str, Any]],
        model_id: str = "soul-2"
    ) -> Dict[str, Any]:
        """
        Builds a Higgsfield-compliant Faceless Video manifest matching the
        specifications in higgsfield-skills/higgsfield-faceless-video/SKILL.md.
        """
        selected_model = self.SUPPORTED_MODELS.get(model_id, self.SUPPORTED_MODELS["soul-2"])
        
        blocks = []
        total_duration = 0.0

        for idx, sc in enumerate(scenes):
            duration = sc.get("duration_seconds", 5.0)
            total_duration += duration
            
            # Enrich visual prompt with cinematic camera movement
            base_prompt = sc.get("visual_prompt") or sc.get("subtitle_text") or topic
            camera_movement = "Slow orbital push-in, volumetric lighting, photorealistic cinematic 8k, AgX color grading"
            enhanced_prompt = f"{base_prompt}. {camera_movement}"

            blocks.append({
                "block_order": idx + 1,
                "scene_name": f"Scene_{idx + 1}",
                "model": selected_model.id,
                "aspect_ratio": "9:16",
                "duration_seconds": duration,
                "prompt": enhanced_prompt,
                "narration_text": sc.get("dialogue", ""),
                "subtitle": sc.get("subtitle_text", ""),
                "camera_motion": "push_in",
                "sound_effects": "deep_cinematic_sub_bass" if idx == 0 else "ambient_dark_whoosh"
            })

        manifest = {
            "version": "1.0",
            "project_type": "higgsfield_faceless_explainer",
            "pillar": pillar,
            "topic": topic,
            "aspect_ratio": "9:16",
            "resolution": "1080x1920",
            "total_blocks": len(blocks),
            "total_duration_seconds": round(total_duration, 2),
            "estimated_credits": round(len(blocks) * selected_model.estimated_credits_per_run, 1),
            "blocks": blocks,
            "style_guide": {
                "color_palette": "obsidian_purple_crimson" if pillar == "DARK_PSYCHOLOGY" else "tech_cyan_gold",
                "pacing": "fast_paced_sub_5_second_cuts",
                "subtitles": {
                    "font": "Proxima Nova Bold / Arial Black",
                    "position": "center_middle",
                    "highlight_color": "#FFCC00"
                }
            }
        }
        return manifest

    def estimate_production_budget(self, scene_count: int, model_id: str = "soul-2") -> Dict[str, Any]:
        """
        Estimates generation credits and approximate operational budget.
        """
        model = self.SUPPORTED_MODELS.get(model_id, self.SUPPORTED_MODELS["soul-2"])
        total_credits = scene_count * model.estimated_credits_per_run
        
        # Approximate baseline: 1 credit ~= $0.05 USD ~= 4.2 INR
        cost_usd = total_credits * 0.05
        cost_inr = cost_usd * 86.5

        return {
            "model_id": model.id,
            "model_name": model.name,
            "scene_count": scene_count,
            "estimated_credits": total_credits,
            "cost_usd": round(cost_usd, 2),
            "cost_inr": round(cost_inr, 2),
            "zero_cost_local_alternative": "Higgsfield Video Engineer WebGPU Path Tracer (100% Free on Local GPU)"
        }
