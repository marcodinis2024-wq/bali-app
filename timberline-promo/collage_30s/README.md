# Timberline · colagem em papel rasgado (30 s) — para correr no Mac

Este pacote tem o guião e a banda sonora; a imagem é gerada no Mac pela skill `paper-collage-film`,
que precisa de macOS (Swift, AVFoundation, `afconvert`).

- `script.md` — tabela de batidas de 30 s (tempos, texto verbatim, som de cada evento).
- `audio/score.wav` — música e efeitos sonoros originais, 30,00 s, 48 kHz, estéreo (120 BPM).
- `audio_collage.py` — o código que gera o `score.wav` (para alterar tempos ou sons).

## Passos no Mac
1. Copiar esta pasta para o Mac.
2. Pedir ao Claude Code no Mac: *"usa a skill paper-collage-film com o brief em `collage_30s/script.md`
   e a música em `collage_30s/audio/score.wav`"*.
3. A skill converte a música com `afconvert -f m4af -d aac -b 256000 audio/score.wav audio/score.m4a`
   e renderiza com `tools/render_film.sh final audio/score.m4a timberline_final.mp4`.

## Decisões já tomadas
- Sem fotografias e sem vetores: só papel rasgado, texturas, meio-tom e tipografia.
  Na skill, isto quer dizer não gerar recortes fotográficos (passo 4) e desenhar tudo em código.
- Texto em português, como o site (a skill usa inglês por defeito).
- Música sintetizada aqui; o `score.html` da skill fica de lado.
- Sem flashes de ecrã inteiro.
