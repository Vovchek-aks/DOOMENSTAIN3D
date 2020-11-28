import pygame as pg
from map import *
from settings import *


def main():
    global screen
    pg.init()
    screen = pg.display.set_mode((size[0] * rect_size2d,
                                 size[1] * rect_size2d))

    draw_map()

    pg.display.flip()
    while pg.event.wait().type != pg.QUIT:
        pass
    pg.quit()


def draw_map():
    for i in range(len(map_)):
        for j in range(len(map_[i])):
            if map_[i][j] == '#':
                pg.draw.rect(screen, rect_color2d, (j * rect_size2d, i * rect_size2d, rect_size2d, rect_size2d), 1)


if __name__ == '__main__':
    main()

