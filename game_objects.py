from SQL import *
import yaml 


# Чтение .yaml файлов со словарями 
with open('init_party.yaml', 'r') as file: 
    init_party_dict = yaml.load(file, Loader=yaml.Loader)
with open('chess_figs.yaml', 'r') as file:
    chess_dict = yaml.load(file, Loader=yaml.Loader)


class Move:
    """docstring for Move"""
    def __init__(self, figure, coords, newcoords, eatenfigure):
        self.figure = figure
        self.coords = coords
        self.newcoords = newcoords
        self.eatenfigure = None
        self.time = None


class Player:
    """docstring for Player"""
    def __init__(self, color, rate):
        self.color = color
        self.rate = rate


class ChessFigure:
    """
    Фигура для помещения в поле, 
    имеет соответствующее новоеазвание *figure*,
    а также атрибуты состояния *eaten* и *moved*
    """
    def __init__(self, figuretype):
        self.figuretype = figuretype
        self.eaten = False # Съедена ли фигура в данной
        self.moved = False # Сделала ли фигура хотя бы один ход


        
class Field:
    '''
    Класса поля, имеющий координаты *coords* и фигуру *figure*
    '''
    def __init__(self, coords, figuretype):
        self.coords = list(divmod(coords,10))
        self.x, self.y = divmod(coords,10)
        self.figuretype = figuretype
        if not self.figuretype == '':
            self.occupied = True # Занято ли поле фигурой
            self.figure = ChessFigure(figuretype)
        else:
            self.occupied = False
            self.figure = None
    

    def get_possible_steps(self, party):
        '''
        Возвращает возможные ходы для фигуры в данной партии из данного поля
        '''
        possible_moves = []
        if not self.occupied:
            return possible_moves
        else:
            pass


    def move(self, party):
        '''
        Перемещает фигуру из поля и возвращает новое состояние *party*
        '''
        return party


class Party:
    """Класс содержит в себе словарь со всеми полями *fields*,
    список со всеми предыдущими ходами *moves*"""
    def __init__(self):
        self.fields = init_party_dict
        for key in self.fields.keys():
            if not self.fields[key] == None: 
                self.fields.update({key: Field(key, self.fields[key])})
        self.active_field = None
        self.moves = []
