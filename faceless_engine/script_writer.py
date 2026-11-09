"""
Faceless Shorts Script Engine
Creates high-retention viral scripts adhering to the strict viral rules:
- No intro preamble (Punchline in the first 2 seconds)
- Pacing: Visual beats every 2.0 to 2.5 seconds
- Seamless loop: Closing sentence connects naturally into the opening hook
- Style adaptations: Tall Tale 3D, Deep Dive 3D, Inside Out, Stick Story, Night File 3D, Paper Atlas
"""
import os
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class SceneBeat:
    scene_index: int
    name: str
    narration: str
    camera_movement: str
    character_action: str
    environment_desc: str
    sfx_cue: str
    est_duration_sec: float

@dataclass
class ViralScript:
    title: str
    style: str
    target_duration: float
    full_narration: str
    scenes: List[SceneBeat]
    loop_transition: str

def generate_tall_tale_bank_script() -> ViralScript:
    """
    Generates the premiere 35-second Tall Tale 3D script about
    The man who bought an entire bank for $1.
    """
    scenes = [
        SceneBeat(
            scene_index=1,
            name="The $1 Hook",
            narration="In 1995, one man walked into Britain's oldest bank and bought the entire empire for exactly one dollar.",
            camera_movement="Fast punch-in from wide street to giant gold $1 coin",
            character_action="Aad Jacobs in tailored navy suit calmly holding a shiny $1 coin with a confident smirk",
            environment_desc="Miniature 3D street corner with classical London bank facade, black ink outlines, warm day lighting",
            sfx_cue="cash_register_ding",
            est_duration_sec=5.0
        ),
        SceneBeat(
            scene_index=2,
            name="The 200-Year Empire",
            narration="This was Barings Bank—founded in 1762, personal banker to the Queen, with billions in royal vaults.",
            camera_movement="Smooth upward crane shot past marble pillars",
            character_action="Royal guards in bearskin hats standing at attention beside bank vaults",
            environment_desc="Grand interior marble hall with golden crown emblem, high vaulted ceilings, stacked bullion",
            sfx_cue="triumph_fanfare",
            est_duration_sec=5.5
        ),
        SceneBeat(
            scene_index=3,
            name="The Rogue Bet",
            narration="Then, a 28-year-old rogue trader secretly placed massive bets from a hidden account labeled 88888.",
            camera_movement="Fast push-in to glowing computer terminal with Dutch tilt 4 degrees",
            character_action="Young trader with bean-head sweating bullets, typing furiously with wide panicked eyes",
            environment_desc="Dim trading pit with red neon ticker tape and papers flying everywhere",
            sfx_cue="computer_beep",
            est_duration_sec=5.5
        ),
        SceneBeat(
            scene_index=4,
            name="The Crash & Panic",
            narration="When the market collapsed, he lost 1.4 billion dollars, completely bankrupting the institution overnight!",
            camera_movement="Camera shake flip-kick with downward screen wipe",
            character_action="Trader grabbing his head in horror as a red stock graph plunges through the floor",
            environment_desc="Stock chart crashing down in dramatic 3D perspective, red alarm lights, ink smoke particles",
            sfx_cue="dramatic_thud",
            est_duration_sec=6.0
        ),
        SceneBeat(
            scene_index=5,
            name="The Historic Deal",
            narration="While panicked executives fled, Dutch investor Aad Jacobs calmly slammed down a single coin and bought the wreckage.",
            camera_movement="Low-angle gliding push toward the mahogany desk",
            character_action="Aad Jacobs sliding the $1 coin across the table while terrified bank directors stare in shock",
            environment_desc="Boardroom with large oak table, scattered contracts, mahogany wood and golden lamplight",
            sfx_cue="coin_slam",
            est_duration_sec=6.5
        ),
        SceneBeat(
            scene_index=6,
            name="The Empire & Loop",
            narration="He rebuilt it into a fifty-billion-dollar juggernaut, proving that if you want to buy an entire financial empire for pocket change, you just need someone else to break it first.",
            camera_movement="Rising aerial pullback to miniature city skyline with confetti burst",
            character_action="Aad Jacobs proudly standing atop a golden skyscraper surrounded by flying dollar bills",
            environment_desc="Vibrant sunny 3D miniature city with green parks, ink outlines, floating dollar signs, celebration glow",
            sfx_cue="whoosh_pop",
            est_duration_sec=7.5
        )
    ]
    
    full_narration = " ".join(s.narration for s in scenes)
    
    return ViralScript(
        title="The Man Who Bought a Bank for $1",
        style="Tall Tale 3D",
        target_duration=36.0,
        full_narration=full_narration,
        scenes=scenes,
        loop_transition="Connects back to 'In 1995, one man walked into Britain's oldest bank...'"
    )

def generate_script_with_groq(title: str, style: str = "Tall Tale 3D") -> Optional[ViralScript]:
    """
    Uses Groq API (Llama 3.3 70B Versatile) for ultra-fast (500+ tok/s) viral script generation.
    """
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        return None
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        
        prompt = f"""You are a master viral short-form director specializing in {style}.
Write a 6-scene viral short script (approx 35 seconds total, ~75 words total).
TOPIC: {title}
STYLE: {style}

STRICT VIRAL RETENTION RULES:
1. Scene 1 MUST be an explosive 2-second hook with NO introductory fluff (no 'Hey guys', no 'Today we look at'). Jump straight to the jaw-dropping punchline.
2. Fast visual pacing: Scene beats change every 4 to 6 seconds.
3. Scene 6 MUST naturally loop back into the first sentence of Scene 1.
4. Output valid JSON with this exact schema:
{{
  "title": "{title}",
  "style": "{style}",
  "target_duration": 35.0,
  "loop_transition": "...",
  "scenes": [
    {{
      "scene_index": 1,
      "name": "The Instant Hook",
      "narration": "...",
      "camera_movement": "Fast punch-in from wide street to hero object",
      "character_action": "...",
      "environment_desc": "...",
      "sfx_cue": "whoosh_pop",
      "est_duration_sec": 5.0
    }}
  ]
}}
Return ONLY JSON, no markdown formatting or extra text."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an elite viral short-form director. Output ONLY raw JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=1500
        )
        data = json.loads(response.choices[0].message.content)
        scenes = [
            SceneBeat(
                scene_index=s.get("scene_index", idx + 1),
                name=s.get("name", f"Scene {idx + 1}"),
                narration=s.get("narration", ""),
                camera_movement=s.get("camera_movement", "Smooth pan"),
                character_action=s.get("character_action", "Hero character acting"),
                environment_desc=s.get("environment_desc", "Miniature 3D world"),
                sfx_cue=s.get("sfx_cue", "whoosh_pop"),
                est_duration_sec=float(s.get("est_duration_sec", 5.5))
            )
            for idx, s in enumerate(data.get("scenes", []))
        ]
        full_narration = " ".join(s.narration for s in scenes)
        return ViralScript(
            title=data.get("title", title),
            style=style,
            target_duration=float(data.get("target_duration", 35.0)),
            full_narration=full_narration,
            scenes=scenes,
            loop_transition=data.get("loop_transition", "Loops back to opening")
        )
    except Exception as e:
        print(f"[ScriptWriter] Groq generation notice: {e}")
        return None

def generate_script_for_topic(title: str, hook: Optional[str] = None, style: str = "Tall Tale 3D") -> ViralScript:
    """
    Dynamically generates a 6-scene viral short script for ANY topic
    strictly following the 2-second hook, fast pacing, and seamless loop.
    """
    if "bank for $1" in title.lower() or "bank for 1" in title.lower():
        return generate_tall_tale_bank_script()

    # 1. Try Groq Llama 3.3 (Fastest 500+ tok/s)
    groq_script = generate_script_with_groq(title, style)
    if groq_script:
        return groq_script
        
    hook_line = hook or f"Did you know the crazy true story behind {title}?"
    
    scenes = [
        SceneBeat(
            scene_index=1,
            name="The Punchline Hook",
            narration=hook_line,
            camera_movement="Fast punch-in from wide establishing shot to character face",
            character_action="Hero character smirking with expressive eyes and confident posture",
            environment_desc="Miniature 3D architectural setting with crisp ink outlines and vibrant sky",
            sfx_cue="whoosh_pop",
            est_duration_sec=5.0
        ),
        SceneBeat(
            scene_index=2,
            name="The Setup & Scale",
            narration=f"It started when everyone thought this was completely impossible, but the rules had one tiny hidden flaw.",
            camera_movement="Smooth upward crane shot past miniature buildings",
            character_action="Character examining a glowing blueprint with curiosity",
            environment_desc="Detailed storybook environment with warm day lighting and horizon depth haze",
            sfx_cue="triumph_fanfare",
            est_duration_sec=5.5
        ),
        SceneBeat(
            scene_index=3,
            name="The Escalation",
            narration=f"Instead of giving up, a plan was put in motion that shocked everyone who was watching.",
            camera_movement="Dutch tilt push-in with dynamic kinetic drift",
            character_action="Character in fast walking cycle gesturing with determination",
            environment_desc="Fast-moving miniature city street with ink outlines",
            sfx_cue="computer_beep",
            est_duration_sec=5.5
        ),
        SceneBeat(
            scene_index=4,
            name="The Critical Turning Point",
            narration=f"Suddenly, the entire system began to shake as the true scale of what happened became impossible to hide!",
            camera_movement="Camera shake flip-kick with dramatic downward wipe",
            character_action="Characters with wide shocked eyes and open mouths in comedic disbelief",
            environment_desc="Dramatic high-contrast red alert atmosphere with flying paper particles",
            sfx_cue="dramatic_thud",
            est_duration_sec=6.0
        ),
        SceneBeat(
            scene_index=5,
            name="The Master Move",
            narration=f"While critics were scrambling for answers, the final move was executed with surgical precision.",
            camera_movement="Low-angle gliding push toward hero prop",
            character_action="Hero character slamming down the winning piece with a satisfied grin",
            environment_desc="Warm golden boardroom with rich wood textures and focused spotlight",
            sfx_cue="coin_slam",
            est_duration_sec=6.5
        ),
        SceneBeat(
            scene_index=6,
            name="The Payoff & Loop",
            narration=f"It turned into one of the most legendary stories in history, proving that when everyone else follows the crowd, the biggest winners find the one detail everyone overlooked.",
            camera_movement="Rising aerial pullback to miniature city skyline with celebration confetti",
            character_action="Hero character standing victorious with celebratory gesture",
            environment_desc="Bright celebratory 3D miniature city with floating golden sparkles",
            sfx_cue="cash_register_ding",
            est_duration_sec=7.5
        )
    ]
    
    full_narration = " ".join(s.narration for s in scenes)
    return ViralScript(
        title=title,
        style=style,
        target_duration=36.0,
        full_narration=full_narration,
        scenes=scenes,
        loop_transition=f"Seamlessly transitions back into: '{hook_line[:40]}...'"
    )
