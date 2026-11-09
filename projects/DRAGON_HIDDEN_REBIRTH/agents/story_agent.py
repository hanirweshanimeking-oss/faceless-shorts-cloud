"""
Agent 2: Story Agent
Develops chapter scripts, dialogue, emotional beats, internal monologues, and ensures narrative continuity.
"""

import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Optional

class StoryAgent:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    def get_canonical_lore(self) -> str:
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT content FROM story_bible WHERE category='PREMISE' LIMIT 1")
            row = cursor.fetchone()
            return row[0] if row else ""

    def get_chapter_data(self, chapter_id: str) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM chapters WHERE id = ?", (chapter_id,))
            row = cursor.fetchone()
            if not row:
                return None
            
            cursor.execute("SELECT * FROM pages WHERE chapter_id = ? ORDER BY page_number ASC", (chapter_id,))
            pages = [dict(p) for p in cursor.fetchall()]
            
            res = dict(row)
            res["pages"] = pages
            return res

    def validate_script_continuity(self, page_id: str) -> Dict[str, Any]:
        """Validates that dialogue does not violate character stoicism or world rules."""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM panels WHERE page_id = ? ORDER BY panel_index ASC", (page_id,))
            panels = [dict(p) for p in cursor.fetchall()]

        issues = []
        for p in panels:
            speaker = p.get("speaker_name")
            dialogue = p.get("dialogue_text") or ""
            if speaker == "Chitran":
                # Chitran must never speak frantic exclamation marks or cowardly pleas
                if "please" in dialogue.lower() or "help me" in dialogue.lower() or "noooo" in dialogue.lower():
                    issues.append(f"Panel {p['panel_index']}: Chitran dialogue breaks stoic character code: '{dialogue}'")
                if len(dialogue.split()) > 25:
                    issues.append(f"Panel {p['panel_index']}: Chitran dialogue is too verbose for a laconic sovereign: '{dialogue}'")
        
        return {
            "status": "VALID" if not issues else "NEEDS_REVISION",
            "page_id": page_id,
            "panel_count": len(panels),
            "issues": issues
        }
