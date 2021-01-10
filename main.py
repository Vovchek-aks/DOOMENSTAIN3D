import pygame as pg
from map import *
from settings import *
from player import Player
import math
# import sys
import os
from time import time

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
    def __init__(self, x, y, *groups, sp=0.25, marsh=None, do_marsh=True):
        super().__init__(all_sprites, objects, *groups)
        self.base_im = obj_spr.get(self.__class__, im_sh)
        self.image = self.base_im
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = -self.rect.w
        self.pos = x, y
        self.sp = sp
        self.is_ded = False
        self.ang = -1

        self.past_d = -1

        self.marsh = [self.pos]
        if marsh is not None:
            self.marsh = marsh

        self.mc = 0
        self.do_marsh = do_marsh

        self.hp = obj_hp.get(self.__class__, 1)

    def step(self, player):
        if self.hp <= 0:
            self.ded()
        self.go_marsh(player)
        self.draw3d(player)

    def go_marsh(self, player):
        if self.do_marsh:
            if self.pos != self.marsh[self.mc]:
                self.move(*self.marsh[self.mc], player)
            else:
                self.mc += 1
                self.mc %= len(self.marsh)

    def move(self, x, y, player):
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
        self.ang = angle_of_points(*player.pos, *self.pos,
                                      player.ang)
        # if dist < 20:
        #     dist = 20
        self.rect.x = self.ang / line_step * line_to_px - self.image.get_rect().w // 2 + shx

        if dist != self.past_d:
            self.image = pg.transform.scale(self.base_im,
                                            (round(self.rect.w / (dist * 0.02)),
                                             round(self.rect.h / (dist * 0.02))))
        self.rect.y = height / 2 - (dist * 0.05) - self.image.get_rect().h // 2 + 20 + self.rect.h / 40 + sh - 15

        self.past_d = dist

    def ded(self):
        self.is_ded = True
        self.pos = -100, -100


class Enemy(GameObject):
    def __init__(self, x, y, sp=0.25, marsh=None, do_marsh=True):
        super().__init__(x, y, enemies, sp=sp, marsh=marsh, do_marsh=do_marsh)

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

    def move(self, x, y, player):
        xx, yy = self.pos
        super().move(x, y, player)

        can_move = True
        for i in objects:
            if (i.__class__ in solid_cl or i.__class__.__bases__[0] in solid_cl) and i is not self and \
               dist_of_points(*self.pos, *i.pos) <= 20:
                can_move = False
                break
        if dist_of_points(*self.pos, *player.pos) <= 20:
            can_move = False
            player.hp -= obj_dam.get(self.__class__, 0)
        if grid_pos(self.x * 4, self.y * 4) in map_coords or not can_move:
            self.pos = self.x, self.y = xx, yy


class Door(GameObject):
    def __init__(self, x, y, sp=0.25, marsh=None, do_marsh=False):
        super().__init__(x, y, enemies, sp=sp, marsh=marsh, do_marsh=do_marsh)

    def go_marsh(self, player):
        super().go_marsh(player)
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
        shx *= d*0.5/20
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


def raycast_png(player):
    ret = []
    x, y = grid_pos(player.x, player.y)
    for i in range(lines):
        a = player.ang + line_step * i - line_step * lines / 2
        cos = math.cos(a)
        sin = math.sin(a)

        # смотрим на пересечение с вертикалями
        vertical, dop_inf_x = (x + rect_size2d, 1) if cos >= 0 else (x, -1)
        for j in range(0, width, rect_size2d):
            rast_vert = (vertical - player.x) / cos  # расстояние до вертикали
            y_vert = player.y + rast_vert * sin      # координата y
            x_vert = player.x + rast_vert * cos
            if grid_pos(vertical + dop_inf_x, y_vert) in map_coords:
                break
            vertical += dop_inf_x * rect_size2d

        # смотрим на пересечение с горизонталями
        horisontal, dop_inf_y = (y + rect_size2d, 1) if sin >= 0 else (y, -1)
        for j in range(0, height, rect_size2d):
            rast_hor = (horisontal - player.y) / (sin + 0.00001)  # расстояние до горизонтали
            x_hor = player.x + rast_hor * cos                     # координата x
            y_hor = player.y + rast_hor * sin
            if grid_pos(x_hor, horisontal + dop_inf_y) in map_coords:
                break
            horisontal += dop_inf_y * rect_size2d

        if rast_vert < rast_hor:
            rast = rast_vert
            yt = grid_pos(x_vert, y_vert)[1]
            shift = (y_vert - yt) / rect_size2d * (stena.get_rect().w - round(line_to_px))
        else:
            rast = rast_hor
            xt = grid_pos(x_hor, y_hor)[0]
            shift = (x_hor - xt) / rect_size2d * (stena.get_rect().w - round(line_to_px))

        rast *= math.cos(player.ang - a)  # стены прямые, без округлостей
        xx = player.x + rast * cos
        yy = player.y + rast * sin

        if rast < 10:
            rast = 10

        ret += [(i, rast, round(shift))]

    return ret


stena = None
egip_stena = None
stena_pre_render = []


def shoot(player):
    if player.ammo1 and time() - player.last_shoot >= 1:
        player.ammo1 -= 1
        player.last_shoot = time()
        for i in objects.sprites():
            if 0.2 < i.ang < 0.8 and dist_of_points(*player.pos, *i.pos) < rect_size2d * 3:
                i.hp -= 1
                break


def draw_bar(sc, font, text, color, num, max_, sz, pos):
    if color != white:
        c = white
    else:
        c = black
    sc.blit(font.render(text, False, gray), pos)
    lsz = sz * (num / max_)
    if num > 0:
        pg.draw.rect(sc, color, (font.size(text + ' ')[0] + pos[0], pos[1],
                                 lsz,  font.size(' ')[1]))
        sc.blit(font.render(str(num), False, c), (font.size(text + ' ')[0] + pos[0] +
                                                  (lsz - font.size(str(num))[1]) / 2,
                                                  pos[1]))


def draw_interface(sc, player, font):
    draw_minimap(sc, player)
    pg.draw.rect(sc, dk_gray, (0, height - 200, width, height))
    draw_bar(sc, font, 'AMMO', red, player.ammo1, 20, 500, (20, height - 150))
    draw_bar(sc, font, 'HP       ', red, round(player.hp), 100, 500, (20, height - 80))


solid_cl = {Door, Enemy}
obj_hp = {Spider: 10,
          Door: 1000000}

obj_dam = {Spider: 1}
obj_spr = {}
im_sh = None


def main():
    global key_d, obj_spr, im_sh, stena, egip_stena, all_sprites, enemies, objects, stena_pre_render
    pg.init()
    sc = pg.display.set_mode((width, height))
    # pg.display.toggle_fullscreen()

    running = True
    clock = pg.time.Clock()

    obj_spr = {Door: load_image('дверь.png'),
               Spider: load_image('321.png')}

    im_sh = load_image('shrek3.png')

    stena = load_image('стена обыкновенная.png')
    egip_stena = load_image('египецкая стена ураааоаоаоаоаоао.jpg')

    for i in range(stena.get_rect().w - round(line_to_px)):
        stena_pre_render += [stena.subsurface(i, 0, round(line_to_px), stena.get_rect().h)]

    font = pygame.font.Font(None, 24)
    font2 = pygame.font.Font(None, 48)

    all_sprites = pg.sprite.Group()
    objects = pg.sprite.Group()
    enemies = pg.sprite.Group()

    player = Player(half_size[0] * rect_size2d - 48 * 4, half_size[1] // 2 * rect_size2d - 48,
                    objects, solid_cl)

    # sh = Spider(5 * rect_size2d, 1 * rect_size2d, do_marsh=True)
    Spider(7 * rect_size2d, 0.55 * rect_size2d, do_marsh=True)
    Door(6.2 * rect_size2d, 0.4 * rect_size2d, marsh=[(6.2 * rect_size2d, 0.10 * rect_size2d)])

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
                    exit(0)
                elif event.key == pg.K_SPACE:
                    shoot(player)

        lin = raycast_png(player)
        draw_3d_png(sc, lin, all_sprites.sprites(), player.pos)
        # lin = raycast_fps_stonks(player)
        # draw_3d(sc, lin, all_sprites.sprites(), player.pos)
        # draw_map(sc, player, lin)
        draw_interface(sc, player, font2)
        for i in objects.sprites():
            if not i.is_ded:
                i.step(player)
        player.step()
        if player.hp <= 0:
            return
        # angle_of_points(*player.pos, *sh.pos, player.ang)
        sc.blit(font.render(str(clock.get_fps()), False, red), (width - 500, 50))
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


def draw_minimap(sc, player):
    pg.draw.rect(sc, black, (0, 0, rect_size2d // 4 * len(map_[0]), rect_size2d // 4 * len(map_)))
    for i in map_coords:
        # print(i[0], i[1], rect_size2d)
        pg.draw.rect(sc, gray, (i[0] // 4, i[1] // 4, rect_size2d // 4, rect_size2d // 4))
        player.draw_minamap(sc)
    # for i in lines:
    #     pg.draw.line(sc, white, player.pos, (i[0][0] // 4, i[0][1] // 4), 1)
    for i in objects.sprites():
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


def draw_3d_png(sc, lin, sp, ppos):
    pg.draw.rect(sc, (50, 30, 0), (0, 0, width, height / 2))
    pg.draw.rect(sc, (40, 30, 0), (0, height / 2, width, height))
    dist = 999

    lin = [(True, i, i[1]) for i in lin]
    sp = [(False, i, dist_of_points(*ppos, *i.pos) * 3.6) for i in sp if not i.is_ded]
    lis = sorted(lin + sp, key=lambda x: -x[-1])
    for i in lis:
        if i[0]:
            pass
            ii = i[1]
            j = ii[1]
            # if ii[2] >= 256:
            #     ii[2] = 253

            wall = stena_pre_render[ii[2] - 1]

            wall = pg.transform.scale(wall, (round(line_to_px), round(dist * rect_size2d / (j + 1)) * 2))
            sc.blit(wall, (ii[0] * round(line_to_px), height / 2 - dist * rect_size2d / (j + 1)))
            # c = 255 / (1 + j * j * 0.00001)
            #
            # color = (int(c / 2), int(c / 3), int(c / 5))
            # pg.draw.rect(sc, color, (i * line_to_px,
            #                          height / 2 - dist * rect_size2d / (j + 1),
            #                          line_to_px + 1,
            #                          dist * rect_size2d / (j + 1) * 2))
        else:
            if -i[1].rect.w * 8 <= i[1].rect.x <= width or False:
                sc.blit(i[1].image, (i[1].rect.x, i[1].rect.y))


if __name__ == '__main__':
    while 1:
        main()
