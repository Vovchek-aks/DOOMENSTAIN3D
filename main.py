import pygame as pg
from map import *
from settings import *
from player import Player
import math
import sys
import os
from time import time
from random import randint

# import numpy as np

all_sprites = pg.sprite.Group()
objects = pg.sprite.Group()
enemies = pg.sprite.Group()

key_d = -1

map_n = 0
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


def point_in_square(x, y, xx, yy, sizex, sizey):
    if xx * sizex <= x <= (xx + 1) * sizex and \
            yy * sizey <= y <= (yy + 1) * sizey:
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


def load_sound(name):
    fullname = os.path.join('data', 'sounds', name)
    if not os.path.isfile(fullname):
        print(f"Файл со звуком '{fullname}' не найден")
        fullname = os.path.join('data', 'sounds', 'empty.wav')
    return pg.mixer.Sound(fullname)


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

        self.hp = obj_hp.get(self.__class__, 1000000)

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
        if dist < 5:
            dist = 5
        self.rect.x = self.ang / line_step * line_to_px - self.image.get_rect().w // 2 + shx

        if dist != self.past_d:
            self.image = pg.transform.scale(self.base_im,
                                            (round(self.rect.w / (dist * 0.02 + 0.000000000001)),
                                             round(self.rect.h / (dist * 0.02 + 0.000000000001))))
        self.rect.y = height / 2 - (
                    dist * 0.05 + 0.000000000001) - self.image.get_rect().h // 2 + 20 + self.rect.h / 40 + sh - 15

        self.past_d = dist

    def ded(self):
        self.is_ded = True
        self.pos = self.x, self.y = -100, -100
        obj_ded_v.get(self.__class__, v_empty).play()


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
                (self.y + lsp[1] * g) // rect_size2d * rect_size2d) in maps[map_n]['map_coords']:
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
        if grid_pos(self.x * 4, self.y * 4) in maps[map_n]['map_coords'] or not can_move:
            self.pos = self.x, self.y = xx, yy

    def ded(self):
        r = randint(0, 5)
        if not r:
            Aptechka(*self.pos)
        elif r == 1:
            Patroni(*self.pos, 0)
        elif r == 2 and map_n >= 1:
            Patroni(*self.pos, 1)
        super().ded()


class Door(GameObject):
    def __init__(self, x, y, marsh=None, key=-1):
        super().__init__(x, y, sp=0.25, marsh=marsh, do_marsh=False)
        self.key = key

    def go_marsh(self, player):
        super().go_marsh(player)
        if self.pos == self.marsh[-1]:
            self.ded()

    def step(self, player):
        if not self.do_marsh and dist_of_points(*self.pos, *player.pos) < 25 and \
                0.3 < angle_of_points(*player.pos, *self.pos, player.ang) < 0.8 and \
                key_d == pg.K_f:
            if self.key in player.keys:
                self.do_marsh = True
                over_v.get('door_open', v_empty).play()
            else:
                set_message(f'Вам нужен ключ {self.key}', 3)
                over_v.get('door_not_open', v_empty).play()
        super().step(player)

    def draw3d(self, player, distd=2.5, sh=1, shx=10):
        d = dist_of_points(*self.pos, *player.pos)
        sh = -d ** 0.9 / 20
        shx *= d * 0.5 / 20
        super().draw3d(player, distd=distd, sh=sh, shx=shx)


class Spider(Enemy):
    pass


class Zombie(Enemy):
    pass


class Spawner(GameObject):
    def __init__(self, x, y, obj=None, marsh=None, chst=1):
        super().__init__(x, y, sp=0, marsh=marsh, do_marsh=False)
        self.chst = chst

        self.obj = obj

        self.sch = 0

    def step(self, player):
        super().step(player)
        self.sch += 1
        if self.sch // 60 >= self.chst:
            self.sch = 0
            can_spawn = True
            for i in all_sprites.sprites():
                if i.__class__ == self.obj and dist_of_points(*self.pos, *i.pos) < 20:
                    can_spawn = False
                    break
            if can_spawn:
                for i in range(100):
                    pos = (self.marsh[0][0] + randint(-rect_size2d, rect_size2d),
                           self.marsh[0][1] + randint(-rect_size2d, rect_size2d))
                    if dist_of_points(*self.pos, *pos) > 30:
                        break

                self.obj(*self.pos, marsh=[pos],
                         do_marsh=True)


class Key(GameObject):
    def __init__(self, x, y, key=-1):
        super().__init__(x, y, sp=0)
        self.key = key

    def step(self, player):
        if dist_of_points(*self.pos, *player.pos) <= 20:
            set_message(f'Вы подобрали ключ {self.key}', 3)
            player.keys.add(self.key)
            self.ded()
        super().step(player)


class Trigger(GameObject):
    def __init__(self, x, y, foo=lambda: None):
        super().__init__(x, y, sp=0)
        self.foo = foo
        self.rect.x, self.rect.y = -1000, -1000

    def step(self, player):
        if dist_of_points(*self.pos, *player.pos) <= 20:
            self.foo()
            self.ded()
        super().step(player)

    def draw3d(self, player, distd=1, sh=0, shx=0):
        pass


class Spr(GameObject):
    def __init__(self, x, y, spr):
        super().__init__(x, y, sp=0)
        self.base_im = self.image = spr


class Aptechka(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, do_marsh=False, sp=0)

    def step(self, player):
        super().step(player)
        if dist_of_points(*self.pos, *player.pos) <= 10:
            player.hp = 100
            self.ded()


class Patroni(GameObject):
    def __init__(self, x, y, tp):
        super().__init__(x, y, do_marsh=False, sp=0)
        self.type = tp
        if tp:
            self.image = self.base_im = obj_spr['p2']
        else:
            self.image = self.base_im = obj_spr['p1']

    def step(self, player):
        super().step(player)
        if dist_of_points(*self.pos, *player.pos) <= 10:
            player.ammo[self.type] = gun_amst[self.type]
            self.ded()


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
    global rast_vert, rast_hor
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
    global rast_hor, rast_vert, x_vert, y_vert, x_hor, y_hor
    ret = []
    x, y = grid_pos(player.x, player.y)
    for i in range(lines):
        a = player.ang + line_step * i - line_step * lines / 2
        cos = math.cos(a)
        sin = math.sin(a)
        is_egipt_vert = False
        is_egipt_hor = False
        # смотрим на пересечение с вертикалями
        vertical, dop_inf_x = (x + rect_size2d, 1) if cos >= 0 else (x, -1)
        for j in range(0, width, rect_size2d):
            rast_vert = (vertical - player.x) / cos  # расстояние до вертикали
            y_vert = player.y + rast_vert * sin  # координата y
            x_vert = player.x + rast_vert * cos
            if grid_pos(vertical + dop_inf_x, y_vert) in maps[map_n]['egypt_coords']:
                is_egipt_vert = True
                break
            elif grid_pos(vertical + dop_inf_x, y_vert) in maps[map_n]['wall_coords']:
                is_egipt_vert = False
                break
            vertical += dop_inf_x * rect_size2d

        # смотрим на пересечение с горизонталями
        horisontal, dop_inf_y = (y + rect_size2d, 1) if sin >= 0 else (y, -1)
        for j in range(0, height, rect_size2d):
            rast_hor = (horisontal - player.y) / (sin + 0.00001)  # расстояние до горизонтали
            x_hor = player.x + rast_hor * cos  # координата x
            y_hor = player.y + rast_hor * sin
            if grid_pos(x_hor, horisontal + dop_inf_y) in maps[map_n]['egypt_coords']:
                is_egipt_hor = True
                break
            elif grid_pos(x_hor, horisontal + dop_inf_y) in maps[map_n]['wall_coords']:
                is_egipt_hor = False
                break
            horisontal += dop_inf_y * rect_size2d

        if rast_vert < rast_hor:
            rast = rast_vert
            yt = grid_pos(x_vert, y_vert)[1]
            shift = (y_vert - yt) / rect_size2d * (stena.get_rect().w - round(line_to_px))
            pict = is_egipt_vert
        else:
            rast = rast_hor
            xt = grid_pos(x_hor, y_hor)[0]
            shift = (x_hor - xt) / rect_size2d * (stena.get_rect().w - round(line_to_px))
            pict = is_egipt_hor

        rast *= math.cos(player.ang - a)  # стены прямые, без округлостей
        # xx = player.x + rast * cos
        # yy = player.y + rast * sin

        if rast < 20:
            rast = 20

        ret += [(i, rast, round(shift), pict)]

    return ret


def draw_button(sc, name, x, y):
    sc.blit(name, (x, y))
    return (x, y)


def start_screen(sc):
    pg.mixer.music.load(os.path.join('data', 'sounds', 'меню.mp3'))
    pg.mixer.music.play()
    pg.mixer.music.set_volume(0.5)

    sc.blit(fon, (0, 0))
    sc.blit(quitt, (width // 2 - menu.get_rect().h * 6, (height - menu.get_rect().h) / 2 + 200))
    clock = pygame.time.Clock()
    running = True
    rect_b_lv = draw_button(sc, but_menu, width // 2 - menu.get_rect().h * 6, (height - menu.get_rect().h) / 2)
    rect_b_quit = draw_button(sc, quitt, width // 2 - menu.get_rect().h * 6, (height - menu.get_rect().h) / 2 + 200)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= rect_b_lv[0] and event.pos[1] >= rect_b_lv[1]:
                    if event.pos[0] <= rect_b_lv[0] + but_menu.get_rect().w and event.pos[1] >= rect_b_lv[1]:
                        if event.pos[0] <= rect_b_lv[0] + but_menu.get_rect().w and \
                                event.pos[1] <= rect_b_lv[1] + but_menu.get_rect().h:
                            if event.pos[0] >= rect_b_lv[0] and event.pos[1] <= rect_b_lv[1] + but_menu.get_rect().h:
                                # level_all(sc)
                                return
                if event.pos[0] >= rect_b_quit[0] and event.pos[1] >= rect_b_quit[1]:
                    if event.pos[0] <= rect_b_quit[0] + but_menu.get_rect().w and event.pos[1] >= rect_b_quit[1]:
                        if event.pos[0] <= rect_b_quit[0] + but_menu.get_rect().w and \
                                event.pos[1] <= rect_b_quit[1] + but_menu.get_rect().h:
                            if event.pos[0] >= rect_b_quit[0] and \
                                    event.pos[1] <= rect_b_quit[1] + but_menu.get_rect().h:
                                pygame.quit()
                                sys.exit()
        pygame.display.flip()
        clock.tick(FPS)


def level_all(sc):
    global map_n, need_break
    lvl_fon_all = pygame.transform.scale(lvl_fon, (width, height))
    sc.blit(lvl_fon_all, (0, 0))
    clock = pygame.time.Clock()
    running = True
    odin = draw_button(sc, one, width / 6 - menu.get_rect().h, height / 4 - menu.get_rect().h)
    dva = draw_button(sc, two, width / 2.1 - menu.get_rect().h, height / 4 - menu.get_rect().h)
    tri = draw_button(sc, three, width / 1.3 - menu.get_rect().h, height / 4 - menu.get_rect().h)
    chetire = draw_button(sc, four, width / 3.1 - menu.get_rect().h, height / 1.5 - menu.get_rect().h)
    piat = draw_button(sc, five, width / 1.6 - menu.get_rect().h, height / 1.5 - menu.get_rect().h)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= odin[0] and event.pos[1] >= odin[1] \
                        and event.pos[0] <= odin[0] + but_menu.get_rect().w and event.pos[1] >= odin[1] \
                        and event.pos[0] <= odin[0] + but_menu.get_rect().w and \
                        event.pos[1] <= odin[1] + but_menu.get_rect().h \
                        and event.pos[0] >= odin[0] and event.pos[1] <= odin[1] + but_menu.get_rect().h:
                    map_n = 0
                    need_break = True
                    return
                elif event.pos[0] >= tri[0] and event.pos[1] >= tri[1]:
                    if event.pos[0] <= tri[0] + but_menu.get_rect().w and event.pos[1] >= tri[1] \
                            and event.pos[0] <= tri[0] + but_menu.get_rect().w and \
                            event.pos[1] <= tri[1] + but_menu.get_rect().h \
                            and event.pos[0] >= tri[0] and \
                            event.pos[1] <= tri[1] + but_menu.get_rect().h:
                        map_n = 1
                        need_break = True
                        return
                elif event.pos[0] >= chetire[0] and event.pos[1] >= chetire[1]:
                    if event.pos[0] <= chetire[0] + but_menu.get_rect().w and event.pos[1] >= chetire[1] \
                            and event.pos[0] <= chetire[0] + but_menu.get_rect().w and \
                            event.pos[1] <= chetire[1] + but_menu.get_rect().h \
                            and event.pos[0] >= chetire[0] and \
                            event.pos[1] <= chetire[1] + but_menu.get_rect().h:
                        map_n = 3
                        need_break = True
                        return
                elif event.pos[0] >= dva[0] and event.pos[1] >= dva[1]:
                    if event.pos[0] <= dva[0] + but_menu.get_rect().w and event.pos[1] >= dva[1] \
                            and event.pos[0] <= dva[0] + but_menu.get_rect().w and \
                            event.pos[1] <= dva[1] + but_menu.get_rect().h \
                            and event.pos[0] >= dva[0] and \
                            event.pos[1] <= dva[1] + but_menu.get_rect().h:
                        map_n = 1
                        need_break = True
                        return
                elif event.pos[0] >= piat[0] and event.pos[1] >= piat[1]:
                    if event.pos[0] <= piat[0] + but_menu.get_rect().w and event.pos[1] >= piat[1]:
                        if event.pos[0] <= piat[0] + but_menu.get_rect().w and \
                                event.pos[1] <= piat[1] + but_menu.get_rect().h:
                            if event.pos[0] >= piat[0] and \
                                    event.pos[1] <= piat[1] + but_menu.get_rect().h:
                                map_n = 4
                                need_break = True
                                return
                                # pygame.quit()
                                # sys.exit()
        pygame.display.flip()
        clock.tick(FPS)


def mini_menu_go(sc):
    global tm_map_m

    tm_map_m = time() - tm_map_m
    pg.mixer.music.load(os.path.join('data', 'sounds', 'меню.mp3'))
    pg.mixer.music.play()
    pg.mixer.music.set_volume(0.5)

    sc.blit(fon, (0, 0))
    running = True
    rect_b_c = draw_button(sc, continue_b, width // 2 - menu.get_rect().h * 6, (height - menu.get_rect().h) / 2)
    rect_b_menu = draw_button(sc, minin_in_menu, width // 2 - menu.get_rect().h * 6,
                              (height - menu.get_rect().h) / 2 + 200)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= rect_b_c[0] and event.pos[1] >= rect_b_c[1]:
                    if event.pos[0] <= rect_b_c[0] + but_menu.get_rect().w and event.pos[1] >= rect_b_c[1]:
                        if event.pos[0] <= rect_b_c[0] + but_menu.get_rect().w and \
                                event.pos[1] <= rect_b_c[1] + but_menu.get_rect().h:
                            if event.pos[0] >= rect_b_c[0] and event.pos[1] <= rect_b_c[1] + but_menu.get_rect().h:
                                pg.mixer.music.load(os.path.join('data', 'sounds', maps_music[map_n]))
                                pg.mixer.music.play(start=tm_map_m)
                                pg.mixer.music.set_volume(0.25)
                                tm_map_m = time() - tm_map_m
                                return
                if event.pos[0] >= rect_b_menu[0] and event.pos[1] >= rect_b_menu[1]:
                    if event.pos[0] <= rect_b_menu[0] + but_menu.get_rect().w and event.pos[1] >= rect_b_menu[1]:
                        if event.pos[0] <= rect_b_menu[0] + but_menu.get_rect().w and \
                                event.pos[1] <= rect_b_menu[1] + but_menu.get_rect().h:
                            if event.pos[0] >= rect_b_menu[0] and \
                                    event.pos[1] <= rect_b_menu[1] + but_menu.get_rect().h:
                                start_screen(sc)
        pygame.display.flip()


def game_stop():
    exit(0)


def next_level():
    global map_n, need_break
    map_n += 1
    map_n %= maps_n
    need_break = True
    set_message(f'Вы были перемещены на уровень {map_n + 1}', 5)


def set_level(n):
    global map_n, need_break
    map_n = n
    need_break = True
    set_message(f'Вы были перемещены на уровень {map_n + 1}', 5)


def shoot(player):
    if player.ammo[player.gun] and time() - player.last_shoot >= gun_rt[player.gun]:
        player.ammo[player.gun] -= 1
        player.last_shoot = time()
        gun_v[player.gun].play()
        objs = []
        for i in objects.sprites():
            if 0.2 < i.ang < 0.8 and dist_of_points(*player.pos, *i.pos) < rect_size2d * 2:
                objs += [i]
        if objs:
            i = sorted(objs, key=lambda x: dist_of_points(*x.pos, *player.pos))[0]
            i.hp -= gun_dam[player.gun]
            obj_v_dam.get(i.__class__, v_empty).play()


def draw_bar(sc, ft, text, color, num, max_, sz, pos):
    if color != white:
        c = white
    else:
        c = black
    sc.blit(ft.render(text, False, gray), pos)
    lsz = sz * (num / max_)
    if num > 0:
        pg.draw.rect(sc, color, (ft.size(text + ' ')[0] + pos[0], pos[1],
                                 lsz, ft.size(' ')[1]))
        sc.blit(ft.render(str(num), False, c), (ft.size(text + ' ')[0] + pos[0] +
                                                (lsz - ft.size(str(num))[1]) / 2,
                                                pos[1]))


def draw_message(sc, ft):
    if time() - tsm <= ttd:
        sc.blit(ft.render(message, False, red), (width // 2 - ft.size(message)[0] // 2, 20))


def set_message(text, t):
    global message, ttd, tsm
    message = text
    tsm = time()
    ttd = t


def draw_interface(sc, player):
    # global font, font2, font3
    global rect_b_menu
    draw_minimap(sc, player)

    draw_message(sc, font2)

    pg.draw.rect(sc, dk_gray, (0, height - 200, width, height))

    rect_b_menu = draw_button(sc, menu, width - menu.get_rect().w - 20, height - 180)

    draw_bar(sc, font2, f'AMMO{player.gun + 1}', red, player.ammo[player.gun], gun_amst[player.gun],
             500, (20, height - 150))

    draw_bar(sc, font2, 'HP         ', red, round(player.hp), 100, 500, (20, height - 80))

    draw_bar(sc, font3, '', blue, round((gun_rt[player.gun] - time() + player.last_shoot) * 100),
             gun_rt[player.gun] * 100, 500, (150, height - 170))


stena = None
menu = None
quitt = None
egip_stena = None
menu_fon = None
but_menu = None
continue_b = None
minin_in_menu = None
one = None
two = None
three = None
four = None
five = None
fon = None
lvl_fon = None

stena_pre_render = []
egipt_stena_pre_render = []
rect_b_menu = []

solid_cl = {Door, Enemy}
obj_nd = {Trigger, Spr}
obj_hp = {Spider: 10,
          Zombie: 2,
          Spawner: 20}

obj_dam = {Spider: 1,
           Zombie: 0.1}

v_empty = None

over_v = {}

gun_dam = [1, 5]
gun_rt = [1, 3]
gun_amst = [20, 5]
gun_v = []

obj_spr = {}
obj_v_dam = {}
obj_ded_v = {}

maps_music = []
menu_music = None
tm_map_m = 0

im_sh = None

font = None
font2 = None
font3 = None

message = ''
tsm = 0
ttd = 0

need_break = False


def main():
    global key_d, obj_spr, im_sh, stena, egip_stena, all_sprites, enemies, \
        objects, stena_pre_render, font, font2, font3, egipt_stena_pre_render, menu, need_break, quitt, menu_fon, \
        but_menu, fon, minin_in_menu, continue_b, one, two, three, four, five, lvl_fon, obj_v_dam, gun_v, v_empty, \
        over_v, obj_ded_v, maps_music, menu_music, tm_map_m

    pg.mixer.pre_init()
    pg.init()
    sc = pg.display.set_mode((width, height))
    # pg.display.toggle_fullscreen()

    clock = pg.time.Clock()

    obj_spr = {Door: load_image('дверь.png'),
               Spider: load_image('321.png'),
               Zombie: load_image('zombie.png'),
               Key: load_image('ключ.png'),
               Spawner: load_image('spawner.png'),
               'portal': load_image('portal.png'),
               Aptechka: load_image('аптечка.png'),
               'p1': load_image('патроны1.png'),
               'p2': load_image('патроны2.png')}

    im_sh = load_image('shrek3.png')
    menu = load_image('menu.png')
    quitt = load_image('quit.png')
    menu_fon = load_image('fon.jpg')
    but_menu = load_image('levels.png')
    minin_in_menu = load_image('mini_menu.png')
    continue_b = load_image('сontinue.png')
    one = load_image('1.png')
    two = load_image('2.png')
    three = load_image('3.png')
    four = load_image('4.png')
    five = load_image('5.png')
    lvl_fon = load_image('lvl_fon.png')
    fon = pygame.transform.scale(menu_fon, (width, height))

    stena = load_image('стена обыкновенная.png')
    egip_stena = load_image('египецкая стена ураааоаоаоаоаоао.png')

    for i in range(stena.get_rect().w - round(line_to_px)):
        stena_pre_render += [stena.subsurface(i, 0, round(line_to_px), stena.get_rect().h)]
        egipt_stena_pre_render += [egip_stena.subsurface(i, 0, round(line_to_px), egip_stena.get_rect().h)]

    font = pygame.font.Font(None, 24)
    font2 = pygame.font.Font(None, 48)
    font3 = pygame.font.Font(None, 10)

    obj_v_dam = {
        Spider: load_sound('spider_damage.wav')
    }

    gun_v = [
        load_sound('shoot_1.wav'),
        load_sound('shoot_2.wav')
    ]

    v_key = load_sound('key.wav')

    obj_ded_v = {
        Key: v_key,
        Aptechka: v_key,
        Patroni: v_key
    }

    maps_music = [
        'ур1.mp3',
        'ур2.mp3',
        'ур3.mp3',
        'ур4.mp3',
        'ур5.mp3'
    ]
    menu_music = 'меню.mp3'

    over_v = {
        'door_open': load_sound('door open.wav'),
        'door_not_open': load_sound('door not open.wav')
    }

    v_empty = load_sound('empty.wav')

    start_screen(sc)

    while True:
        running = True

        tm_map_m = time() - tm_map_m
        pg.mixer.music.load(os.path.join('data', 'sounds', maps_music[map_n]))
        pg.mixer.music.play()
        pg.mixer.music.set_volume(0.25)

        all_sprites = pg.sprite.Group()
        objects = pg.sprite.Group()
        enemies = pg.sprite.Group()

        ppos = None

        # player = Player(10 * rect_size2d, 10 * rect_size2d,
        #                 objects, solid_cl, map_n)

        # Spider(5 * rect_size2d, 1 * rect_size2d)
        # Spider(7 * rect_size2d, 0.55 * rect_size2d)

        # Door(6.2 * rect_size2d, 0.4 * rect_size2d, marsh=[(6.2 * rect_size2d, 0.10 * rect_size2d)])
        # Door(27 * rect_size2d // 4, 14.7 * rect_size2d // 4, marsh=[(27 * rect_size2d // 4, 13.5 * rect_size2d // 4)],
        #      key=0)

        # Key(30 * rect_size2d // 4, 2.5 * rect_size2d // 4, key=0)

        # Trigger(30 * rect_size2d // 4, 14.7 * rect_size2d // 4, foo=game_stop)

        # Spr(31 * rect_size2d // 4, 14.7 * rect_size2d // 4, spr=obj_spr['portal'])

        # unit generation

        player = Player(*map_obj[map_n]['player'], objects, solid_cl, map_n)

        for i in map_obj[map_n]['spider']:
            Spider(*i)

        for i in map_obj[map_n]['zombie']:
            Zombie(*i)

        for i in map_obj[map_n]['aptechka']:
            Aptechka(*i)

        for i in map_obj[map_n]['patroni']:
            Patroni(*i[:-1], i[-1])

        for i in map_obj[map_n]['spawner']:
            Spawner(*i[:2], eval(i[2]), *i[3:])

        for i in map_obj[map_n]['door']:
            Door(*i)

        for i in map_obj[map_n]['key']:
            Key(*i)

        for i in map_obj[map_n]['trigger']:
            Trigger(*i[:-1], foo=eval(i[-1]))

        for i in map_obj[map_n]['spr']:
            Spr(*i[:-1], spr=eval(i[-1]))

        while running:
            sc.fill((0, 0, 0))
            key_d = -1
            for event in pygame.event.get():
                if event.type == pg.QUIT:
                    running = False
                    exit(0)
                elif event.type == pg.KEYDOWN:
                    key_d = event.key
                    if event.key == pg.K_ESCAPE:
                        mini_menu_go(sc)
                    elif event.key == pg.K_SPACE:
                        shoot(player)
                    elif event.key == pg.K_1:
                        player.gun = 0
                    elif event.key == pg.K_2:
                        player.gun = 1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] >= rect_b_menu[0] and event.pos[1] >= rect_b_menu[1]:
                        if event.pos[0] <= rect_b_menu[0] + menu.get_rect().w and event.pos[1] >= rect_b_menu[1]:
                            if event.pos[0] <= rect_b_menu[0] + menu.get_rect().w and \
                                    event.pos[1] <= rect_b_menu[1] + menu.get_rect().h:
                                if event.pos[0] >= rect_b_menu[0] and event.pos[1] <= rect_b_menu[1] + \
                                        menu.get_rect().h:
                                    mini_menu_go(sc)
                                    # start_screen(sc)

            if (player.pos, player.ang) != ppos:
                lin = raycast_png(player)
            draw_3d_png(sc, lin, all_sprites.sprites(), player.pos)
            # lin = raycast_fps_stonks(player)
            # draw_3d(sc, lin, all_sprites.sprites(), player.pos)
            # draw_map(sc, player, lin)
            draw_interface(sc, player)
            for i in objects.sprites():
                if not i.is_ded:
                    i.step(player)

            ppos = (player.pos, player.ang)
            player.step()
            if player.hp <= 0:
                running = False
            # angle_of_points(*player.pos, *sh.pos, player.ang)
            sc.blit(font.render(str(round(clock.get_fps())), False, red), (width - 100, 50))
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

            if need_break:
                need_break = False
                break

    # pg.quit()


def draw_map(sc, player, lines):
    for i in map_coords:
        pg.draw.rect(sc, white, (i[0], i[1], rect_size2d, rect_size2d), 1)
        player.draw(sc)
    for i in lines:
        pg.draw.line(sc, gray, player.pos, i[0], 1)


def draw_minimap(sc, player):
    pg.draw.rect(sc, black, (0, 0, rect_size2d // 4 * len(map_[map_n][0]), rect_size2d // 4 * len(map_[map_n])))
    for i in maps[map_n]['map_coords']:
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
        if not i.is_ded and i.__class__ not in obj_nd:
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
    sp = [(False, i, dist_of_points(*ppos, *i.pos) * 3.85) for i in sp if not i.is_ded]
    lis = sorted(lin + sp, key=lambda x: -x[-1])
    for i in lis:
        if i[0]:
            ii = i[1]
            j = ii[1]
            # if ii[2] >= 256:
            #     ii[2] = 253
            if ii[3]:
                wall = egipt_stena_pre_render[ii[2] - 1]
            else:
                wall = stena_pre_render[ii[2] - 1]

            wall = pg.transform.scale(wall, (round(line_to_px), round(dist * rect_size2d / (j + 1)) * 2))
            sc.blit(wall, (ii[0] * round(line_to_px), height / 2 - dist * rect_size2d / (j + 1)))

            # c = 255 / (1 + j * j * 0.00001)
            # color = (c, c, c)
            # pg.draw.rect(sc, color, (ii[2] * line_to_px,
            #                          height / 2 - dist * rect_size2d / (j + 1),
            #                          line_to_px + 1,
            #                          dist * rect_size2d / (j + 1) * 2))
        else:
            if -i[1].rect.w * 8 <= i[1].rect.x <= width or False:
                sc.blit(i[1].image, (i[1].rect.x, i[1].rect.y))


if __name__ == '__main__':
    main()
