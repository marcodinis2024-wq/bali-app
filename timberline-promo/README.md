# Timberline — vídeo promocional

`timberline-promo-16x9-60fps.mp4` — anúncio de 42 s, 1920×1080, 60 fps, H.264 + AAC (−14 LUFS).

Motion graphics 100% em código, com o mesmo método do vídeo do Bali: sem IA generativa e sem imagens externas.
Os textos, as especificações técnicas, os serviços e os contactos vêm do site da Timberline.
A casa é desenhada em vetores isométricos e construída camada a camada, como o "Sistema construtivo" do site.

## Guião

| Tempo | Cena | O que mostra | Som |
|---|---|---|---|
| 0–2 s | **Gancho** | "Não construímos casas de madeira." | linha dourada, ticks, riser |
| 2–4 s | **Viragem** | "Construímos **engenharia** com a alma da madeira." | boom, flash |
| 4–8 s | **Marca** | O emblema desenha-se, depois TIMBERLINE · Construção Wood Frame e "Construímos hoje os lares de amanhã." A grelha e o lote desenham-se | brilho, whoosh |
| 8–28 s | **Construção, 6 passos** | 01 Fundação (XPS + laje) · 02 Estrutura (vigas Classe IV) · 03 Contraventamento (OSB 3/4) · 04 Isolamento (fibra de madeira, fusão térmica, vidros) · 05 Fachada (ETICS, pedra, ripado) · 06 Conforto interior (luz quente, VMC) | batidas de madeira, pregos, painéis, chiado, vidro, ar |
| 28–32 s | **A porta está aberta.** | Cai a noite, aparecem os pinheiros e a casa acende-se. Chave na mão · À medida | boom, interruptor |
| 32–36 s | **Diferenciais** | Timberline vs Standard: 4 comparações | whooshes |
| 36–39 s | **Serviços** | Moradias Personalizadas · Chave na Mão · Estruturas em Madeira | pops |
| 39–42 s | **Final** | "Vamos construir a sua casa." Iniciar Conversa, telefones e email | acorde final |

Paleta e tipografia do site: fundo `#0b0a08`, dourado `#E3B65A`, Inter Tight e JetBrains Mono.
A Cabinet Grotesk (Fontshare) não estava acessível, por isso os títulos usam a Archivo, uma grotesca pesada semelhante.
O emblema é uma recriação vetorial; para usar o logótipo original, substitua o SVG `#emb`/`#emb2` em `ad.html`.

## Voltar a renderizar

```bash
cd timberline-promo && ./render.sh
```
Para ver em tempo real: abra `ad.html#play`.
