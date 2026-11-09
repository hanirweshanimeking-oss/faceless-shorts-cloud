"""
Dragon Studios India - Claude-Video (/watch) Perception Adapter
Integrates bradautomates/claude-video (/watch skill) into Dragon Studios.
Enables agents to download, extract timestamped frames, parse transcripts,
and 'watch' any video URL or local file for research, QA, and style replication.
"""

from __future__ import annotations

import os
import sys
import subprocess
import re
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CLAUDE_VIDEO_DIR = os.path.join(WORKSPACE_DIR, "claude-video")
WATCH_SCRIPT_PATH = os.path.join(CLAUDE_VIDEO_DIR, "skills", "watch", "scripts", "watch.py")
SETUP_SCRIPT_PATH = os.path.join(CLAUDE_VIDEO_DIR, "skills", "watch", "scripts", "setup.py")


class VideoFrameCue(BaseModel):
    timestamp: str
    path: str
    reason: str = "keyframe"


class VideoPerceptionDossier(BaseModel):
    source: str
    title: str = ""
    duration_seconds: float = 0.0
    duration_formatted: str = "00:00"
    resolution: str = "unknown"
    detail_mode: str = "balanced"
    frame_count: int = 0
    frames: List[VideoFrameCue] = Field(default_factory=list)
    transcript: str = ""
    gemini_answer: Optional[str] = None
    work_dir: Optional[str] = None
    status: str = "success"
    error_message: Optional[str] = None


class ClaudeVideoAdapter:
    """
    Adapter connecting Dragon Studios agents to the claude-video /watch engine.
    Supports local keyframe extraction, native caption parsing, whisper transcription,
    and video model question answering.
    """

    def __init__(self, workspace_dir: str = WORKSPACE_DIR):
        self.workspace_dir = workspace_dir
        self.claude_video_dir = os.path.join(workspace_dir, "claude-video")
        self.watch_script = os.path.join(self.claude_video_dir, "skills", "watch", "scripts", "watch.py")
        self.setup_script = os.path.join(self.claude_video_dir, "skills", "watch", "scripts", "setup.py")
        self.python_bin = self._resolve_python_executable()

    def _resolve_python_executable(self) -> str:
        """
        Locates the preferred Python interpreter with yt-dlp & ffmpeg available.
        """
        venv_py = os.path.join(self.workspace_dir, ".venv", "Scripts", "python.exe")
        if os.path.exists(venv_py):
            return venv_py
        return sys.executable

    def check_readiness(self) -> Dict[str, Any]:
        """
        Runs setup.py --json to check environment readiness.
        """
        if not os.path.exists(self.setup_script):
            return {
                "ready": False,
                "error": f"claude-video setup script not found at {self.setup_script}"
            }

        try:
            cmd = [self.python_bin, self.setup_script, "--json"]
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if res.returncode == 0:
                data = json.loads(res.stdout)
                return {
                    "ready": data.get("can_proceed", False),
                    "engine": data.get("engine", "local"),
                    "tools": data.get("tools", {}),
                    "status": data.get("status", "unknown")
                }
            return {"ready": False, "error": res.stderr.strip()}
        except Exception as e:
            return {"ready": False, "error": str(e)}

    def watch(
        self,
        source: str,
        detail: str = "balanced",
        max_frames: int = 20,
        timestamps: Optional[List[str]] = None,
        question: Optional[str] = None,
        engine: str = "local"
    ) -> VideoPerceptionDossier:
        """
        Watches a video (local file or URL) and produces a VideoPerceptionDossier.
        """
        # If claude-video scripts exist, invoke watch.py
        if os.path.exists(self.watch_script):
            try:
                cmd = [
                    self.python_bin,
                    self.watch_script,
                    source,
                    "--engine", engine,
                    "--detail", detail,
                    "--max-frames", str(max_frames)
                ]
                if timestamps:
                    cmd.extend(["--timestamps", ",".join(timestamps)])
                if question:
                    cmd.extend(["--question", question])

                res = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    check=False
                )

                if res.returncode == 0:
                    dossier = self._parse_watch_output(source, res.stdout)
                    if dossier.frame_count > 0 or dossier.gemini_answer or dossier.transcript:
                        return dossier
            except Exception as exc:
                # Log and fallback to native ffmpeg
                pass

        # Resilient fallback: direct FFmpeg extraction
        return self._fallback_local_watch(source, max_frames=max_frames)

    def _parse_watch_output(self, source: str, stdout: str) -> VideoPerceptionDossier:
        """
        Parses the Markdown output generated by watch.py into a structured VideoPerceptionDossier.
        """
        duration_sec = 0.0
        duration_fmt = "00:00"
        resolution = "unknown"
        detail_mode = "balanced"
        title = os.path.basename(source)
        frames: List[VideoFrameCue] = []
        transcript = ""
        gemini_answer = None
        work_dir = None

        # Parse duration: - **Duration:** 00:29 (28.5s)
        dur_match = re.search(r"\*\*Duration:\*\*\s*([\d:]+)\s*\(([\d\.]+)s\)", stdout)
        if dur_match:
            duration_fmt = dur_match.group(1)
            duration_sec = float(dur_match.group(2))

        # Parse resolution: - **Resolution:** 1080x1920
        res_match = re.search(r"\*\*Resolution:\*\*\s*([^\n\r]+)", stdout)
        if res_match:
            resolution = res_match.group(1).strip()

        # Parse detail: - **Detail:** efficient
        detail_match = re.search(r"\*\*Detail:\*\*\s*([^\n\r]+)", stdout)
        if detail_match:
            detail_mode = detail_match.group(1).strip()

        # Parse work dir: _Work dir: `...`
        work_match = re.search(r"_Work dir:\s*`([^`]+)`", stdout)
        if work_match:
            work_dir = work_match.group(1).strip()

        # Parse frames
        # Example: - `C:\path\to\frame_0001.jpg` (t=00:00, reason=keyframe)
        frame_matches = re.findall(r"-\s*`([^`]+)`\s*\(([^)]+)\)", stdout)
        for path_str, meta_str in frame_matches:
            if path_str.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
                t_match = re.search(r"t=([\d:]+)", meta_str)
                r_match = re.search(r"reason=([\w]+)", meta_str)
                timestamp = t_match.group(1) if t_match else "00:00"
                reason = r_match.group(1) if r_match else "keyframe"
                frames.append(VideoFrameCue(timestamp=timestamp, path=path_str, reason=reason))

        # Parse Gemini Answer
        if "## Answer (from Gemini)" in stdout:
            parts = stdout.split("## Answer (from Gemini)")
            if len(parts) > 1:
                gemini_answer = parts[1].split("## ")[0].strip()

        # Parse Transcript
        if "## Transcript" in stdout:
            parts = stdout.split("## Transcript")
            if len(parts) > 1:
                transcript_block = parts[1].split("---")[0].strip()
                if not transcript_block.startswith("_Unavailable"):
                    transcript = transcript_block

        return VideoPerceptionDossier(
            source=source,
            title=title,
            duration_seconds=duration_sec,
            duration_formatted=duration_fmt,
            resolution=resolution,
            detail_mode=detail_mode,
            frame_count=len(frames),
            frames=frames,
            transcript=transcript,
            gemini_answer=gemini_answer,
            work_dir=work_dir,
            status="success"
        )

    def _fallback_local_watch(self, source: str, max_frames: int = 10) -> VideoPerceptionDossier:
        """
        Pure FFmpeg & ffprobe fallback when watch.py fails or is offline.
        """
        if not os.path.exists(source):
            return VideoPerceptionDossier(
                source=source,
                status="error",
                error_message=f"Source file not found: {source}"
            )

        # Probe file with ffprobe
        duration_sec = 0.0
        resolution = "unknown"
        try:
            cmd = [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                source
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if res.returncode == 0:
                data = json.loads(res.stdout)
                duration_sec = float(data.get("format", {}).get("duration", 0.0))
                for s in data.get("streams", []):
                    if s.get("codec_type") == "video":
                        resolution = f"{s.get('width', 0)}x{s.get('height', 0)}"
                        break
        except Exception:
            pass

        # Extract frames to a temp directory
        out_dir = Path(WORKSPACE_DIR) / "output" / "watch_cache" / Path(source).stem
        out_dir.mkdir(parents=True, exist_ok=True)

        frames: List[VideoFrameCue] = []
        if duration_sec > 0:
            step = duration_sec / max(1, max_frames)
            for i in range(max_frames):
                t_sec = i * step
                frame_path = out_dir / f"frame_{i+1:04d}.jpg"
                try:
                    extract_cmd = [
                        "ffmpeg", "-y",
                        "-ss", f"{t_sec:.2f}",
                        "-i", source,
                        "-vframes", "1",
                        "-q:v", "2",
                        "-vf", "scale='min(512,iw)':-1",
                        str(frame_path)
                    ]
                    subprocess.run(extract_cmd, capture_output=True, check=False)
                    if frame_path.exists():
                        mins = int(t_sec // 60)
                        secs = int(t_sec % 60)
                        frames.append(VideoFrameCue(
                            timestamp=f"{mins:02d}:{secs:02d}",
                            path=str(frame_path),
                            reason="uniform_sample"
                        ))
                except Exception:
                    pass

        mins = int(duration_sec // 60)
        secs = int(duration_sec % 60)
        return VideoPerceptionDossier(
            source=source,
            title=Path(source).name,
            duration_seconds=duration_sec,
            duration_formatted=f"{mins:02d}:{secs:02d}",
            resolution=resolution,
            detail_mode="fallback_ffmpeg",
            frame_count=len(frames),
            frames=frames,
            work_dir=str(out_dir),
            status="success"
        )

    def deconstruct_for_recreation(self, source: str) -> Dict[str, Any]:
        """
        Deconstructs an existing video's visual and audio rhythm to generate a Dragon Studios
        Recreation Blueprint (scene-by-scene timing, hook breakdown, and prompt guides).
        """
        dossier = self.watch(source, detail="balanced", max_frames=12)
        if dossier.status == "error":
            return {"error": dossier.error_message}

        duration = dossier.duration_seconds
        cut_count = max(1, dossier.frame_count)
        pacing_sec_per_cut = round(duration / cut_count, 2) if cut_count > 0 else 3.0

        # Pacing assessment
        if pacing_sec_per_cut < 2.0:
            pacing_category = "Ultra-Fast (TikTok / Gen-Z Brainrot)"
        elif pacing_sec_per_cut <= 3.5:
            pacing_category = "High-Retention Viral Standard (Raj Shamani / Alex Hormozi)"
        else:
            pacing_category = "Cinematic / Documentary Pacing"

        # Shot breakdown
        reconstructed_scenes = []
        for idx, f in enumerate(dossier.frames):
            reconstructed_scenes.append({
                "scene_number": idx + 1,
                "timestamp": f.timestamp,
                "frame_path": f.path,
                "target_duration_seconds": pacing_sec_per_cut,
                "shot_type": "Close-Up Hook" if idx == 0 else ("Contrarian Truth" if idx == 1 else "Visual Reinforcement"),
                "visual_prompt_direction": f"Replicate aesthetic of frame at {f.timestamp} with ultra-clean 9:16 framing, 8k render, hyper-detailed lighting"
            })

        return {
            "source": dossier.source,
            "title": dossier.title,
            "total_duration_seconds": duration,
            "detected_aspect_ratio": dossier.resolution,
            "pacing_category": pacing_category,
            "average_seconds_per_shot": pacing_sec_per_cut,
            "cut_frequency_per_minute": round((60.0 / pacing_sec_per_cut) if pacing_sec_per_cut > 0 else 20.0, 1),
            "transcript_summary": dossier.transcript[:200] + "..." if len(dossier.transcript) > 200 else dossier.transcript,
            "hook_frame": dossier.frames[0].path if dossier.frames else None,
            "scene_count": len(reconstructed_scenes),
            "reconstructed_scenes": reconstructed_scenes,
            "recreation_strategy": {
                "hook_rule": "Retain < 2.5s first scene duration to prevent drop-off",
                "recommended_voice": "en-US-ChristopherNeural (Authoritative Contrarian)",
                "recommended_captions": "Word-by-word kinetic gold highlight with Hypit SVML anchoring"
            }
        }
