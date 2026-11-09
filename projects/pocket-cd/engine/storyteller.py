"""Pocket Creator Director - Storyteller & Voice Engine.

Narration & VSL script writing with ElevenLabs V4 syntax and Edge-TTS audio synthesis.
"""

import asyncio
import json
import os
import re
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

import edge_tts

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SCRIPTS_FILE = DATA_DIR / "scripts.json"
STATIC_ASSETS_DIR = Path(__file__).resolve().parent.parent / "static" / "assets"

# Available neural voices for Edge-TTS fallback
AVAILABLE_VOICES = {
    "carl": "en-US-ChristopherNeural",  # Warm, conversational, authoritative
    "christopher": "en-US-ChristopherNeural",
    "ryan": "en-GB-RyanNeural",          # Deep British narrative
    "brian": "en-US-BrianNeural",        # Dynamic commercial
    "emma": "en-US-EmmaNeural",          # Crisp clear presenter
    "jenny": "en-US-JennyNeural",        # Fast viral short
    "guy": "en-US-GuyNeural"
}

# ElevenLabs V4 Voice Presets
ELEVENLABS_PRESETS = {
    "carl_voice": {
        "name": "Nate - Warm & Conversational (Carl's Voice)",
        "model": "eleven_turbo_v2_5 / v4",
        "voice_id": "CYw3kZ02Hs0563khs1Fj",
        "stability": 0.55,
        "similarity_boost": 0.75,
        "style": 0.35,
        "use_speaker_boost": True,
        "tone": "Warm, confident, conversational, peer-to-peer"
    },
    "documentary_investor": {
        "name": "Christopher - Deep & Authoritative",
        "model": "eleven_multilingual_v2 / v4",
        "voice_id": "onwK4e9ZLuTAKqWW03F9",
        "stability": 0.70,
        "similarity_boost": 0.80,
        "style": 0.45,
        "use_speaker_boost": True,
        "tone": "Suspenseful, high retention, documentary investor"
    },
    "viral_short_punch": {
        "name": "Brian - High Energy Punch",
        "model": "eleven_turbo_v2_5 / v4",
        "voice_id": "nPczCjzI2devNBz1zQrb",
        "stability": 0.45,
        "similarity_boost": 0.85,
        "style": 0.60,
        "use_speaker_boost": True,
        "tone": "Punchy, fast-paced, retention hook focused"
    }
}


class StorytellerEngine:
    """Manages ElevenLabs V4 scripting and Edge-TTS audio generation."""

    def __init__(self, scripts_path: Optional[Path] = None):
        self.scripts_path = scripts_path or SCRIPTS_FILE
        STATIC_ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    def load_scripts(self) -> List[Dict[str, Any]]:
        """Load scripts from disk."""
        if not self.scripts_path.exists():
            return []
        try:
            with open(self.scripts_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save_script(self, script_data: Dict[str, Any]) -> None:
        """Save or update script in scripts.json."""
        scripts = self.load_scripts()
        idx = next((i for i, s in enumerate(scripts) if s.get("id") == script_data.get("id")), None)
        if idx is not None:
            scripts[idx] = script_data
        else:
            scripts.append(script_data)
        with open(self.scripts_path, "w", encoding="utf-8") as f:
            json.dump(scripts, f, indent=2)

    def generate_vsl_script(
        self,
        topic: str,
        style: str = "carl_voice",
        target_duration_sec: int = 25
    ) -> Dict[str, Any]:
        """Generate structured VSL script formatted with ElevenLabs V4 syntax."""
        preset = ELEVENLABS_PRESETS.get(style, ELEVENLABS_PRESETS["carl_voice"])
        script_id = f"script_{uuid.uuid4().hex[:8]}"

        # Craft structured ElevenLabs V4 script with pauses and emotional bracket tags
        if "carl" in style or "launch" in topic.lower():
            title = f"Pocket Creative Director - {topic.title()}"
            content = (
                f"[emotion: relaxed, warm] Carl, relaxed hi... what is {topic}?\n\n"
                f"Okay, so you recorded a video. The recording took ten minutes. "
                f"[pause: 0.3s]\n"
                f"And now everything after it is waiting for you: the cut, the graphics, the sound, the captions. "
                f"[emphasis: high] That part eats the whole day.\n\n"
                f"[emotion: confident] Pocket Creative Director is the team that does that part. "
                f"It lives in a folder on your computer. It writes directly in the editing apps you already use: "
                f"DaVinci Resolve, After Effects, and Premiere.\n\n"
                f"[pause: 0.4s]\n"
                f"You record on your camera. Then it edits every single thing: the cut, the graphics, "
                f"the color grade, the sound, the captions. "
                f"Right there in your actual timeline, zero upload, zero web app, and zero manual work."
            )
        elif "ackman" in topic.lower() or "investor" in style or "finance" in topic.lower():
            title = f"Investor Bio Breakdown - {topic.title()}"
            content = (
                f"[emotion: suspenseful, intense] {topic} might be the only case where an entire career "
                f"came down to a single high-stakes bet against corporate titans.\n\n"
                f"[pause: 0.4s]\n"
                f"Not even an army of short sellers could withstand what happened next. "
                f"[whisper: subtle] Here is the untold playbook of how he engineered a billion-dollar turnaround.\n\n"
                f"[pause: 0.3s]\n"
                f"[emotion: authoritative] Every single move was calculated. Every public interview was a weapon. "
                f"And the results rewrote Wall Street history forever."
            )
        else:
            title = f"Viral Masterclass: {topic.title()}"
            content = (
                f"[emotion: energetic] Most creators spend eighty percent of their day editing the same three things.\n\n"
                f"[pause: 0.3s]\n"
                f"The hook cut, the kinetic typography, and the audio ducking. "
                f"[emphasis: strong] What if you never had to touch a timeline manually again?\n\n"
                f"[pause: 0.4s]\n"
                f"[emotion: punchy] This is Pocket Creative Director. "
                f"Decompile any viral video DNA, direct edits with simple prompts, "
                f"and export directly to After Effects and DaVinci Resolve."
            )

        script_obj = {
            "id": script_id,
            "title": title,
            "voice": preset["name"],
            "model": "ElevenLabs v4",
            "voice_preset": style,
            "stability": f"Dynamic ({preset['stability']})",
            "similarity": str(preset["similarity_boost"]),
            "tone": preset["tone"],
            "created_at": "2026-11-09",
            "status": "ready",
            "target_duration_sec": target_duration_sec,
            "content": content,
            "elevenlabs_settings": {
                "voice_id": preset["voice_id"],
                "stability": preset["stability"],
                "similarity_boost": preset["similarity_boost"],
                "style": preset["style"],
                "use_speaker_boost": preset["use_speaker_boost"]
            }
        }

        self.save_script(script_obj)
        return script_obj

    def clean_elevenlabs_markup_for_tts(self, text: str) -> str:
        """Strip ElevenLabs bracket tags to create clean spoken speech for Edge-TTS."""
        # Replace pauses like [pause: 0.3s] with comma / ellipses for natural cadence
        cleaned = re.sub(r"\[pause:\s*[\d\.]+s?\]", "...", text, flags=re.IGNORECASE)
        # Remove emotion/bracket tags like [emotion: warm], [whisper], [emphasis: high]
        cleaned = re.sub(r"\[[^\]]+\]", "", cleaned)
        # Normalize whitespace
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned

    async def synthesize_speech_async(
        self,
        text: str,
        voice_key: str = "carl",
        output_filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """Synthesize audio using Edge-TTS asynchronously."""
        voice = AVAILABLE_VOICES.get(voice_key.lower(), AVAILABLE_VOICES["carl"])
        cleaned_text = self.clean_elevenlabs_markup_for_tts(text)

        if not output_filename:
            output_filename = f"narration_{uuid.uuid4().hex[:8]}.mp3"

        out_path = STATIC_ASSETS_DIR / output_filename
        communicate = edge_tts.Communicate(cleaned_text, voice)
        await communicate.save(str(out_path))

        # Estimate duration: average ~140 words per minute -> 2.33 words/sec
        words = len(cleaned_text.split())
        estimated_duration = max(2.0, round(words / 2.33, 1))

        return {
            "success": True,
            "audio_filename": output_filename,
            "audio_path": f"/static/assets/{output_filename}",
            "absolute_path": str(out_path),
            "voice": voice,
            "word_count": words,
            "duration_sec": estimated_duration,
            "cleaned_text": cleaned_text
        }

    def synthesize_speech(
        self,
        text: str,
        voice_key: str = "carl",
        output_filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """Synchronous wrapper for synthesize_speech_async."""
        return asyncio.run(self.synthesize_speech_async(text, voice_key, output_filename))


storyteller = StorytellerEngine()
