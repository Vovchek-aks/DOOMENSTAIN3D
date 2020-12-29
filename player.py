import pygame as pg
from settings import *
import math


class Player:
    def __init__(self):
        self.pos = self.x, self.y = half_size[0] * rect_size2d - 48 * 4, half_size[1] * rect_size2d - 48
        self.ang = 0
        self.sp = 3

    def draw(self, sc):
        pg.draw.circle(sc, green, self.pos, 5)
        pg.draw.line(sc, green, self.pos, (self.x // 4 + rect_size2d * math.cos(self.ang),
                                           self.y // 4 + rect_size2d * math.sin(self.ang)), 1)

    def step(self, sc):
        key = pg.key.get_pressed()

        cos = math.cos(self.ang)
        sin = math.sin(self.ang)

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
            self.ang -= 0.05
        elif key[pg.K_e]:
            self.ang += 0.05

        self.pos = self.x // 4, self.y // 4

        # self.draw(sc)

