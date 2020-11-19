import yaml 


# Чтение .yaml файлов со словарями 
with open('init_party.yaml', 'r') as file: 
    init_party_dict = yaml.load(file, Loader=yaml.Loader)
with open('chess_figs.yaml', 'r') as file:
    chess_dict = yaml.load(file, Loader=yaml.Loader)
print(chess_dict)
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
        self.lighten = False

    def get_possible_steps(self, party, x, y): # TODO: Для правил нужен отдельный модуль, слишком много проверок
        '''
        Возвращает возможные поля для хода для фигуры
        '''
        possible_moves = []
        for move in chess_dict[self.figuretype][1]:
            move = [x + move[0], y + move[1]]
            if move in desk_list:
                move = move[0]*10 + move[1]
                possible_moves.append(party.fields[move])
        return possible_moves


    def move(self, party):
        '''
        Перемещает фигуру из поля в поле *newfield* и возвращает новое состояние *party*
        '''
        attack_figuretype = party.active_field.figuretype
        for field in party.fields.values():
            field.lighten = False
            if field == party.active_field:
                field.figuretype = ''
            if field == self:
                field.figuretype = attack_figuretype
        party.active_field = None
        return party


class Party:
    """Класс содержит в себе словарь со всеми полями *fields*,
    список со всеми предыдущими ходами *moves*"""
    def __init__(self):
        self.fields = init_party_dict
        for key in self.fields.keys():
            self.fields.update({key: Field(self.fields[key])})
        self.active_field = None
        self.end_flag = False
        self.web_id = 0
        self.moves = []

