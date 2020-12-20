import pygame as pg
from map import *
from settings import *
from player import Player
import math


def raycast(sc, player):
    for i in range(lines):
        dist = 255
        a = player.ang - (fow * 2) + line_step * i
        cos = math.cos(a)
        sin = math.sin(a)
        for j in range(0, draw_dist, 8):
            xx = player.x + j * cos
            yy = player.y + j * sin
            if (int(xx // rect_size2d * rect_size2d), int(yy // rect_size2d * rect_size2d)) in map_coords:
                dist = j / 4
                break

        # pg.draw.line(sc, gray, player.pos, (xx, yy), 1)

        color = (255 - dist * 0.5,
                 255 - dist * 0.5,
                 255 - dist * 0.5)

        pg.draw.rect(sc, color, (i * line_to_px,
                                 height / 2 - bese_wall_h + dist * 2,
                                 line_to_px, (bese_wall_h - dist * 2) * 2))


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

        # draw_map(sc)
        player.step(sc)
        raycast(sc, player)
        pg.display.flip()
        clock.tick(FPS)

    pg.quit()


def draw_map(sc):
    for i in map_coords:
        pg.draw.rect(sc, white, (i[0], i[1], rect_size2d, rect_size2d), 1)


if __name__ == '__main__':
    main()
