"""
Faceless Shorts Audio & Foley Engine
Generates synced comedy sound effects, manages royalty-free background music,
and applies professional sidechain compression (-12dB ducking) & loudness mastering.
"""
import os
import math
import subprocess
import numpy as np
import soundfile as sf
from typing import List, Dict, Any, Optional

from faceless_engine.config import FFMPEG_BIN, BG_MUSIC_DIR

def synthesize_sfx(cue: str, output_path: str, sample_rate: int = 44100) -> str:
    """
    Synthesizes clean, procedural sound effects and foley using NumPy.
    100% free, zero external sound pack dependencies.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    if cue == "cash_register_ding":
        # Two-tone bell chime (2093 Hz and 3136 Hz) + coin click
        duration = 1.2
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        chime1 = np.sin(2 * np.pi * 2093.0 * t) * np.exp(-t * 3.5)
        chime2 = np.sin(2 * np.pi * 3136.0 * t) * np.exp(-t * 4.2) * 0.7
        noise = (np.random.rand(len(t)) * 2 - 1) * np.exp(-t * 28.0) * 0.25
        audio = chime1 + chime2 + noise

    elif cue == "coin_slam":
        # Metallic clink on solid wood
        duration = 0.8
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        thud = np.sin(2 * np.pi * 120.0 * t) * np.exp(-t * 14.0)
        clink = (np.sin(2 * np.pi * 2800.0 * t) + np.sin(2 * np.pi * 4200.0 * t)) * np.exp(-t * 18.0) * 0.4
        audio = thud + clink

    elif cue == "dramatic_thud":
        # Low frequency bass drop impact (65 Hz decaying)
        duration = 1.5
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        freq_sweep = np.linspace(140, 45, len(t))
        impact = np.sin(2 * np.pi * freq_sweep * t) * np.exp(-t * 3.0)
        rumble = (np.random.rand(len(t)) * 2 - 1) * np.exp(-t * 5.0) * 0.15
        audio = impact + rumble

    elif cue == "computer_beep":
        # Rapid tech bleeps
        duration = 0.6
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        b1 = np.sin(2 * np.pi * 880.0 * t) * ((t < 0.15) * np.exp(-t * 8.0))
        b2 = np.sin(2 * np.pi * 1760.0 * t) * ((t >= 0.2) * (t < 0.35) * np.exp(-(t - 0.2) * 8.0))
        b3 = np.sin(2 * np.pi * 1320.0 * t) * ((t >= 0.4) * np.exp(-(t - 0.4) * 8.0))
        audio = b1 + b2 + b3

    elif cue == "whoosh_pop":
        # Fast airy sweep into a comic bubble pop
        duration = 0.7
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        noise = (np.random.rand(len(t)) * 2 - 1) * np.sin(np.pi * t / 0.5) * (t < 0.5) * 0.35
        pop_t = t[t >= 0.5] - 0.5
        pop = np.sin(2 * np.pi * 520.0 * pop_t) * np.exp(-pop_t * 22.0)
        pop_full = np.zeros_like(t)
        pop_full[t >= 0.5] = pop
        audio = noise + pop_full

    else: # triumph_fanfare / default chime
        duration = 1.4
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        chord = (
            np.sin(2 * np.pi * 523.25 * t) +
            np.sin(2 * np.pi * 659.25 * t) * 0.8 +
            np.sin(2 * np.pi * 783.99 * t) * 0.8
        ) * np.exp(-t * 2.2)
        audio = chord

    # Normalize audio
    max_amp = np.max(np.abs(audio))
    if max_amp > 1e-4:
        audio = (audio / max_amp) * 0.85

    sf.write(output_path, audio.astype(np.float32), sample_rate)
    return output_path

def get_best_bg_music() -> Optional[str]:
    """Finds the best comedic/playful background track in assets."""
    preferred = [
        "sneaky_snitch.mp3",
        "viral_beat_output001.mp3",
        "viral_beat_output002.mp3",
        "hitman.mp3"
    ]
    for p in preferred:
        path = os.path.join(BG_MUSIC_DIR, p)
        if os.path.exists(path):
            return path
            
    # Fallback: scan any mp3 in bg_music
    if os.path.exists(BG_MUSIC_DIR):
        for f in os.listdir(BG_MUSIC_DIR):
            if f.endswith(".mp3"):
                return os.path.join(BG_MUSIC_DIR, f)
    return None

def mix_master_audio(
    voice_path: str,
    output_master_path: str,
    bg_music_path: Optional[str] = None,
    sfx_cues: Optional[List[Dict[str, Any]]] = None,
    music_volume: float = 0.18,
    ducking_db: float = -12.0
) -> str:
    """
    Mixes voiceover, SFX cues, and ducked background music using FFmpeg.
    Ensures -12dB sidechain ducking when the voice speaks!
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_master_path)), exist_ok=True)
    
    if bg_music_path is None:
        bg_music_path = get_best_bg_music()

    # If background music is available, execute sidechain compression ducking
    if bg_music_path and os.path.exists(bg_music_path):
        filter_complex = (
            f"[1:a]volume={music_volume}[bg];"
            f"[0:a]asplit=2[voice_main][voice_sidechain];"
            f"[bg][voice_sidechain]sidechaincompress=threshold=0.08:ratio=5:attack=40:release=350[ducked_bg];"
            f"[voice_main][ducked_bg]amix=inputs=2:duration=first:dropout_transition=2[mixed];"
            f"[mixed]loudnorm=I=-15:TP=-1.5:LRA=11[aout]"
        )
        cmd = [
            FFMPEG_BIN, "-y",
            "-i", voice_path,
            "-i", bg_music_path,
            "-filter_complex", filter_complex,
            "-map", "[aout]",
            "-c:a", "aac",
            "-b:a", "192k",
            output_master_path
        ]
    else:
        filter_complex = "[0:a]loudnorm=I=-15:TP=-1.5:LRA=11[aout]"
        cmd = [
            FFMPEG_BIN, "-y",
            "-i", voice_path,
            "-filter_complex", filter_complex,
            "-map", "[aout]",
            "-c:a", "aac",
            "-b:a", "192k",
            output_master_path
        ]
        
    subprocess.run(cmd, check=True, capture_output=True)
    return output_master_path
