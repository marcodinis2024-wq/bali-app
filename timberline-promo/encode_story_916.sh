#!/usr/bin/env bash
# Monta o anúncio 9:16 em 4K e pré-visualizações leves.
cd "$(dirname "$0")"
FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
$FF -hide_banner -loglevel error -y -framerate 60 -i frames_story_916/%05d.jpg -i audio_story.wav \
  -c:v libx264 -preset medium -b:v 40M -maxrate 60M -bufsize 80M -pix_fmt yuv420p -profile:v high -level 5.1 -r 60 -g 120 \
  -c:a aac -b:a 320k -af loudnorm=I=-14:TP=-1:LRA=11 -ar 48000 -movflags +faststart -shortest timberline-story-9x16-4k-60fps.mp4
$FF -hide_banner -loglevel error -y -i timberline-story-9x16-4k-60fps.mp4 -vf scale=1080:1920 \
  -c:v libx264 -preset medium -b:v 3M -maxrate 4M -bufsize 6M -pix_fmt yuv420p -r 60 -c:a aac -b:a 128k -movflags +faststart preview-9x16-1080p.mp4
echo ENCODE_916_DONE
