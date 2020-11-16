from SQL import *
"""coords = []
for i in range(1,9):
    for j in range(ord('a'),ord('i')):
        coords.append(chr(j)+str(i))
print(coords)"""


class Chess_Figure:
    """Класс-родитель для шахматных фигур,
    имеет формат *coords* a1, d8 итд"""
    def __init__(self, coords,type):
        self.id = id(self)
        self.type = type
        self.coords = coords
        self.potmoves = None
        self.image = None
        self.eaten = False


    def move(self, newcoords, allies, enemies):
        """Перемещает фигуру на *newcoords*,
        если там фигура из *enemies* съедает её,
        eсли фигура из *allies* выдаёт ошибку
        """
        canmove = True
        for ally in allies: 
            if not (ally == self) and (ally.coords == newcoords):
                print("Поле " + str(newcoords) + " занято союзником")
                canmove = False
        if canmove:        
            for enemy in enemies:
                if enemy.coords == newcoords:
                    enemy.eaten = True 
                    enemy.coords = None
            self.coords = newcoords


"""pawn = Chess_Figure('e2')
rook = Chess_Figure('e3')
enemies = [rook]
pawn.move('e3', enemies, [])
print(rook.coords)
print(pawn.coords)
print(rook.eaten)"""


class Move:
    """docstring for Move"""
    def __init__(self, figure, coords, newcoords, eaten):
        self.figure = figure
        self.coords = coords
        self.newcoords = newcoords
        self.eaten = None
        self.time = None

class Player:
    """docstring for Player"""
    def __init__(self, color, rate):
        self.color = color
        self.rate = rate


class field():
    '''
    Конструктор класса поля, имеющего координаты *coords* и фигуру *figure*.
    '''
    def __init__(self, coords, figure):
        self.x, self.y = coords
        self.figure = figure
        


class Party:
    pass

