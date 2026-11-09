"""
Agent 4: World Agent
Maintains world-building, geography, obsidian architecture, magic circles, and atmospheric environments.
"""

import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Optional

class WorldAgent:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    def get_location(self, location_id: str) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM world_locations WHERE id = ?", (location_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def build_environment_prompt(self, location_id: str, weather_or_mood: str = "ominous violet mist") -> str:
        loc = self.get_location(location_id)
        if not loc:
            return f"dark fantasy manga environment, {weather_or_mood}, high contrast screentone"
        
        return (
            f"masterpiece manga background, {loc['visual_prompt']}, atmospheric depth, "
            f"{weather_or_mood}, detailed architectural inking, clean perspective lines, "
            f"gothic volcanic masonry, 8k manga screentone"
        )
