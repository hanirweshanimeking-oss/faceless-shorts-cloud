"""
Dragon Studios India - Stage 10: Continuous Improvement & Self-Optimization Agent
Closes the loop between post-launch analytics and the next production cycle,
adjusting ideation weights, hook formulas, and pacing heuristics dynamically.
"""

import os
import json
from typing import Dict, Any, List
from pydantic import BaseModel, Field

LEARNINGS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "studio_learnings.json"))

class FeedbackOptimization(BaseModel):
    project_id: str
    target_metric: str
    current_performance: float
    recommended_hook_style: str
    recommended_duration_seconds: float
    pacing_adjustment: str
    next_topic_recommendation: str

class ImproveAgent:
    @staticmethod
    def analyze_and_optimize(
        project_id: str,
        analytics_data: Dict[str, Any],
        pillar: str = "DARK_PSYCHOLOGY"
    ) -> FeedbackOptimization:
        """
        Analyzes performance metrics and formulates concrete adjustments
        for subsequent ideation and scripting runs.
        """
        save_rate = analytics_data.get("save_rate_pct", 2.0)
        retention = analytics_data.get("retention_rate_pct", 75.0)

        # 1. Pacing & Duration adjustment
        if retention < 60.0:
            recommended_duration = 18.0
            pacing_adjustment = "Tighten cuts from 4.5s to 2.8s per scene. Increase audio tempo by 1.1x."
            hook_style = "Visual Shock / In medias res (No intro, immediate contrarian statement)"
        else:
            recommended_duration = 24.0
            pacing_adjustment = "Current 4.0s-5.0s pacing is healthy. Maintain cinematic pauses on punchlines."
            hook_style = "Triple Hook (Visual + Sub-bass drop + Open curiosity loop)"

        # 2. Topic recommendation
        if pillar == "DARK_PSYCHOLOGY":
            next_topic = "RULE #36: How to Disarm Narcissistic Ego Without Saying a Word"
        elif pillar == "AI_TOOLS":
            next_topic = "Top 3 Open-Source AI Agents That Build Mobile Apps from Figma"
        else:
            next_topic = "CHITRAN: Chapter 2 - The Celestial Blade Breaks"

        optimization = FeedbackOptimization(
            project_id=project_id,
            target_metric="3-Second Retention & Save Rate",
            current_performance=round((save_rate * 10) + (retention * 0.5), 1),
            recommended_hook_style=hook_style,
            recommended_duration_seconds=recommended_duration,
            pacing_adjustment=pacing_adjustment,
            next_topic_recommendation=next_topic
        )

        # Save to persistent learnings history
        all_learnings = []
        if os.path.exists(LEARNINGS_FILE):
            try:
                with open(LEARNINGS_FILE, "r", encoding="utf-8") as f:
                    all_learnings = json.load(f)
            except Exception:
                all_learnings = []

        all_learnings.append(optimization.model_dump())
        with open(LEARNINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(all_learnings, f, indent=2)

        return optimization
