FPS = 60

width = 1920
height = 1080

size = 32, 16
half_size = size[0] // 2, size[1] // 2  # середина карты
rect_size2d = width / size[0]  # размер квадрата на карте

draw_dist = 1500  # длина луча

fow = 60  # угол прорисовки
lines = 100  # кол-во линий
line_step = fow / lines / 50  # угол между 2-мя лучами
line_to_px = width / lines  # ширина у 3д стены

bese_wall_h = 300  # высота у 3д стены

white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
gray = (128, 128, 128)
