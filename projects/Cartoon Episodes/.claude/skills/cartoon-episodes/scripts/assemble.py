#!/usr/bin/env python3
"""
assemble.py — stitch the scene clips of one episode into episode.mp4.
Dialogue and sound live inside each clip, so this is a straight concat at a
uniform size and fps.
Usage: python assemble.py <project_dir> [--aspect 16:9|9:16]
"""
import sys
import os
import glob
import subprocess
import argparse

def assemble(project_dir, aspect="16:9"):
    project_dir = os.path.abspath(project_dir)
    if aspect == "16:9":
        w, h = 1920, 1080
    elif aspect == "9:16":
        w, h = 1080, 1920
    else:
        raise ValueError("aspect must be 16:9 or 9:16")

    scenes_dir = os.path.join(project_dir, "scenes")
    clips = sorted(glob.glob(os.path.join(scenes_dir, "*.mp4")))
    if not clips:
        print(f"Error: no clips at {scenes_dir}/*.mp4")
        sys.exit(1)

    n = len(clips)
    first_clip = clips[0]

    fps_res = subprocess.run([
        "ffprobe", "-v", "0", "-select_streams", "v:0",
        "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", first_clip
    ], capture_output=True, text=True)
    fps = fps_res.stdout.strip() or "30"

    vin = []
    fc = []
    vmap = []

    for i, clip in enumerate(clips):
        vin.extend(["-i", clip])
        a_check = subprocess.run([
            "ffprobe", "-v", "error", "-select_streams", "a",
            "-show_entries", "stream=index", "-of", "csv=p=0", clip
        ], capture_output=True, text=True)
        has_audio = bool(a_check.stdout.strip())

        if has_audio:
            fc.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo[a{i}];")
        else:
            dur_check = subprocess.run([
                "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", clip
            ], capture_output=True, text=True)
            dur = dur_check.stdout.strip() or "5"
            fc.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={dur}[a{i}];")

        fc.append(f"[{i}:v]scale={w}:{h}:flags=lanczos:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,fps={fps},setpts=PTS-STARTPTS[v{i}];")
        vmap.append(f"[v{i}][a{i}]")

    fc_str = "".join(fc) + "".join(vmap) + f"concat=n={n}:v=1:a=1[v][ca];[ca]loudnorm=I=-16:TP=-1.5[a]"
    output_path = os.path.join(project_dir, "episode.mp4")

    cmd = ["ffmpeg", "-loglevel", "error", "-y"] + vin + [
        "-filter_complex", fc_str,
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        output_path
    ]

    res = subprocess.run(cmd)
    if res.returncode != 0:
        print(f"ffmpeg failed with exit code {res.returncode}")
        sys.exit(res.returncode)

    subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "stream=width,height:format=duration",
        "-of", "default=noprint_wrappers=1", output_path
    ])
    print(f"done -> {output_path} ({n} scenes)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir", help="Project directory")
    parser.add_argument("--aspect", default="16:9", choices=["16:9", "9:16"])
    args = parser.parse_args()
    assemble(args.project_dir, args.aspect)
