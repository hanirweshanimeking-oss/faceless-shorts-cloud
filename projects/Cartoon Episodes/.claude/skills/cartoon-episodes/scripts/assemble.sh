#!/usr/bin/env bash
# assemble.sh — stitch the scene clips of one episode into episode.mp4.
# Dialogue and sound live inside each clip, so this is a straight concat at a
# uniform size and fps. Usage: assemble.sh <project_dir> [--aspect 16:9|9:16]
set -euo pipefail
DIR="${1:?usage: assemble.sh <project_dir> [--aspect 16:9]}"; shift
ASPECT="16:9"
while [ $# -gt 0 ]; do case "$1" in --aspect) ASPECT="$2"; shift 2;; *) echo "unknown arg $1"; exit 1;; esac; done
for b in ffmpeg ffprobe; do command -v $b >/dev/null || { echo "$b not found (brew install ffmpeg)"; exit 1; }; done
case "$ASPECT" in 16:9) W=1920; H=1080;; 9:16) W=1080; H=1920;; *) echo "aspect must be 16:9 or 9:16"; exit 1;; esac
cd "$DIR"
clips=(scenes/*.mp4)
[ -e "${clips[0]}" ] || { echo "no clips at scenes/*.mp4"; exit 1; }
N=${#clips[@]}
FPS=$(ffprobe -v 0 -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "${clips[0]}")
i=0; vin=""; fc=""; vmap=""
for clip in "${clips[@]}"; do
  vin="$vin -i $clip"
  if ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$clip" | grep -q .; then
    fc="$fc[$i:a]aformat=sample_rates=48000:channel_layouts=stereo[a$i];"
  else
    fc="$fc anullsrc=r=48000:cl=stereo,atrim=duration=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$clip")[a$i];"
  fi
  fc="$fc[$i:v]scale=$W:$H:flags=lanczos:force_original_aspect_ratio=decrease,pad=$W:$H:(ow-iw)/2:(oh-ih)/2,fps=${FPS},setpts=PTS-STARTPTS[v$i];"
  vmap="$vmap[v$i][a$i]"; i=$((i+1))
done
ffmpeg -loglevel error -y $vin -filter_complex "${fc}${vmap}concat=n=$N:v=1:a=1[v][ca];[ca]loudnorm=I=-16:TP=-1.5[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset veryfast -crf 17 -pix_fmt yuv420p -c:a aac -b:a 192k episode.mp4
ffprobe -v error -show_entries stream=width,height:format=duration -of default=noprint_wrappers=1 episode.mp4
echo "done → $DIR/episode.mp4 ($N scenes)"
