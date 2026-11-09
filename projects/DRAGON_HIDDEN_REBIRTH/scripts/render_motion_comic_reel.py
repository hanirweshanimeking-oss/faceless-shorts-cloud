"""
CHITRAN: THE MANGA - Chapter 2 Motion Comic Reel Generator
Produces high-impact 9:16 vertical anime motion comic reel using:
- 1080x1920 vertical composition
- Smooth Ken Burns dynamic camera zooms/pans
- Neural anime voiceover via Edge-TTS (en-US-ChristopherNeural)
- Layered SFX impacts, whooshes, risers
- Stylized ASS animated subtitles
- Official CHITRAN branding & ending banner
"""

import os
import sys
import asyncio
import subprocess
from pathlib import Path
import edge_tts
from PIL import Image

FFMPEG_BIN = r"C:\Users\DESKTOP\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"
ROOT_DIR = Path(r"C:\Users\DESKTOP\Downloads\money")
PROJECT_DIR = ROOT_DIR / "DRAGON_HIDDEN_REBIRTH"
ART_DIR = PROJECT_DIR / "generated_art" / "chapter_002_hd"
AUDIO_DIR = PROJECT_DIR / "generated_audio"
OUT_DIR = PROJECT_DIR / "final_videos"
SFX_DIR = ROOT_DIR / "openmontage" / ".agents" / "skills" / "hyperframes-media" / "assets" / "sfx"
LOGO_PATH = PROJECT_DIR / "reference_standards" / "chitran_logo_perfect.png"
BANNER_PATH = Path(r"C:\Users\DESKTOP\.gemini\antigravity\brain\d0e83fc1-b00a-4e33-b50b-cc4e26bfa5c3\banner_crop.png")

OUT_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# 1. Narration Script with Timing Markers
NARRATION_SEGMENTS = [
    ("Beneath the forgotten ruins of Kashi... an ancient seal was shattered.", 3.2),
    ("A primordial terror rose from the abyss.", 2.8),
    ("Inside the boy... a dormant sun ignited!", 3.0),
    ("And from the shattered heavens... the Sovereign of Night descended.", 3.5),
    ("CHITRAN: Chapter 2 is live now.", 2.5)
]

FULL_VOICE_TEXT = "Beneath the forgotten ruins of Kashi... an ancient seal was shattered. A primordial terror rose from the abyss. Inside the boy... a dormant sun ignited! And from the shattered heavens... the Sovereign of Night descended. CHITRAN: Chapter 2 is live now."

async def generate_voiceover(output_path: Path):
    print("[*] Generating Edge-TTS neural narration...")
    communicate = edge_tts.Communicate(FULL_VOICE_TEXT, "en-US-ChristopherNeural", rate="-3%", pitch="-2Hz")
    await communicate.save(str(output_path))
    print(f"[+] Voiceover saved: {output_path} ({output_path.stat().st_size} bytes)")

def create_ass_subtitles(ass_path: Path):
    """Create styled ASS subtitle file for 1080x1920 vertical format."""
    ass_content = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: MotionComic,Impact,52,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,4,2,2,40,40,240,1
Style: AccentTitle,Arial Black,44,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,3,0,1,3,1,8,40,40,140,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.20,0:00:03.20,MotionComic,,0,0,0,,{\\fade(150,150)}BENEATH THE FORGOTTEN RUINS OF KASHI...
Dialogue: 0,0:00:01.80,0:00:03.20,MotionComic,,0,0,0,,{\\fade(100,100)}AN ANCIENT SEAL WAS SHATTERED.
Dialogue: 0,0:00:03.40,0:00:06.00,MotionComic,,0,0,0,,{\\c&H003333FF&\\fade(150,150)}A PRIMORDIAL TERROR ROSE FROM THE ABYSS!
Dialogue: 0,0:00:06.20,0:00:09.20,MotionComic,,0,0,0,,{\\c&H0000D4FF&\\fade(150,150)}INSIDE THE BOY... A DORMANT SUN IGNITED!
Dialogue: 0,0:00:09.40,0:00:12.80,MotionComic,,0,0,0,,{\\c&H00FF88FF&\\fade(150,150)}AND FROM THE SHATTERED HEAVENS...
Dialogue: 0,0:00:11.00,0:00:12.80,MotionComic,,0,0,0,,{\\c&H00FFCC00&\\fade(150,150)}THE SOVEREIGN OF NIGHT DESCENDED.
Dialogue: 0,0:00:13.00,0:00:15.50,MotionComic,,0,0,0,,{\\c&H00FFFFFF&\\fade(150,200)}CHITRAN: CHAPTER 2 IS LIVE NOW.
Dialogue: 0,0:00:00.00,0:00:15.50,AccentTitle,,0,0,0,,{\\c&H00FFAA00&\\an8}CHITRAN: THE MANGA
"""
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_content)
    print(f"[+] Subtitles created: {ass_path}")

def prepare_scene_image(img_path: Path, temp_out: Path, target_w=1080, target_h=1920):
    """Prepare high-res center-cropped base image for FFmpeg zoompan."""
    with Image.open(img_path) as im:
        im = im.convert("RGBA")
        iw, ih = im.size
        # Scale image to cover 1080x1920 with high quality
        scale = max(target_w / iw, target_h / ih) * 1.15  # 15% extra margin for zoompan
        nw, nh = int(iw * scale), int(ih * scale)
        im_resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
        
        # Center crop to 1242 x 2208 (1.15x of 1080x1920)
        cw, ch = int(target_w * 1.15), int(target_h * 1.15)
        left = (nw - cw) // 2
        top = (nh - ch) // 2
        im_cropped = im_resized.crop((left, top, left + cw, top + ch))
        im_cropped.convert("RGB").save(temp_out, "PNG")

def build_motion_comic():
    temp_dir = PROJECT_DIR / "temp_motion"
    temp_dir.mkdir(parents=True, exist_ok=True)

    voice_path = AUDIO_DIR / "ch2_voiceover.mp3"
    ass_path = temp_dir / "subtitles.ass"
    master_video = OUT_DIR / "chitran_ch2_motion_comic.mp4"

    # Step 1: Voiceover
    asyncio.run(generate_voiceover(voice_path))
    create_ass_subtitles(ass_path)

    # Step 2: Prepare scene images
    scenes = [
        ("p1_1_sanctum_wide.png", 3.2, "zoom_in"),
        ("p2_1_void_erupt.png", 1.4, "zoom_in_fast"),
        ("p2_2_void_fangs.png", 1.4, "shake"),
        ("p2_5_aarav_eyes_ignite.png", 1.5, "zoom_in"),
        ("p2_6_celestial_flame_burst.png", 1.7, "pan_up"),
        ("p3_2_neel_arrival.png", 2.0, "zoom_out"),
        ("p3_4_vortex_shockwave.png", 1.8, "zoom_in_fast"),
        ("p3_8_temple_roof_constellation.png", 2.5, "slow_pan")
    ]

    scene_clips = []
    fps = 30

    print("[*] Rendering dynamic animated video scenes with FFmpeg...")
    for idx, (img_name, duration, anim) in enumerate(scenes):
        src_img = ART_DIR / img_name
        temp_img = temp_dir / f"scene_{idx:02d}.png"
        prepare_scene_image(src_img, temp_img)
        scene_mp4 = temp_dir / f"clip_{idx:02d}.mp4"

        frames = int(duration * fps)

        # Build zoompan filter based on animation type
        if anim == "zoom_in":
            vf = f"zoompan=z='min(zoom+0.0015,1.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={fps}"
        elif anim == "zoom_in_fast":
            vf = f"zoompan=z='min(zoom+0.0035,1.35)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={fps}"
        elif anim == "zoom_out":
            vf = f"zoompan=z='if(lte(zoom,1.0),1.25,max(1.0,zoom-0.002))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={fps}"
        elif anim == "pan_up":
            vf = f"zoompan=z=1.15:x='iw/2-(iw/zoom/2)':y='if(lte(on,1),ih*0.3,max(0,y-1.5))':d={frames}:s=1080x1920:fps={fps}"
        elif anim == "shake":
            vf = f"zoompan=z=1.18:x='iw/2-(iw/zoom/2)+sin(on*2)*12':y='ih/2-(ih/zoom/2)+cos(on*3)*12':d={frames}:s=1080x1920:fps={fps}"
        else: # slow_pan
            vf = f"zoompan=z='min(zoom+0.0008,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={fps}"

        cmd = [
            FFMPEG_BIN, "-y",
            "-loop", "1",
            "-i", str(temp_img),
            "-vf", vf,
            "-c:v", "libx264",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            "-r", str(fps),
            str(scene_mp4)
        ]
        if not scene_mp4.exists() or scene_mp4.stat().st_size == 0:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res.returncode != 0:
                print(f"[!] Error rendering scene {idx}:", res.stderr.decode("utf-8", errors="ignore"))
                sys.exit(1)
        scene_clips.append(scene_mp4)
        print(f"    [+] Scene {idx+1}/{len(scenes)} ready ({anim}, {duration}s)")

    # Step 3: Concat video scenes
    concat_list_file = temp_dir / "concat_list.txt"
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for clip in scene_clips:
            f.write(f"file '{clip.resolve()}'\n")

    raw_concat_mp4 = temp_dir / "raw_concat.mp4"
    print("[*] Concatenating scenes into unified timeline...")
    cmd_concat = [
        FFMPEG_BIN, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy",
        str(raw_concat_mp4)
    ]
    subprocess.run(cmd_concat, check=True)

    # Step 4: Layer Audio (Voiceover + SFX at specific keyframe marks)
    # SFX Marks:
    # 0.0s: impact-bass-1.mp3 (Sanctum reveal)
    # 3.2s: whoosh-cinematic.mp3 + glitch-1.mp3 (Void Stalker erupts)
    # 6.0s: riser.mp3 (Aarav eye ignite)
    # 7.4s: impact-bass-2.mp3 (Celestial flame burst)
    # 9.0s: whoosh-cinematic.mp3 (Neel arrival)
    # 10.8s: impact-bass-1.mp3 (Vortex shockwave)
    # 13.0s: chime.mp3 (Title banner)
    
    sfx1 = SFX_DIR / "impact-bass-1.mp3"
    sfx_whoosh = SFX_DIR / "whoosh-cinematic.mp3"
    sfx_glitch = SFX_DIR / "glitch-1.mp3"
    sfx_riser = SFX_DIR / "riser.mp3"
    sfx2 = SFX_DIR / "impact-bass-2.mp3"
    sfx_chime = SFX_DIR / "chime.mp3"

    print("[*] Mixing audio with sidechain dynamic ducking & SFX layers...")
    
    # Complex filtergraph for multi-track SFX positioning & ducking
    # Input 0: raw_concat.mp4
    # Input 1: voiceover
    # Input 2-7: SFX
    
    filter_complex = (
        # Delay and volume adjustments for each SFX cue
        "[2:a]adelay=0|0,volume=1.2[sfx0];"
        "[3:a]adelay=3200|3200,volume=1.0[sfx1];"
        "[4:a]adelay=3400|3400,volume=0.8[sfx2];"
        "[5:a]adelay=5800|5800,volume=0.9[sfx3];"
        "[6:a]adelay=7400|7400,volume=1.3[sfx4];"
        "[3:a]adelay=9000|9000,volume=1.0[sfx5];"
        "[2:a]adelay=10800|10800,volume=1.2[sfx6];"
        "[7:a]adelay=13000|13000,volume=1.1[sfx7];"
        # Combine all SFX
        "[sfx0][sfx1][sfx2][sfx3][sfx4][sfx5][sfx6][sfx7]amix=inputs=8:dropout_transition=0:normalize=0[sfx_all];"
        # Split voiceover for sidechain detection and final mix
        "[1:a]volume=1.4,asplit=2[voice_sc][voice_mix];"
        "[sfx_all][voice_sc]sidechaincompress=threshold=0.1:ratio=3:attack=10:release=150[sfx_ducked];"
        "[sfx_ducked][voice_mix]amix=inputs=2:dropout_transition=0:normalize=0[audio_out];"
        # Subtitle overlay filter (relative path with forward slashes for Windows FFmpeg)
        "[0:v]subtitles='DRAGON_HIDDEN_REBIRTH/temp_motion/subtitles.ass'[v_sub]"
    )

    cmd_master = [
        FFMPEG_BIN, "-y",
        "-i", str(raw_concat_mp4),
        "-i", str(voice_path),
        "-i", str(sfx1),
        "-i", str(sfx_whoosh),
        "-i", str(sfx_glitch),
        "-i", str(sfx_riser),
        "-i", str(sfx2),
        "-i", str(sfx_chime),
        "-filter_complex", filter_complex,
        "-map", "[v_sub]",
        "-map", "[audio_out]",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "256k",
        "-shortest",
        str(master_video)
    ]

    print("[*] Encoding final master motion comic reel...")
    res = subprocess.run(cmd_master, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        print("[!] FFmpeg master encode error:", res.stderr.decode("utf-8", errors="ignore"))
        # Fallback to direct mix without complex subtitles if path issue
        sys.exit(1)

    print(f"\n[+] MASTER MOTION COMIC PRODUCED SUCCESSFULLY!")
    print(f"    File: {master_video}")
    print(f"    Size: {master_video.stat().st_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    build_motion_comic()
