from settings import *

maps_n = 5  # кличество карт

maps = []  # информация о картах

map_ = [  # карты
    [
        '############################',
        '#--------------------------#',
        '#------------@-------------#',
        '#--------------------------#',
        '#--------------------------#',
        '##@##----------------------#',
        '#---###########------------#',
        '#---#----------------------#',
        '#---#---------#------------#',
        '#---########@##------------#',
        '#-------------#------------#',
        '#-------------#------------#',
        '#-------------#------------#',
        '#--------------------------#',
        '############################',
    ],
    [
        '############################',
        '#--#--#--------------------#',
        '#--#--#--------------------#',
        '#--#--#----#-------------#-#',
        '#--#--#----#-------------#-#',
        '#--#--#----#-------------#-#',
        '#--#--######-------------#-#',
        '#--#--#-------------#----#-#',
        '#--#--#-------------@----#-#',
        '#--#--#------#-----------#-#',
        '#--#--#------@#----------#--#',
        '#--#--#------------#-----#-#',
        '#-##--#------------#-----#-#',
        '#------------------------#-#',
        '#------------------------#-#',
        '#------------------------#-#',
        '#------------------------#-#',
        '############################',
    ],
    [
        '#########################',
        '#--------#------------#-#',
        '#--------#-####-------#-#',
        '#-----A--#-#--#-------#-#',
        '#----##--#-##-#----#--#-#',
        '#--------#--#-#---##--#-#',
        '#--#-----#--#-#---#---#-#',
        '#--#-----####-#@####--#-#',
        '#--#-------#-----#------#',
        '#----------#-----#---#A##',
        '#-------------#---------#',
        '#########################',
    ],
    [
        '--------------------------------',
        '--------------------------------',
        '--------------------------------',
        '--------------------------------',
        '################################',
        '#---#---------#----------------#',
        '#---#--------#-------@---------#',
        '##-##--####---#-------#--------#',
        '#-------------#-------####-----#',
        '#----#--------#----------------#',
        '#@-###--------#----------------#',
        '#------------------------------#',
        '#------------------------------#',
        '#------------------------------#',
        '#------#-----------------------#',
        '#-----##-----------------------#',
        '#-----#------------------------#',
        '#-------------#----------------#',
        '#-------------#----------------#',
        '#-------------#----------------#',
        '#-##----------#----------#####-#',
        '#--##---------#----------#---#-#',
        '#---@---------#--------------#-@',
        '################################',
    ],
    [
        '######################################################',
        '#--#---#-----#-#-----------#-----#--#-----#--@--#--#-#',
        '#-##---#-----#-#-----------#-----#--#-----#--#--#--#-#',
        '#------#-----#-#-----------#-----#--#-----#--#--#--#--',
        '#------#-------#-----------#-----#--#-----#--#--#--#-#',
        '#------#-------#-########--#-----#--#-----#--#--#----#',
        '#------@-------#--------#--------#--#-----#--#--#----#',
        '#------#-------#--------#--------#--#-----#--#--#----#',
        '#------#-------#--------#--------#--#-----#--#--#-#@##',
        '#------#----#--#--------#--------#--#-----#--#--#----#',
        '#------#----#--#--------#--------#-@#-----#--#--#----#',
        '#-######----#--#------#-#-----------------#--@--#----#',
        '#-----------#--########-#-----------------#--@--###-##',
        '#-----------#-----------#-------#---------#--#-------#',
        '#-----------#-----------#-------#---------#--#-------#',
        '#-----------#-----------#-------#---------#----------#',
        '#-----------#-------------------@#--------#-##########',
        '#-----------#-----------#-----------------#----------#',
        '#-----------#-----------#-----------------#----@-----#',
        '#-----------#-----------#----------------------------#',
        '#-----------#-----------#----------------------------#',
        '#########################@############################',
    ]
]

map_obj = [  # объекты на карте
    {
        'player': (2 * rect_size2d // 4, 8 * rect_size2d // 4),
        'spider': [],
        'zombie': [(4 * rect_size2d // 2, 2 * rect_size2d // 2), (8 * rect_size2d // 2, 2 * rect_size2d // 2),
                   (2 * rect_size2d // 2, 6 * rect_size2d // 2), (3.5 * rect_size2d // 2, 6 * rect_size2d // 2),
                   (8 * rect_size2d // 2, 3 * rect_size2d // 2)],
        'spawner': [],
        'door': [(14.5 * rect_size2d // 4, 13.5 * rect_size2d // 4,
                  [(14.5 * rect_size2d // 4, 15 * rect_size2d // 4)], -1),
                 (14.5 * rect_size2d // 4, 7.5 * rect_size2d // 4,
                  [(14.5 * rect_size2d // 4, 8.5 * rect_size2d // 4)], 0)],
        'key': [(2 * rect_size2d // 2, 2 * rect_size2d // 2, 0)],
        'trigger': [(8 * rect_size2d // 4, 8 * rect_size2d // 4, 'next_level')],
        'spr': [(7 * rect_size2d // 4, 8 * rect_size2d // 4, "obj_spr['portal']"),
                (2.5 * rect_size2d // 2, 1.55 * rect_size2d // 2, "obj_spr['fikus']")],
        'aptechka': [],
        'patroni': [],
    },
    {
        'player': (5.5 * rect_size2d // 4, 2 * rect_size2d // 4),
        'spider': [(10.5 * rect_size2d // 4, 5 * rect_size2d // 4), (7.5 * rect_size2d // 4, 4 * rect_size2d // 4),
                   (12.5 * rect_size2d // 4, 7 * rect_size2d // 4), (14.5 * rect_size2d // 4, 9.5 * rect_size2d // 4),
                   (4 * rect_size2d // 4, 15 * rect_size2d // 4), (2 * rect_size2d // 4, 2.5 * rect_size2d // 4),
                   (27.5 * rect_size2d // 4, 10.5 * rect_size2d // 4), (12 * rect_size2d // 4, 8 * rect_size2d // 4),
                   (12 * rect_size2d // 4, 13 * rect_size2d // 4)],
        'zombie': [(4.5 * rect_size2d // 4, 8 * rect_size2d // 4), (26.5 * rect_size2d // 4, 6 * rect_size2d // 4),
                   (5.5 * rect_size2d // 4, 5 * rect_size2d // 4), (10 * rect_size2d // 4, 10 * rect_size2d // 4),
                   (26.5 * rect_size2d // 4, 9 * rect_size2d // 4), (15 * rect_size2d // 4, 14 * rect_size2d // 4),
                   (11 * rect_size2d // 4, 15 * rect_size2d // 4)],
        'spawner': [],
        'door': [(1.5 * rect_size2d // 4, 12.5 * rect_size2d // 4,
                  [(1 * rect_size2d // 4, 12.5 * rect_size2d // 4)], 0),
                 (26.5 * rect_size2d // 4, 4.5 * rect_size2d // 4,
                  [(25.5 * rect_size2d // 4, 4.5 * rect_size2d // 4)], 1)],
        'key': [(8 * rect_size2d // 4, 5 * rect_size2d // 4, 1), (9 * rect_size2d // 4, 8 * rect_size2d // 4, 0)],
        'trigger': [(26.5 * rect_size2d // 4, 15 * rect_size2d // 4, 'next_level')],
        'spr': [(26.5 * rect_size2d // 4, 16 * rect_size2d // 4, "obj_spr['portal']"),
                (10 * rect_size2d // 2, 3 * rect_size2d // 2, "obj_spr['statya']")],
        'aptechka': [],
        'patroni': [(2 * rect_size2d // 4, 2 * rect_size2d // 4, 1), (2 * rect_size2d // 4, 3 * rect_size2d // 4, 1),
                    (2 * rect_size2d // 4, 4 * rect_size2d // 4, 1), (2 * rect_size2d // 4, 5 * rect_size2d // 4, 1)],
    },
    {
        'player': (11 * rect_size2d, 6 * rect_size2d),
        'spider': [(2 * rect_size2d // 4, 7 * rect_size2d // 4), (8.5 * rect_size2d // 4, 4.5 * rect_size2d // 4),
                   (15 * rect_size2d // 4, 8.5 * rect_size2d // 4), (23.5 * rect_size2d // 4, 5 * rect_size2d // 4),
                   (23.5 * rect_size2d // 4, 6 * rect_size2d // 4)],
        'zombie': [(3 * rect_size2d // 4, 4 * rect_size2d // 4), (4 * rect_size2d // 4, 5 * rect_size2d // 4),
                   (8 * rect_size2d // 4, 7 * rect_size2d // 4), (10.5 * rect_size2d // 4, 3.5 * rect_size2d // 4),
                   (10 * rect_size2d // 4, 9 * rect_size2d // 4), (17 * rect_size2d // 4, 5 * rect_size2d // 4),
                   (13.5 * rect_size2d // 4, 5 * rect_size2d // 4), (13.5 * rect_size2d // 4, 6 * rect_size2d // 4),
                   (18 * rect_size2d // 4, 3 * rect_size2d // 4), (20 * rect_size2d // 4, 3 * rect_size2d // 4),
                   (20 * rect_size2d // 4, 6.5 * rect_size2d // 4), (20 * rect_size2d // 4, 9 * rect_size2d // 4),
                   (22 * rect_size2d // 4, 10.5 * rect_size2d // 4)],
        'spawner': [],
        'door': [(13.5 * rect_size2d // 4, 7.5 * rect_size2d // 4,
                  [(13 * rect_size2d // 4, 8 * rect_size2d // 4)], 2), (21 * rect_size2d // 4, 10.5 * rect_size2d // 4,
                                                                        [(
                                                                         21 * rect_size2d // 4, 11 * rect_size2d // 4)],
                                                                        1),
                 (23.5 * rect_size2d // 4, 7.5 * rect_size2d // 4,
                  [(22.5 * rect_size2d // 4, 7.5 * rect_size2d // 4)], 3)],
        'key': [(13 * rect_size2d // 4, 4 * rect_size2d // 4, 3), (5.5 * rect_size2d // 4, 3.5 * rect_size2d // 4, 1),
                (23 * rect_size2d // 4, 10.5 * rect_size2d // 4, 2)],
        'trigger': [(23 * rect_size2d // 4, 3 * rect_size2d // 4, 'next_level')],
        'spr': [(23 * rect_size2d // 4, 2 * rect_size2d // 4, "obj_spr['portal']"),
                (5 * rect_size2d // 4, 5 * rect_size2d // 4, "obj_spr['fikus']"),
                (7 * rect_size2d // 4, 8 * rect_size2d // 4, "obj_spr['statya']")],
        'aptechka': [],
        'patroni': [(6 * rect_size2d // 4, 2.5 * rect_size2d // 4, 1), (3 * rect_size2d // 4, 10 * rect_size2d // 4, 0),
                    (12 * rect_size2d // 4, 10.5 * rect_size2d // 4, 1),
                    (19 * rect_size2d // 9, 3 * rect_size2d // 9, 1),
                    (2 * rect_size2d // 4, 7 * rect_size2d // 4, 1)],
    },
    {
        'player': (2.5 * rect_size2d, 6 * rect_size2d),
        'spider': [],
        'zombie': [],
        'spawner': [(5.5 * rect_size2d // 2, 3 * rect_size2d // 2, 'Zombie', [(5 * rect_size2d, 3 * rect_size2d)], 9),
                    (5.5 * rect_size2d // 2, 10 * rect_size2d // 2, 'Zombie', [(5 * rect_size2d, 9 * rect_size2d)], 9),
                    (12 * rect_size2d // 2, 3 * rect_size2d // 2, 'Spider', [(11 * rect_size2d, 4 * rect_size2d)], 9),
                    (12 * rect_size2d // 2, 10 * rect_size2d // 2, 'Spider', [(11 * rect_size2d, 9 * rect_size2d)], 9)],
        'door': [(12.75 * rect_size2d // 2, 11.25 * rect_size2d // 2,
                  [(12.75 * rect_size2d // 2, 12.25 * rect_size2d // 2)], 0)],
        'key': [(14.5 * rect_size2d // 2, 3 * rect_size2d // 2, 0)],
        'trigger': [(14.5 * rect_size2d // 2, 11 * rect_size2d // 2, 'next_level')],
        'spr': [(14.5 * rect_size2d // 2, 11 * rect_size2d // 2, "obj_spr['portal']")],
        'aptechka': [(9 * rect_size2d // 2, 4 * rect_size2d // 2), (9 * rect_size2d // 2, 9 * rect_size2d // 2)],
        'patroni': [(3 * rect_size2d // 2, 4 * rect_size2d // 2, 0), (3 * rect_size2d // 2, 9 * rect_size2d // 2, 0),
                    (7 * rect_size2d // 2, 6 * rect_size2d // 2, 1), (13 * rect_size2d // 2, 5 * rect_size2d // 2, 1),
                    (13 * rect_size2d // 2, 8 * rect_size2d // 2, 1)],
    },
    {
        'player': (1.3 * rect_size2d // 4, 5 * rect_size2d // 4),
        'spider': [(22 * rect_size2d // 2, 8 * rect_size2d // 2), (12 * rect_size2d // 2, 6 * rect_size2d // 2),
                   (17 * rect_size2d // 2, 2 * rect_size2d // 2), (2 * rect_size2d // 2, 10 * rect_size2d // 2)],
        'zombie': [(6.5 * rect_size2d // 2, 2 * rect_size2d // 2), (7.5 * rect_size2d // 2, 7 * rect_size2d // 2),
                   (18 * rect_size2d // 2, 6 * rect_size2d // 2), (3.5 * rect_size2d // 2, 2 * rect_size2d // 2),
                   (16 * rect_size2d // 2, 5 * rect_size2d // 2), (6 * rect_size2d // 2, 4 * rect_size2d // 2), ],
        'spawner': [
            (5 * rect_size2d // 4, 2 * rect_size2d // 4, 'Zombie', [(5 * rect_size2d // 2, 2 * rect_size2d // 2)], 3),
            (3 * rect_size2d // 2, 5 * rect_size2d // 2, 'Spider', [(2.5 * rect_size2d // 2, 4.5 * rect_size2d // 2)],
             10),
            (2.5 * rect_size2d // 2, 10 * rect_size2d // 2, 'Zombie', [(2.5 * rect_size2d // 2, 9 * rect_size2d // 2)],
             3),
            (7.5 * rect_size2d // 2, 10 * rect_size2d // 2, 'Spider', [(7.5 * rect_size2d // 2, 9 * rect_size2d // 2)],
             10),
            (9.5 * rect_size2d // 2, 2 * rect_size2d // 2, 'Spider', [(9.5 * rect_size2d // 2, 4 * rect_size2d // 2)],
             10),
            (11.5 * rect_size2d // 2, 2 * rect_size2d // 2, 'Zombie', [(12.5 * rect_size2d // 2, 3 * rect_size2d // 2)],
             1),
            (17.5 * rect_size2d // 2, 3 * rect_size2d // 2, 'Zombie', [(16.5 * rect_size2d // 2, 3 * rect_size2d // 2)],
             3),
            (11.5 * rect_size2d // 2, 5 * rect_size2d // 2, 'Zombie', [(12.5 * rect_size2d // 2, 6 * rect_size2d // 2)],
             3),
            (16.5 * rect_size2d // 2, 10 * rect_size2d // 2, 'Zombie',
             [(16.5 * rect_size2d // 2, 10 * rect_size2d // 2)], 3),
            (18.5 * rect_size2d // 2, 10 * rect_size2d // 2, 'Spider',
             [(18.5 * rect_size2d // 2, 10 * rect_size2d // 2)], 10),
            (22.5 * rect_size2d // 2, 10 * rect_size2d // 2, 'Spider',
             [(21.5 * rect_size2d // 2, 11 * rect_size2d // 2)], 10),
            (19.5 * rect_size2d // 2, 7 * rect_size2d // 2, 'Zombie', [(20.5 * rect_size2d // 2, 7 * rect_size2d // 2)],
             3),
            (22 * rect_size2d // 2, 5 * rect_size2d // 2, 'Spider', [(22.5 * rect_size2d // 2, 6 * rect_size2d // 2)],
             10)],
        'door': [(1.5 * rect_size2d // 4, 11.5 * rect_size2d // 4,
                  [(0.5 * rect_size2d // 4, 11.5 * rect_size2d // 4)]),
                 (14.5 * rect_size2d // 4, 3.75 * rect_size2d // 4,
                  [(13 * rect_size2d // 4, 3.75 * rect_size2d // 4)]),
                 (23.5 * rect_size2d // 4, 11.5 * rect_size2d // 4,
                  [(22.5 * rect_size2d // 4, 11.5 * rect_size2d // 4)], 1),
                 (16.5 * rect_size2d // 4, 5.5 * rect_size2d // 4,
                  [(15.5 * rect_size2d // 4, 5.5 * rect_size2d // 4)], 2),
                 (24.5 * rect_size2d // 4, 16.5 * rect_size2d // 4,
                  [(24.5 * rect_size2d // 4, 15.5 * rect_size2d // 4)]),
                 (34.5 * rect_size2d // 4, 10.5 * rect_size2d // 4,
                  [(33.5 * rect_size2d // 4, 10.5 * rect_size2d // 4)], 3),
                 (1.5 * rect_size2d // 4, 2.5 * rect_size2d // 4,
                  [(2.5 * rect_size2d // 4, 2.5 * rect_size2d // 4)], 0),
                 (43.5 * rect_size2d // 4, 16.5 * rect_size2d // 4,
                  [(42.5 * rect_size2d // 4, 16.5 * rect_size2d // 4)]),
                 (45.5 * rect_size2d // 4, 15.5 * rect_size2d // 4,
                  [(44.5 * rect_size2d // 4, 15.5 * rect_size2d // 4)]),
                 (51.5 * rect_size2d // 4, 12.5 * rect_size2d // 4,
                  [(50.5 * rect_size2d // 4, 12.5 * rect_size2d // 4)], 4),
                 (25.5 * rect_size2d // 4, 5.5 * rect_size2d // 4,
                  [(24.5 * rect_size2d // 4, 5.5 * rect_size2d // 4)], 404),
                 (26.5 * rect_size2d // 4, 5.5 * rect_size2d // 4,
                  [(27.5 * rect_size2d // 4, 5.5 * rect_size2d // 4)], 404),
                 (53.5 * rect_size2d // 4, 3.5 * rect_size2d // 4,
                  [(53.5 * rect_size2d // 4, 4.5 * rect_size2d // 4)], 404)
                 ],
        'key': [(14.5 * rect_size2d // 4, 1.75 * rect_size2d // 4, 1),
                (21.5 * rect_size2d // 4, 9.5 * rect_size2d // 4, 2),
                (21.5 * rect_size2d // 4, 3 * rect_size2d // 4, 3),
                (51.5 * rect_size2d // 4, 19 * rect_size2d // 4, 4),
                (52.5 * rect_size2d // 4, 1.5 * rect_size2d // 4, 0)],
        'trigger': [(1.5 * rect_size2d // 4, 1.5 * rect_size2d // 4, 'end')],
        'spr': [(1.5 * rect_size2d // 4, 1 * rect_size2d // 4, "obj_spr['portal']"),
                (2 * rect_size2d // 4, 7 * rect_size2d // 4, "obj_spr['fikus']"),
                (1.5 * rect_size2d // 4, 40 * rect_size2d // 4, "obj_spr['fikus']")],
        'aptechka': [(7 * rect_size2d // 4, 16 * rect_size2d // 4), (20.5 * rect_size2d // 4, 3 * rect_size2d // 4),
                     (48 * rect_size2d // 4, 20 * rect_size2d // 4), (40 * rect_size2d // 4, 20 * rect_size2d // 4)],
        'patroni': [(35 * rect_size2d // 4, 18 * rect_size2d // 4, 0),
                    (27 * rect_size2d // 4, 10 * rect_size2d // 4, 1),
                    (29 * rect_size2d // 4, 8 * rect_size2d // 4, 1),
                    (32 * rect_size2d // 4, 5 * rect_size2d // 4, 1),
                    (29 * rect_size2d // 4, 20 * rect_size2d // 4, 1),
                    (38 * rect_size2d // 4, 5 * rect_size2d // 4, 0),
                    (41 * rect_size2d // 4, 5 * rect_size2d // 4, 0),
                    (39.5 * rect_size2d // 4, 7 * rect_size2d // 4, 0),
                    (19 * rect_size2d // 4, 14 * rect_size2d // 4, 1),
                    (21 * rect_size2d // 4, 16 * rect_size2d // 4, 0)],
    }
]

for gg in range(maps_n):  # формирование удобных данных
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
