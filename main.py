import pygame as pg
from map import *
from settings import *
from player import Player
import math
import sys
import os

all_sprites = pg.sprite.Group()
objects = pg.sprite.Group()
enemies = pg.sprite.Group()


def angle_of_points(x1, y1, x2, y2, ang):
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    f = math.atan2(dx, dy)
    if dx < 0 and dy < 0 or dx > 0 and 180 <= math.degrees(ang) <= 360:
        f *= math.pi * 2
    return f - ang


def load_image(name, colorkey=None):
    fullname = os.path.join('data', 'sprites', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        fullname = os.path.join('data', 'sprites', 'shrek3.png')
    image = pg.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class GameObject(pg.sprite.Sprite):
    def __init__(self, x, y, spr, *groups):
        super().__init__(all_sprites, objects, *groups)
        self.image = load_image(spr)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.pos = x, y

    def step(self):
        self.draw3d()

    def draw3d(self):
        global player
        angle_of_points(*player.pos, *self.pos, player.a)


class Enemy(GameObject):
    def __init__(self, x, y, spr):
        super().__init__(x, y, spr, enemies)


def raycast(sc, player):
    ret = []
    for i in range(lines):
        dist = 999
        a = player.ang + line_step * i - line_step * lines / 2

        cos = math.cos(a)
        sin = math.sin(a)
        for j in range(0, draw_dist, 5):
            xx = player.x + j * cos
            yy = player.y + j * sin

            if (int(xx // rect_size2d * rect_size2d), int(yy // rect_size2d * rect_size2d)) in map_coords:
                j *= math.cos(player.ang - a)

                ret += [((xx, yy), j, i)]

                break

    return ret


def raycast_fps_stonks(sc, player):
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

    # sh = pg.sprite.Sprite(all_sprites)
    # sh.image = load_image('shrek3.png', -1)
    # sh.rect = sh.image.get_rect()
    # print(all_sprites.sprites()[0])

    while running:
        sc.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

        lin = raycast(sc, player)
        draw_3d(sc, lin)
        # draw_map(sc, player, lin)
        draw_minimap(sc, player)
        all_sprites.draw(sc)
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


def draw_3d(sc, lin):
    pg.draw.rect(sc, (50, 30, 0), (0, 0, width, height / 2))
    pg.draw.rect(sc, (40, 30, 0), (0, height / 2, width, height))
    dist = 999
    for ret in lin:
        i = ret[2]
        j = ret[1]

        c = 255 / (1 + j * j * 0.00001)

        color = (int(c / 2), int(c / 3), int(c / 5))
        pg.draw.rect(sc, color, (i * line_to_px,
                                 height / 2 - dist * rect_size2d / (j + 1),
                                 line_to_px + 1,
                                 dist * rect_size2d / (j + 1) * 2))


if __name__ == '__main__':
    main()
