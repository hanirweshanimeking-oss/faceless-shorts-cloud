"""
Dragon Studios India - Clean Viral Hook Agent
Manages watermark-free viral hook video clips for short-form content (Reels / Shorts).
Enforces strict Zero-Watermark policy, downloads verified clips, normalizes to 9:16 vertical,
and supplies high-retention 2-3 second openers for video production.
"""

import os
import json
import random
import urllib.request
import subprocess
from typing import List, Dict, Any, Optional

# Locate FFmpeg binary
FFMPEG_BIN = "C:\\Users\\DESKTOP\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-9.0.2-full_build\\bin\\ffmpeg.exe"
if not os.path.exists(FFMPEG_BIN):
    FFMPEG_BIN = "ffmpeg"

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HOOKS_DIR = os.path.join(BASE_DIR, "assets", "clean_hooks")
CATALOG_PATH = os.path.join(HOOKS_DIR, "discovered_hooks.json")

# Built-in verified watermark-free direct MP4 hooks
VERIFIED_CLEAN_HOOKS = [
    {"title": "Car Bump", "url": "https://media.shorthooks.com/hooks/car-bump.mp4", "category": "shock"},
    {"title": "Car Flip", "url": "https://media.shorthooks.com/hooks/car-flip.mp4", "category": "stunt"},
    {"title": "Cart Crash", "url": "https://media.shorthooks.com/hooks/cart-crash.mp4", "category": "action"},
    {"title": "Dashcammer", "url": "https://media.shorthooks.com/hooks/dashcammer.mp4", "category": "tension"},
    {"title": "Easy Applause", "url": "https://media.shorthooks.com/hooks/easy-applause.mp4", "category": "crowd"},
    {"title": "Hi Front Seat", "url": "https://media.shorthooks.com/hooks/hi-front-seat.mp4", "category": "humor"},
    {"title": "Low Battery", "url": "https://media.shorthooks.com/hooks/low-battery.mp4", "category": "relatable"},
    {"title": "No Crunch", "url": "https://media.shorthooks.com/hooks/no-crunch.mp4", "category": "satisfying"},
    {"title": "Rice Bear", "url": "https://media.shorthooks.com/hooks/rice-bear.mp4", "category": "aesthetic"},
    {"title": "Rip Open", "url": "https://media.shorthooks.com/hooks/rip-open.mp4", "category": "curiosity"},
    {"title": "Roof Roller", "url": "https://media.shorthooks.com/hooks/roof-roller.mp4", "category": "extreme"},
    {"title": "Sandal Throw", "url": "https://media.shorthooks.com/hooks/sandal-throw.mp4", "category": "humor"},
    {"title": "Stone Tumble", "url": "https://media.shorthooks.com/hooks/stone-tumble.mp4", "category": "physics"},
    {"title": "Wrap It Lol", "url": "https://media.shorthooks.com/hooks/wrap-it-lol.mp4", "category": "satisfying"}
]

class CleanHookAgent:
    def __init__(self, hooks_dir: str = HOOKS_DIR):
        self.hooks_dir = hooks_dir
        os.makedirs(self.hooks_dir, exist_ok=True)
        self._ensure_catalog()

    def _ensure_catalog(self):
        """Ensures the local catalog JSON exists with verified clean hooks."""
        if not os.path.exists(CATALOG_PATH):
            with open(CATALOG_PATH, "w", encoding="utf-8") as f:
                json.dump(VERIFIED_CLEAN_HOOKS, f, indent=2)

    def load_catalog(self) -> List[Dict[str, Any]]:
        """Loads available hook metadata."""
        if os.path.exists(CATALOG_PATH):
            try:
                with open(CATALOG_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return VERIFIED_CLEAN_HOOKS

    def list_local_hooks(self) -> List[str]:
        """Lists normalized MP4 hook files currently stored locally."""
        if not os.path.exists(self.hooks_dir):
            return []
        return [
            os.path.join(self.hooks_dir, f)
            for f in os.listdir(self.hooks_dir)
            if f.endswith(".mp4") and not f.startswith("raw_")
        ]

    def download_hook(self, hook_entry: Dict[str, Any]) -> str:
        """Downloads a clean hook clip without any watermarks."""
        url = hook_entry["url"]
        filename = url.split("/")[-1]
        raw_dest = os.path.join(self.hooks_dir, f"raw_{filename}")
        norm_dest = os.path.join(self.hooks_dir, filename)

        if os.path.exists(norm_dest):
            return norm_dest

        # Download raw video
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=15) as resp, open(raw_dest, "wb") as f:
            f.write(resp.read())

        # Normalize to 9:16 vertical (1080x1920), 30 fps, 2.5s duration
        self.normalize_hook(raw_dest, norm_dest, duration=2.5)

        # Cleanup raw file if normalized successfully
        if os.path.exists(norm_dest) and os.path.getsize(norm_dest) > 1000:
            try:
                os.remove(raw_dest)
            except OSError:
                pass

        return norm_dest

    def normalize_hook(
        self,
        input_path: str,
        output_path: str,
        duration: float = 2.5,
        target_width: int = 1080,
        target_height: int = 1920
    ) -> str:
        """
        Normalizes any hook video into vertical 9:16 (1080x1920) at 30 fps,
        trimmed to the specified duration, zero watermarks.
        """
        filter_complex = (
            f"[0:v]scale={target_width}:{target_height}:force_original_aspect_ratio=increase,"
            f"crop={target_width}:{target_height},"
            f"fps=30,format=yuv420p[v]"
        )

        cmd = [
            FFMPEG_BIN, "-y",
            "-i", input_path,
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-t", str(duration),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "22",
            "-an",  # Strip original hook audio to prevent clash with TTS narrative
            output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path

    def prepare_hook_for_scene(
        self,
        hook_path: str,
        target_duration: float,
        output_path: str
    ) -> str:
        """
        Adapts a clean hook video to match the exact duration of Scene 1,
        looping seamlessly if necessary and ensuring 1080x1920 vertical format.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        filter_complex = (
            f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
            f"crop=1080:1920,fps=30,format=yuv420p[v]"
        )
        cmd = [
            FFMPEG_BIN, "-y",
            "-stream_loop", "-1",
            "-i", hook_path,
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-t", str(target_duration),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "22",
            "-an",
            output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path

    def get_clean_hook(self, preferred_category: Optional[str] = None) -> str:
        """
        Retrieves a verified watermark-free hook.
        If a local normalized hook exists, returns it; otherwise downloads and prepares one.
        """
        local = self.list_local_hooks()
        if local:
            return random.choice(local)

        catalog = self.load_catalog()
        if preferred_category:
            filtered = [h for h in catalog if h.get("category") == preferred_category]
            choice = random.choice(filtered) if filtered else random.choice(catalog)
        else:
            choice = random.choice(catalog)

        return self.download_hook(choice)

    def batch_download(self, count: int = 5) -> List[str]:
        """Downloads and normalizes the top `count` hooks from the catalog."""
        catalog = self.load_catalog()
        downloaded = []
        for hook in catalog:
            if len(downloaded) >= count:
                break
            filename = hook["url"].split("/")[-1]
            dest = os.path.join(self.hooks_dir, filename)
            if not os.path.exists(dest):
                try:
                    path = self.download_hook(hook)
                    downloaded.append(path)
                except Exception as e:
                    print(f"Error downloading {hook['title']}: {e}")
            else:
                downloaded.append(dest)
        return downloaded
