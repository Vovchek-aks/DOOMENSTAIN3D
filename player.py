import pygame as pg
import math
from map import *


def grid_pos(x, y):
    return x // rect_size2d * rect_size2d, y // rect_size2d * rect_size2d


def dist_of_points(x1, y1, x2, y2):
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return (dx ** 2 + dy ** 2) ** 0.5


class Player:
    def __init__(self, x, y, all_s, solid_cl, map_n):
        self.pos = self.x, self.y = x, y
        self.ang = 0
        self.sp = 5

        self.hp = 100
        self.ammo = [20, 5]
        self.gun = 0
        self.last_shoot = 0

        self.keys = {-1}

        self.all_sp = all_s
        self.solid_sp = solid_cl

        self.map_n = map_n

    def draw(self, sc):
        pg.draw.circle(sc, green, (self.pos[0] * rect_size2d, self.pos[1] * rect_size2d), 5)
        pg.draw.line(sc, green, self.pos, (self.x + rect_size2d * math.cos(self.ang),
                                           self.y + rect_size2d * math.sin(self.ang)), 1)

    def draw_minamap(self, sc):
        pg.draw.circle(sc, green, self.pos, 5)
        pg.draw.line(sc, green, self.pos, (self.x // 4 + rect_size2d // 4 * math.cos(self.ang),
                                           self.y // 4 + rect_size2d // 4 * math.sin(self.ang)), 1)

    def step(self):
        key = pg.key.get_pressed()

        cos = math.cos(self.ang)
        sin = math.sin(self.ang)

        xx, yy = self.pos

        if key[pg.K_w]:
            self.x += self.sp * cos
            self.y += self.sp * sin
        if key[pg.K_s]:
            self.x += -self.sp * cos
            self.y += -self.sp * sin
        if key[pg.K_a]:
            self.x += self.sp * sin
            self.y += -self.sp * cos
        if key[pg.K_d]:
            self.x += -self.sp * sin
            self.y += self.sp * cos
        if key[pg.K_q]:
            self.ang -= 0.06
        elif key[pg.K_e]:
            self.ang += 0.06
        self.ang %= math.pi * 2

        self.pos = self.x // 4, self.y // 4

        can_move = True
        for i in self.all_sp:
            if (i.__class__ in self.solid_sp or i.__class__.__bases__[0] in self.solid_sp) and \
                    dist_of_points(*self.pos, *i.pos) <= 20:
                can_move = False
                break

        if (grid_pos(self.x, self.y) in maps[self.map_n]['map_coords'] or not can_move) and True:
            self.x, self.y = xx * 4, yy * 4
            self.pos = self.x // 4, self.y // 4

        # self.draw(sc)
