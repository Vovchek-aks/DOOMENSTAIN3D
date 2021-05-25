import math
from screeninfo import get_monitors


# это можно настроить по желанию

lines = 200  # Количество лучей (качество картинки)
is_minimap = False  # нужно ли рисовать миникарту
max_unit = 30  # максимальное количество мобов

# то что ниже трогать нельзя!!!!!

FPS = 60  # фпс

width = get_monitors()[0].width  # получение разрешения экрана
height = get_monitors()[0].height

# size = 32, 32  # размер карты
# half_size = size[0] // 2, size[1] // 2  # центр карты и начальнаяпозиция игрока
rect_size2d = 60  # размер 2д прямоугольника на карте

fow = 60  # область видимости
line_step = fow / lines / 50  # угол между лучами
line_to_px = width / lines  # ширина линии в 3д

# всякие нужные цвета
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
gray = (128, 128, 128)
dk_gray = (16, 16, 16)
black = (0, 0, 0)
blue = (10, 128, 255)
