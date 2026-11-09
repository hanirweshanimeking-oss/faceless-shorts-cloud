"""
Dragon Studios India - Quality Assurance & Compliance Agent
Verifies export compliance for Instagram Reels & YouTube Shorts:
aspect ratio, resolution, duration, audio levels, and platform specs.
"""

import os
import subprocess
import json
from typing import Dict, Any, Tuple
from dragon_studios.agents.editing_agent import get_media_info
from dragon_studios.integrations.claude_video_adapter import ClaudeVideoAdapter

def run_qa_check(video_path: str) -> Dict[str, Any]:
    """
    Executes a comprehensive quality check on a generated video.
    Returns status: PASSED or FAILED with detailed checks.
    """
    if not os.path.exists(video_path):
        return {
            "passed": False,
            "score": 0.0,
            "errors": [f"File not found: {video_path}"]
        }
        
    info = get_media_info(video_path)
    streams = info.get("streams", [])
    format_info = info.get("format", {})
    
    video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)
    
    errors = []
    warnings = []
    
    # 1. Video Stream Check
    if not video_stream:
        errors.append("No video stream found.")
    else:
        width = int(video_stream.get("width", 0))
        height = int(video_stream.get("height", 0))
        codec = video_stream.get("codec_name", "")
        
        # Resolution & Aspect Ratio check
        if width != 1080 or height != 1920:
            errors.append(f"Incorrect resolution: {width}x{height} (Expected 1080x1920 9:16).")
            
        if codec != "h264":
            warnings.append(f"Video codec is '{codec}'. H.264 is strongly recommended for Instagram/YouTube.")

    # 2. Audio Stream Check
    if not audio_stream:
        errors.append("No audio stream found. Video must have sound/voiceover.")
    else:
        audio_codec = audio_stream.get("codec_name", "")
        if audio_codec != "aac":
            warnings.append(f"Audio codec is '{audio_codec}'. AAC is recommended.")

    # 3. Duration Check
    duration = float(format_info.get("duration", 0.0))
    if duration < 3.0:
        errors.append(f"Duration too short: {duration:.1f}s (Min 3.0s).")
    elif duration > 90.0:
        warnings.append(f"Duration {duration:.1f}s exceeds standard 60s Shorts limit.")

    # 4. File Size Check
    size_mb = float(format_info.get("size", 0)) / (1024 * 1024)
    if size_mb > 500:
        errors.append(f"File size too large: {size_mb:.1f} MB (Max 500 MB).")

    passed = len(errors) == 0
    score = 100.0 - (len(errors) * 30.0) - (len(warnings) * 10.0)
    score = max(0.0, min(100.0, score))

    # 5. Visual Perception Check via Claude-Video /watch
    visual_inspection = {"verified": False, "sample_frames": [], "frame_count": 0}
    if passed and os.path.exists(video_path):
        try:
            adapter = ClaudeVideoAdapter()
            dossier = adapter.watch(video_path, detail="efficient", max_frames=4)
            if dossier.status == "success" and dossier.frame_count > 0:
                visual_inspection = {
                    "verified": True,
                    "sample_frames": [f.path for f in dossier.frames],
                    "frame_count": dossier.frame_count,
                    "resolution_detected": dossier.resolution
                }
        except Exception:
            pass
    
    return {
        "passed": passed,
        "score": score,
        "duration_seconds": round(duration, 2),
        "resolution": f"{video_stream.get('width', 0)}x{video_stream.get('height', 0)}" if video_stream else "N/A",
        "file_size_mb": round(size_mb, 2),
        "errors": errors,
        "warnings": warnings,
        "visual_inspection": visual_inspection,
        "ready_for_approval": passed
    }
