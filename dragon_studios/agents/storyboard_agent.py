"""
Dragon Studios India - Stage 4: Storyboard & Prompt Architect Agent
Translates script narrative into scene-by-scene visual blueprints,
generating camera blocking, text overlay safe zones, and Midjourney/FLUX/Sora prompts.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from dragon_studios.agents.script_agent import VideoProductionPlan, SceneBlueprint

class StoryboardPanel(BaseModel):
    scene_order: int
    duration_seconds: float
    shot_type: str
    camera_movement: str
    color_palette: str
    text_overlay: str
    text_position: str  # 'CENTER', 'BOTTOM_SAFE', 'TOP_BANNER'
    visual_prompt_midjourney: str
    visual_prompt_flux: str
    audio_sync_cue: str

class StoryboardManifest(BaseModel):
    project_id: str
    title: str
    aspect_ratio: str = "9:16"
    resolution: str = "1080x1920"
    total_panels: int
    total_duration_seconds: float
    panels: List[StoryboardPanel]

class StoryboardAgent:
    @staticmethod
    def generate_storyboard(plan: VideoProductionPlan) -> StoryboardManifest:
        """
        Converts a VideoProductionPlan into an actionable, detailed storyboard.
        """
        panels = []
        for s in plan.scenes:
            # Determine shot composition and text positioning based on scene order and pillar
            if s.scene_order == 1:
                shot_type = "Extreme Close-Up / Impact Hook"
                text_position = "TOP_BANNER"
                palette = "Deep Obsidian #0b0c10, High-Voltage Violet #7928ca, Neon Cyan rim light"
            elif s.scene_order == len(plan.scenes):
                shot_type = "Branded Wide Reveal / Call-To-Action"
                text_position = "BOTTOM_SAFE"
                palette = "Midnight Black #000000, Dragon Purple #9333ea, White Typography"
            else:
                shot_type = "Medium Tracking Shot / Dynamic Pacing"
                text_position = "CENTER"
                palette = "Moody Cinematic Dark Slate, Subtle Golden / Neon Accents"

            # Build generation prompts for modern AI video & image models
            mj_prompt = (
                f"{s.visual_prompt} shot on 35mm anamorphic lens, volumetric lighting, "
                f"cinematic color grading, 8k resolution, photorealistic detail --ar 9:16 --v 6.1 --style raw"
            )
            flux_prompt = (
                f"A masterwork vertical 9:16 cinematic scene: {s.visual_prompt}. "
                f"Sharp focus, intricate textures, dramatic rim lighting, unreal engine 5 render style."
            )

            panels.append(StoryboardPanel(
                scene_order=s.scene_order,
                duration_seconds=s.duration_seconds,
                shot_type=shot_type,
                camera_movement=s.camera_movement,
                color_palette=palette,
                text_overlay=s.subtitle_text,
                text_position=text_position,
                visual_prompt_midjourney=mj_prompt,
                visual_prompt_flux=flux_prompt,
                audio_sync_cue=s.sound_cue
            ))

        return StoryboardManifest(
            project_id=plan.project_id,
            title=plan.title,
            aspect_ratio=plan.aspect_ratio,
            resolution="1080x1920",
            total_panels=len(panels),
            total_duration_seconds=plan.total_duration_seconds,
            panels=panels
        )
