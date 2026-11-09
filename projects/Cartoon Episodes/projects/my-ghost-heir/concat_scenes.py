import subprocess
import os

FFMPEG = r"C:\Users\DESKTOP\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"
PROJECT_DIR = r"c:\Users\DESKTOP\Downloads\money\Cartoon Episodes\projects\my-ghost-heir"
SCENES_DIR = os.path.join(PROJECT_DIR, "scenes")

s1 = os.path.join(SCENES_DIR, "01-the-awakening.mp4")
s2 = os.path.join(SCENES_DIR, "02-the-blood-oath.mp4")
s3 = os.path.join(SCENES_DIR, "03-the-first-command.mp4")

list_txt = os.path.join(PROJECT_DIR, "concat_list.txt")
with open(list_txt, "w", encoding="utf-8") as f:
    f.write(f"file '{s1.replace(chr(92), '/')}'\n")
    f.write(f"file '{s2.replace(chr(92), '/')}'\n")
    f.write(f"file '{s3.replace(chr(92), '/')}'\n")

out_mp4 = os.path.join(PROJECT_DIR, "episode.mp4")

cmd = [
    FFMPEG, "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", list_txt,
    "-c", "copy",
    out_mp4
]

res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    print(f"SUCCESS: {out_mp4} ({os.path.getsize(out_mp4)} bytes)")
else:
    print("Direct copy concat failed, trying filter concat...")
    # fallback to re-encode filter concat
    cmd2 = [
        FFMPEG, "-y",
        "-i", s1, "-i", s2, "-i", s3,
        "-filter_complex", "[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[v][a]",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
        out_mp4
    ]
    res2 = subprocess.run(cmd2, capture_output=True, text=True)
    if res2.returncode == 0:
        print(f"SUCCESS FILTER CONCAT: {out_mp4} ({os.path.getsize(out_mp4)} bytes)")
    else:
        print(f"ERROR: {res2.stderr}")
