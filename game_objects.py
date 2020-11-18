import yaml 


# Чтение .yaml файлов со словарями 
with open('init_party.yaml', 'r') as file: 
    init_party_dict = yaml.load(file, Loader=yaml.Loader)
with open('chess_figs.yaml', 'r') as file:
    chess_dict = yaml.load(file, Loader=yaml.Loader)
#print(chess_dict)
desk_list = [] 
for i in range(1,9):
    for j in range(1,9):
        desk_list.append([i,j])


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
        self.lighten = False
        if not self.figuretype == '':
            self.occupied = True # Занято ли поле фигурой
            self.figure = ChessFigure(figuretype)
        else:
            self.occupied = False
            self.figure = None
    

    def get_possible_steps(self, party): # TODO: Для правил нужен отдельный модуль, слишком много проверок
        '''
        Возвращает возможные поля для хода для фигуры
        '''
        possible_moves = []
        if not self.occupied:
            return possible_moves
        else:
            for move in chess_dict[self.figuretype][1]:
                move = [self.coords[0] + move[0], self.coords[1] + move[1]]
                if move in desk_list:
                    move = move[0]*10 + move[1]
                    possible_moves.append(party.fields[move])
            return possible_moves


    def move(self, party, newfield):
        '''
        Перемещает фигуру из поля в поле *newfield* и возвращает новое состояние *party*
        '''
        if self.occupied and newfield.occupied:
            if newfield in self.get_possible_steps(party):
                if self.figuretype[0] == newfield.figuretype[0]:
                    print("Field is occupied by ally figure")
                elif newfield.occupied:
                    newfield.figure.eaten = True
                    newfield.figure = self.figure
                    newfield.figure.moved = True
                    newfield.figuretype = self.figuretype
                    self.occupied = False
                    self.figuretype = ''
                    self.figure = None
        elif self.occupied:
            newfield.figure = self.figure
            newfield.figure.moved = True
            newfield.figuretype = self.figuretype
            newfield.occupied = True
            self.occupied = False
            self.figuretype = ''
            self.figure = None
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
        self.end_flag = False
        self.moves = []

