"""
Dragon Studios India - Growth Strategy & Analytics Agent
Analyzes post-publication performance, calculates virality ratios,
and stores strategic content insights back into the database.
"""

import uuid
from typing import Dict, Any, List
from dragon_studios.database.db_manager import save_growth_insight, log_analytics

def evaluate_reels_performance(
    views: int,
    reach: int,
    likes: int,
    comments: int,
    shares: int,
    saves: int,
    watch_time_seconds: float,
    video_duration: float
) -> Dict[str, Any]:
    """
    Computes critical Instagram Reels engagement and virality signals.
    """
    effective_reach = max(reach, views, 1)
    
    save_rate = (saves / effective_reach) * 100.0
    share_rate = (shares / effective_reach) * 100.0
    retention_rate = (watch_time_seconds / max(video_duration, 1.0)) * 100.0 if video_duration > 0 else 0.0
    
    # Algorithmic health evaluation
    insights = []
    
    if save_rate >= 3.0:
        insights.append("HIGH SAVE RATE (>3%): Strong psychological/educational value. Audiences are bookmarking for reference.")
    elif save_rate < 1.0:
        insights.append("LOW SAVE RATE (<1%): Script needs punchier, more actionable takeaway rules.")

    if share_rate >= 2.0:
        insights.append("HIGH SHARE RATE (>2%): High viral velocity. Audience identifies emotionally with the quote/story.")
        
    if retention_rate >= 80.0:
        insights.append("HIGH RETENTION (>80%): Pacing and visual transitions are optimal.")
    elif retention_rate < 50.0:
        insights.append("DROP-OFF DETECTED (<50%): First 3-second hook needs higher contrast and immediate audio punch.")

    overall_score = (save_rate * 3.0) + (share_rate * 3.0) + (retention_rate * 0.4)
    overall_score = round(min(100.0, overall_score), 1)

    return {
        "save_rate_pct": round(save_rate, 2),
        "share_rate_pct": round(share_rate, 2),
        "retention_rate_pct": round(retention_rate, 2),
        "overall_score": overall_score,
        "recommendations": insights
    }

def record_experiment_learning(
    topic_category: str,
    finding: str,
    action_item: str,
    confidence: float = 0.85
) -> str:
    """Logs a learned principle into the growth knowledgebase."""
    insight_id = f"insight_{uuid.uuid4().hex[:8]}"
    save_growth_insight(
        insight_id=insight_id,
        insight_key=topic_category,
        category=topic_category,
        finding=finding,
        confidence_score=confidence,
        recommended_action=action_item
    )
    return insight_id
