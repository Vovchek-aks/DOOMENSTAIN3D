import pygame as pg
from settings import *


class Player:
    def __init__(self):
        self.pos = self.x, self.y = half_size[0] * rect_size2d, half_size[1] * rect_size2d
        self.ang = 0
        self.sp = 2

    def draw(self, cs):
        pg.draw.circle(cs, green, self.pos, 10)

    def step(self, sc):
        key = pg.key.get_pressed()

        if key[pg.K_w]:
            self.y -= self.sp
        if key[pg.K_s]:
            self.y += self.sp
        if key[pg.K_a]:
            self.x -= self.sp
        if key[pg.K_d]:
            self.x += self.sp
        if key[pg.K_q]:
            self.ang -= 1
            self.ang %= 360
        if key[pg.K_e]:
            self.ang += 1
            self.ang %= 360

        self.pos = self.x, self.y

        self.draw(sc)

