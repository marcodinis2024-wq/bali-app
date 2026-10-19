#!/usr/bin/env bash
# Espera a renderização 16:9 terminar e depois renderiza a 9:16 em 4K.
cd "$(dirname "$0")"
until [ "$(ls frames_story 2>/dev/null | wc -l)" -ge 3000 ]; do sleep 20; done
mkdir -p frames_story_916
export NODE_PATH=/opt/node22/lib/node_modules DPR=2 VW=1080 VH=1920 OUT=frames_story_916 PAGE=ad_story_916.html
(node render_story_916.js 0 750 & node render_story_916.js 750 1500 & node render_story_916.js 1500 2250 & node render_story_916.js 2250 3000 & wait)
echo "916 frames done"
