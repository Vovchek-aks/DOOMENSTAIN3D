import pygame as pg
from map import *
from settings import *
from player import Player
import math


# def raycast(sc, player):
#     ret = []
#     for i in range(lines):
#         dist = 999
#         a = player.ang + line_step * i - line_step * lines / 2
#
#         cos = math.cos(a)
#         sin = math.sin(a)
#         for j in range(0, draw_dist, 5):
#             xx = player.x + j * cos
#             yy = player.y + j * sin
#
#             if (int(xx // rect_size2d * rect_size2d), int(yy // rect_size2d * rect_size2d)) in map_coords:
#                 j *= math.cos(player.ang - a)
#
#                 c = 255 / (1 + j * j * 0.00001)
#                 color = (int(c / 2), int(c / 3), int(c / 5))
#
#                 ret += [((xx, yy), j)]
#
#                 pg.draw.rect(sc, color, (i * line_to_px,
#                                          height / 2 - dist * rect_size2d / (j + 1),
#                                          line_to_px + 1,
#                                          dist * rect_size2d / (j + 1) * 2))
#
#                 break
#
#     return ret


def raycast(sc, player):
    x, y = player.x // rect_size2d * rect_size2d, player.y // rect_size2d * rect_size2d

    for i in range(lines):

        a = player.ang + line_step * i - line_step * lines / 2
        cos = math.cos(a)
        sin = math.sin(a)

        # смотрим на пересечение с вертикалями
        vertical, dop_inf_x = (x + rect_size2d, 1) if cos >= 0 else (x, -1)
        for j in range(0, width, rect_size2d):
            rast_vert = (vertical - x) / cos
            y_vert = player.y + rast_vert * sin
            if rast_vert // rect_size2d * rect_size2d in map_coords and y_vert // rect_size2d * rect_size2d \
                    in map_coords:
                break
            rast_vert += dop_inf_x * rect_size2d

        # смотрим на пересечение с горизонталями
        horisontal, dop_inf_y = (y + rect_size2d, 1) if sin >= 0 else (y, -1)
        for j in range(0, height, rect_size2d):
            rast_hor = (horisontal - y) / (sin - 1)
            x_hor = player.x + rast_hor * cos
            if rast_hor // rect_size2d * rect_size2d in map_coords and x_hor // rect_size2d * rect_size2d \
                    in map_coords:
                break
            rast_hor += dop_inf_y * rect_size2d
        rast = rast_vert if rast_hor < rast_hor else rast_hor
        rast *= math.cos(player.ang - a)

        c = 255 / (1 + rast * rast * 0.00001)
        color = (int(c / 2), int(c / 3), int(c / 5))

        pg.draw.rect(sc, color, (i * line_to_px,
                                 height / 2 - 999 * rect_size2d // 2,
                                 line_to_px + 1,
                                 rast * rect_size2d // 2))


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
        # draw_map(sc, player, lin)
        draw_minimap(sc, player)
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


def draw_minimap(sc, player):
    pg.draw.rect(sc, black, (0, 0, rect_size2d // 4 * len(map_[0]), rect_size2d // 4 * len(map_)))
    for i in map_coords:
        # print(i[0], i[1], rect_size2d)
        pg.draw.rect(sc, gray, (i[0] // 4, i[1] // 4, rect_size2d // 4, rect_size2d // 4))
        player.draw_minamap(sc)


def draw_3d(sc):
    pg.draw.rect(sc, (50, 30, 0), (0, 0, width, height / 2))
    pg.draw.rect(sc, (40, 30, 0), (0, height / 2, width, height))


if __name__ == '__main__':
    main()
