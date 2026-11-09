"""
Agent 6: Illustration Agent
Generates individual panel artwork using the multi-tier zero-budget image generation engine.
"""

import sqlite3
from pathlib import Path
from typing import Dict, Any, Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.image_generator import MangaImageGenerator

class IllustrationAgent:
    def __init__(self, db_path: Path, output_dir: Path):
        self.db_path = db_path
        self.output_dir = output_dir
        self.generator = MangaImageGenerator(output_dir)

    def render_panel(self, panel_id: str, prefer_cloud: bool = False) -> Dict[str, Any]:
        """Fetches panel record from DB and renders its artwork."""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM panels WHERE id = ?", (panel_id,))
            panel = cursor.fetchone()
            if not panel:
                return {"status": "ERROR", "reason": f"Panel {panel_id} not found."}

        # Render panel
        img_path = self.generator.generate_panel(
            panel_id=panel["id"],
            width=panel["bbox_w"],
            height=panel["bbox_h"],
            shot_type=panel["shot_type"],
            visual_prompt=panel["visual_prompt"],
            screentone_style=panel["screentone_style"] or "FINE_TONE",
            prefer_cloud=prefer_cloud
        )

        # Update DB status
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE panels 
                SET raw_panel_path = ?, status = 'GENERATED'
                WHERE id = ?
            """, (str(img_path), panel_id))
            conn.commit()

        return {
            "status": "SUCCESS",
            "panel_id": panel_id,
            "image_path": str(img_path),
            "width": panel["bbox_w"],
            "height": panel["bbox_h"]
        }
