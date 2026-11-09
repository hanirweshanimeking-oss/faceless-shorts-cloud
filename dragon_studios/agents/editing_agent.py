"""
Dragon Studios India - Intelligent Video Editing Engine
Automates vertical 9:16 video compositing, scene assembly, audio ducking,
styled subtitle burning using FFmpeg, and CapCut Pro project export.
"""

import os
import subprocess
import json
import shutil
from typing import List, Dict, Any, Optional

# Locate FFmpeg binary
FFMPEG_BIN = "C:\\Users\\DESKTOP\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-9.0.2-full_build\\bin\\ffmpeg.exe"
FFPROBE_BIN = "C:\\Users\\DESKTOP\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-9.0.2-full_build\\bin\\ffprobe.exe"

if not os.path.exists(FFMPEG_BIN):
    FFMPEG_BIN = "ffmpeg"
    FFPROBE_BIN = "ffprobe"

def get_media_info(file_path: str) -> Dict[str, Any]:
    """Uses ffprobe to extract video/audio stream properties."""
    cmd = [
        FFPROBE_BIN,
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        file_path
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception:
        pass
    return {}

def create_color_background_clip(
    output_path: str,
    duration: float,
    color: str = "#0b0c10",
    width: int = 1080,
    height: int = 1920,
    fps: int = 30
) -> str:
    """Generates a blank 9:16 background video with specified color."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    cmd = [
        FFMPEG_BIN, "-y",
        "-f", "lavfi",
        "-i", f"color=c={color}:s={width}x{height}:d={duration}:r={fps}",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-t", str(duration),
        output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path

def convert_to_vertical_9_16(
    input_video: str,
    output_video: str,
    target_width: int = 1080,
    target_height: int = 1920
) -> str:
    """
    Converts any video into vertical 9:16 with blurred background padding.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_video)), exist_ok=True)
    
    filter_complex = (
        f"[0:v]split=2[bg][fg];"
        f"[bg]scale={target_width}:{target_height}:force_original_aspect_ratio=increase,"
        f"crop={target_width}:{target_height},boxblur=20:5[blurred];"
        f"[fg]scale={target_width}:-1:force_original_aspect_ratio=decrease[scaled];"
        f"[blurred][scaled]overlay=(W-w)/2:(H-h)/2[v]"
    )
    
    cmd = [
        FFMPEG_BIN, "-y",
        "-i", input_video,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        output_video
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_video

def composite_scene(
    video_clip_path: str,
    voice_audio_path: str,
    output_path: str,
    bg_music_path: Optional[str] = None,
    subtitle_text: Optional[str] = None,
    ducking_db: float = -12.0
) -> str:
    """
    Combines video clip with voiceover audio, optional background music with ducking,
    and kinetic on-screen text overlays.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # Escape special characters for FFmpeg drawtext filter
    safe_text = (subtitle_text or "").replace("\\", "\\\\").replace("'", "").replace(":", "-").replace('"', "").replace("%", "\\\\\\%").strip()
    text_filter = ""
    if safe_text:
        text_filter = (
            f",drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='{safe_text}':"
            f"fontsize=46:fontcolor=white:borderw=4:bordercolor=black:"
            f"x=(w-text_w)/2:y=h*0.72"
        )
    
    # Video-Use inspired: cinematic color grading & 30ms anti-pop audio fades
    color_grade = ",eq=contrast=1.12:saturation=1.1:brightness=-0.01"
    video_filter = f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920{color_grade}{text_filter}[v]"
    audio_filter = "afade=t=in:st=0:d=0.03"
    
    if bg_music_path and os.path.exists(bg_music_path):
        cmd = [
            FFMPEG_BIN, "-y",
            "-i", video_clip_path,
            "-i", voice_audio_path,
            "-i", bg_music_path,
            "-filter_complex",
            f"{video_filter};"
            f"[2:a]volume=0.25[music];"
            f"[1:a]asplit=2[voice_sc][voice_out];"
            f"[music][voice_sc]sidechaincompress=threshold=0.1:ratio=4:attack=50:release=300[ducked_music];"
            f"[voice_out][ducked_music]amix=inputs=2:duration=first[a]",
            "-map", "[v]",
            "-map", "[a]",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "21",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_path
        ]
    else:
        cmd = [
            FFMPEG_BIN, "-y",
            "-i", video_clip_path,
            "-i", voice_audio_path,
            "-filter_complex", f"{video_filter};[1:a]{audio_filter}[a]",
            "-map", "[v]",
            "-map", "[a]",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "21",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_path
        ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        if text_filter:
            clean_filter = f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920{color_grade}[v]"
            cmd_fallback = [c if c != video_filter else clean_filter for c in cmd]
            subprocess.run(cmd_fallback, check=True, capture_output=True)
        else:
            raise e
    return output_path

def concatenate_scenes(
    scene_video_paths: List[str],
    final_output_path: str
) -> str:
    """Concatenates multiple completed scene clips into a final master video."""
    os.makedirs(os.path.dirname(os.path.abspath(final_output_path)), exist_ok=True)
    
    concat_list_path = os.path.join(os.path.dirname(final_output_path), "concat_list.txt")
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for path in scene_video_paths:
            normalized_path = os.path.abspath(path).replace("\\", "/")
            f.write(f"file '{normalized_path}'\n")
            
    cmd = [
        FFMPEG_BIN, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "19",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        final_output_path
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)
    
    if os.path.exists(concat_list_path):
        os.remove(concat_list_path)
        
    return final_output_path

def export_capcut_draft(
    project_id: str,
    scenes_data: List[Dict[str, Any]],
    output_dir: str
) -> str:
    """
    Exports a structured CapCut Pro / Premiere EDL compatible draft manifest
    allowing professional video editors to import and tweak keyframes, transitions, and text.
    """
    draft_dir = os.path.join(output_dir, "capcut_draft")
    os.makedirs(draft_dir, exist_ok=True)

    tracks = {
        "video_track": [],
        "audio_track": [],
        "subtitle_track": []
    }

    current_time_ms = 0
    for s in scenes_data:
        duration_ms = int(float(s.get("duration_seconds", 4.0)) * 1000)
        tracks["video_track"].append({
            "scene_order": s.get("scene_order", 1),
            "start_time_ms": current_time_ms,
            "duration_ms": duration_ms,
            "clip_source": s.get("video_asset_path") or s.get("visual_clip_path", ""),
            "transition": "CROSS_DISSOLVE"
        })
        tracks["audio_track"].append({
            "scene_order": s.get("scene_order", 1),
            "start_time_ms": current_time_ms,
            "duration_ms": duration_ms,
            "audio_source": s.get("audio_asset_path") or s.get("voice_audio_path", "")
        })
        tracks["subtitle_track"].append({
            "scene_order": s.get("scene_order", 1),
            "start_time_ms": current_time_ms,
            "duration_ms": duration_ms,
            "text": s.get("subtitle_text", ""),
            "font_size": 48,
            "color": "#FFFFFF",
            "stroke_color": "#000000"
        })
        current_time_ms += duration_ms

    manifest = {
        "project_id": project_id,
        "format": "CAPCUT_PRO_COMPATIBLE_DRAFT",
        "canvas_ratio": "9:16",
        "resolution": {"width": 1080, "height": 1920},
        "fps": 30,
        "total_duration_ms": current_time_ms,
        "tracks": tracks
    }

    draft_file = os.path.join(draft_dir, "draft_manifest.json")
    with open(draft_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return draft_file
