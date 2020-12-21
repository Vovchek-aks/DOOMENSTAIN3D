import pygame as pg
from map import *
from settings import *
from player import Player
import math


def raycast(sc, player):
    for i in range(lines):
        dist = 255
        a = player.ang + line_step * i - line_step * lines / 2
        cos = math.cos(a)
        sin = math.sin(a)
        for j in range(0, draw_dist, 8):
            xx = player.x + j * cos
            yy = player.y + j * sin
            if (int(xx // rect_size2d * rect_size2d), int(yy // rect_size2d * rect_size2d)) in map_coords:
                dist = j / 4
                break

        # pg.draw.line(sc, red, player.pos, (xx, yy), 1)

        dist *= math.cos(player.ang - a)

        c = 255 / (1 + dist * dist * 0.0001)
        if c < 0:
            c = 0
        elif c > 200:
            c = 200

        if (bese_wall_h - dist * 1.5) * 2 > 0:
            pg.draw.rect(sc, (55 + c, 20 + c, c / 2), (i * line_to_px,
                                                   height / 2 - bese_wall_h + dist * 1.5,
                                                   line_to_px + 1,
                                                   (bese_wall_h - dist * 1.5) * 2))
        else:
            pg.draw.rect(sc, (55 + c, 55 + c, c), (i * line_to_px,
                                                   height / 2 - 1,
                                                   line_to_px + 1,
                                                   2))


def main():
    pg.init()
    sc = pg.display.set_mode((size[0] * rect_size2d,
                              size[1] * rect_size2d))

    running = True
    clock = pg.time.Clock()

    player = Player()

    while running:
        sc.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        raycast(sc, player)
        draw_map(sc)
        player.step(sc)
        pg.display.flip()
        clock.tick(FPS)

    pg.quit()


def draw_map(sc):
    for i in map_coords:
        pg.draw.rect(sc, white, (i[0], i[1], rect_size2d, rect_size2d), 1)


if __name__ == '__main__':
    main()
