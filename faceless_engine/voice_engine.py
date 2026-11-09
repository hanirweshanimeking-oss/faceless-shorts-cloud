"""
Faceless Shorts Voice Engine
Supports 100% free local Kokoro Neural TTS with Edge-TTS resilient fallback.
Zero API costs, running locally on CPU.
"""
import os
import sys
import asyncio
import soundfile as sf
from typing import Optional, Dict, Any

from faceless_engine.config import (
    KOKORO_MODEL_PATH,
    KOKORO_VOICES_PATH,
    FFMPEG_BIN
)

# Kokoro voice mappings
KOKORO_VOICE_MAP = {
    "adam": "am_adam",
    "michael": "am_michael",
    "bella": "af_bella",
    "nicole": "af_nicole",
    "echo": "am_echo",
    "fenrir": "am_fenrir",
    "liam": "am_liam",
    "onyx": "am_onyx",
    "puck": "am_puck"
}

_kokoro_instance = None

def get_kokoro_model():
    global _kokoro_instance
    if _kokoro_instance is None:
        if os.path.exists(KOKORO_MODEL_PATH) and os.path.exists(KOKORO_VOICES_PATH):
            import kokoro_onnx
            _kokoro_instance = kokoro_onnx.Kokoro(KOKORO_MODEL_PATH, KOKORO_VOICES_PATH)
    return _kokoro_instance

def synthesize_kokoro(
    text: str,
    output_path: str,
    voice: str = "am_adam",
    speed: float = 1.05,
    lang: str = "en-us"
) -> bool:
    """Synthesizes speech using local Kokoro ONNX model."""
    try:
        kokoro = get_kokoro_model()
        if kokoro is None:
            return False
            
        target_voice = KOKORO_VOICE_MAP.get(voice.lower(), voice)
        samples, sample_rate = kokoro.create(
            text=text,
            voice=target_voice,
            speed=speed,
            lang=lang
        )
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        sf.write(output_path, samples, sample_rate)
        return os.path.exists(output_path) and os.path.getsize(output_path) > 1000
    except Exception as e:
        print(f"[VoiceEngine] Kokoro generation notice: {e}")
        return False

async def synthesize_edgetts_async(
    text: str,
    output_path: str,
    voice: str = "en-US-ChristopherNeural",
    rate: str = "+4%"
) -> bool:
    """Synthesizes speech using Microsoft Edge Neural TTS."""
    try:
        import edge_tts
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        comm = edge_tts.Communicate(text=text, voice=voice, rate=rate)
        await comm.save(output_path)
        return os.path.exists(output_path) and os.path.getsize(output_path) > 1000
    except Exception as e:
        print(f"[VoiceEngine] Edge-TTS error: {e}")
        return False

# Mapping Kokoro voice aliases to Microsoft Edge Neural voices for high-fidelity fallback
EDGE_VOICE_MAP = {
    "am_adam": "en-US-ChristopherNeural",
    "am_michael": "en-US-GuyNeural",
    "am_echo": "en-US-EricNeural",
    "af_bella": "en-US-JennyNeural",
    "af_nicole": "en-US-AriaNeural",
    "am_fenrir": "en-GB-RyanNeural",
    "am_liam": "en-GB-ThomasNeural",
    "am_onyx": "en-US-RogerNeural",
    "af_sarah": "en-GB-SoniaNeural",
    "adam": "en-US-ChristopherNeural",
    "michael": "en-US-GuyNeural",
    "echo": "en-US-EricNeural",
    "bella": "en-US-JennyNeural",
    "nicole": "en-US-AriaNeural",
    "fenrir": "en-GB-RyanNeural",
    "liam": "en-GB-ThomasNeural",
    "onyx": "en-US-RogerNeural",
    "eric": "en-US-EricNeural",
    "guy": "en-US-GuyNeural",
    "ryan": "en-GB-RyanNeural",
    "jenny": "en-US-JennyNeural"
}

def resolve_edge_voice(voice_preference: str) -> str:
    """Resolves a requested voice identifier to an active Edge-TTS neural voice."""
    if not voice_preference:
        return "en-US-ChristopherNeural"
    if "-" in voice_preference and voice_preference.endswith("Neural"):
        return voice_preference
    return EDGE_VOICE_MAP.get(voice_preference.lower(), "en-US-ChristopherNeural")

def generate_voiceover(
    text: str,
    output_path: str,
    voice_preference: str = "en-US-ChristopherNeural",
    speed: float = 1.05
) -> str:
    """
    Main voice generator:
    1. Attempts local Kokoro ONNX model first ($0, zero internet required).
    2. Falls back to Edge-TTS neural narration with the resolved distinct voice.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # 1. Try local Kokoro
    success = synthesize_kokoro(text, output_path, voice=voice_preference, speed=speed)
    if success:
        print(f"[VoiceEngine] Successfully generated voice with Kokoro ONNX -> {output_path}")
        return output_path
        
    # 2. Try Edge-TTS fallback with chosen persona voice
    resolved_voice = resolve_edge_voice(voice_preference)
    print(f"[VoiceEngine] Synthesizing neural narration with Edge-TTS voice: '{resolved_voice}'...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    edge_success = loop.run_until_complete(
        synthesize_edgetts_async(text, output_path, voice=resolved_voice)
    )
    loop.close()
    
    if edge_success:
        print(f"[VoiceEngine] Successfully generated voice with Edge-TTS ({resolved_voice}) -> {output_path}")
        return output_path
        
    raise RuntimeError(f"Failed to generate voiceover for text: {text[:50]}...")
