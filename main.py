import sys
import pygame as pg

pg.init()
clock = pg.time.Clock()
tps = 20

SIZE = 800  # cell size 50
sc = pg.display.set_mode((SIZE, SIZE))
pg.display.set_caption("anotherLife")

is_setting_rules = True
is_setting_cells = False
running = False

board = []
rules = [{3}, {2, 3}]  # B/S
active1 = False
active2 = False
text1 = ""
text2 = ""
textbox1 = pg.draw.rect(sc, "Black", (150, 200, 600, 100), 5)
textbox2 = pg.draw.rect(sc, "Black", (150, 500, 600, 100), 5)
allowed_symbols = [ord(str(i)) for i in range(10)]

myfont = pg.font.Font("fonts/Sonic Logo RUS/Sonic Logo Bold RUS by vania5617sonfan.ttf", 100)
_myfont = pg.font.Font("fonts/Sonic Logo RUS/Sonic Logo Bold RUS by vania5617sonfan.ttf", 80)

frame = 0
flag = True

while True:
    sc.fill("White")
    if is_setting_rules:
        textbox1 = pg.draw.rect(sc, "Black", (150, 200, 600, 100), 5)
        textbox2 = pg.draw.rect(sc, "Black", (150, 500, 600, 100), 5)
        b_text = myfont.render("B", True, "Black")
        s_text = myfont.render("S", True, "Black")
        sc.blit(b_text, (10, 200))
        sc.blit(s_text, (10, 500))
        text1_surf = _myfont.render(text1, True, "Black")
        text2_surf = _myfont.render(text2, True, "Black")
        sc.blit(text1_surf, (160, 205))
        sc.blit(text2_surf, (160, 505))

        if active1:
            if flag:
                frame = 0
            flag = False
            frame += 1
            if frame == 20:
                frame = 0
            if frame <= 10:
                cursor1 = pg.draw.rect(sc, "Black", (150 + text1_surf.get_width() + 10, 210, 5, 80))
        if active2:
            if not flag:
                frame = 0
            flag = True
            frame += 1
            if frame == 20:
                frame = 0
            if frame <= 10:
                cursor2 = pg.draw.rect(sc, "Black", (150 + text2_surf.get_width() + 10, 510, 5, 80))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYUP:
            if event.key == pg.K_r:
                board.clear()
                running = False
                is_setting_cells = False
                is_setting_rules = True
            if event.key in allowed_symbols:
                if active1:
                    if chr(event.key) not in text1:
                        text1 += chr(event.key)
                elif active2:
                    if chr(event.key) not in text2:
                        text2 += chr(event.key)
            elif event.key == pg.K_BACKSPACE:
                if active1:
                    if text1:
                        text1 = text1[:-1]
                if active2:
                    if text2:
                        text2 = text2[:-1]
        if event.type == pg.MOUSEBUTTONDOWN:
            if is_setting_rules:
                pos = event.pos
                if textbox1.collidepoint(pos):
                    active1 = True
                    active2 = False
                elif textbox2.collidepoint(pos):
                    active1 = False
                    active2 = True
                else:
                    active1 = False
                    active2 = False

    clock.tick(tps)
    pg.display.update()
