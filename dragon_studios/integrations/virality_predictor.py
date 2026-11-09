"""
Dragon Studios India - Multi-Factor Virality Predictor
Implements statistical and heuristic virality scoring algorithms inspired by
allenwang28/YouTube-Virality-Predictor and TikTok virality models.
Predicts hook retention, 3-second hold rate, and share-to-save ratios before rendering.
"""

import re
from typing import Dict, Any, List
from pydantic import BaseModel, Field

class ViralityForecast(BaseModel):
    viral_potential_score: float = Field(..., ge=0.0, le=10.0)
    predicted_3s_hold_rate: float  # e.g. 68.5%
    predicted_completion_rate: float  # e.g. 42.0%
    predicted_share_save_ratio: float  # e.g. 1.35
    hook_strength_score: float  # 0 to 100
    curiosity_gap_score: float  # 0 to 100
    emotional_valence_score: float  # 0 to 100
    optimization_recommendations: List[str]

class ViralityPredictorEngine:
    """
    Evaluates concept titles, hooks, and scene dialogue to predict short-form virality.
    """
    VIRAL_TRIGGERS = [
        "never", "stop", "secret", "destroy", "psychology", "rule", "law",
        "mistake", "truth", "trap", "power", "control", "danger", "lies",
        "nobody", "silence", "weak", "enemy", "manipulate", "ego", "100%"
    ]

    HIGH_RETENTION_STARTERS = [
        "if you", "why you", "the truth about", "stop doing", "never let",
        "the secret to", "how to destroy", "how to control", "watch this before",
        "this rule will", "most people don't know"
    ]

    def predict(
        self,
        title: str,
        hook_text: str,
        pillar: str = "DARK_PSYCHOLOGY",
        scene_count: int = 4
    ) -> ViralityForecast:
        """
        Runs comprehensive multi-factor prediction on the video concept.
        """
        combined = f"{title.lower()} {hook_text.lower()}"
        
        # 1. Trigger word density
        trigger_matches = sum(1 for trigger in self.VIRAL_TRIGGERS if trigger in combined)
        trigger_score = min(100.0, trigger_matches * 22.0)

        # 2. Curiosity gap evaluation
        has_proven_starter = any(combined.startswith(s) or s in combined for s in self.HIGH_RETENTION_STARTERS)
        curiosity_score = 85.0 if has_proven_starter else 55.0
        if "?" in hook_text or "..." in hook_text or "—" in hook_text:
            curiosity_score += 10.0
        curiosity_score = min(100.0, curiosity_score)

        # 3. Emotional valence and tension
        tension_words = ["destroy", "enemy", "danger", "weak", "trap", "manipulate", "lies", "ego"]
        has_tension = any(tw in combined for tw in tension_words)
        emotional_score = 90.0 if has_tension else 65.0

        # 4. Hook conciseness & impact (ideal hook is between 6 and 14 words)
        hook_words = len(hook_text.split())
        if 6 <= hook_words <= 14:
            length_bonus = 20.0
        elif hook_words < 6:
            length_bonus = 10.0
        else:
            length_bonus = 5.0
            
        hook_strength = min(100.0, (trigger_score * 0.4) + (curiosity_score * 0.4) + length_bonus)

        # Composite Viral Potential Score (0.0 to 10.0)
        vps = round(((hook_strength * 0.45) + (curiosity_score * 0.30) + (emotional_score * 0.25)) / 10.0, 1)
        vps = max(1.0, min(9.9, vps))

        # Predict behavioral metrics
        predicted_3s = round(min(88.0, 52.0 + (vps * 3.4)), 1)
        predicted_completion = round(min(58.0, 24.0 + (vps * 2.8) - (max(0, scene_count - 4) * 2.5)), 1)
        predicted_share_save = round(0.6 + (vps * 0.08), 2)

        recommendations = []
        if hook_words > 14:
            recommendations.append("Shorten opening hook to under 12 words for faster retention lock.")
        if trigger_matches < 2:
            recommendations.append("Inject at least 2 high-urgency psychological trigger words (e.g., 'silence', 'secret', 'never').")
        if not has_proven_starter:
            recommendations.append("Reframe opening using a direct-address prompt (e.g. 'If you...', 'Stop doing...').")
        if not recommendations:
            recommendations.append("Hook architecture is optimal. Pacing ready for production.")

        return ViralityForecast(
            viral_potential_score=vps,
            predicted_3s_hold_rate=predicted_3s,
            predicted_completion_rate=predicted_completion,
            predicted_share_save_ratio=predicted_share_save,
            hook_strength_score=round(hook_strength, 1),
            curiosity_gap_score=round(curiosity_score, 1),
            emotional_valence_score=round(emotional_score, 1),
            optimization_recommendations=recommendations
        )
