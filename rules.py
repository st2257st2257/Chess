import copy

def checkin(x, y):
    '''
    Проверяет, находятся ли *x* и *y* в пределах от 1 до 8
    '''
    if x in range(1,9) and y in range(1,9):
        return True
    else:
        return False


def get_king_pos(color, fields):
    '''
    Возвращает поле с королём цвета *color* в партии *fields*
    '''
    for field in fields.values():
        if 'king' in field.figuretype and color in field.figuretype:
            return field


def get_attacked_fields(color, fields):
    '''
    Возвращает список атакованных полей фигурами цвета *color*
    '''
    attacked = []
    for coords, field in fields.items():
        if color in field.figuretype:
            x, y = coords
            attacked = attacked + get_trivial_moves(field, fields, x, y)
    return attacked


def get_trivial_moves(field, fields, x, y):
    '''
    Возвращает список доступных для хода *field* полей из *fields*,
    Не учитывает, ограничения, накладываемые на 
    '''
    def get_diag_moves(field, fields, x, y):
        '''
        Возвращает список доступных диагональных ходов
        '''
        diag_moves = []
        for j in [-1, 1]:
            for k in [-1, 1]:
                for i in range(1,9):
                    if (checkin(x+i*j, y+i*k) and 
                            fields[(x+i*j, y+i*k)].figuretype[0] != case[0]):
                        diag_moves.append(fields[(x+i*j, y+i*k)])
                        if fields[(x+i*j, y+i*k)].figuretype != 'empty':
                            break
                    else: 
                        break
        return diag_moves

    def get_dir_moves(field, fields, x, y):
        '''
        Возвращает список доступных продольных ходов
        '''
        dir_moves = []
        for j, k in zip([-1, 1, 0, 0],[0, 0, -1, 1]):
            for i in range(1,9):
                if (checkin(x+i*j, y+i*k) and 
                        fields[(x+i*j, y+i*k)].figuretype[0] != case[0]):
                    dir_moves.append(fields[(x+i*j, y+i*k)])
                    if fields[(x+i*j, y+i*k)].figuretype != 'empty':
                        break
                else: 
                    break
        return dir_moves

    possible_moves = []
    case = field.figuretype # Для короткого обращения к строке figuretype поля

    if 'pawn' in case:
        if 'black' in case:
            j = -1
        else:
            j = 1
        if checkin(x, y+j) and fields[(x, y+j)].figuretype == 'empty':
            possible_moves.append(fields[(x, y+j)])
            if field.figmoved == False:
                if (checkin(x, y+2*j) and 
                        fields[(x, y+2*j)].figuretype == 'empty'):
                    possible_moves.append(fields[(x, y+2*j)])
        for i in [-1,1]:
            if (checkin(x+i, y+j) and 
                    fields[(x+i, y+j)].figuretype[0] != case[0] and 
                    fields[(x+i, y+j)].figuretype != 'empty'):
                possible_moves.append(fields[(x+i, y+j)])

    if 'knight' in case:
        for i in [-1, 1, -2, 2]:
            for j in [-1, 1, -2, 2]:
                if (checkin(x+i, y+j) and 
                        abs(j) != abs(i) and
                        fields[(x+i, y+j)].figuretype[0] != case[0]):
                    possible_moves.append(fields[(x+i, y+j)])

    if 'king' in case:
        for i in [-1, 1, 0]:
            for j in [-1, 1, 0]:
                if (checkin(x+i, y+j) and 
                        fields[(x+i, y+j)].figuretype[0] != case[0]):
                    possible_moves.append(fields[(x+i, y+j)])

    if 'bishop' in case:
        possible_moves = get_diag_moves(field, fields, x, y)

    if 'rook' in case:
        possible_moves = get_dir_moves(field, fields, x, y)

    if 'queen' in case:
        possible_moves = get_diag_moves(field, fields, x, y) + get_dir_moves(field, fields, x, y)
    return possible_moves


def get_moves(field, fields, x, y):
    possible_moves = []
    if field.figuretype == 'empty':
        return possible_moves
    color = field.figuretype[:5]
    trivial_moves = get_trivial_moves(field, fields, x, y)
    for move in trivial_moves:
        figure_clone = move.figuretype
        move.figuretype = field.figuretype
        field.figuretype = 'empty'
        if not checkcheck(color, fields):
            possible_moves.append(move)
        field.figuretype = move.figuretype
        move.figuretype = figure_clone
    return possible_moves   


def checkcheck(color, fields):
    '''
    Возвращает True, если шах поставлен команде цвета *color*
    '''
    if color == 'white':
        enemy_color = 'black'
    else:
        enemy_color = 'white'
    attacked = get_attacked_fields(enemy_color, fields)
    if get_king_pos(color, fields) in attacked:
        return True
    else:
        return False


def checkstalemate(color, fields):
    '''
    Возвращает True, если команда цвета *color* в состоянии пата
    '''
    moves = []
    for coords, field in fields.items():
        if color in field.figuretype:
            x, y = coords
            moves = moves + get_moves(field, fields, x, y)
    if not moves:
        return True
    else:
        return False
            


def checkmate(color, fields):
    '''
    Возвращает True, если мат поставлен команде цвета *color*
    '''
    return checkcheck and checkstalemate

