def checkin(x, y):
    '''
    Проверяет, находятся ли *x* и *y* в пределах от 1 до 8
    '''
    if x in range(1,9) and y in range(1,9):
        return True
    else:
        return False


def get_king_pos(color, party):
    '''
    Возвращает поле с королём цвета *color* в партии *party.fields*
    '''
    for field in party.fields.values():
        if 'king' in field.figuretype and color in field.figuretype:
            return field


def get_attacked_fields(color, party):
    '''
    Возвращает список атакованных полей фигурами цвета *color*
    '''
    attacked = []
    for coords, field in party.fields.items():
        if color in field.figuretype:
            x, y = coords
            attacked = attacked + get_trivial_moves(field, party, x, y)
    return attacked


def get_trivial_moves(field, party, x, y):
    '''
    Возвращает список доступных для хода *field* полей из *party.fields*,
    не учитывает рокировку и ограничения, связанные с тем, 
    что союзный король не должен быть атакованным после хода 
    '''
    def get_diag_moves(field, party, x, y):
        '''
        Возвращает список доступных диагональных ходов
        '''
        diag_moves = []
        for j in [-1, 1]:
            for k in [-1, 1]:
                for i in range(1,9):
                    if (checkin(x+i*j, y+i*k) and 
                            party.fields[(x+i*j, y+i*k)].figuretype[0] != case[0]):
                        diag_moves.append(party.fields[(x+i*j, y+i*k)])
                        if party.fields[(x+i*j, y+i*k)].figuretype != 'empty':
                            break
                    else: 
                        break
        return diag_moves

    def get_dir_moves(field, party, x, y):
        '''
        Возвращает список доступных продольных ходов
        '''
        dir_moves = []
        for j, k in zip([-1, 1, 0, 0],[0, 0, -1, 1]):
            for i in range(1,9):
                if (checkin(x+i*j, y+i*k) and 
                        party.fields[(x+i*j, y+i*k)].figuretype[0] != case[0]):
                    dir_moves.append(party.fields[(x+i*j, y+i*k)])
                    if party.fields[(x+i*j, y+i*k)].figuretype != 'empty':
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
        if checkin(x, y+j) and party.fields[(x, y+j)].figuretype == 'empty':
            possible_moves.append(party.fields[(x, y+j)])
            if field.figmoved == False:
                if (checkin(x, y+2*j) and 
                        party.fields[(x, y+2*j)].figuretype == 'empty'):
                    possible_moves.append(party.fields[(x, y+2*j)])
                    party.fields[(x, y+2*j)].long_pawn_move = True # Добавление отметки для взятия на проходе (en passant):
        for i in [-1,1]:
            if (checkin(x+i, y+j) and 
                    party.fields[(x+i, y+j)].figuretype[0] != case[0] and 
                    party.fields[(x+i, y+j)].figuretype != 'empty'):
                possible_moves.append(party.fields[(x+i, y+j)])
        for i in [-1,1]:
            if (y == 4 and checkin(x+i, y) and ('black' in case) and 
                    party.fields[(x+i, y)].pawn_moved and party.fields[(x+i, y)] == party.last_pawn):
                possible_moves.append(party.fields[(x+i, y-1)])
                party.fields[(x+i, y-1)].enpassant = True
            if (y == 5 and checkin(x+i, y) and ('white' in case) and 
                    party.fields[(x+i, y)].pawn_moved and party.fields[(x+i, y)] == party.last_pawn):
                possible_moves.append(party.fields[(x+i, y+1)])
                party.fields[(x+i, y+1)].enpassant = True
                
    if 'knight' in case:
        for i in [-1, 1, -2, 2]:
            for j in [-1, 1, -2, 2]:
                if (checkin(x+i, y+j) and 
                        abs(j) != abs(i) and
                        party.fields[(x+i, y+j)].figuretype[0] != case[0]):
                    possible_moves.append(party.fields[(x+i, y+j)])

    if 'king' in case:
        for i in [-1, 1, 0]:
            for j in [-1, 1, 0]:
                if (checkin(x+i, y+j) and 
                        party.fields[(x+i, y+j)].figuretype[0] != case[0]):
                    possible_moves.append(party.fields[(x+i, y+j)])

        

    if 'bishop' in case:
        possible_moves = get_diag_moves(field, party, x, y)

    if 'rook' in case:
        possible_moves = get_dir_moves(field, party, x, y)

    if 'queen' in case:
        possible_moves = get_diag_moves(field, party, x, y) + get_dir_moves(field, party, x, y)
    return possible_moves


def get_moves(field, party, x, y):
    '''
    Возвращает список доступных для хода *field* полей из *party.fields*,
    учитывает все ограничения используя get_trivial_moves
    '''
    possible_moves = []
    if field.figuretype == 'empty':
        return possible_moves
    color = field.figuretype[:5]
    trivial_moves = get_trivial_moves(field, party, x, y)
    if 'king' in field.figuretype:
        if color == 'white':
            enemy_color = 'black'
        else:
            enemy_color = 'white'
        attacked = get_attacked_fields(enemy_color, party)
        if (checkin(x+3, y) and
                not (party.fields[(x+1,y)] in attacked or party.fields[(x+2,y)] in attacked) and 
                party.fields[(x+1,y)].figuretype == 'empty' and 
                party.fields[(x+2,y)].figuretype == 'empty' and
                not party.fields[(x+3,y)].figmoved and 
                not checkcheck(color, party) and 
                not field.figmoved):
            trivial_moves.append(party.fields[(x+2,y)])
            party.fields[(x+2,y)].castling = True
        if (checkin(x-4, y) and
                not (party.fields[(x-1,y)] in attacked or party.fields[(x-2,y)] in attacked) and 
                party.fields[(x-1,y)].figuretype == 'empty' and 
                party.fields[(x-2,y)].figuretype == 'empty' and
                party.fields[(x-3,y)].figuretype == 'empty' and
                not party.fields[(x-4,y)].figmoved and 
                not checkcheck(color, party) and 
                not field.figmoved):
            trivial_moves.append(party.fields[(x-2,y)])
            party.fields[(x-2,y)].castling = True

    for move in trivial_moves:
        figure_clone = move.figuretype
        move.figuretype = field.figuretype
        field.figuretype = 'empty'
        if not checkcheck(color, party):
            possible_moves.append(move)
        field.figuretype = move.figuretype
        move.figuretype = figure_clone
    
    return possible_moves   


def checkcheck(color, party):
    '''
    Возвращает True, если шах поставлен команде цвета *color*
    '''
    if color == 'white':
        enemy_color = 'black'
    else:
        enemy_color = 'white'
    attacked = get_attacked_fields(enemy_color, party)
    if get_king_pos(color, party) in attacked:
        return True
    else:
        return False


def checkstalemate(color, party):
    '''
    Возвращает True, если команда цвета *color* в не имеет разрешённых ходов
    '''
    moves = []
    for coords, field in party.fields.items():
        if color in field.figuretype:
            x, y = coords
            moves = moves + get_moves(field, party, x, y)
    if not moves:
        return True
    else:
        return False        


def checkmate(color, party):
    '''
    Возвращает True, если мат поставлен команде цвета *color*
    '''
    return checkcheck and checkstalemate

