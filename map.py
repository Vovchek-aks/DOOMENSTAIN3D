import pygame
from settings import *


map_ = [
    '################################',
    '#------------------------------#',
    '#--#--------------------#------#',
    '#-----#-----------------########',
    '#----###-----------------------#',
    '#----#-------------------------#',
    '#------------------------------#',
    '#------------------------#-----#',
    '#-------------#######----------#',
    '#----------------#-------------#',
    '#----------------#-------------#',
    '#----------------#-------------#',
    '#-------------#######----------#',
    '#------------------------------#',
    '#------------------------------#',
    '################################',
]

# map_ = [
#     '################################',
#     '#------------------------------#',
#     '#------------------------------#',
#     '#------------------------------#',
#     '#------------------------------#',
#     '#------------------------------#',
#     '#------------------------------#',
#     '#------------------------------#',
#     '#------------------------------#',
#     '#------------------------------#',
#     '#------------------------------#',
#     '#------------------------------#',
#     '#------------------------------#',
#     '#------------------------------#',
#     '#------------------------------#',
#     '################################',
# ]

map_coords = set()
map_list = [[True if j == '-' else False for j in i] for i in map_]

for i, f in enumerate(map_):
    for j, g in enumerate(f):
        if g != '-':
            map_coords.add((j * rect_size2d, i * rect_size2d))
