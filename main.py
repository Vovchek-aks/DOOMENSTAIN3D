import pygame as pg
from map import *
from settings import *
from player import Player
import math
# import sys
import os

# import numpy as np

all_sprites = pg.sprite.Group()
objects = pg.sprite.Group()
enemies = pg.sprite.Group()

key_d = -1

znak = lambda x: 1 if x > 0 else -1


def angle_of_points(x1, y1, x2, y2, ang):
    dx = -(x1 - x2)
    dy = (y1 - y2)
    f = math.atan2(dx, dy)
    r = f - ang
    if not (y1 < y2 and x1 < x2 or ang == 0 and y1 >= y2) or y1 < y2 and ang >= math.radians(270):
        r += math.pi * 2

    if x1 < x2 and y1 >= y2 and math.radians(90) > ang > 0:
        r -= math.pi * 2
    return r - 1


def dist_of_points(x1, y1, x2, y2):
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return (dx ** 2 + dy ** 2) ** 0.5


def lines_collision(x1_1, y1_1, x1_2, y1_2,
                    x2_1, y2_1, x2_2, y2_2):
    def point(xx):
        if min(x1_1, x1_2) <= xx <= max(x1_1, x1_2):
            return True
        return False

    A1 = y1_1 - y1_2
    B1 = x1_2 - x1_1
    C1 = x1_1 * y1_2 - x1_2 * y1_1
    A2 = y2_1 - y2_2
    B2 = x2_2 - x2_1
    C2 = x2_1 * y2_2 - x2_2 * y2_1

    if B1 * A2 - B2 * A1 and A1:
        y = (C2 * A1 - C1 * A2) / (B1 * A2 - B2 * A1)
        x = (-C1 - B1 * y) / A1
        return point(x)
    elif B1 * A2 - B2 * A1 and A2:
        y = (C2 * A1 - C1 * A2) / (B1 * A2 - B2 * A1)
        x = (-C2 - B2 * y) / A2
        return point(x)
    return False


# def lines_collision(x1_1, y1_1, x1_2, y1_2,
#                     x2_1, y2_1, x2_2, y2_2):
#     """
#     Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
#     a1: [x, y] a point on the first line
#     a2: [x, y] another point on the first line
#     b1: [x, y] a point on the second line
#     b2: [x, y] another point on the second line
#     """
#
#     a1, a2 = (x1_1, y1_1), (x1_2, y1_2)
#     b1, b2 = (x2_1, y2_1), (x2_2, y2_2)
#
#     s = np.vstack([a1,a2,b1,b2])        # s for stacked
#     h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
#     l1 = np.cross(h[0], h[1])           # get first line
#     l2 = np.cross(h[2], h[3])           # get second line
#     x, y, z = np.cross(l1, l2)          # point of intersection
#     if z == 0:                          # lines are parallel
#         return False
#     return True


def lines_from_square(x, y, size=rect_size2d):
    return ((x, y, x + size, y),
            (x, y, x, y + size),
            (x + size, y, x + size, y + size),
            (x, y + size, x + size, y + size))


def point_in_square(x, y, xx, yy, size=rect_size2d):
    if xx * size <= x <= (xx + 1) * size and \
            yy * size <= y <= (yy + 1) * size:
        return True
    return False


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
    def __init__(self, x, y, spr, *groups, sp=0.25, marsh=None, do_marsh=True):
        super().__init__(all_sprites, objects, *groups)
        self.base_im = load_image(spr)
        self.image = self.base_im
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = -self.rect.w
        self.pos = x, y
        self.sp = sp
        self.is_ded = False

        self.marsh = [self.pos]
        if marsh is not None:
            self.marsh = marsh

        self.mc = 0
        self.do_marsh = do_marsh

    def step(self, player):
        self.go_marsh()
        self.draw3d(player)

    def go_marsh(self):
        if self.do_marsh:
            if self.pos != self.marsh[self.mc]:
                self.move(*self.marsh[self.mc])
            else:
                self.mc += 1
                self.mc %= len(self.marsh)

    def move(self, x, y):
        if abs(self.x - x) > self.sp:
            self.x -= self.sp * znak(self.x - x)
        else:
            self.x = x
        if abs(self.y - y) > self.sp:
            self.y -= self.sp * znak(self.y - y)
        else:
            self.y = y
        self.pos = self.x, self.y

    def draw3d(self, player, distd=1, sh=0, shx=0):
        dist = dist_of_points(*self.pos, *player.pos) / distd
        # if dist < 20:
        #     dist = 20
        self.rect.x = angle_of_points(*player.pos, *self.pos,
                                      player.ang) / line_step * line_to_px - self.image.get_rect().w // 2 + shx

        self.image = pg.transform.scale(self.base_im,
                                        (round(self.rect.w / (dist * 0.02)),
                                         round(self.rect.h / (dist * 0.02))))
        self.rect.y = height / 2 - (dist * 0.05) - self.image.get_rect().h // 2 + 20 + self.rect.h / 40 + sh - 15

    def ded(self):
        self.is_ded = True
        self.pos = -100, -100


class Enemy(GameObject):
    def __init__(self, x, y, spr, sp=0.25, marsh=None, do_marsh=True):
        super().__init__(x, y, spr, enemies, sp=sp, marsh=marsh, do_marsh=do_marsh)
        self.in_wall = False

    def step(self, player):
        self.find_player(player)
        super().step(player)

    def find_player(self, player):
        pass
        f = False
        lsp = (player.pos[0] - self.x, player.pos[1] - self.y)
        disk = round(dist_of_points(*self.pos, *player.pos))

        for g in range(1, disk + 1):
            g = g / disk
            if ((self.x + lsp[0] * g) // rect_size2d * rect_size2d,
                (self.y + lsp[1] * g) // rect_size2d * rect_size2d) in map_coords:
                f = True
                # print(((self.x + lsp[0] * g) // rect_size2d * rect_size2d,
                #     (self.y + lsp[1] * g) // rect_size2d * rect_size2d))
                break

        if not f and dist_of_points(*self.pos, *player.pos) <= 100:
            self.marsh = [player.pos]
            self.mc = 0

    def move(self, x, y):
        xx, yy = self.pos
        super().move(x, y)
        self.in_wall = False
        if grid_pos(self.x * 4, self.y * 4) in map_coords:
            self.pos = self.x, self.y = xx, yy
            self.in_wall = True


class Door(GameObject):
    def __init__(self, x, y, spr, sp=0.25, marsh=None, do_marsh=False):
        super().__init__(x, y, spr, enemies, sp=sp, marsh=marsh, do_marsh=do_marsh)

    def go_marsh(self):
        super().go_marsh()
        if self.pos == self.marsh[-1]:
            self.ded()

    def step(self, player):
        if dist_of_points(*self.pos, *player.pos) < 25 and \
           0.3 < angle_of_points(*player.pos, *self.pos, player.ang) < 0.8 and \
           key_d == pg.K_f:
            self.do_marsh = True
        super().step(player)

    def draw3d(self, player, distd=2.5, sh=1, shx=10):
        d = dist_of_points(*self.pos, *player.pos)
        sh = -d**0.9 / 20
        shx *= d/100
        super().draw3d(player, distd=distd, sh=sh, shx=shx)


class Spider(Enemy):
    pass


def raycast(player):
    ret = []
    for i in range(lines):
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


def grid_pos(x, y):
    return x // rect_size2d * rect_size2d, y // rect_size2d * rect_size2d


def raycast_fps_stonks(player):
    ret = []
    x, y = grid_pos(player.x, player.y)
    for i in range(lines):

        a = player.ang + line_step * i - line_step * lines / 2
        cos = math.cos(a)
        sin = math.sin(a)

        # смотрим на пересечение с вертикалями
        vertical, dop_inf_x = (x + rect_size2d, 1) if cos >= 0 else (x, -1)
        for j in range(0, width, rect_size2d):
            rast_vert = (vertical - player.x) / cos
            y_vert = player.y + rast_vert * sin
            if grid_pos(vertical + dop_inf_x, y_vert) in map_coords:
                break
            vertical += dop_inf_x * rect_size2d

        # смотрим на пересечение с горизонталями
        horisontal, dop_inf_y = (y + rect_size2d, 1) if sin >= 0 else (y, -1)
        for j in range(0, height, rect_size2d):
            rast_hor = (horisontal - player.y) / (sin + 0.00001)
            x_hor = player.x + rast_hor * cos
            if grid_pos(x_hor, horisontal + dop_inf_y) in map_coords:
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


solid_cl = {Door, Enemy}
hp = {Spider: 10}


def main():
    global key_d
    pg.init()
    sc = pg.display.set_mode((width, height))
    # pg.display.toggle_fullscreen()

    running = True
    clock = pg.time.Clock()

    font = pygame.font.Font(None, 24)

    player = Player(half_size[0] * rect_size2d - 48 * 4, half_size[1] // 2 * rect_size2d - 48,
                    all_sprites, solid_cl)

    Spider(7 * rect_size2d, 0.55 * rect_size2d, '321.png', do_marsh=True)
    Door(6.2 * rect_size2d, 0.4 * rect_size2d, 'дверь.png', marsh=[(6.2 * rect_size2d, 0.10 * rect_size2d)])

    while running:
        sc.fill((0, 0, 0))
        key_d = -1
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                key_d = event.key
                if event.key == pg.K_ESCAPE:
                    running = False

        lin = raycast_fps_stonks(player)
        draw_3d(sc, lin, all_sprites.sprites(), player.pos)
        # draw_map(sc, player, lin)
        draw_minimap(sc, player, lin)
        for i in all_sprites.sprites():
            if not i.is_ded:
                i.step(player)
        player.step()
        # angle_of_points(*player.pos, *sh.pos, player.ang)
        # sc.blit(font.render(str(dist_of_points(*sh.pos, *player.pos)), False, red), (width - 500, 50))
        # sc.blit(font.render(str((sh.x, sh.y,)), False, red), (width - 500, 100))
        # if sh.in_wall:
        #     color = red
        # else:
        #     color = green
        # pg.draw.rect(sc, color, (sh.pos[0] // (rect_size2d // 4) * (rect_size2d // 4),
        #                          sh.pos[1] // (rect_size2d // 4) * (rect_size2d // 4),
        #                          rect_size2d // 4,
        #                          rect_size2d // 4))
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
    # for i in lines:
    #     pg.draw.line(sc, white, player.pos, (i[0][0] // 4, i[0][1] // 4), 1)
    for i in all_sprites.sprites():
        if i.__class__ == Enemy or i.__class__.__bases__[0] == Enemy:
            color = red
        else:
            color = blue
        if not i.is_ded:
            pg.draw.circle(sc, color, i.pos, 5)
        # pg.draw.line(sc, green, i.pos, (i.x // 4 + rect_size2d // 4 * math.cos(i.ang),
        #                                    i.y // 4 + rect_size2d // 4 * math.sin(i.ang)), 1)
        # print(i.pos)


def draw_3d(sc, lin, sp, ppos):
    pg.draw.rect(sc, (50, 30, 0), (0, 0, width, height / 2))
    pg.draw.rect(sc, (40, 30, 0), (0, height / 2, width, height))
    dist = 999
    lin = [(True, i, i[1]) for i in lin]
    sp = [(False, i, dist_of_points(*ppos, *i.pos) * 3.6) for i in sp if not i.is_ded]
    lis = sorted(lin + sp, key=lambda x: -x[-1])
    for ret in lis:
        if ret[0]:
            i = ret[1][2]
            j = ret[1][1]

            c = 255 / (1 + j * j * 0.00001)

            color = (int(c / 2), int(c / 3), int(c / 5))
            pg.draw.rect(sc, color, (i * line_to_px,
                                     height / 2 - dist * rect_size2d / (j + 1),
                                     line_to_px + 1,
                                     dist * rect_size2d / (j + 1) * 2))
        else:
            if -ret[1].rect.w * 8 <= ret[1].rect.x <= width or False:
                sc.blit(ret[1].image, (ret[1].rect.x, ret[1].rect.y))


if __name__ == '__main__':
    main()
