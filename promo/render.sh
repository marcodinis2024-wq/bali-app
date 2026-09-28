#!/usr/bin/env bash
# Renderiza o anúncio a 60 fps, 42 s, H.264 + AAC.
#   ./render.sh          → 16:9 (1920x1080)
#   FORMAT=916 ./render.sh → 9:16 (1080x1920, Reels/TikTok/Stories)
# Requisitos: node + playwright (Chromium), python3 com numpy, scipy e pillow, ffmpeg.
set -euo pipefail
cd "$(dirname "$0")"
FPS=60; TOTAL=$((42 * FPS)); JOBS=${JOBS:-4}

if [[ "${FORMAT:-169}" == "916" ]]; then
  python3 make_916.py
  export PAGE=ad_916.html W=1080 H=1920 OUT=frames_916; NAME=bali-promo-9x16-60fps.mp4
else
  export PAGE=ad.html W=1920 H=1080 OUT=frames; NAME=bali-promo-16x9-60fps.mp4
fi

if [[ "${RECAPTURE:-0}" == "1" ]]; then     # voltar a fotografar a app (APP_HTML=/caminho/index.html)
  node capture.js && python3 prep_shots.py
fi

python3 audio.py                            # música + efeitos sonoros → audio.wav

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
  "$NAME"
