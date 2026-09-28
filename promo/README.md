# Bali Food & Drinks — vídeo promocional

`bali-promo-16x9-60fps.mp4` — anúncio de 42 s, 1920×1080, 60 fps, H.264 + AAC (−14 LUFS).

Mostra a ementa digital real ([bali-food-drinks](https://github.com/marcodinis2024-wq/bali-food-drinks)).
Todas as imagens dentro do telemóvel são capturas da própria app.

## Guião

| Tempo | Cena | O que mostra | Som |
|---|---|---|---|
| 0–2 s | **Gancho** | "Fome?" surge em pop e aparecem autocolantes de comida | whoosh, pop, cascata de pops |
| 2–4 s | **Marca** | Selo Bali (EST. 2018) com impacto e o texto "agora no telemóvel" | boom, flash, brilho |
| 4–8 s | **A app** | Telemóvel entra em 3D, faz scroll no início; aparecem os balões *Aberto agora*, *4,8 ★*, *PT·EN* | whoosh, pops |
| 8–12 s | **142 pratos** | Contador 0→142, 16 categorias, scroll rápido da ementa | ticks, ding, pops |
| 12–16 s | **Procura. Filtra. Encontra.** | Toque no filtro Vegan, escreve "manga" letra a letra, etiquetas | toques, teclado |
| 16–20 s | **Personaliza** | Abre o Açaí Bowl, o painel sobe, +1 e o preço passa de 8,00 € para 16,00 € | swoosh, toque, pop |
| 20–24 s | **Junta à mesa!** | Toast "Juntámos à mesa", pratos voam para o separador Mesa (2→5), confettis | ka-ching, pops, brilho |
| 24–28 s | **A tua mesa, pronta.** | Take-away, notas, total a contar até 51,00 € | pops, ticks, ding |
| 28–32 s | **Envia por WhatsApp** | O pedido voa para o chat, visto azul, "Pedido enviado!" | swoosh, ding duplo, boom |
| 32–36 s | **Tudo num só sítio** | 3 telemóveis (EN, horário, avaliações) com etiquetas | pops |
| 36–42 s | **Final** | Selo, "Comida fresca, feita no momento.", CTA, morada e @instagram | boom, final |

Música original gerada por código (`audio.py`, 120 BPM, Sol maior): marimba, steel pan, baixo, kick com sidechain.
As pausas antes da cena WhatsApp e do final servem para dar respiração.

## Voltar a renderizar

```bash
cd promo
./render.sh                  # usa as capturas em shots/
RECAPTURE=1 APP_HTML=/caminho/para/bali-food-drinks/index.html ./render.sh   # volta a fotografar a app
```

Para ver a animação em tempo real no browser, abra `ad.html#play`.

- `ad.html` — a composição inteira; `render(t)` desenha o frame no instante `t` (determinístico).
- `audio.py` — música e efeitos, com os tempos sincronizados com `ad.html`.
- `capture.js` / `prep_shots.py` — capturas da app (390×844 @2x).
- `render_frames.js` — exporta os frames com o Playwright; o `ffmpeg` junta imagem e som.
- `fonts/` — Fraunces, Outfit e Yellowtail (Google Fonts, licença OFL) incluídas localmente, para o render não depender da rede.
