"""
Faceless Shorts Director Agent
Acts as the Chief Autonomous Media Director for each video project:
1. Analyzes the user's prompt and requested style.
2. Selects the ideal neural voice narrator (Edge-TTS) suited for the genre.
3. Configures dynamic color palettes, character archetypes, props, and camera choreography.
4. Ensures every single video is visually distinct and tailored to the topic.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

@dataclass
class VisualDirection:
    style: str
    palette_top: tuple
    palette_horizon: tuple
    accent_color: tuple
    character_archetype: str  # 'cartoon_hero', 'anatomical_figure', 'stick_figure', 'detective', 'engineer', 'commander'
    outfit: str               # 'suit', 'hoodie', 'lab_coat', 'trench_coat', 'survival_gear', 'scrubs'
    hair_style: str           # 'short', 'messy', 'parted', 'bald', 'ponytail'
    skin_tone: tuple
    voice: str
    bg_theme: str             # 'office', 'medical_lab', 'noir_street', 'wild_nature', 'blueprint', 'parchment_map'
    scene_badges: List[str]

# Curated high-retention voices for each style
STYLE_VOICE_MAP = {
    "Deep Dive 3D": "en-US-EricNeural",           # Fast, energetic, clinical like Zack D. Films
    "Night File 3D": "en-GB-RyanNeural",          # Chilling, deep British mystery narrator
    "Stick Story": "en-US-GuyNeural",             # Casual, fast-paced survivalist
    "Inside Out": "en-US-JennyNeural",            # Clear, smart, engaging female science explainer
    "Paper Atlas": "en-GB-ThomasNeural",          # Authoritative historical documentary voice
    "Tall Tale 3D": "en-US-ChristopherNeural"     # Dramatic, punchy, confident storyteller
}

class DirectorAgent:
    @staticmethod
    def direct_production(prompt: str, requested_style: Optional[str] = None, requested_voice: Optional[str] = None) -> VisualDirection:
        """
        Directs visual palette, voice actor, and character persona for the video.
        """
        lower_prompt = prompt.lower()
        
        # 1. Detect or respect style
        style = requested_style or "Tall Tale 3D"
        if not requested_style:
            if any(k in lower_prompt for k in ["what happens", "stung", "swallow", "body", "medical", "disease", "organ", "nail", "brain", "heart"]):
                style = "Deep Dive 3D"
            elif any(k in lower_prompt for k in ["mystery", "spooky", "crime", "unsolved", "ghost", "dark", "creepy", "killer"]):
                style = "Night File 3D"
            elif any(k in lower_prompt for k in ["survival", "survive", "island", "stranded", "hack", "wild", "forest", "bear", "shark", "desert"]):
                style = "Stick Story"
            elif any(k in lower_prompt for k in ["how it works", "engine", "inside", "machine", "physics", "technology", "car"]):
                style = "Inside Out"
            elif any(k in lower_prompt for k in ["history", "war", "battle", "empire", "ancient", "map", "conquest"]):
                style = "Paper Atlas"
            else:
                style = "Tall Tale 3D"

        # 2. Select voice
        voice = requested_voice
        if not voice or voice in ["am_adam", "default"]:
            voice = STYLE_VOICE_MAP.get(style, "en-US-ChristopherNeural")

        # 3. Configure Visual Archetypes and Palettes per Style
        if style == "Deep Dive 3D":
            return VisualDirection(
                style="Deep Dive 3D",
                palette_top=(15, 22, 35),
                palette_horizon=(25, 45, 70),
                accent_color=(0, 210, 255),       # Bio-cyan glow
                character_archetype="anatomical_figure",
                outfit="scrubs",
                hair_style="short",
                skin_tone=(240, 200, 175),
                voice=voice,
                bg_theme="medical_lab",
                scene_badges=["BIO-SCAN", "INTERNAL VIEW", "CELLULAR LEVEL", "THE REACTION", "CRITICAL IMPACT", "THE VERDICT"]
            )
        elif style == "Night File 3D":
            return VisualDirection(
                style="Night File 3D",
                palette_top=(8, 10, 16),
                palette_horizon=(22, 28, 42),
                accent_color=(255, 60, 60),        # Red alarm/evidence
                character_archetype="detective",
                outfit="trench_coat",
                hair_style="messy",
                skin_tone=(230, 205, 185),
                voice=voice,
                bg_theme="noir_street",
                scene_badges=["EVIDENCE #1", "SUSPICION", "DARK LEAD", "THE DISCOVERY", "UNSOLVED", "THE TWIST"]
            )
        elif style == "Stick Story":
            return VisualDirection(
                style="Stick Story",
                palette_top=(240, 140, 45),        # Golden survival sunset
                palette_horizon=(255, 215, 110),
                accent_color=(255, 90, 0),
                character_archetype="stick_figure",
                outfit="survival_gear",
                hair_style="bald",
                skin_tone=(255, 225, 190),
                voice=voice,
                bg_theme="wild_nature",
                scene_badges=["RULE 1: SURVIVE", "THE THREAT", "CRAFT & BUILD", "VITAL STATS", "ESCAPE PLAN", "SURVIVAL TIP"]
            )
        elif style == "Inside Out":
            return VisualDirection(
                style="Inside Out",
                palette_top=(10, 18, 32),
                palette_horizon=(18, 38, 65),
                accent_color=(70, 240, 180),       # High-voltage neon mint
                character_archetype="engineer",
                outfit="hoodie",
                hair_style="parted",
                skin_tone=(245, 215, 190),
                voice=voice,
                bg_theme="blueprint",
                scene_badges=["SCHEMATIC", "CROSS SECTION", "CORE MECHANISM", "PRESSURE FLOW", "ENERGY SURGE", "FULL SYSTEM"]
            )
        elif style == "Paper Atlas":
            return VisualDirection(
                style="Paper Atlas",
                palette_top=(225, 205, 170),       # Antique parchment
                palette_horizon=(245, 230, 205),
                accent_color=(180, 40, 40),        # Crimson wax seal
                character_archetype="commander",
                outfit="suit",
                hair_style="parted",
                skin_tone=(235, 210, 185),
                voice=voice,
                bg_theme="parchment_map",
                scene_badges=["YEAR IN REVIEW", "MARCH FORWARD", "TERRITORY CLASH", "THE SIEGE", "EMPIRE BORDERS", "LEGACY"]
            )
        else: # Tall Tale 3D
            # Dynamic cartoon character based on prompt topic
            outfit = "suit"
            badge_prefix = "LOOPHOLE"
            if "student" in lower_prompt or "school" in lower_prompt:
                outfit = "hoodie"
                badge_prefix = "STUDENT IQ"
            elif "doctor" in lower_prompt or "hospital" in lower_prompt:
                outfit = "lab_coat"
                badge_prefix = "MEDICAL"
            elif "cop" in lower_prompt or "police" in lower_prompt or "thief" in lower_prompt:
                outfit = "trench_coat"
                badge_prefix = "HEIST"

            return VisualDirection(
                style="Tall Tale 3D",
                palette_top=(55, 125, 220),        # Vibrant storybook sky
                palette_horizon=(200, 225, 250),
                accent_color=(255, 205, 50),       # Gold accent
                character_archetype="cartoon_hero",
                outfit=outfit,
                hair_style="messy",
                skin_tone=(255, 226, 194),
                voice=voice,
                bg_theme="office",
                scene_badges=[f"{badge_prefix} #1", "THE HIDDEN RULE", "THE EXECUTION", "THE PAYOFF", "TOTAL VICTORY", "THE SECRET"]
            )
