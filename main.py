import sys
import pygame as pg

pg.init()
clock = pg.time.Clock()
tps = 20

SIZE = 800, 800
sc = pg.display.set_mode(SIZE)

is_setting_rules = True
is_setting_squares = False
running = False

board = []

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYUP:
            if event.key == pg.K_r:
                board.clear()
                running = False
                is_setting_squares = False
                is_setting_rules = True

    pg.display.update()
