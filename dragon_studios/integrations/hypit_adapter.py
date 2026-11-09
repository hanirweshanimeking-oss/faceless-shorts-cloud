"""
Dragon Studios India - Hypit SVML & Multi-Variant Generator
Transforms video scripts into Semantic Video Markup Language (SVML), anchoring visual effects,
B-roll transitions, and kinetic typography directly to words in the speech transcript.
Generates multi-variant A/B testing packages to maximize retention across platforms.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("HypitAdapter")

class SVMLWordNode(BaseModel):
    word: str
    emphasis: bool = False
    visual_cue: Optional[str] = None
    sfx: Optional[str] = None

class SVMLScene(BaseModel):
    scene_index: int
    duration_seconds: float
    dialogue_raw: str
    word_nodes: List[SVMLWordNode]
    broll_query: str
    camera_effect: str

class HypitVariant(BaseModel):
    variant_id: str
    hook_type: str  # "confrontational", "data_driven", "curiosity_gap", "identity_threat"
    hook_text: str
    thumbnail_hook: str
    predicted_relative_retention: float

class HypitAdapter:
    """
    Adapter implementing Hypit SVML and Multi-Variant A/B testing architecture.
    """
    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = workspace_root or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )
        self.hypit_dir = os.path.join(self.workspace_root, "hypit")
        self.available = os.path.exists(self.hypit_dir)

    def convert_to_svml(
        self,
        scene_index: int,
        dialogue: str,
        duration: float,
        pillar: str = "DARK_PSYCHOLOGY"
    ) -> SVMLScene:
        """
        Parses dialogue into semantic word nodes with automated emphasis and SFX cues.
        """
        words = dialogue.strip().split()
        word_nodes = []
        
        # Power words that trigger emphasis and sound effects
        emphasis_triggers = {
            "never", "stop", "destroy", "control", "power", "silence",
            "free", "secret", "trap", "observe", "strike", "awake"
        }
        
        for idx, w in enumerate(words):
            clean_word = w.lower().strip(".,!?:;")
            is_emp = clean_word in emphasis_triggers or idx == 0
            sfx_cue = "sub_bass_drop" if (is_emp and idx < 3) else None
            visual_cue = "kinetic_zoom" if is_emp else None
            
            word_nodes.append(SVMLWordNode(
                word=w,
                emphasis=is_emp,
                visual_cue=visual_cue,
                sfx=sfx_cue
            ))

        return SVMLScene(
            scene_index=scene_index,
            duration_seconds=duration,
            dialogue_raw=dialogue,
            word_nodes=word_nodes,
            broll_query=f"{pillar.lower()} cinematic dramatic lighting {dialogue[:30]}",
            camera_effect="slow_push" if scene_index % 2 == 0 else "orbital_rotate"
        )

    def generate_viral_variants(
        self,
        base_topic: str,
        pillar: str = "DARK_PSYCHOLOGY"
    ) -> List[HypitVariant]:
        """
        Generates 4 distinct hook variants for multi-variant A/B publishing.
        """
        variants = [
            HypitVariant(
                variant_id="var_A_curiosity",
                hook_type="curiosity_gap",
                hook_text=f"The most dangerous habit regarding {base_topic} that 99% ignore.",
                thumbnail_hook="THE 99% MISTAKE",
                predicted_relative_retention=1.18
            ),
            HypitVariant(
                variant_id="var_B_confrontational",
                hook_type="confrontational",
                hook_text=f"Stop lying to yourself about {base_topic}. Here is the truth.",
                thumbnail_hook="STOP LYING TO YOURSELF",
                predicted_relative_retention=1.24
            ),
            HypitVariant(
                variant_id="var_C_identity",
                hook_type="identity_threat",
                hook_text=f"If you still care about {base_topic}, you have already lost.",
                thumbnail_hook="YOU ALREADY LOST",
                predicted_relative_retention=1.31
            ),
            HypitVariant(
                variant_id="var_D_data",
                hook_type="data_driven",
                hook_text=f"3 psychological laws of {base_topic} proven by human history.",
                thumbnail_hook="3 UNBREAKABLE LAWS",
                predicted_relative_retention=1.15
            )
        ]
        return variants
