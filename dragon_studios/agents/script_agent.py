"""
Dragon Studios India - Scriptwriting & Storyboard Agent
Produces retention-optimized, high-stakes anime scripts and scene-by-scene blueprints
specifically calibrated for @dragon.studios.india across Dark Psychology, AI Tools, and Manga.
"""

import uuid
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class SceneBlueprint(BaseModel):
    scene_order: int
    duration_seconds: float
    dialogue: str
    visual_prompt: str
    camera_movement: str
    sound_cue: str
    subtitle_text: str

class VideoProductionPlan(BaseModel):
    project_id: str
    title: str
    pillar: str  # 'DARK_PSYCHOLOGY', 'ORIGINAL_MANGA', 'AI_TOOLS', 'CINEMATIC_EDIT'
    hook: str
    total_duration_seconds: float
    aspect_ratio: str = "9:16"
    caption: str
    hashtags: str
    pinned_comment: str
    scenes: List[SceneBlueprint]

def generate_dark_psychology_script(
    title: str = "HOW TO DESTROY AN ENEMY'S EGO",
    topic_focus: str = "Total apathy and silent power"
) -> VideoProductionPlan:
    """
    Generates a structured, high-retention dark anime psychology script.
    Optimized for Instagram Reels & YouTube Shorts saves/shares.
    """
    proj_id = f"proj_{uuid.uuid4().hex[:8]}"
    
    scenes = [
        SceneBlueprint(
            scene_order=1,
            duration_seconds=3.5,
            dialogue="The ego is the most fragile armor. Strike it with absolute indifference.",
            visual_prompt="Dark anime male protagonist, piercing glowing violet eyes, obsidian cloak, looking downward with utter calm, ominous purple aura, cinematic dramatic lighting, 8k anime artstyle, hyper-detailed, masterpiece.",
            camera_movement="Slow zoom into the glowing eyes with subtle glitch shake",
            sound_cue="Deep sub-bass drop followed by eerie clock tick",
            subtitle_text="RULE #1: ZERO REACTION"
        ),
        SceneBlueprint(
            scene_order=2,
            duration_seconds=5.0,
            dialogue="Arguing gives them importance. Total apathy makes them feel invisible.",
            visual_prompt="Opponent screaming in anger and swinging blade, anime protagonist effortlessly turns away without looking, motion blur on blade, sparks flying in background, dark medieval corridor.",
            camera_movement="Smooth lateral pan past the ignored attacker",
            sound_cue="Muffled blade woosh cut into dead silence",
            subtitle_text="Arguing validates them. Apathy erases them."
        ),
        SceneBlueprint(
            scene_order=3,
            duration_seconds=6.0,
            dialogue="People who boast about their power are trembling in their own shadows. Let them speak into the void.",
            visual_prompt="Shadowy throne room, silhouetted anime figures whispering, shadows stretching menacingly across stone floor, lone figure standing motionless in beam of moonlight.",
            camera_movement="High-angle crane shot descending into silhouette",
            sound_cue="Low atmospheric cello drone swelling slowly",
            subtitle_text="Loud words hide trembling hands."
        ),
        SceneBlueprint(
            scene_order=4,
            duration_seconds=6.5,
            dialogue="They want to drag you into the mud. Operate at a frequency they cannot comprehend.",
            visual_prompt="Anime protagonist stepping over cracked marble, dark dragon aura manifesting behind him, lightning crackling subtly in atmospheric rain, wind blowing dark hair.",
            camera_movement="Low-angle heroic tracking shot forward",
            sound_cue="Thunderclap in distance with metallic sword scrape",
            subtitle_text="Operate where they cannot touch you."
        ),
        SceneBlueprint(
            scene_order=5,
            duration_seconds=5.0,
            dialogue="Elevate your standards. Silence is your deadliest weapon.",
            visual_prompt="Dragon Studios dark dragon sigil glowing with purple fire, smoke curling, cinematic endcard, stylized anime typography.",
            camera_movement="Pull back to reveal glowing emblem",
            sound_cue="Cinematic orchestral impact hitting pitch-black silence",
            subtitle_text="SAVE THIS REMINDER. FOLLOW FOR MORE."
        )
    ]
    
    caption = (
        f"{title}. ♟️\n\n"
        f"\"The ego is the most fragile armor. Strike it with absolute indifference.\"\n\n"
        f"1. ZERO REACTION — Arguing gives them importance. Total apathy makes them feel invisible.\n"
        f"2. EXPOSE THE INSECURITY — People who boast about their power are trembling in their shadows.\n"
        f"3. ELEVATE YOUR STANDARDS — They want to drag you into the mud. Operate at a frequency they cannot reach.\n\n"
        f"Save this for when you need cold composure. Follow @dragon.studios.india for daily anime psychology & original stories.\n\n"
        f"#DragonStudiosIndia #DarkPsychology #AnimeMindset #Stoicism #AnimeEdits #ReelsIndia #ExplorePage"
    )
    
    hashtags = "#DragonStudiosIndia #DarkPsychology #AnimeMindset #Stoicism #AnimeEdits #ReelsIndia #ExplorePage"
    pinned_comment = "Which rule hits hardest for you? Drop a ♟️ below."
    total_duration = sum(s.duration_seconds for s in scenes)
    
    return VideoProductionPlan(
        project_id=proj_id,
        title=title,
        pillar="DARK_PSYCHOLOGY",
        hook="The ego is the most fragile armor. Strike it with absolute indifference.",
        total_duration_seconds=total_duration,
        aspect_ratio="9:16",
        caption=caption,
        hashtags=hashtags,
        pinned_comment=pinned_comment,
        scenes=scenes
    )

def generate_ai_tools_script(
    title: str = "NEVER PAY FOR VIDEO EDITING AGAIN",
    topic: str = "AI Video Generation Pipeline"
) -> VideoProductionPlan:
    """
    Generates a viral tech / AI tools script implementing the Triple Hook formula.
    """
    proj_id = f"proj_{uuid.uuid4().hex[:8]}"
    
    scenes = [
        SceneBlueprint(
            scene_order=1,
            duration_seconds=3.5,
            dialogue=f"Stop paying monthly subscriptions for {topic.lower()}. Someone just open-sourced the entire pipeline for free.",
            visual_prompt="Futuristic holographic code terminal running in dark studio, high-speed code matrix glowing electric cyan and purple, ultra-sharp 4k UI visuals.",
            camera_movement="Fast whip zoom into the terminal screen",
            sound_cue="Heavy digital riser into bass drop",
            subtitle_text="STOP PAYING SUBSCRIPTIONS"
        ),
        SceneBlueprint(
            scene_order=2,
            duration_seconds=5.0,
            dialogue="It handles your scripting, generates studio voiceovers, and auto-edits full 9:16 reels in under 60 seconds.",
            visual_prompt="Split-screen showcasing automated video timeline assembling itself with timeline markers snapping in place effortlessly.",
            camera_movement="Smooth lateral slide left to right",
            sound_cue="Keyboard mechanical clicks and digital chime",
            subtitle_text="Full 9:16 Reels in 60 Seconds"
        ),
        SceneBlueprint(
            scene_order=3,
            duration_seconds=5.5,
            dialogue="No browser clicking, no manual keyframing. Just a single terminal command that runs completely on your own PC.",
            visual_prompt="Modern minimalist developer workspace, glowing neon backlight, terminal executing with green checkmarks.",
            camera_movement="Subtle slow push-in",
            sound_cue="Subtle synthesizer pulse",
            subtitle_text="100% Local. Zero API Costs."
        ),
        SceneBlueprint(
            scene_order=4,
            duration_seconds=4.0,
            dialogue="Comment 'STUDIO' below and I will send you the complete GitHub setup guide and code right to your DMs.",
            visual_prompt="Dragon Studios India branded call-to-action card with bookmark icon bouncing gently, purple gradient background.",
            camera_movement="Static hold with pulsating button",
            sound_cue="Notification ping followed by energetic whoosh",
            subtitle_text="COMMENT 'STUDIO' FOR THE REPO"
        )
    ]
    
    caption = (
        f"{title} ⚡\n\n"
        f"You don't need expensive monthly tools to generate high-retention video content anymore.\n\n"
        f"✅ 100% Free & Open-Source\n"
        f"✅ Auto-Scripting + Neural Voice\n"
        f"✅ Kinetic Subtitles & 9:16 Vertical Video\n\n"
        f"Comment 'STUDIO' to get the full GitHub repo and setup tutorial!\n\n"
        f"#DragonStudiosIndia #AITools #VideoEditing #Coding #Automation #TechReels #ExplorePage"
    )
    
    return VideoProductionPlan(
        project_id=proj_id,
        title=title,
        pillar="AI_TOOLS",
        hook=f"Stop paying monthly subscriptions for {topic.lower()}.",
        total_duration_seconds=sum(s.duration_seconds for s in scenes),
        aspect_ratio="9:16",
        caption=caption,
        hashtags="#DragonStudiosIndia #AITools #VideoEditing #Coding #Automation #TechReels #ExplorePage",
        pinned_comment="Comment 'STUDIO' to get the free GitHub link in your DMs! 🚀",
        scenes=scenes
    )

def generate_chitran_manga_script(chapter_number: int = 1) -> VideoProductionPlan:
    """
    Generates a dark anime original manga teaser script (Chitran: The Dark Flame).
    """
    proj_id = f"proj_{uuid.uuid4().hex[:8]}"
    
    scenes = [
        SceneBlueprint(
            scene_order=1,
            duration_seconds=4.0,
            dialogue="In the ruins of the Obsidian City, the seal has fractured. He has opened his eyes.",
            visual_prompt="Crumbling ancient obsidian monoliths, dark violet clouds rolling over apocalyptic cityscape, lightning illuminating a kneeling figure with long raven hair and black blindfold.",
            camera_movement="Fast tracking shot flying low between monoliths stopping right in front of character",
            sound_cue="Low cinematic horn boom vibrating through stone",
            subtitle_text="CHITRAN: CHAPTER ONE - THE AWAKENING"
        ),
        SceneBlueprint(
            scene_order=2,
            duration_seconds=5.5,
            dialogue="They called his clan demons. But demons don't bleed pure celestial fire.",
            visual_prompt="Character untying the blindfold with one hand, black cloth drifting in slow motion into wind, single eye opening revealing a burning indigo flame pupil, shockwave rippling through dust.",
            camera_movement="Macro extreme close-up on eye with pupil igniting",
            sound_cue="Sound of fabric tearing, then sudden vacuum of silence before flame roar",
            subtitle_text="Demons don't bleed celestial fire."
        ),
        SceneBlueprint(
            scene_order=3,
            duration_seconds=6.0,
            dialogue="Every blade that stood against him shattered into dust before touching his skin.",
            visual_prompt="Dozens of elite shadow warriors leaping forward with drawn katana blades, their steel blades vaporizing into glowing purple embers inches from Chitran's silhouette.",
            camera_movement="360-degree bullet-time orbit around the central figure",
            sound_cue="High-pitched metallic shattering glass crescendo",
            subtitle_text="Every blade shattered into dust."
        ),
        SceneBlueprint(
            scene_order=4,
            duration_seconds=5.5,
            dialogue="He looked at the blackened horizon and whispered: The hunt begins today.",
            visual_prompt="Chitran walking forward in slow motion, twin black dragon daggers glowing at his hips, embers swirling around his dark trench coat, rain sizzling against his skin.",
            camera_movement="Slow crane shot rising upward as character walks into distance",
            sound_cue="Heavy heartbeat thud thud with dark anime guitar riff rising",
            subtitle_text="The hunt begins today."
        ),
        SceneBlueprint(
            scene_order=5,
            duration_seconds=4.0,
            dialogue="Chitran. Chapter 1 drops this week. Read exclusively on Dragon Studios India.",
            visual_prompt="Dramatic manga cover art reveal, high-contrast black and purple styling with Japanese kanji calligraphy, official Dragon Studios India seal.",
            camera_movement="Snap zoom back into centered logo with smoke fade",
            sound_cue="Anvil hit resonance fading into dark ambient drone",
            subtitle_text="READ CHAPTER 1 EXCLUSIVELY ON DRAGON STUDIOS"
        )
    ]
    
    caption = (
        f"CHITRAN: THE DARK FLAME — CHAPTER {chapter_number} TEASER. ⚔️🔥\n\n"
        f"\"They called his clan demons. But demons don't bleed pure celestial fire.\"\n\n"
        f"The original manga universe created by Dragon Studios India is here. "
        f"Drop a 🔥 if you want the first 20 pages dropped early!\n\n"
        f"#DragonStudiosIndia #ChitranManga #OriginalManga #AnimeIndia #MangaArt #AnimeCommunity #Webtoon"
    )
    
    return VideoProductionPlan(
        project_id=proj_id,
        title=f"CHITRAN: CHAPTER {chapter_number} - THE AWAKENING",
        pillar="ORIGINAL_MANGA",
        hook="In the ruins of the Obsidian City, the seal has fractured.",
        total_duration_seconds=sum(s.duration_seconds for s in scenes),
        aspect_ratio="9:16",
        caption=caption,
        hashtags="#DragonStudiosIndia #ChitranManga #OriginalManga #AnimeIndia #MangaArt",
        pinned_comment="Should we release Chapter 1 as a motion comic? Let us know below! 👇",
        scenes=scenes
    )

def generate_conversational_podcast_script(
    title: str = "IS YOUR FIRST 1 CRORE WORTHLESS?",
    topic: str = "The First Crore Wealth Trap"
) -> VideoProductionPlan:
    """
    Generates a viral conversational interrogation script (Raj Shamani / Figuring Out format).
    Uses high-contrast dual perspectives: Questioning Host vs. Insightful Guest.
    """
    proj_id = f"proj_{uuid.uuid4().hex[:8]}"
    
    scenes = [
        SceneBlueprint(
            scene_order=1,
            duration_seconds=3.5,
            dialogue="Wait. You are telling me making your first one crore does not change your life at all?",
            visual_prompt="Split screen podcast interview, host leaning in aggressively with microphone, intense eye contact, high-contrast studio lighting, warm bokeh background.",
            camera_movement="Fast whip zoom into interviewer",
            sound_cue="Sub-bass impact cut sharply into dead silence",
            subtitle_text="WAIT... IS 1 CRORE WORTHLESS?"
        ),
        SceneBlueprint(
            scene_order=2,
            duration_seconds=5.0,
            dialogue="Zero. Look at the math. In Mumbai or Delhi, one crore gets you half an apartment and five years of inflation.",
            visual_prompt="Guest smiling wryly, leaning back on studio couch, gesturing with authority, shallow depth of field, warm cinema tone.",
            camera_movement="Slow lateral pan across guest",
            sound_cue="Low atmospheric synth drone begins",
            subtitle_text="IT BUYS ASSETS, NOT FREEDOM."
        ),
        SceneBlueprint(
            scene_order=3,
            duration_seconds=5.5,
            dialogue="The first crore is not wealth. The first crore is simply proof that you figured out how to create value from thin air.",
            visual_prompt="Kinetic infographic of compounding asset curve ascending exponentially, golden glow, clean dark interface.",
            camera_movement="Smooth tracking shot upward",
            sound_cue="Mechanical click sound effect with bass swell",
            subtitle_text="THE FIRST CRORE IS PROOF OF SKILL."
        ),
        SceneBlueprint(
            scene_order=4,
            duration_seconds=5.5,
            dialogue="Most people stop when they reach it because they buy liabilities. The top one percent immediately reinvest it into asymmetric bets.",
            visual_prompt="Split screen high-tension dialogue shot, alternating between guest and host, dramatic rim lighting, moody podcast studio.",
            camera_movement="Creeping slow push-in",
            sound_cue="Tension riser pulse",
            subtitle_text="REINVEST OR GET CRUSHED BY INFLATION."
        ),
        SceneBlueprint(
            scene_order=5,
            duration_seconds=4.0,
            dialogue="Would you reinvest it, or buy your dream car? Drop your answer in the comments below.",
            visual_prompt="Interviewer looking directly into lens, Dragon Studios India verified badge glowing, bookmark icon pulsating.",
            camera_movement="Slow pull-back to center",
            sound_cue="Notification chime into deep outro rumble",
            subtitle_text="WHAT WOULD YOU DO? DROP A COMMENT."
        )
    ]
    
    caption = (
        f"{title} 🎙️💰\n\n"
        f"\"The first crore is not wealth. The first crore is simply proof that you figured out how to create value from thin air.\"\n\n"
        f"1. Zero Reaction to Fluff — Look at the raw math after inflation and living expenses.\n"
        f"2. Capability > Currency — The skill to earn it again is the actual asset.\n"
        f"3. Asymmetric Compounding — Why the 1% never upgrade lifestyle at the first milestone.\n\n"
        f"Would you reinvest it or buy your dream car? Let us know in the comments below! 👇\n\n"
        f"#FiguringOut #RajShamani #MoneyMindset #StartupIndia #FinancialFreedom #ReelsIndia #WealthBuilding"
    )
    
    return VideoProductionPlan(
        project_id=proj_id,
        title=title,
        pillar="CONVERSATIONAL_PODCAST",
        hook="Wait. You are telling me making your first one crore does not change your life at all?",
        total_duration_seconds=sum(s.duration_seconds for s in scenes),
        aspect_ratio="9:16",
        caption=caption,
        hashtags="#FiguringOut #RajShamani #MoneyMindset #StartupIndia #FinancialFreedom",
        pinned_comment="Drop 'WEALTH' in the comments if you want our breakdown of asymmetric bets! ♟️",
        scenes=scenes
    )
