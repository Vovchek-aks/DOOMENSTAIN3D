import math

FPS = 60

width = 1366
height = 769

size = 32, 16  # размер карты
half_size = size[0] // 2, size[1] // 2  # центр карты и начальнаяпозиция игрока
rect_size2d = 1920 // size[0]  # размер 2д прямоугольника на карте

draw_dist = 20000  # Длина лучей

fow = 60  # область видимости
lines = 500  # Количество лучей
line_step = fow / lines / 50  # угол между лучами
line_to_px = width / lines  # ширина линии в 3д

bese_wall_h = 600  # дальность прорисовки

# всякие нужные цвета
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
gray = (128, 128, 128)
black = (0, 0, 0)


