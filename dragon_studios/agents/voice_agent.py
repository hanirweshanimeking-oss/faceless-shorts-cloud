"""
Dragon Studios India - Voice-over & Audio Agent
Powered by Microsoft Edge Neural Speech (Edge-TTS) with Self-Healing Fallback
100% Free, zero-cost, unlimited neural voice generation with dramatic pacing.
"""

import os
import sys
import time
import asyncio
import subprocess
import edge_tts
from typing import Dict, Any, Optional

DEFAULT_VOICE = "en-US-ChristopherNeural"  # Deep, dramatic, authoritative narrator

FFMPEG_BIN = "C:\\Users\\DESKTOP\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-9.0.2-full_build\\bin\\ffmpeg.exe"
if not os.path.exists(FFMPEG_BIN):
    FFMPEG_BIN = "ffmpeg"

def _generate_silent_audio_fallback(output_path: str, duration: float = 3.0) -> None:
    """Generates a clean, silent audio placeholder using FFmpeg if network is unreachable."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    cmd = [
        FFMPEG_BIN, "-y",
        "-f", "lavfi",
        "-i", f"anullsrc=channel_layout=stereo:sample_rate=44100",
        "-t", str(duration),
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)

async def synthesize_speech_async(
    text: str,
    output_path: str,
    voice: str = DEFAULT_VOICE,
    rate: str = "+0%",
    pitch: str = "-2Hz",
    volume: str = "+0%",
    max_retries: int = 3
) -> Dict[str, Any]:
    """
    Synthesizes speech to an MP3 file with automatic retry and resilient fallback.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            communicate = edge_tts.Communicate(
                text=text,
                voice=voice,
                rate=rate,
                pitch=pitch,
                volume=volume
            )
            await communicate.save(output_path)
            
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                file_size = os.path.getsize(output_path)
                return {
                    "status": "SUCCESS",
                    "output_path": output_path,
                    "voice": voice,
                    "text": text,
                    "file_size_bytes": file_size,
                    "attempt": attempt
                }
        except Exception as e:
            last_error = e
            time.sleep(1.0 * attempt)
            
    # Resilient Self-Healing Fallback: generate placeholder audio if network drops
    try:
        # Approximate duration based on word count (~150 words per minute)
        word_count = len(text.split())
        est_duration = max(2.5, min(10.0, (word_count / 150.0) * 60.0))
        _generate_silent_audio_fallback(output_path, duration=est_duration)
        return {
            "status": "FALLBACK_AUDIO",
            "output_path": output_path,
            "voice": voice,
            "text": text,
            "file_size_bytes": os.path.getsize(output_path) if os.path.exists(output_path) else 0,
            "warning": f"Network dropped ({last_error}); generated resilient audio placeholder."
        }
    except Exception as fallback_err:
        return {
            "status": "FAILED",
            "output_path": output_path,
            "error": str(last_error or fallback_err)
        }

def synthesize_speech(
    text: str,
    output_path: str,
    voice: str = DEFAULT_VOICE,
    rate: str = "+0%",
    pitch: str = "-2Hz"
) -> Dict[str, Any]:
    """Synchronous wrapper for synthesize_speech_async."""
    return asyncio.run(synthesize_speech_async(
        text=text,
        output_path=output_path,
        voice=voice,
        rate=rate,
        pitch=pitch
    ))

async def list_available_voices(filter_lang: str = "en") -> list:
    """Lists available high-quality neural voices filtered by language prefix."""
    voices = await edge_tts.list_voices()
    return [v for v in voices if v["Locale"].startswith(filter_lang)]
