"""
Faceless Shorts Automation Engine - Configuration
Hardware-adapted for Windows, CPU FFmpeg Compositor, Kokoro Neural TTS & Faster-Whisper
"""
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Verified binary paths
FFMPEG_BIN = "C:\\Users\\DESKTOP\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-9.0.2-full_build\\bin\\ffmpeg.exe"
if not os.path.exists(FFMPEG_BIN):
    FFMPEG_BIN = "ffmpeg"

FFPROBE_BIN = "C:\\Users\\DESKTOP\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-9.0.2-full_build\\bin\\ffprobe.exe"
if not os.path.exists(FFPROBE_BIN):
    FFPROBE_BIN = "ffprobe"

PYTHON_BIN = "C:\\Users\\DESKTOP\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
if not os.path.exists(PYTHON_BIN):
    PYTHON_BIN = sys.executable

# Model paths
KOKORO_MODEL_PATH = os.path.join(BASE_DIR, "models", "kokoro", "kokoro-v1.0.onnx")
KOKORO_VOICES_PATH = os.path.join(BASE_DIR, "models", "kokoro", "voices-v1.0.bin")

# Output directory
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "faceless")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Asset directories
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
BG_MUSIC_DIR = os.path.join(ASSETS_DIR, "bg_music")
FONTS_DIR = os.path.join(os.path.dirname(__file__), "assets", "fonts")
if not os.path.exists(FONTS_DIR):
    FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
os.makedirs(FONTS_DIR, exist_ok=True)

# Supported styles
STYLES = [
    "Tall Tale 3D",
    "Deep Dive 3D",
    "Inside Out",
    "Stick Story",
    "Night File 3D",
    "Paper Atlas"
]
