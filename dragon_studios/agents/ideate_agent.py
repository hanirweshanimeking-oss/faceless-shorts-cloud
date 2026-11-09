"""
Dragon Studios India - Stage 2: Ideation & Concept Agent
Generates high-retention video concepts, computes Viral Potential Scores (VPS),
and locks in the Triple-Hook narrative angle.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import uuid

class ConceptPitch(BaseModel):
    concept_id: str
    title: str
    pillar: str
    target_audience: str
    core_thesis: str
    visual_hook_3s: str
    auditory_hook_3s: str
    curiosity_gap: str
    viral_potential_score: float = Field(..., ge=0.0, le=10.0)
    estimated_retention_rate: float = Field(..., ge=0.0, le=100.0)

class IdeateAgent:
    @staticmethod
    def brainstorm_concepts(topic: str, pillar: str = "DARK_PSYCHOLOGY", num_concepts: int = 3) -> List[ConceptPitch]:
        """
        Brainstorms multiple creative angles for a topic and scores them.
        """
        concepts = []
        
        if pillar == "DARK_PSYCHOLOGY":
            pitches = [
                {
                    "title": f"THE COLD RULE OF {topic.upper()}",
                    "core_thesis": "Never react emotionally; silence and calculated delay always dismantle opposing leverage.",
                    "visual_hook": "High-contrast silhouette with subtle smoke, sudden zoom on cold gaze.",
                    "auditory_hook": f"The moment you explain {topic.lower()} to someone, you surrender all control.",
                    "curiosity_gap": "Here is the exact psychological mechanism masterminds use to win silently.",
                    "vps": 9.4,
                    "retention": 84.5
                },
                {
                    "title": f"HOW TO WIN BEFORE {topic.upper()} BEGINS",
                    "core_thesis": "Victorious warriors win first and then go to war, while defeated warriors go to war first.",
                    "visual_hook": "Dark chessboard where a single black pawn knocks over a king.",
                    "auditory_hook": f"Most people fight {topic.lower()} directly. That is why they always lose.",
                    "curiosity_gap": "The real battle ended three moves before anyone even noticed.",
                    "vps": 9.1,
                    "retention": 81.0
                },
                {
                    "title": f"RULE #35: THE DANGEROUS PSYCHOLOGY OF {topic.upper()}",
                    "core_thesis": "Selective attention and deliberate unpredictability force others to reveal their motives.",
                    "visual_hook": "Glitch effect with neon typography: 'RULE #35: NEVER EXPLAIN'.",
                    "auditory_hook": f"When you practice {topic.lower()} correctly, people cannot read your next move.",
                    "curiosity_gap": "Notice how the most dangerous person in the room never speaks first.",
                    "vps": 9.6,
                    "retention": 87.0
                }
            ]
        elif pillar == "AI_TOOLS":
            pitches = [
                {
                    "title": f"NEVER PAY FOR {topic.upper()} AGAIN",
                    "core_thesis": "Open-source GitHub models and local scripts replace $50/month paid SaaS platforms.",
                    "visual_hook": "Screen recording showing a complex project auto-generated in 5 seconds.",
                    "auditory_hook": f"Big tech companies are charging $200 a year for {topic.lower()}. Stop paying them.",
                    "curiosity_gap": "This single open-source command runs the entire pipeline locally for free.",
                    "vps": 9.7,
                    "retention": 89.0
                },
                {
                    "title": f"HOW AI AGENTS AUTOMATE {topic.upper()} IN 15 SECONDS",
                    "core_thesis": "Autonomous agents eliminate human browser clicks and manual edits.",
                    "visual_hook": "Split screen comparing a frustrated human editor vs a high-speed agent terminal.",
                    "auditory_hook": f"You are still doing {topic.lower()} manually in 2026? Watch this.",
                    "curiosity_gap": "Here is the exact repository you need to clone right now.",
                    "vps": 9.3,
                    "retention": 83.5
                },
                {
                    "title": f"THE SECRET GITHUB REPO FOR {topic.upper()}",
                    "core_thesis": "Reverse-engineering top creator workflows using lightweight automation scripts.",
                    "visual_hook": "Terminal executing with colored log lines and instant video output.",
                    "auditory_hook": f"Developers don't want you to know about this {topic.lower()} tool.",
                    "curiosity_gap": "It has 26,000 stars on GitHub and takes 2 minutes to install.",
                    "vps": 9.5,
                    "retention": 86.0
                }
            ]
        else: # ORIGINAL_MANGA
            pitches = [
                {
                    "title": f"THE AWAKENING: {topic.upper()}",
                    "core_thesis": "Limits are an illusion crafted by fear; true strength emerges only when ego dies.",
                    "visual_hook": "High-contrast monochrome manga panel with glowing eye VFX and ink splatter.",
                    "auditory_hook": f"They thought {topic.lower()} was a weakness. They were dead wrong.",
                    "curiosity_gap": "The transformation happens the second all hope is abandoned.",
                    "vps": 9.5,
                    "retention": 86.5
                },
                {
                    "title": f"SURVIVING THE VOID: {topic.upper()}",
                    "core_thesis": "Pain is not a obstacle; it is the forge.",
                    "visual_hook": "Fast cinematic whip pan across rain-soaked battle terrain.",
                    "auditory_hook": f"Only a true monster can walk through {topic.lower()} and smile.",
                    "curiosity_gap": "Watch what happens when the seal finally breaks.",
                    "vps": 9.2,
                    "retention": 82.0
                }
            ]

        for p in pitches[:num_concepts]:
            concepts.append(ConceptPitch(
                concept_id=f"c_{uuid.uuid4().hex[:8]}",
                title=p["title"],
                pillar=pillar,
                target_audience="High-growth creators, developers, ambitious minds",
                core_thesis=p["core_thesis"],
                visual_hook_3s=p["visual_hook"],
                auditory_hook_3s=p["auditory_hook"],
                curiosity_gap=p["curiosity_gap"],
                viral_potential_score=p["vps"],
                estimated_retention_rate=p["retention"]
            ))

        # Sort by viral potential score descending
        return sorted(concepts, key=lambda x: x.viral_potential_score, reverse=True)
