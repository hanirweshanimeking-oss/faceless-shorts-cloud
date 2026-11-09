"""
Dragon Studios India - OpenMontage Multi-Pipeline Adapter
Exposes OpenMontage's agentic video production pipelines:
1. Sci-Fi Cinematic Trailer (Veo/Kling motion clips + sound design)
2. Animated Explainer 3D (Character consistency + word-level captions)
3. Dark Psychology Documentary (Archival motion retrieval + orchestral score)
4. AI Tool Showcase (Rapid cuts, product UI highlight)
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("OpenMontageAdapter")

class OpenMontagePipelineSpec(BaseModel):
    pipeline_id: str
    display_name: str
    description: str
    recommended_duration: float
    asset_types: List[str]
    rendering_backend: str  # "remotion", "ffmpeg", "three_js"
    budget_estimate_usd: float

class OpenMontageAdapter:
    """
    Adapter implementing OpenMontage pipeline configurations.
    """
    PIPELINES = {
        "sci_fi_cinematic_trailer": OpenMontagePipelineSpec(
            pipeline_id="sci_fi_cinematic_trailer",
            display_name="Cinematic Sci-Fi Trailer",
            description="Veo and Kling motion clips, intense sound design, letterbox cinematic styling",
            recommended_duration=45.0,
            asset_types=["3d_motion_clips", "sub_bass_sfx", "orchestral_drone"],
            rendering_backend="remotion",
            budget_estimate_usd=2.50
        ),
        "animated_explainer_3d": OpenMontagePipelineSpec(
            pipeline_id="animated_explainer_3d",
            display_name="3D Animated Explainer",
            description="Character consistency, camera gliding, kinetic word-level typography",
            recommended_duration=60.0,
            asset_types=["three_js_scenes", "tts_narration", "upbeat_acoustic"],
            rendering_backend="three_js",
            budget_estimate_usd=0.0  # 100% Free on local GPU
        ),
        "dark_psychology_documentary": OpenMontagePipelineSpec(
            pipeline_id="dark_psychology_documentary",
            display_name="Dark Psychology Documentary",
            description="Obsidian pacing, archival motion clips, sidechain ducked ambient score",
            recommended_duration=35.0,
            asset_types=["dark_procedural_frames", "edge_tts_narration", "dark_ambient_music"],
            rendering_backend="ffmpeg",
            budget_estimate_usd=0.0  # 100% Free local
        ),
        "ai_tool_showcase": OpenMontagePipelineSpec(
            pipeline_id="ai_tool_showcase",
            display_name="AI Tool Viral Showcase",
            description="High-energy cuts, UI zoom highlights, direct comparison overlays",
            recommended_duration=28.0,
            asset_types=["ui_screen_captures", "sound_whooshes", "kinetic_text"],
            rendering_backend="ffmpeg",
            budget_estimate_usd=0.0  # 100% Free local
        )
    }

    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = workspace_root or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )
        self.openmontage_dir = os.path.join(self.workspace_root, "openmontage")
        self.available = os.path.exists(self.openmontage_dir)

    def list_pipelines(self) -> List[OpenMontagePipelineSpec]:
        """Returns all supported OpenMontage pipeline definitions."""
        return list(self.PIPELINES.values())

    def get_pipeline(self, pipeline_id: str) -> Optional[OpenMontagePipelineSpec]:
        """Returns specific pipeline configuration."""
        return self.PIPELINES.get(pipeline_id)
