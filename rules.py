
def check(x, y):
    '''
    Проверяет, находятся ли *x* и *y* в пределах от 1 до 8
    '''
    if x in range(1,9) and y in range(1,9):
        return True
    else:
        return False

def get_moves(field, party, x, y):
    '''
    Возвращает список доступных для хода *field* полей из *party.fields*,
    Не учитывает, ограничения, накладываемые на 
    '''
    def get_diag_moves(field, party, x, y):
        diag_moves = []
        for i in range(1,9):
            if (check(x+i, y+i) and 
                    party.fields[(x+i, y+i)].figuretype[0] != case[0]):
                diag_moves.append(party.fields[(x+i, y+i)])
                if party.fields[(x+i, y+i)].figuretype != 'empty':
                    break
            else: 
                break
        for i in range(1,9):
            if (check(x-i, y-i) and 
                    party.fields[(x-i, y-i)].figuretype[0] != case[0]):
                diag_moves.append(party.fields[(x-i, y-i)])
                if party.fields[(x-i, y-i)].figuretype != 'empty':
                    break
            else: 
                break
        for i in range(1,9):
            if (check(x-i, y+i) and 
                    party.fields[(x-i, y+i)].figuretype[0] != case[0]):
                diag_moves.append(party.fields[(x-i, y+i)])
                if party.fields[(x-i, y+i)].figuretype != 'empty':
                    break
            else: 
                break
        for i in range(1,9):
            if (check(x+i, y-i) and 
                    party.fields[(x+i, y-i)].figuretype[0] != case[0]):
                diag_moves.append(party.fields[(x+i, y-i)])
                if party.fields[(x+i, y-i)].figuretype != 'empty':
                    break
            else: 
                break 
        return diag_moves
    def get_dir_moves(field, party, x, y):
        pass

    possible_moves = []
    case = field.figuretype # Для короткого обращения к строке figuretype поля

    if 'pawn' in case:
        if 'black' in case:
            j = -1
        else:
            j = 1
        if check(x, y+j) and party.fields[(x, y+j)].figuretype == 'empty':
            possible_moves.append(party.fields[(x, y+j)])
            if field.figmoved == False:
                if (check(x, y+2*j) and 
                        party.fields[(x, y+2*j)].figuretype == 'empty'):
                    possible_moves.append(party.fields[(x, y+2*j)])
        for i in [-1,1]:
            if (check(x+i, y+j) and 
                    party.fields[(x+i, y+j)].figuretype[0] != case[0] and 
                    party.fields[(x+i, y+j)].figuretype != 'empty'):
                possible_moves.append(party.fields[(x+i, y+j)])

    if 'knight' in case:
        for i in [-1, 1, -2, 2]:
            for j in [-1, 1, -2, 2]:
                if (check(x+i, y+j) and 
                        abs(j) != abs(i) and
                        party.fields[(x+i, y+j)].figuretype[0] != case[0]):
                    possible_moves.append(party.fields[(x+i, y+j)])

    if 'king' in case:
        for i in [-1, 1, 0]:
            for j in [-1, 1, 0]:
                if (check(x+i, y+j) and 
                        party.fields[(x+i, y+j)].figuretype[0] != case[0]):
                    possible_moves.append(party.fields[(x+i, y+j)])

    if 'bishop' in case:
        possible_moves = get_diag_moves(field, party, x, y)
    print(case, ':', possible_moves)
    return possible_moves
