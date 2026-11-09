"""
Dragon Studios India - Integrations Ecosystem Hub
Unified gateway connecting all 12 viral video generation, editing, and agentic production frameworks.
"""

import os
from typing import Dict, Any

from dragon_studios.integrations.reelmimic_adapter import ReelMimicAdapter
from dragon_studios.integrations.hypit_adapter import HypitAdapter
from dragon_studios.integrations.paradee_voice import ParadeeVoiceEngine
from dragon_studios.integrations.virality_predictor import ViralityPredictorEngine
from dragon_studios.integrations.openmontage_adapter import OpenMontageAdapter
from dragon_studios.integrations.claude_video_adapter import ClaudeVideoAdapter
from dragon_studios.integrations.google_flow_adapter import GoogleFlowAdapter

INTEGRATED_REPOS = [
    ("claude-video", "Claude-Video (/watch) Agent Multi-Modal Video Perception"),
    ("reelmimic", "ReelMimic Video Style Deconstruction"),
    ("video-use", "Video-Use Agentic Editing & Pop-Free Cuts"),
    ("paradee", "Paradee 1.2 8.5MB Ultra-Fast Multi-Voice TTS"),
    ("hypit", "Hypit SVML & Multi-Variant Generator"),
    ("claude-animated-shorts", "Claude Animated Shorts (Three.js + Remotion)"),
    ("lemo-opuscar", "Lemo-Opuscar Code-Driven Film Framework"),
    ("reticle", "Reticle Machine-Native Runtime Perception"),
    ("autoswarm", "AutoSwarm Multi-Agent Swarm Hub"),
    ("open-generative-ai", "Open Generative AI (600+ Model Studio)"),
    ("openmontage", "OpenMontage 12-Pipeline Video Engine"),
    ("virality-predictor", "Machine Learning Virality Predictor"),
    ("laya-coreml", "Laya Typed Decision Architecture"),
    ("open-higgsfield", "OpenHiggsfield 38-Model Next.js Studio")
]

def get_integrations_health_check(workspace_root: str = None) -> Dict[str, Any]:
    """
    Scans the workspace to verify the installation and readiness of all 13 integrated tools.
    """
    workspace = workspace_root or os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )

    statuses = {}
    ready_count = 0

    for folder_name, display_name in INTEGRATED_REPOS:
        target_path = os.path.join(workspace, folder_name)
        exists = os.path.exists(target_path)
        if exists:
            ready_count += 1
        statuses[folder_name] = {
            "name": display_name,
            "installed": exists,
            "path": target_path if exists else None
        }

    return {
        "total_repositories": len(INTEGRATED_REPOS),
        "installed_count": ready_count,
        "all_ready": ready_count == len(INTEGRATED_REPOS),
        "repositories": statuses
    }

__all__ = [
    "ClaudeVideoAdapter",
    "ReelMimicAdapter",
    "HypitAdapter",
    "ParadeeVoiceEngine",
    "ViralityPredictorEngine",
    "OpenMontageAdapter",
    "GoogleFlowAdapter",
    "get_integrations_health_check",
    "INTEGRATED_REPOS"
]
