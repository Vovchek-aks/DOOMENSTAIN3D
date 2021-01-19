import pygame as pg
from map import *
from settings import *
from player import Player
import math
import sys
import os
from time import time
from random import randint

all_sprites = pg.sprite.Group()  # группы спрайтов
objects = pg.sprite.Group()
enemies = pg.sprite.Group()

key_d = -1  # последняя нажатая клавиша для открытия дверей

map_n = 0  # номер текущей карты

znak = lambda x: 1 if x > 0 else -1  # возвращает знак числа


def angle_of_points(x1, y1, x2, y2, ang):  # игол между точками для определения х спайта
    dx = -(x1 - x2)
    dy = (y1 - y2)
    f = math.atan2(dx, dy)
    r = f - ang
    if not (y1 < y2 and x1 < x2 or ang == 0 and y1 >= y2) or y1 < y2 and ang >= math.radians(270):
        r += math.pi * 2

    if x1 < x2 and y1 >= y2 and math.radians(90) > ang > 0:
        r -= math.pi * 2
    return r - 1


def dist_of_points(x1, y1, x2, y2):  # растояние между точками
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return (dx ** 2 + dy ** 2) ** 0.5


def load_image(name, colorkey=None):  # загружает картинки
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


def load_sound(name):  # загружает звуки
    fullname = os.path.join('data', 'sounds', name)
    if not os.path.isfile(fullname):
        print(f"Файл со звуком '{fullname}' не найден")
        fullname = os.path.join('data', 'sounds', 'empty.wav')
    return pg.mixer.Sound(fullname)


class GameObject(pg.sprite.Sprite):  # родительский объект для всех внутреигровых объектов
    def __init__(self, x, y, *groups, sp=0.25, marsh=None, do_marsh=True):
        super().__init__(all_sprites, objects, *groups)
        self.base_im = obj_spr.get(self.__class__, im_sh)
        if self in enemies.sprites():
            self.base_im = self.base_im[0]
        self.image = self.base_im
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = -self.rect.w
        self.pos = x, y
        self.sp = sp
        self.is_ded = False
        self.ang = -1

        self.marsh = [self.pos]
        if marsh is not None:
            self.marsh = marsh

        self.mc = 0
        self.do_marsh = do_marsh

        self.hp = obj_hp.get(self.__class__, 1000000)

    def step(self, player):  # шаг, выполняется каждый кадр
        if self.hp <= 0:
            self.ded()
        self.go_marsh(player)
        self.draw3d(player)

    def go_marsh(self, player):  # перемещение по маршруту
        if self.do_marsh:
            if self.pos != self.marsh[self.mc]:
                self.move(*self.marsh[self.mc], player)
            else:
                self.mc += 1
                self.mc %= len(self.marsh)

    def move(self, x, y, player):  # перемещение к конкретной точке
        if abs(self.x - x) > self.sp:
            self.x -= self.sp * znak(self.x - x)
        else:
            self.x = x
        if abs(self.y - y) > self.sp:
            self.y -= self.sp * znak(self.y - y)
        else:
            self.y = y
        self.pos = self.x, self.y

    def draw3d(self, player, distd=1, sh=0, shx=0):  # подгонка размера и координаты из хотя из положения игрока
        dist = dist_of_points(*self.pos, *player.pos) / distd
        self.ang = angle_of_points(*player.pos, *self.pos,
                                   player.ang)
        if dist < 5:
            dist = 5
        self.rect.x = self.ang / line_step * line_to_px - self.image.get_rect().w // 2 + shx

        self.image = pg.transform.scale(self.base_im,
                                        (round(self.rect.w / (dist * 0.02 + 0.000000000001)),
                                         round(self.rect.h / (dist * 0.02 + 0.000000000001))))
        self.rect.y = height / 2 - (
                dist * 0.05 + 0.000000000001) - self.image.get_rect().h // 2 + 20 + self.rect.h / 40 + sh - 15

    def ded(self):  # смэрть
        self.is_ded = True
        self.pos = self.x, self.y = -100, -100
        obj_ded_v.get(self.__class__, v_empty).play()


class Enemy(GameObject):  # родительский класс противника
    def __init__(self, x, y, sp=0.25, marsh=None, do_marsh=True):
        super().__init__(x, y, enemies, sp=sp, marsh=marsh, do_marsh=do_marsh)
        self.tdd = 0

    def step(self, player):
        self.find_player(player)
        super().step(player)
        if self.hp <= obj_hp[self.__class__] // 2 and self.base_im != obj_spr[self.__class__][1]:
            self.base_im = obj_spr[self.__class__][1]

    def find_player(self, player):  # криво работающая функция поиска игрока
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

    def move(self, x, y, player):  # то же что и у родителя но сталкивается с пепятствиями
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

    def ded(self):  # +выбрасывание дропа
        r = randint(0, 5)
        if not r:
            Aptechka(*self.pos)
        elif r == 1:
            Patroni(*self.pos, 0)
        elif r == 2 and map_n >= 1:
            Patroni(*self.pos, 1)
        super().ded()


class Door(GameObject):  # дверь
    def __init__(self, x, y, marsh=None, key=-1):
        super().__init__(x, y, sp=0.25, marsh=marsh, do_marsh=False)
        self.key = key

    def go_marsh(self, player):  # смерть по открытию
        super().go_marsh(player)
        if self.pos == self.marsh[-1]:
            self.ded()

    def step(self, player):  # проверка открытия
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

    def draw3d(self, player, distd=2.5, sh=1, shx=10):  # дверь нужно рисовать чутка подругому
        d = dist_of_points(*self.pos, *player.pos)
        sh = -d ** 0.9 / 20
        shx *= d * 0.5 / 20
        super().draw3d(player, distd=distd, sh=sh, shx=shx)


class Spider(Enemy):  # паук
    pass


class Zombie(Enemy):  # зомби
    pass


class Spawner(GameObject):  # спавнер
    def __init__(self, x, y, obj=None, marsh=None, chst=1):
        super().__init__(x, y, sp=0, marsh=marsh, do_marsh=False)
        self.chst = chst

        self.obj = obj

        self.sch = 0

    def step(self, player):  # создание врагов с определённой частотой
        super().step(player)
        self.sch += 1
        if self.sch // 60 >= self.chst and len([i for i in enemies.sprites() if not i.is_ded]) < max_unit and \
                dist_of_points(*self.pos, *player.pos) <= rect_size2d * 2:
            self.sch = 0
            can_spawn = True
            for i in enemies.sprites():
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


class Key(GameObject):  # ключ
    def __init__(self, x, y, key=-1):
        super().__init__(x, y, sp=0)
        self.key = key

    def step(self, player):  # проверка сталкновения с игроком
        if dist_of_points(*self.pos, *player.pos) <= 20:
            set_message(f'Вы подобрали ключ {self.key}', 3)
            player.keys.add(self.key)
            self.ded()
        super().step(player)


class Trigger(GameObject):  # триггер
    def __init__(self, x, y, foo=lambda: None):
        super().__init__(x, y, sp=0)
        self.foo = foo
        self.rect.x, self.rect.y = -1000, -1000

    def step(self, player):  # проверка сталкновения с игроком
        if dist_of_points(*self.pos, *player.pos) <= 20:
            self.foo()
            self.ded()
        super().step(player)

    def draw3d(self, player, distd=1, sh=0, shx=0):  # триггер не рисуется
        pass


class Spr(GameObject):  # спрайт
    def __init__(self, x, y, spr):
        super().__init__(x, y, sp=0)
        self.base_im = self.image = spr


class Aptechka(GameObject):  # аптечка
    def __init__(self, x, y):
        super().__init__(x, y, do_marsh=False, sp=0)

    def step(self, player):  # проверка сталкновения с игроком
        super().step(player)
        if dist_of_points(*self.pos, *player.pos) <= 10:
            player.hp = 100
            self.ded()


class Patroni(GameObject):  # патроны
    def __init__(self, x, y, tp):
        super().__init__(x, y, do_marsh=False, sp=0)
        self.type = tp
        if tp:
            self.image = self.base_im = obj_spr['p2']
        else:
            self.image = self.base_im = obj_spr['p1']

    def step(self, player):  # проверка сталкновения с игроком
        super().step(player)
        if dist_of_points(*self.pos, *player.pos) <= 10:
            player.ammo[self.type] = gun_amst[self.type]
            self.ded()


def grid_pos(x, y):  # координаты квадрата в котором стоим
    return x // rect_size2d * rect_size2d, y // rect_size2d * rect_size2d


def raycast_png(player):  # пускает лучи с целью узнать где рисовать 3д стены
    global rast_hor, rast_vert, x_vert, y_vert, x_hor, y_hor
    ret = []
    st_b = stena.get_rect()
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
            shift = (y_vert - yt) / rect_size2d * (st_b.w - round(line_to_px))
            pict = is_egipt_vert
        else:
            rast = rast_hor
            xt = grid_pos(x_hor, y_hor)[0]
            shift = (x_hor - xt) / rect_size2d * (st_b.w - round(line_to_px))
            pict = is_egipt_hor

        rast *= math.cos(player.ang - a)  # стены прямые, без округлостей
        # xx = player.x + rast * cos
        # yy = player.y + rast * sin

        if rast < 20:
            rast = 20

        ret += [(i, rast, round(shift), pict)]

    return ret


def draw_button(sc, name, x, y):  # рисует кнопку
    sc.blit(name, (x, y))
    return (x, y)


def start_screen(sc):  # рисует стартовое меню
    menu_rect = menu.get_rect()
    b_rect = but_menu.get_rect()
    pg.mixer.music.load(os.path.join('data', 'sounds', 'меню.mp3'))
    pg.mixer.music.play()
    pg.mixer.music.set_volume(1)

    sc.blit(fon, (0, 0))
    running = True
    rect_b_lv = draw_button(sc, but_menu, width // 2 - menu_rect.h * 6, (height - menu_rect.h) / 2.5 - 50)
    rect_b_quit = draw_button(sc, quitt, width // 2 - menu_rect.h * 6, (height - menu_rect.h) / 2 + 220)
    regul_b = draw_button(sc, regulations, width // 2 - menu_rect.h * 6,
                          (height - menu_rect.h) / 2.5 + 135)
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.pos[0] >= regul_b[0] and event.pos[1] >= regul_b[1]:
                    if event.pos[0] <= regul_b[0] + b_rect.w and event.pos[1] >= regul_b[1]:
                        if event.pos[0] <= regul_b[0] + b_rect.w and \
                                event.pos[1] <= regul_b[1] + b_rect.h:
                            if event.pos[0] >= regul_b[0] and event.pos[1] <= regul_b[1] + b_rect.h:
                                pravila(sc)
                if event.pos[0] >= rect_b_lv[0] and event.pos[1] >= rect_b_lv[1]:
                    if event.pos[0] <= rect_b_lv[0] + b_rect.w and event.pos[1] >= rect_b_lv[1]:
                        if event.pos[0] <= rect_b_lv[0] + b_rect.w and \
                                event.pos[1] <= rect_b_lv[1] + b_rect.h:
                            if event.pos[0] >= rect_b_lv[0] and event.pos[1] <= rect_b_lv[1] + b_rect.h:
                                return
                if event.pos[0] >= rect_b_quit[0] and event.pos[1] >= rect_b_quit[1]:
                    if event.pos[0] <= rect_b_quit[0] + b_rect.w and event.pos[1] >= rect_b_quit[1]:
                        if event.pos[0] <= rect_b_quit[0] + b_rect.w and \
                                event.pos[1] <= rect_b_quit[1] + b_rect.h:
                            if event.pos[0] >= rect_b_quit[0] and \
                                    event.pos[1] <= rect_b_quit[1] + b_rect.h:
                                pg.quit()
                                sys.exit()
        pg.display.flip()


def pravila(sc):  # рисует правила
    global en_rus

    rus = ["Введение", "",
           "И так.... Вы - известный археолог,  у которого цель в жизни - найти самую большую гробницу ",
           "в мире (гробницу императора Нинтоку) и забрать все её сокровища себе. ",
           "Много лет вы не могли норамально спать и есть, всё время думая об этой загадочной гробнице.",
           "И вот однажды идя один по заброшенной пустыне, куда вас выбросило после огромного взрыва, ",
           "который произошол из-за перегрева двигателя самолёта на котором вы летели на экспедицию, наконец-то",
           " вдали показалась верхушка той самой гробницы!",
           "Дойдя до неё вы обнаружили длинный тонель в который не думая зашли...А зря... ",
           "Дверь которая вела наружу за вами закрылась... И теперь чтобы добраться до сокровищ и вернуться",
           "невредимым домой вы должны пройти все уровни, которые приготовила вам судьба...."]
    ru_prav = ["Правила игры", "",
               "DOOMENSTAIN3D это неповторимая пародия классической трёхмерной игры wolfenstain с элементами doom.",
               "Цель игры пройти все уровни (их 5),  убивая на своём пути всех монстров... ",
               "Да, никто не говорил, что это просто, но как вы хотели? ",
               "w - вперёд  s - назад",
               "а - влево боком  d - вправо боком",
               "q - поворот налево  е - поворот направо",
               "В игре есть двери, к некоторым из них нужен ключ, который необходимо собрать",
               "f - открыть дверь",
               "Изначально у игрока будет полный запас патронов, пополнить их можно, найдя их на дороге или ",
               "подобрать из побеждённого монстра",
               "Пробел - стрелять  1 - пистолет  2 - дробовик"]
    sc.blit(lvl_fon, (0, 0))
    menu_rect = menu.get_rect()
    b_rect = but_menu.get_rect()
    regul_b = draw_button(sc, back, width - menu_rect.h - 100, height - menu_rect.h - 50)
    next_b = draw_button(sc, next, width - menu_rect.h - 100, height - menu_rect.h - 150)
    text_coord = 150
    for line in rus:
        string_rendered = font_play.render(line, 1, pg.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 150
        text_coord += intro_rect.height
        sc.blit(string_rendered, intro_rect)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.pos[0] >= regul_b[0] and event.pos[1] >= regul_b[1]:
                    if event.pos[0] <= regul_b[0] + b_rect.w and event.pos[1] >= regul_b[1]:
                        if event.pos[0] <= regul_b[0] + b_rect.w and \
                                event.pos[1] <= regul_b[1] + b_rect.h:
                            if event.pos[0] >= regul_b[0] and event.pos[1] <= regul_b[1] + b_rect.h:
                                start_screen(sc)
                                return
                if event.pos[0] >= next_b[0] and event.pos[1] >= next_b[1] and \
                        event.pos[0] <= next_b[0] + b_rect.w and event.pos[1] >= next_b[1] and \
                        event.pos[0] <= next_b[0] + b_rect.w and \
                        event.pos[1] <= next_b[1] + b_rect.h and event.pos[0] >= next_b[0] and \
                        event.pos[1] <= next_b[1] + b_rect.h:
                    sc.blit(lvl_fon, (0, 0))
                    regul_b = draw_button(sc, back, width - menu_rect.h - 100, height - menu_rect.h - 50)
                    text_coord = 150
                    for line in ru_prav:
                        string_rendered = font_play.render(line, 1, pg.Color('black'))
                        intro_rect = string_rendered.get_rect()
                        text_coord += 10
                        intro_rect.top = text_coord
                        intro_rect.x = 150
                        text_coord += intro_rect.height
                        sc.blit(string_rendered, intro_rect)

        pg.display.flip()


def mini_menu_go(sc):  # рисует меню паузы
    global tm_map_m

    menu_rect = menu.get_rect()
    b_rect = but_menu.get_rect()

    tm_map_m = time() - tm_map_m
    pg.mixer.music.load(os.path.join('data', 'sounds', 'меню.mp3'))
    pg.mixer.music.play()
    pg.mixer.music.set_volume(0.5)

    sc.blit(fon, (0, 0))
    running = True
    rect_b_c = draw_button(sc, continue_b, width // 2 - menu_rect.h * 6, (height - menu_rect.h) / 2)
    rect_b_menu = draw_button(sc, minin_in_menu, width // 2 - menu_rect.h * 6,
                              (height - menu_rect.h) / 2 + 200)
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.pos[0] >= rect_b_c[0] and event.pos[1] >= rect_b_c[1]:
                    if event.pos[0] <= rect_b_c[0] + b_rect.w and event.pos[1] >= rect_b_c[1]:
                        if event.pos[0] <= rect_b_c[0] + b_rect.w and \
                                event.pos[1] <= rect_b_c[1] + b_rect.h:
                            if event.pos[0] >= rect_b_c[0] and event.pos[1] <= rect_b_c[1] + b_rect.h:
                                pg.mixer.music.load(os.path.join('data', 'sounds', maps_music[map_n]))
                                pg.mixer.music.play(start=tm_map_m)
                                pg.mixer.music.set_volume(0.25)
                                tm_map_m = time() - tm_map_m
                                return
                if event.pos[0] >= rect_b_menu[0] and event.pos[1] >= rect_b_menu[1]:
                    if event.pos[0] <= rect_b_menu[0] + b_rect.w and event.pos[1] >= rect_b_menu[1]:
                        if event.pos[0] <= rect_b_menu[0] + b_rect.w and \
                                event.pos[1] <= rect_b_menu[1] + b_rect.h:
                            if event.pos[0] >= rect_b_menu[0] and \
                                    event.pos[1] <= rect_b_menu[1] + b_rect.h:
                                start_screen(sc)
                                set_level(0)
                                return
        pg.display.flip()


def game_stop():  # оч сложная для понимания функция
    exit(0)


def end():
    global need_break, tm_map_m

    tm_map_m = time() - tm_map_m
    pg.mixer.music.load(os.path.join('data', 'sounds', 'меню.mp3'))
    pg.mixer.music.play()
    pg.mixer.music.set_volume(0.5)
    sc = pg.display.set_mode((width, height))
    sc.blit(lvl_fon, (0, 0))
    start_o = start_over.get_rect()
    k = 0
    over = draw_button(sc, start_over, (width - start_over.get_rect().w) // 2, height - 300)
    end_txt = ['После долгих и возможно мучительных дней в гробнице, вы наконец-то',
               'выбрались от туда и вернулись с нехилым таким состоянием к себе домой !']
    text_coord = 150
    for line in end_txt:
        string_rendered = font_end.render(line, 1, black)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 150
        text_coord += intro_rect.height
        sc.blit(string_rendered, intro_rect)
    while True:
        if rich.get_rect().w + k < width - 200:
            socrovishe_b = draw_button(sc, socrovishe, rich.get_rect().w + k, height - 450)
            k += 150
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.pos[0] >= over[0] and event.pos[1] >= over[1]:
                    if event.pos[0] <= over[0] + start_o.w and event.pos[1] >= over[1]:
                        if event.pos[0] <= over[0] + start_o.w and \
                                event.pos[1] <= over[1] + start_o.h:
                            if event.pos[0] >= over[0] and \
                                    event.pos[1] <= over[1] + start_o.h:
                                start_screen(sc)
                                set_level(0)
                                return
        pg.display.flip()



def next_level():  # тож непонятно
    global map_n, need_break
    map_n += 1
    map_n %= maps_n
    need_break = True
    set_message(f'Уровень {map_n + 1}', 5)


def set_level(n):  # и тут
    global map_n, need_break
    map_n = n
    need_break = True
    set_message(f'Уровень {map_n + 1}', 5)


def shoot(player):  # выстрел игрока (это должно быть в классе игрока, но не страшно)
    global tdsh
    if time() - player.last_shoot >= gun_rt[player.gun]:
        if player.ammo[player.gun]:
            player.ammo[player.gun] -= 1
            player.last_shoot = time()
            gun_v[player.gun].play()
            tdsh = time()
            objs = []
            for i in objects.sprites():
                if 0.2 < i.ang < 0.8 and dist_of_points(*player.pos, *i.pos) < rect_size2d * 2:
                    objs += [i]
            if objs:
                i = sorted(objs, key=lambda x: dist_of_points(*x.pos, *player.pos))[0]
                i.hp -= gun_dam[player.gun]
                if i in enemies.sprites():
                    i.tdd = time()
                obj_v_dam.get(i.__class__, v_empty).play()
        else:
            over_v['no_ammo'].play()


def draw_bar(sc, ft, text, color, num, max_, sz, pos):  # рисует название величины и саму величину
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


def draw_message(sc, ft):  # рисует сообщение пользователю
    if time() - tsm <= ttd:
        sc.blit(ft.render(message, False, red), (width // 2 - ft.size(message)[0] // 2, 20))


def set_message(text, t):  # устанавливает сообщение пользователю
    global message, ttd, tsm
    message = text
    tsm = time()
    ttd = t


def draw_gun(sc, player):  # рисует выбранную пушку
    im = obj_spr['guns'][player.gun]
    r = im.get_rect()
    sc.blit(im, (width // 2 - r.w // 2, height - 200 - r.h))


def draw_shoot(sc):  # рисует выстрел
    if time() - tdsh <= 0.1:
        im = obj_spr['shoot']
        r = im.get_rect()
        sc.blit(im, (width // 2 - r.w // 2, height - 250 - r.h))


def draw_interface(sc, player):  # рисует интерфейс
    # global font, font2, font3
    global rect_b_menu

    if is_minimap:
        draw_minimap(sc, player)

    draw_message(sc, font2)

    pg.draw.rect(sc, dk_gray, (0, height - 200, width, height))

    rect_b_menu = draw_button(sc, menu, width - menu.get_rect().w - 20, height - 180)

    draw_bar(sc, font2, f'AMMO{player.gun + 1}', red, player.ammo[player.gun], gun_amst[player.gun],
             500, (20, height - 150))

    draw_bar(sc, font2, 'HP         ', red, round(player.hp), 100, 500, (20, height - 80))

    draw_bar(sc, font3, '', blue, round((gun_rt[player.gun] - time() + player.last_shoot) * 100),
             gun_rt[player.gun] * 100, 500, (150, height - 170))

    draw_shoot(sc)

    draw_gun(sc, player)


stena = None  # страшные настины переменные (Нормальные!)
menu = None
quitt = None
egip_stena = None
menu_fon = None
but_menu = None
start_over = None
continue_b = None
minin_in_menu = None
regulations = None
fon = None
lvl_fon = None
back = None
az = None
next = None
rich = None
socrovishe = None

stena_pre_render = []  # пре ренддеренные кусочки стены
egipt_stena_pre_render = []
rect_b_menu = []

solid_cl = {Door, Enemy}  # различная информация об объектах
obj_nd = {Trigger, Spr}
obj_hp = {Spider: 10,
          Zombie: 2,
          Spawner: 5}

obj_dam = {Spider: 1,
           Zombie: 0.1}

obj_spr = {}
obj_v_dam = {}
obj_ded_v = {}

v_empty = None  # пустой звук

over_v = {}  # другие звуки

gun_dam = [1, 5]  # всё связанное с пушкой
gun_rt = [1, 3]
gun_amst = [20, 5]
gun_v = []

maps_music = []  # музыка
menu_music = None
tm_map_m = 0

im_sh = None  # вщ хз (Вова поставил Шрека, но сам его вщ не уважает, КАК ТАК ВОВА ТЫ МОГ ЗАБЫТЬ ПРО ШРЕКА?!)

font = None  # шрифты
font2 = None
font3 = None
font_play = None
font_end = None

message = ''  # глобальные переменные нужные для работы сообщений
tsm = 0
ttd = 0

need_break = False  # необходимость перезагрузить уровень

tdsh = 0  # для рисование выстрела


def main():  # мэин
    # берём в глобал всю эту радость
    global key_d, obj_spr, im_sh, stena, egip_stena, all_sprites, enemies, \
        objects, stena_pre_render, font, font2, font3, egipt_stena_pre_render, menu, need_break, quitt, menu_fon, \
        but_menu, fon, minin_in_menu, continue_b, lvl_fon, obj_v_dam, gun_v, v_empty, \
        over_v, obj_ded_v, maps_music, menu_music, tm_map_m, back, regulations, font_play, az, next, rich, font_end, \
        start_over, socrovishe

    # необхадимая настройка перед главным циклом
    pg.mixer.pre_init()
    pg.init()
    sc = pg.display.set_mode((width, height))
    # pg.display.toggle_fullscreen()

    clock = pg.time.Clock()

    obj_spr = {Door: load_image('дверь.png'),
               Spider: [load_image('spider.png'),
                        load_image('spider ранен(.png')],
               Zombie: [load_image('zombie.png'),
                        load_image('zombie2.png')],
               Key: load_image('ключ.png'),
               Spawner: load_image('spawner.png'),
               'portal': load_image('portal.png'),
               Aptechka: load_image('аптечка.png'),
               'p1': load_image('патроны1.png'),
               'p2': load_image('патроны2.png'),
               'guns': [load_image('gun1.png'),
                        load_image('gun2.png')],
               'shoot': load_image('bank.png')}

    im_sh = load_image('shrek3.png')
    menu = load_image('menu.png')
    quitt = load_image('quit.png')
    menu_fon = load_image('fon.jpg')
    but_menu = load_image('levels.png')
    minin_in_menu = load_image('mini_menu.png')
    continue_b = load_image('сontinue.png')
    regulations = load_image('regulations.png')
    lvl_fon = load_image('lvl_fon.png')
    back = load_image('back.png')
    az = load_image('lang.png')
    next = load_image('next.png')
    rich = load_image('rich_end.png')
    start_over = load_image('Start_over.png')
    socrovishe = load_image('socrovishe.png')
    fon = pg.transform.scale(menu_fon, (width, height))
    lvl_fon = pg.transform.scale(lvl_fon, (width, height))
    stena = load_image('стена обыкновенная.png')
    egip_stena = load_image('египецкая стена ураааоаоаоаоаоао.png')

    for i in range(stena.get_rect().w - round(line_to_px)):
        stena_pre_render += [stena.subsurface(i, 0, round(line_to_px), stena.get_rect().h)]
        egipt_stena_pre_render += [egip_stena.subsurface(i, 0, round(line_to_px), egip_stena.get_rect().h)]

    font = pg.font.Font(None, 24)
    font2 = pg.font.Font(None, 48)
    font3 = pg.font.Font(None, 9)
    font_play = pg.font.Font(os.path.join('data', 'fonts', '20179.ttf'), 30)
    font_end = pg.font.Font(os.path.join('data', 'fonts', '20179.ttf'), 50)

    obj_v_dam = {
        Spider: load_sound('spider_damage.wav'),
        Zombie: load_sound('zombie_damage.wav'),
        Spawner: load_sound('spawner_damage.wav')
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

    over_v = {
        'door_open': load_sound('door open.wav'),
        'door_not_open': load_sound('door not open.wav'),
        'no_ammo': load_sound('no_ammo.wav')
    }

    v_empty = load_sound('empty.wav')

    maps_music = [
        'ур1.mp3',
        'ур2.mp3',
        'ур3.mp3',
        'ур4.mp3',
        'ур5.mp3'
    ]
    menu_music = 'меню.mp3'

    start_screen(sc)  # рисуем меню

    while True:  # цикл уровней
        running = True

        tm_map_m = time() - tm_map_m  # подрубаем музон
        pg.mixer.music.load(os.path.join('data', 'sounds', maps_music[map_n]))
        pg.mixer.music.play()
        pg.mixer.music.set_volume(0.25)

        # загружаем уровень
        all_sprites = pg.sprite.Group()
        objects = pg.sprite.Group()
        enemies = pg.sprite.Group()

        ppos = None

        # ставим юнитов и игрока

        player = Player(*map_obj[map_n]['player'], objects, solid_cl, map_n)

        if True:  # важно!!!!
            for i in map_obj[map_n]['spider']:
                Spider(*i)

            for i in map_obj[map_n]['zombie']:
                Zombie(*i)

            for i in map_obj[map_n]['spawner']:
                Spawner(*i[:2], eval(i[2]), *i[3:])

        for i in map_obj[map_n]['aptechka']:
            Aptechka(*i)

        for i in map_obj[map_n]['patroni']:
            Patroni(*i[:-1], i[-1])

        for i in map_obj[map_n]['door']:
            Door(*i)

        for i in map_obj[map_n]['key']:
            Key(*i)

        for i in map_obj[map_n]['trigger']:
            Trigger(*i[:-1], foo=eval(i[-1]))

        for i in map_obj[map_n]['spr']:
            Spr(*i[:-1], spr=eval(i[-1]))

        while running:  # цикл внитри уровня
            sc.fill((0, 0, 0))
            key_d = -1
            for event in pg.event.get():
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
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.pos[0] >= rect_b_menu[0] and event.pos[1] >= rect_b_menu[1]:
                        if event.pos[0] <= rect_b_menu[0] + menu.get_rect().w and event.pos[1] >= rect_b_menu[1]:
                            if event.pos[0] <= rect_b_menu[0] + menu.get_rect().w and \
                                    event.pos[1] <= rect_b_menu[1] + menu.get_rect().h:
                                if event.pos[0] >= rect_b_menu[0] and event.pos[1] <= rect_b_menu[1] + \
                                        menu.get_rect().h:
                                    mini_menu_go(sc)

            if (player.pos, player.ang) != ppos:
                lin = raycast_png(player)
            draw_3d_png(sc, lin, all_sprites.sprites(), player.pos)
            draw_interface(sc, player)
            for i in objects.sprites():
                if not i.is_ded:
                    i.step(player)

            ppos = (player.pos, player.ang)
            player.step()
            if player.hp <= 0:
                running = False
            sc.blit(font.render(str(round(clock.get_fps())), False, red), (width - 100, 50))
            pg.display.flip()
            clock.tick(FPS)

            if need_break:
                need_break = False
                break


def draw_minimap(sc, player):  # рисует миникарту (можно врубить в настройках)
    pg.draw.rect(sc, black, (0, 0, rect_size2d // 4 * len(map_[map_n][0]), rect_size2d // 4 * len(map_[map_n])))
    for i in maps[map_n]['map_coords']:
        pg.draw.rect(sc, gray, (i[0] // 4, i[1] // 4, rect_size2d // 4, rect_size2d // 4))
        player.draw_minamap(sc)
    for i in objects.sprites():
        if i.__class__ == Enemy or i.__class__.__bases__[0] == Enemy:
            color = red
        else:
            color = blue
        if not i.is_ded and i.__class__ not in obj_nd:
            pg.draw.circle(sc, color, i.pos, 5)


def draw_3d_png(sc, lin, sp, ppos):  # рисует стены
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
            if ii[3]:
                wall = egipt_stena_pre_render[ii[2] - 1]
            else:
                wall = stena_pre_render[ii[2] - 1]

            wall = pg.transform.scale(wall, (round(line_to_px), round(dist * rect_size2d / (j + 1)) * 2))
            sc.blit(wall, (ii[0] * round(line_to_px), height / 2 - dist * rect_size2d / (j + 1)))
        else:
            if -i[1].rect.w * 8 <= i[1].rect.x <= width or False:
                sc.blit(i[1].image, (i[1].rect.x, i[1].rect.y))


if __name__ == '__main__':
    main()
