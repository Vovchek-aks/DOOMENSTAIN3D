import pygame as pg
from map import *
from settings import *
from player import Player
import math


def raycast(sc, player):
    ret = []
    for i in range(lines):
        dist = 255
        a = player.ang + line_step * i - line_step * lines / 2

        cos = math.cos(a)
        sin = math.sin(a)
        for j in range(0, draw_dist, 10):
            xx = player.x + j * cos
            yy = player.y + j * sin
            if (int(xx // rect_size2d * rect_size2d), int(yy // rect_size2d * rect_size2d)) in map_coords:
                dist = j / 4
                break

        dist *= math.cos(player.ang - a)  # inposter tyt!!!!!!!!!!!!!!!!!!!

        # dist *= abs(lines / 2 - i) / 100 + 0000.1

        ret += [((xx, yy), dist)]

        c = 255 / (1 + dist ** 2 * 0.0001)

        if c < 1:
            c = 1
        elif c > 255:
            c = 255

        color = [c / 2, c / 3, c / 5]

        for cc in range(len(color)):
            if color[cc] < 0:
                color[cc] = 0
            elif color[cc] > 255:
                color[cc] = 255

        # dist /= abs(lines / 2 - i) + 0.1

        if (bese_wall_h - dist) * 2 > 0:
            pg.draw.rect(sc, color, (i * line_to_px,
                                     height / 2 - bese_wall_h + dist,
                                     line_to_px + 1,
                                     (bese_wall_h - dist) * 2))  # i tyt!!!!!!!!!!!!
        else:
            pg.draw.rect(sc, color, (i * line_to_px,
                                     height / 2 - 2,
                                     line_to_px + 1,
                                     4))

    return ret


def main():
    pg.init()
    sc = pg.display.set_mode((width, height))
    # pg.display.toggle_fullscreen()

    running = True
    clock = pg.time.Clock()

    player = Player()

    while running:
        sc.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

        draw_3d(sc)
        lin = raycast(sc, player)
        draw_map(sc, player, lin)
        player.step(sc)
        pg.display.flip()
        clock.tick(FPS)

    pg.quit()


def draw_map(sc, player, lines):
    for i in map_coords:
        pg.draw.rect(sc, white, (i[0], i[1], rect_size2d, rect_size2d), 1)
    player.draw(sc)
    for i in lines:
        pg.draw.line(sc, gray, player.pos, i[0], 1)


def draw_3d(sc):
    pg.draw.rect(sc, (20, 150, 250), (0, 0, width, height / 2))
    pg.draw.rect(sc, (70, 50, 10), (0, height / 2, width, height))


if __name__ == '__main__':
    main()
