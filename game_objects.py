import yaml 
from rules import *

# Чтение .yaml файлов со словарями 
with open('init_party.yaml', 'r') as file: 
    init_party_dict = yaml.load(file, Loader=yaml.Loader)

desk_list = [] 
for i in range(1,9):
    for j in range(1,9):
        desk_list.append([i,j])

char_dict = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}

class Move:
    """docstring for Move"""
    def __init__(self, figuretype, coords, newcoords, eatenfigure):
        self.figuretype = figuretype
        self.coords = coords
        self.newcoords = newcoords
        self.eatenfigure = None
        self.time = None


class Player:
    """docstring for Player"""
    def __init__(self, color, rate):
        self.web_login = ""
        self.web_password = ""
        self.color = color
        self.rate = rate


class Field:
    '''
    Класса поля, имеющий координаты *coords* и фигуру *figure*

    '''
    def __init__(self, figuretype):
        self.figuretype = figuretype
        self.figmoved = False # Флаг, что в поле фигура, делавшая ход
        self.lighten = False # Флаг, что поле подсвечено для хода какой-либо фигуры

    def move(self, party, field):
        '''
        Перемещает фигуру из поля *self* в поле *field*
        '''
        field.figuretype = self.figuretype
        field.figmoved = True
        self.figuretype = 'empty'

class Party:
    """Класс содержит в себе словарь со всеми полями *fields*,
    список со всеми предыдущими ходами *moves*"""
    def __init__(self):
        self.fields = init_party_dict.copy()
        for key in self.fields.keys():
            self.fields.update({key: Field(self.fields[key])})
        self.active_field = None # Поле, по которому нажали для хода
        self.end_flag = False
        self.web_id = 0
        self.moves = []
        self.wking_pos = get_king_pos('white', self.fields)
        self.bking_pos = get_king_pos('black', self.fields)
        self.wattacked = get_attacked_fields('white', self.fields)
        self.battacked = get_attacked_fields('black', self.fields)
