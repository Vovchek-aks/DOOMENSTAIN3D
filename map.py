import pygame
from settings import *

maps_n = 2

maps = []

# map_ = [
#     '-'
# ]

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


map_ = [
    [
        '################################',
        '#------------------------------#',
        '#--@--------------------#------#',
        '#-----#-----------------########',
        '#----###-----------------------#',
        '#----#-------------------------#',
        '#------------------------------#',
        '#------------------------@-----#',
        '#-------------#######----------#',
        '#----------------#-------------#',
        '#----------------@-------------#',
        '#----------------#-------------#',
        '#-------------#######----------#',
        '#-------------------------######',
        '#------------------------------#',
        '################################',
    ],
    [
        '################################',
        '#------------------------------#',
        '#------------------------------#',
        '#------------------------------#',
        '#------------------------------#',
        '#------------------------------#',
        '#------------------------------#',
        '#------------------------------#',
        '#------------------------------#',
        '#------------------------------#',
        '#------------------------------#',
        '#------------------------------#',
        '#------------------------------#',
        '#------------------------------#',
        '#------------------------------#',
        '################################',
    ],
    [
        '###########',
        '#---------#',
        '#####-----#',
        '#---####--#',
        '#---#-----#',
        '#---####--#',
        '#---------#',
        '###########',
    ],
    [
        '################',
        '#-#-#----------#',
        '#-#-#--------#-#',
        '#-#-#--------#-#',
        '#-#-#---#----#-#',
        '#-#-#--------#-#',
        '#-#-#-----#--#-#',
        '#------------#-#',
        '################',
    ],
    [
        '#########################',
        '#--------#------------#-#',
        '#--------#-####-------#-#',
        '#-----#--#-#--#-------#-#',
        '#----##--#-##-#----#--#-#',
        '#--------#--#-#---##--#-#',
        '#--#-----#--#-#---#---#-#',
        '#--#-----####-######--#-#',
        '#--#-------#-----#------#',
        '#----------#--#--#---####',
        '#-------------#---------#',
        '#########################',
    ],
    [
        '################',
        '#-----#--------#',
        '#-----#--------#',
        '#-----#--------#',
        '#--------------#',
        '#--------------#',
        '#--------------#',
        '#--------------#',
        '#-----#--------#',
        '#-----#------#-#',
        '#-----#------#-#',
        '################',
    ],
    [
        '#-#######################################',
        '#---#---#-#------#--#--#-#------#-#-#-#-#',
        '#---#---#-#------#-----#-#------#-#-#-#--',
        '#---#-----#-####-#-----#-#------#-#-#---#',
        '#---#--#--#----#-#-----#-#------#-#-#-###',
        '#---#--#--#----#-#-----#-#------#-#-#---#',
        '#-###--#--####-#----------------#---###-#',
        '#------#-------#-------#--------#-#-----#',
        '#------#---------------##-------#-#######',
        '#------#-------#--------------#-#----#--#',
        '#------#-------#------------------------#',
        '#########################################',
    ]
]

map_obj = [
    {
        'player': (10 * rect_size2d, 10 * rect_size2d),
        'spider': [(5 * rect_size2d, 1 * rect_size2d), (7 * rect_size2d, 0.55 * rect_size2d)],
        'zombie': [],
        'spawner': [],
        'door': [(6.2 * rect_size2d, 0.4 * rect_size2d,
                  [(6.2 * rect_size2d, 0.10 * rect_size2d)]),

                 (27 * rect_size2d // 4, 14.7 * rect_size2d // 4,
                  [(27 * rect_size2d // 4, 13.5 * rect_size2d // 4)], 0)],

        'key': [(30 * rect_size2d // 4, 2.5 * rect_size2d // 4, 0)],
        'trigger': [(30 * rect_size2d // 4, 14.7 * rect_size2d // 4, 'next_level')],
        'spr': [(31 * rect_size2d // 4, 14.7 * rect_size2d // 4, "obj_spr['portal']")]
    },
    {
        'player': (10 * rect_size2d, 10 * rect_size2d),
        'spider': [],
        'zombie': [],
        'spawner': [(5 * rect_size2d, 1 * rect_size2d, 'Zombie', [(5 * rect_size2d, 2 * rect_size2d)], 3)],
        'door': [],
        'key': [],
        'trigger': [],
        'spr': []
    }
]

for gg in range(maps_n):
    map_coords = set()
    wall_coords = set()
    egypt_coords = set()
    map_list = [[True if j == '-' else False for j in i] for i in map_[gg]]

    for i, f in enumerate(map_[gg]):
        for j, g in enumerate(f):
            if g != '-':
                map_coords.add((j * rect_size2d, i * rect_size2d))
                if g == '#':
                    wall_coords.add((j * rect_size2d, i * rect_size2d))
                else:
                    egypt_coords.add((j * rect_size2d, i * rect_size2d))

    maps += [{
        'map_coords': map_coords,
        'wall_coords': wall_coords,
        'egypt_coords': egypt_coords,
        'map_list': map_list
    }]
