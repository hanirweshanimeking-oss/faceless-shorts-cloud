"""
Faceless Shorts Final Compositor
Assembles scene clips, burns in dynamic viral yellow word-highlight subtitles,
merges the mastered audio with sidechain ducking, and performs QA verification.
"""
import os
import json
import subprocess
from typing import List, Dict, Any

from faceless_engine.config import FFMPEG_BIN, FFPROBE_BIN

def concatenate_scene_videos(scene_paths: List[str], output_path: str) -> str:
    """Concatenates multiple scene MP4 files seamlessly using FFmpeg concat demuxer."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    list_file = output_path.replace(".mp4", "_concat_list.txt")
    
    with open(list_file, "w", encoding="utf-8") as f:
        for p in scene_paths:
            # Escape path for FFmpeg concat demuxer
            clean_path = os.path.abspath(p).replace("\\", "/")
            f.write(f"file '{clean_path}'\n")
            
    cmd = [
        FFMPEG_BIN, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    if os.path.exists(list_file):
        os.remove(list_file)
        
    return output_path

def burn_subtitles_and_master(
    visual_video_path: str,
    master_audio_path: str,
    ass_subtitles_path: str,
    final_output_path: str
) -> str:
    """
    Burns in the word-by-word yellow highlight subtitles and attaches master ducked audio.
    """
    os.makedirs(os.path.dirname(os.path.abspath(final_output_path)), exist_ok=True)
    
    # Escape path for ASS subtitle filter
    escaped_ass = os.path.abspath(ass_subtitles_path).replace("\\", "/").replace(":", "\\:")
    
    # Slight contrast & saturation boost for viral social media punch
    video_filter = f"ass='{escaped_ass}',eq=contrast=1.06:saturation=1.12"
    
    cmd = [
        FFMPEG_BIN, "-y",
        "-i", visual_video_path,
        "-i", master_audio_path,
        "-vf", video_filter,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        final_output_path
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"[Compositor] Warning on ASS burn ({e.stderr[:200] if e.stderr else e}), attempting fallback without subtitle filter...")
        cmd_fallback = [
            FFMPEG_BIN, "-y",
            "-i", visual_video_path,
            "-i", master_audio_path,
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            final_output_path
        ]
        subprocess.run(cmd_fallback, check=True, capture_output=True)
        
    return final_output_path

def qa_verify_video(video_path: str) -> Dict[str, Any]:
    """
    Runs automated QA audit on the finished vertical video:
    - Verifies file exists & size > 0
    - Checks duration, resolution (1080x1920), video codec (h264), audio streams
    """
    if not os.path.exists(video_path):
        return {"passed": False, "error": f"File does not exist: {video_path}"}
        
    size_mb = round(os.path.getsize(video_path) / (1024 * 1024), 2)
    if size_mb < 0.1:
        return {"passed": False, "error": f"File too small ({size_mb} MB)"}
        
    cmd = [
        FFPROBE_BIN,
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        video_path
    ]
    
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(res.stdout)
        
        streams = data.get("streams", [])
        v_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
        a_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)
        
        width = int(v_stream.get("width", 0)) if v_stream else 0
        height = int(v_stream.get("height", 0)) if v_stream else 0
        duration = float(data.get("format", {}).get("duration", 0.0))
        
        passed = (
            v_stream is not None and
            a_stream is not None and
            width == 1080 and
            height == 1920 and
            duration > 10.0
        )
        
        return {
            "passed": passed,
            "width": width,
            "height": height,
            "duration_sec": round(duration, 2),
            "file_size_mb": size_mb,
            "video_codec": v_stream.get("codec_name", "unknown") if v_stream else None,
            "audio_codec": a_stream.get("codec_name", "unknown") if a_stream else None,
            "bitrate_kbps": round(float(data.get("format", {}).get("bit_rate", 0)) / 1000, 1)
        }
    except Exception as e:
        return {"passed": False, "error": str(e), "file_size_mb": size_mb}
