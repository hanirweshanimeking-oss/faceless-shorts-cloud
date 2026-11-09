"""
Agent 3: Character Agent
Maintains character identities, reference databases, visual prompts, and visual continuity across chapters.
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

class CharacterAgent:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    def get_character(self, character_id: str) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM characters WHERE id = ?", (character_id,))
            row = cursor.fetchone()
            if not row:
                return None
            data = dict(row)
            data["hair_details"] = json.loads(data["hair_details"]) if data.get("hair_details") else {}
            data["eye_details"] = json.loads(data["eye_details"]) if data.get("eye_details") else {}
            data["clothing_details"] = json.loads(data["clothing_details"]) if data.get("clothing_details") else {}
            data["weapons"] = json.loads(data["weapons"]) if data.get("weapons") else []
            data["personality_traits"] = json.loads(data["personality_traits"]) if data.get("personality_traits") else []
            return data

    def build_conditioned_prompt(self, character_id: str, scene_action: str, emotion: str = "stoic") -> str:
        """Constructs an ultra-consistent manga visual prompt combining canonical features with scene action."""
        char = self.get_character(character_id)
        if not char:
            return scene_action

        # Format visual features
        hair = char["hair_details"].get("style", "messy black hair")
        eyes = char["eye_details"].get("left", "glowing indigo violet dragon pupil")
        clothing = char["clothing_details"].get("main_attire", "dark trench coat")
        
        prompt = (
            f"masterpiece manga art, highly detailed Japanese inking, sharp G-pen linework, "
            f"chiaroscuro black and white, professional screentones, "
            f"{char['name']}, {hair}, {eyes}, {clothing}, {emotion} facial expression, "
            f"{scene_action}, dynamic manga panel composition, 8k resolution, award-winning illustration"
        )
        return prompt

    def get_negative_prompt(self, character_id: str) -> str:
        char = self.get_character(character_id)
        if char and char.get("negative_prompt"):
            return char["negative_prompt"]
        return "lowres, blurry, extra limbs, bad anatomy, deformed hands, missing fingers, western comic style, full color, photorealistic, 3d render"
