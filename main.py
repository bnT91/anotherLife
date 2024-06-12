import sys
import pygame as pg

pg.init()
clock = pg.time.Clock()
tps = 40

SIZE = 800  # cell size 25
sc = pg.display.set_mode((SIZE, SIZE))
pg.display.set_caption("anotherLife")

is_setting_rules = True
is_setting_cells = False
running = False

board = list()
rules = []  # B/S
active1 = False
active2 = False
text1 = ""
text2 = ""
textbox1 = pg.draw.rect(sc, "Black", (150, 200, 600, 100), 5)
textbox2 = pg.draw.rect(sc, "Black", (150, 500, 600, 100), 5)
allowed_symbols = [ord(str(i)) for i in range(9)]

speed = 10

myfont = pg.font.Font("fonts/Sonic Logo RUS/Sonic Logo Bold RUS by vania5617sonfan.ttf", 100)
_myfont = pg.font.Font("fonts/Sonic Logo RUS/Sonic Logo Bold RUS by vania5617sonfan.ttf", 80)

btns = [pg.transform.scale(pg.image.load("img/btn.png"), (200, 100)), pg.transform.scale(pg.image.load("img/btn_hover.png"), (200, 100))]
currbtn = 0

frame = 0
flag = True
fl = True
f = 0

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
        sc.blit(btns[currbtn], (300, 650))

        if active1:
            if flag:
                frame = 0
            flag = False
            frame += 1
            if frame == tps:
                frame = 0
            if frame <= tps//2:
                cursor1 = pg.draw.rect(sc, "Black", (150 + text1_surf.get_width() + 10, 210, 5, 80))
        if active2:
            if not flag:
                frame = 0
            flag = True
            frame += 1
            if frame == tps:
                frame = 0
            if frame <= tps//2:
                cursor2 = pg.draw.rect(sc, "Black", (150 + text2_surf.get_width() + 10, 510, 5, 80))

        btn_rect = pg.rect.Rect(300, 650, 200, 100)
        if btn_rect.collidepoint(pg.mouse.get_pos()):
            currbtn = 1
        else:
            currbtn = 0
    elif is_setting_cells:
        for x in range(32):
            for y in range(32):
                pg.draw.rect(sc, "Grey", (x*25, y*25, 25, 25), 1)

        for cell in board:
            pg.draw.rect(sc, "Black", (cell[0]*25, cell[1]*25, 25, 25))

        pos = pg.mouse.get_pos()
        if pg.mouse.get_pressed()[0]:
            if not fl:
                new_cell_coords = [pos[0] // 25, pos[1] // 25]
                if new_cell_coords not in board:
                    board.append(new_cell_coords)
        elif pg.mouse.get_pressed()[2]:
            del_cell_coords = [pos[0] // 25, pos[1] // 25]
            if del_cell_coords in board:
                board.remove(del_cell_coords)
    else:
        for x in range(32):
            for y in range(32):
                pg.draw.rect(sc, "Grey", (x*25, y*25, 25, 25), 1)

        for draw_cell in board:
            pg.draw.rect(sc, "Black", (draw_cell[0]*25, draw_cell[1]*25, 25, 25))

        f += 1
        if f >= speed:
            f = 0
            next_generation = []
            for x in range(32):
                for y in range(32):
                    neighbours = []
                    for new_neighbour in [[x-1, y-1], [x-1, y], [x-1, y+1],
                                          [x, y-1],               [x, y+1],
                                          [x+1, y-1], [x+1, y], [x+1, y+1]]:
                        if 0 <= new_neighbour[0] <= 31 and 0 <= new_neighbour[1] <= 31 and new_neighbour in board:
                            neighbours.append(new_neighbour)

                    if [x, y] in board:
                        if len(neighbours) in rules[1]:
                            next_generation.append([x, y])
                    else:
                        if len(neighbours) in rules[0]:
                            next_generation.append([x, y])

            board = next_generation

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
            if event.key == pg.K_RETURN:
                if is_setting_cells:
                    is_setting_cells = False
                    running = True
            if event.key == pg.K_UP:
                speed += 1
                print(speed)
            if event.key == pg.K_DOWN:
                if speed >= 2:
                    speed -= 1
                print(speed)
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

                btn_rect = pg.rect.Rect(300, 650, 200, 100)
                if btn_rect.collidepoint(pos):
                    rules = [[int(i) for i in text1], [int(j) for j in text2]]
                    is_setting_rules = False
                    is_setting_cells = True
                    fl = True
        if event.type == pg.MOUSEBUTTONUP:
            if is_setting_cells:
                fl = False

    clock.tick(tps)
    pg.display.update()
