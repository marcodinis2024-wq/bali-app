#!/usr/bin/env bash
# Renderiza o anúncio Timberline: 1920x1080, 60 fps, 42 s, H.264 + AAC.
# Requisitos: node + playwright (Chromium), python3 com numpy e scipy, ffmpeg.
set -euo pipefail
cd "$(dirname "$0")"
FPS=60; TOTAL=$((42 * FPS)); JOBS=${JOBS:-4}
export PAGE=ad.html W=1920 H=1080 OUT=frames
python3 audio.py
mkdir -p "$OUT"
STEP=$(( (TOTAL + JOBS - 1) / JOBS ))
for ((i = 0; i < JOBS; i++)); do
  a=$((i * STEP)); b=$(( a + STEP < TOTAL ? a + STEP : TOTAL ))
  node render_frames.js "$a" "$b" &
done
wait
ffmpeg -y -framerate $FPS -i "$OUT/%05d.jpg" -i audio.wav \
  -c:v libx264 -preset slow -b:v 12M -maxrate 18M -bufsize 24M -pix_fmt yuv420p -profile:v high -level 4.2 -r $FPS -g 120 \
  -c:a aac -b:a 320k -af loudnorm=I=-14:TP=-1:LRA=11 -ar 48000 -movflags +faststart -shortest \
  timberline-promo-16x9-60fps.mp4
