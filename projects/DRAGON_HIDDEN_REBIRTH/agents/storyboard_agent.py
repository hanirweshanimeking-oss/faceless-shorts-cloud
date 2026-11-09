"""
Agent 5: Storyboard Agent
Converts scene beats into professional manga page layouts, calculating panel geometries, gutters, and reading direction.
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, List

class StoryboardAgent:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    def calculate_standard_layout(
        self,
        page_width: int = 2480,
        page_height: int = 3508,
        panel_count: int = 4,
        margin: int = 100,
        gutter: int = 40
    ) -> List[Dict[str, int]]:
        """
        Generates traditional Japanese manga panel layout bounding boxes (RTL flow).
        Supports 3, 4, or 5 panel asymmetric dynamic compositions.
        """
        usable_w = page_width - (margin * 2)
        usable_h = page_height - (margin * 2)
        
        panels = []
        if panel_count == 4:
            # Panel 1: Establishing Top Wide (full width)
            h1 = int(usable_h * 0.28)
            panels.append({"panel_index": 1, "x": margin, "y": margin, "w": usable_w, "h": h1})
            
            # Mid tier: 2 vertical panels side-by-side (RTL: Panel 2 on right, Panel 3 on left)
            h_mid = int(usable_h * 0.35)
            y_mid = margin + h1 + gutter
            w_half = (usable_w - gutter) // 2
            
            # Panel 2 (Right side first in Japanese RTL)
            panels.append({"panel_index": 2, "x": margin + w_half + gutter, "y": y_mid, "w": w_half, "h": h_mid})
            # Panel 3 (Left side second in RTL)
            panels.append({"panel_index": 3, "x": margin, "y": y_mid, "w": w_half, "h": h_mid})
            
            # Bottom tier: Panel 4 Climax Wide (full width)
            y_bot = y_mid + h_mid + gutter
            h_bot = page_height - margin - y_bot
            panels.append({"panel_index": 4, "x": margin, "y": y_bot, "w": usable_w, "h": h_bot})
            
        elif panel_count == 3:
            # 3-tier horizontal dynamic layout
            h_tier = (usable_h - (gutter * 2)) // 3
            for i in range(3):
                y = margin + (i * (h_tier + gutter))
                panels.append({"panel_index": i + 1, "x": margin, "y": y, "w": usable_w, "h": h_tier})
        else:
            # Fallback dynamic vertical strip
            h_tier = (usable_h - (gutter * (panel_count - 1))) // panel_count
            for i in range(panel_count):
                y = margin + (i * (h_tier + gutter))
                panels.append({"panel_index": i + 1, "x": margin, "y": y, "w": usable_w, "h": h_tier})
                
        return panels

    def get_page_panels(self, page_id: str) -> List[Dict[str, Any]]:
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM panels WHERE page_id = ? ORDER BY panel_index ASC", (page_id,))
            return [dict(p) for p in cursor.fetchall()]
