import math

FPS = 60

width = 1920
height = 1080

size = 32, 16  # размер карты
half_size = size[0] // 2, size[1] // 2  # центр карты и начальнаяпозиция игрока
rect_size2d = width / size[0]

draw_dist = 1500  # Длина лучей

fow = 30  # область видимости(FOV)
lines = 400  # Количество лучей(NUM_RAYS)
line_step = fow / lines / 50  # угол между лучами(DELTA_ANGLE)
line_to_px = width / lines  # ширина линии в 3д

bese_wall_h = 600  # дальность прорисовки (MAX_DEPTH)
# всякие нужные цвета
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
gray = (128, 128, 128)


