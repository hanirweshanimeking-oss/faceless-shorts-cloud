"""
Dragon Studios India - OmniVoice ONNX Zero-Shot Voice Cloning Engine
Integrates k2-fsa / Prince-1 OmniVoice with Higgs Audio Tokenizer:
- Acoustic feature extraction + semantic encoding from anime reference audio
- 32-step iterative unmasking LLM decoder
- Multilingual zero-shot voice cloning (English, Hindi, Japanese, 600+ languages)
- Pure CPU execution via ONNX Runtime
"""

import os
import sys
import subprocess
from typing import Dict, Any, Optional

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OMNIVOICE_DIR = os.path.join(WORKSPACE_ROOT, "models", "omnivoice")
HIGGS_DIR = os.path.join(OMNIVOICE_DIR, "audio_tokenizer")
DEFAULT_AYANOKOJI_REF = os.path.join(WORKSPACE_ROOT, "models", "ayanokoji_reference", "ayanokoji_short_quote_en.wav")


def synthesize_omnivoice_clone(
    text: str,
    output_path: str,
    ref_audio_path: str = DEFAULT_AYANOKOJI_REF,
    ref_text: str = "All people are nothing but tools.",
    num_steps: int = 16,
    num_audio_tokens: int = 160
) -> Dict[str, Any]:
    """
    Synthesizes speech conditioned on a reference voice using OmniVoice ONNX.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    inference_script = os.path.join(OMNIVOICE_DIR, "inference.py")
    if not os.path.exists(inference_script):
        raise FileNotFoundError(f"OmniVoice inference script not found at {inference_script}")

    temp_wav = output_path if output_path.endswith(".wav") else output_path.replace(".mp3", ".wav")
    
    cmd = [
        sys.executable,
        inference_script,
        "--model_dir", OMNIVOICE_DIR,
        "--higgs_dir", HIGGS_DIR,
        "--text", text,
        "--ref_audio", ref_audio_path,
        "--ref_text", ref_text,
        "--num_steps", str(num_steps),
        "--num_audio_tokens", str(num_audio_tokens),
        "--output", temp_wav
    ]

    subprocess.run(cmd, check=True)

    final_path = output_path
    if output_path.endswith(".mp3"):
        ffmpeg_cmd = ["ffmpeg", "-y", "-i", temp_wav, "-b:a", "192k", output_path]
        subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    file_size = os.path.getsize(final_path) if os.path.exists(final_path) else 0

    return {
        "status": "SUCCESS",
        "output_path": final_path,
        "engine": "OmniVoice_ONNX_Higgs",
        "reference_audio": ref_audio_path,
        "text": text,
        "num_steps": num_steps,
        "file_size_bytes": file_size
    }
