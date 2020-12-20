import pygame as pg
from map import *
from settings import *
from player import Player


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

        draw_map(sc)
        player.step(sc)
        pg.display.flip()
        clock.tick(FPS)

    pg.quit()


def draw_map(sc):
    for i in range(len(map_)):
        for j in range(len(map_[i])):
            if map_[i][j] == '#':
                pg.draw.rect(sc, white, (j * rect_size2d, i * rect_size2d, rect_size2d, rect_size2d), 1)


if __name__ == '__main__':
    main()

