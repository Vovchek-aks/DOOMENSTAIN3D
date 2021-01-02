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


def dist_of_points(x1, y1, x2, y2):
    global player
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return (dx ** 2 + dy ** 2) ** 0.5


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
        self.base_im = load_image(spr)
        self.image = self.base_im
        self.rect = self.image.get_rect()
        self.rect.x = -self.rect.w
        self.rect.y = -self.rect.h
        self.x = x
        self.y = y
        self.pos = x, y

    def step(self, player):
        self.draw3d(player)

    def draw3d(self, player):
        self.rect.x = angle_of_points(*player.pos, *self.pos, player.ang) / line_step * line_to_px
        self.image = pg.transform.scale(self.base_im,
                                        (round(self.rect.w / (dist_of_points(*self.pos, *player.pos) * 0.01)),
                                         round(self.rect.h / (dist_of_points(*self.pos, *player.pos) * 0.01))))


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


def dop_shtyki(x, y):
    return (x // rect_size2d) * rect_size2d, (y // rect_size2d) * rect_size2d


def raycast_fps_stonks(sc, player):
    ret = []
    x, y = dop_shtyki(player.x, player.y)
    for i in range(lines):

        a = player.ang + line_step * i - line_step * lines / 2
        cos = math.cos(a)
        sin = math.sin(a)

        # смотрим на пересечение с вертикалями
        vertical, dop_inf_x = (x + rect_size2d, 1) if cos >= 0 else (x, -1)
        for j in range(0, width, rect_size2d):
            rast_vert = (vertical - player.x) / cos
            y_vert = player.y + rast_vert * sin
            if dop_shtyki(vertical + dop_inf_x, y_vert) in map_coords:
                break
            vertical += dop_inf_x * rect_size2d

        # смотрим на пересечение с горизонталями
        horisontal, dop_inf_y = (y + rect_size2d, 1) if sin >= 0 else (y, -1)
        for j in range(0, height, rect_size2d):
            rast_hor = (horisontal - player.y) / (sin + 0.00001)
            x_hor = player.x + rast_hor * cos
            if dop_shtyki(x_hor, horisontal + dop_inf_y) in map_coords:
                break
            horisontal += dop_inf_y * rect_size2d
        if rast_vert < rast_hor:
            rast = rast_vert
        else:
            rast = rast_hor
        rast *= math.cos(player.ang - a)  # стены прямые, без округлостей
        xx = player.x + rast * cos
        yy = player.y + rast * sin

        ret += [((xx, yy), rast, i)]

    return ret


def main():
    pg.init()
    sc = pg.display.set_mode((width, height))
    # pg.display.toggle_fullscreen()

    running = True
    clock = pg.time.Clock()

    player = Player()

    sh = GameObject(half_size[0] + rect_size2d, half_size[1] + rect_size2d, '1.png')

    while running:
        sc.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

        lin = raycast_fps_stonks(sc, player)
        draw_3d(sc, lin)
        # draw_map(sc, player, lin)
        draw_minimap(sc, player, lin)
        sh.step(player)
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


def draw_minimap(sc, player, lines):
    pg.draw.rect(sc, black, (0, 0, rect_size2d // 4 * len(map_[0]), rect_size2d // 4 * len(map_)))
    for i in map_coords:
        # print(i[0], i[1], rect_size2d)
        pg.draw.rect(sc, gray, (i[0] // 4, i[1] // 4, rect_size2d // 4, rect_size2d // 4))
        player.draw_minamap(sc)
    for i in lines:
        pg.draw.line(sc, white, player.pos, (i[0][0] // 4, i[0][1] // 4), 1)
    for i in all_sprites.sprites():
        pg.draw.circle(sc, red, i.pos, 5)
        # pg.draw.line(sc, green, i.pos, (i.x // 4 + rect_size2d // 4 * math.cos(i.ang),
        #                                    i.y // 4 + rect_size2d // 4 * math.sin(i.ang)), 1)
        # print(i.pos)


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
