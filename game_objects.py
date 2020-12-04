import yaml 


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
        self.figmoved = False
        self.lighten = False

    def move(self, party):
        '''
        Перемещает фигуру из поля в поле *newfield* и возвращает новое состояние *party*
        '''
        attack_figuretype = party.active_field.figuretype
        for field in party.fields.values():
            field.lighten = False
            if field == party.active_field:
                field.figuretype = 'empty'
            if field == self:
                field.figuretype = attack_figuretype
                field.figmoved = True
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

