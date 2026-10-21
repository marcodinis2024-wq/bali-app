# Timberline · colagem em papel rasgado · 30 s · 16:9

Brief para correr no Mac com a skill `paper-collage-film`.
Sem fotografias e sem vetores: só papel rasgado (formas recortadas, bordas de fibra branca, texturas,
meio-tom gerado em código) e tipografia. Sem IA gerativa. Movimento "a dois tempos" (12 desenhos/s).
Música e efeitos sonoros: `audio/score.wav` (gerado por `audio_collage.py`), 120 BPM, grelha de 0,5 s.

Texto em português, como o site (a skill usa inglês por defeito; isto é uma decisão a confirmar).

| tempo | música | o que se vê | texto no ecrã (verbatim) | som |
|---|---|---|---|---|
| 0.00–1.50 | silêncio, um batimento | página preta; uma tira de papel rasga-se do centro | "Tudo começa com uma linha." | rasgo de papel |
| 1.50–4.00 | entra o groove (1.5) | a página branca cai com a marca; a palavra TIMBERLINE em caixa alta | TIMBERLINE · WOOD FRAME | queda + pop |
| 4.00–8.00 | sobe o baixo | seis separadores de papel saltam um a um | Início · Sistema · Diferenciais · Serviços · Projetos · Contacto | estalos por separador |
| 8.00–13.00 | refrão (8.0) | cinco camadas de papel empilham-se, cada uma com a sua cor | 01 Fundação · 02 Estrutura · 03 Contraventamento · 04 Isolamento · 05 Fachada · "Cinco camadas, uma só casa." | batida por camada |
| 13.00–17.00 | quebra (13.0) | página dividida: à esquerda papel creme TIMBERLINE, à direita cinzento riscado STANDARD | "Onde o mercado standard para, nós continuamos." | tesoura + tique por linha |
| 17.00–21.00 | groove volta (17.0) | três cartões de papel viram-se para a frente | 01 Moradias Personalizadas · 02 Chave na Mão · 03 Estruturas em Madeira | flip + pop |
| 21.00–24.00 | build (21.0) | seis azulejos de papel com legendas, em grelha | Projetos · Casas Timberline | pops em sequência |
| 24.00–27.00 | cordas, sem bateria | formulário de papel escreve-se letra a letra; botão "Falar Connosco" | "Vamos construir a sua casa." | teclas + clique |
| 27.00–30.00 | resolução (27.0) | rasgo final leva ao logótipo; última pancada | Em breve no ar · geraltimberline@gmail.com | rasgo + sino final |

## Regras de produção
- Cada evento de imagem cai numa batida (0,5 s). Sincronizar pelo `score.html`, não à mão.
- Nada fica parado mais de 1 s, exceto o título final e o logótipo (≥ 1,5 s).
- Nenhum elemento tapa o texto; o rasgo final não pode cortar o logótipo.
- Sem flashes de ecrã inteiro (fotossensibilidade).
- Texto de cada etiqueta ≥ 36 px e cada uma ≥ 0,8 s no ecrã.
