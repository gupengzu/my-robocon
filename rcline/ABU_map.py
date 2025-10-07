from rcline import *

map = Map(width=6, height=12, title='ABU Map',grid=0.5)

entity_list = [
    Polygon([(5,0),(5,1),(6,1)],close=False),
    #井字棋区域
    Polygon([(0,0.44),(0.135,0.44),(0.135,1.920),(0,1.920)],close=False,solid=True),
    Polygon([(0,2.5),(4.5,2.5)],close=False,solid=True),
    #武器使用区域
    Polygon([(1,2.5),(1,2.2),(2.5,2.2),(2.5,2.5)],close=True,solid=False),
    #下坡区域
    Polygon([(4.5,1.2),(4.5,2.7)],close=False,solid=True),
    Polygon([(4.5,1.2),(4.5,2.7),(6,2.7),(6,1.2)],close=True,solid=False),
    #梅林
    Polygon([(1.2,4),(4.8,4),(4.8,8.8),(1.2,8.8)],close=True,solid=False),
    Line([(2.4,4),(2.4,8.8)],solid=False),
    Line([(3.6,4),(3.6,8.8)],solid=False),
    Line([(1.2,5.2),(4.8,5.2)],solid=False),
    Line([(1.2,6.4),(4.8,6.4)],solid=False),
    Line([(1.2,7.6),(4.8,7.6)],solid=False),

    Line([(0,10),(6,10)],solid=False),

    Polygon([(1,12),(1,11.2),(1.8,11.2),(1.8,12)],close=False,solid=False),
    #武器架
    Polygon([(3,12),(3,11.7),(3.8,11.7),(3.8,12)],close=True,solid=True),
    Polygon([(0,10.45),(0.125,10.45),(0.125,11.65),(0,11.65)],close=True,solid=True),

    Polygon([(5,12),(5,11),(6,11),(6,12)],close=False,solid=False)
]
#R2
cat_path = [
    (1.4, 11.6),
    (0.5, 11),
    (3, 11.25),
    (3, 6),
    (4.25, 6),
    (4.25, 3.5),
    (5, 3.5),
    (5, 0.75),
    (0.5, 0.75)
]
cat = Cat(cat_path[0], radius=0.3, move_acceleration=8, friction=0.9, controllable=False)
cat.path_points = cat_path
cat.path_index = 1


for i in entity_list:
    map.add_entity(i)

map.add_entity(cat)
map.start_simulation(interval=1)
