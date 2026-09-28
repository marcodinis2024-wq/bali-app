#!/usr/bin/env bash
# Renderiza o anúncio: 1920x1080, 60 fps, 42 s, H.264 + AAC.
# Requisitos: node + playwright (Chromium), python3 com numpy, scipy e pillow, ffmpeg.
set -euo pipefail
cd "$(dirname "$0")"
FPS=60; TOTAL=$((42 * FPS)); JOBS=${JOBS:-4}

if [[ "${RECAPTURE:-0}" == "1" ]]; then     # voltar a fotografar a app (APP_HTML=/caminho/index.html)
  node capture.js && python3 prep_shots.py
fi

python3 audio.py                            # música + efeitos sonoros → audio.wav

mkdir -p frames
STEP=$(( (TOTAL + JOBS - 1) / JOBS ))
for ((i = 0; i < JOBS; i++)); do
  a=$((i * STEP)); b=$(( a + STEP < TOTAL ? a + STEP : TOTAL ))
  node render_frames.js "$a" "$b" &
done
wait

ffmpeg -y -framerate $FPS -i frames/%05d.jpg -i audio.wav \
  -c:v libx264 -preset slow -b:v 12M -maxrate 18M -bufsize 24M -pix_fmt yuv420p -profile:v high -level 4.2 -r $FPS -g 120 \
  -c:a aac -b:a 320k -af loudnorm=I=-14:TP=-1:LRA=11 -movflags +faststart -shortest \
  bali-promo-16x9-60fps.mp4
