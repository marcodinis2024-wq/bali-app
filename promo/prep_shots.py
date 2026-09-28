# Recorta a ementa longa e as barras de separadores a partir das capturas.
from PIL import Image
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots'))
Image.open('menu_full.png').crop((0, 0, 780, 7000)).save('menu_long.png')
for src, dst in [('home', 'tab_home'), ('menu', 'tab_menu'), ('table2', 'tab_table')]:
    Image.open(f'{src}.png').crop((0, 1688 - 136, 780, 1688)).save(f'{dst}.png')
