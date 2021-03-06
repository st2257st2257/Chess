# coding: utf-8 import pygame
import pygame
import yaml
from rules import *

FPS = 30

with open('config.yaml', 'r') as file:
    config = yaml.load(file, Loader=yaml.Loader)

fig_style = 'fig_styles/' + config['figs'] + '/'

desk_style = 'desk_styles/' + config['desk'] + '/'

theme = 'themes/' + config['theme'] + '/'

window_width = config['resolution'][0]

window_height = config['resolution'][1]

field_size = window_height / 8

desk_x_coord = (window_width - window_height) / 2

scale_x = window_width / 1600

scale_y = window_height / 900

black = (0, 0, 0)
white = (255, 255, 255)
lighten = (255, 218, 185)

letters_dict = {
        '1': 'a', '2': 'b', '3': 'c', '4': 'd', '5': 'e',
        '6': 'f', '7': 'g', '8': 'h'}

figs_dict = {
        'white_king': '\u2654', 'white_queen': '\u2655',
        'white_rook': '\u2656', 'white_bishop': '\u2657',
        'white_knight': '\u2658', 'white_pawn': '\u2659',
        'black_king': '\u265A', 'black_queen': '\u265B',
        'black_rook': '\u265C', 'black_bishop': '\u265D',
        'black_knight': '\u265E', 'black_pawn': '\u265F'
}

clock = pygame.time.Clock()

back_image = pygame.image.load(theme + 'back.png')
back_image = back_image.convert_alpha(
        pygame.display.set_mode((window_width, window_height)))
background = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
pygame.transform.smoothscale(
        back_image, (window_width, window_height), background)

button_img = pygame.image.load(theme + 'Button.png')
button_img = button_img.convert_alpha(
        pygame.display.set_mode((window_width, window_height)))

button_pushed_img = pygame.image.load(theme + 'Button_pushed.png')
button_pushed_img = button_pushed_img.convert_alpha(
        pygame.display.set_mode((window_width, window_height)))

field_img = pygame.image.load(theme + 'field.png')
field_img = field_img.convert_alpha(
        pygame.display.set_mode((window_width, window_height)))

field_active_img = pygame.image.load(theme + 'field_active.png')
field_img = field_active_img.convert_alpha(
        pygame.display.set_mode((window_width, window_height)))

rect_img = pygame.image.load(theme + 'rect.png')
rect_img = rect_img.convert_alpha(
        pygame.display.set_mode((window_width, window_height)))

rect_active_img = pygame.image.load(theme + 'rect.png')
rect_active_img = rect_active_img.convert_alpha(
        pygame.display.set_mode((window_width, window_height)))

login_image = pygame.image.load('themes/background.png')
login_image = login_image.convert_alpha(
        pygame.display.set_mode((window_width, window_height)))
login_pic = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
pygame.transform.smoothscale(
        login_image, (window_width, window_height), login_pic)

sq_size = (int(field_size), int(field_size))

light_field_img = pygame.image.load(desk_style + 'light_field.png')
light_field_img = light_field_img.convert_alpha(
        pygame.display.set_mode((window_width, window_height)))
light_field_image = pygame.Surface(sq_size, pygame.SRCALPHA)
pygame.transform.smoothscale(
        light_field_img, sq_size, light_field_image)

white_field_img = pygame.image.load(desk_style + 'white_field.png')
white_field_img = white_field_img.convert_alpha(
        pygame.display.set_mode((window_width, window_height)))
white_field_image = pygame.Surface(sq_size, pygame.SRCALPHA)
pygame.transform.smoothscale(
        white_field_img, sq_size, white_field_image)

black_field_img = pygame.image.load(desk_style + 'black_field.png')
black_field_img = black_field_img.convert_alpha(
        pygame.display.set_mode((window_width, window_height)))
black_field_image = pygame.Surface(sq_size, pygame.SRCALPHA)
pygame.transform.smoothscale(
        black_field_img, sq_size, black_field_image)


with open('chess_figs.yaml', 'r') as file:
    fig_images = yaml.load(file, Loader=yaml.Loader)


def set_image(file):
    '''
    Создает поверхность с изображением из файла *file*. Размер поверхности
    равен размеру поля.
    '''
    size = (int(field_size), int(field_size))
    image = pygame.image.load(file)
    image = image.convert_alpha(
        pygame.display.set_mode((window_width, window_height)))
    surfscaled = pygame.Surface(size, pygame.SRCALPHA)
    pygame.transform.smoothscale(image, size, surfscaled)
    return surfscaled


for figure in fig_images.keys():
    fig_images.update({figure: set_image(fig_style + fig_images[figure])})
fig_images.update({'empty': pygame.Surface((0, 0))})


def init():
    '''
    Функция инициализирует модуль pygame и создает окно.
    '''
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))


def get_screen():
    '''
    Возвращает экран отрисовки.
    '''
    return pygame.display.get_surface()


def fill():
    '''
    Fills the screen with theme picture.
    '''
    screen = get_screen()
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))


def login_fill():
    '''
    Fills the login screen with given picture.
    '''
    get_screen().fill((255, 255, 255))
    get_screen().blit(login_pic, (0, 0))


def quit():
    '''
    Выходит из модуля pygame.
    '''
    pygame.quit()


def draw_field(field, field_x, field_y):
    '''
    Draws *field* with *field_x* x coordinate and *field_y*
    y coordinate.
    '''
    screen = get_screen()
    size = (int(field_size), int(field_size))
    x = int(desk_x_coord + (field_x - 1) * field_size)
    y = int((8 - field_y) * field_size)
    rectan = (x, y, *size)
    color_rgb = (field_x + field_y) % 2 * 150 + 100
    if (field_x + field_y) % 2 == 1:
        get_screen().blit(black_field_image, (x, y))
    else:
        get_screen().blit(white_field_image, (x, y))
    if field.lighten:
        get_screen().blit(light_field_image, (x, y))
    screen.blit(fig_images[field.figuretype], (x, y))


def field_mouse_check(field_x, field_y):
    '''
    Checks if mouse in field with coords *field_x*, *field_y*.
    '''
    x0 = desk_x_coord + (field_x - 1) * field_size
    y0 = (8 - field_y) * field_size
    x, y = pygame.mouse.get_pos()
    return (x > x0) and (x < x0 + field_size) and (
        y > y0) and (y < y0 + field_size)


def write_text(text, coords, surface, font):
    '''
    Draws *text* with *coords* on a *surface* with the *font*.
    '''
    textsurface = font.render(text, False, (0, 0, 0))
    x, y = textsurface.get_size()
    surf = pygame.Surface(textsurface.get_size(), pygame.SRCALPHA)
    surfscaled = pygame.Surface(
            (x // 2, y // 2), pygame.SRCALPHA)
    surf.blit(textsurface, (0, 0))
    pygame.transform.smoothscale(
            surf, (x // 2, y // 2), surfscaled)
    surface.blit(surfscaled, coords)
    return (x // 2, y // 2)


def move_to_string(move):
    '''
    Converts *move* in a database format into readable format.
    '''
    fig = move[4:]
    if 'O-O' in move:
        if move[1] == '1':
            if move[2] == '7':
                output = 'O-O' + figs_dict['white_king']
            else:
                output = 'O-O-O' + figs_dict['white_king']
        else:
            if move[2] == '7':
                output = 'O-O' + figs_dict['black_king']
            else:
                output = 'O-O-O' + figs_dict['black_king']
        return output
    if 'enpassant' in move:
        output = letters_dict[move[0]] + move[1] + '\u00D7' + letters_dict[
                move[2]] + move[3]
        if int(move[3]) > int(move[1]):
            output += figs_dict['black_pawn']
        else:
            output += figs_dict['white_pawn']
        return output
    if fig == 'empty':
        output = letters_dict[move[0]] + move[1] + '-' + letters_dict[
                move[2]] + move[3]
    else:
        output = letters_dict[move[0]] + move[1] + '\u00D7' + letters_dict[
                move[2]] + move[3] + figs_dict[fig]
    return output


def draw_party(party):
    '''
    Прорисовка всех составляющих игры *party*.
    '''
    fill()
    for field_num in party.fields.keys():
        field = party.fields[field_num]
        x, y = field_num
        draw_field(field, x, y)
    pygame.display.update()
    clock.tick(FPS)


def draw_party_1(party, color, moves_vis, players_data=None):
    '''
    Multiplayer version of *draw_party* function. Takes *party* to
    draw, *color* of user seeing board, *moves_vis* - Scroll_window
    object that represents moves, and *players_data* dictionary to
    illustrate if necessary.
    '''
    fill()
    font = pygame.font.SysFont('Arial', int(50 * scale_x))
    font_pl = pygame.font.SysFont('Arial', int(80 * scale_x))
    for field_num in party.fields.keys():
        field = party.fields[field_num]
        x, y = field_num
        if color == 'black':
            y = 9 - y
        draw_field(field, x, y)
    moves = moves_vis.data.copy()
    for move in range(len(moves)):
        if 'win' not in moves[move]:
            moves_vis.data[move] = move_to_string(moves[move])
    moves_vis.draw()
    moves_vis.data = moves
    for i in range(8):
        if color == 'white':
            write_text(str(8 - i), (
                desk_x_coord, field_size * i), get_screen(), font)
        else:
            write_text(str(i + 1), (
                desk_x_coord, field_size * i), get_screen(), font)
        write_text(letters_dict[str(i + 1)], (desk_x_coord + int(
            field_size * (i + 0.8)), field_size * 7), get_screen(), font)
    if players_data is not None:
        write_text(players_data['player'] + '|' + players_data[
            'player_rating'], (
                desk_x_coord + field_size * 8 + 10,
                675 * scale_y
            ), get_screen(), font_pl)
        write_text(players_data['opponent'] + '|' + players_data[
                'opponent_rating'], (
                    desk_x_coord + field_size * 8 + 10,
                    225 * scale_y
                ), get_screen(), font_pl)
    clock.tick(FPS)


def change_flag(prior_flag):
    '''
    Смена флага очередности.
    '''
    if prior_flag == 'white':
        return 'black'
    else:
        return 'white'


def event_handler(party, prior_flag):
    '''
    Обработчик событий. *party* --- игра. prior_flag --- флаг очередности.
    Возвращает (игру после изменений, флаг очередности, флаг цикличности)
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return (party, prior_flag, True)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for field_num in party.fields.keys():
                field = party.fields[field_num]
                x, y = field_num
                if field_mouse_check(x, y) and (
                        prior_flag in field.figuretype):
                    steps = get_moves(field, party, x, y)
                    for field_ in party.fields.values():
                        field_.lighten = False
                        if field_ in steps:
                            field_.lighten = True
                    party.active_field = field
                    return (party, prior_flag, False)
                elif field_mouse_check(x, y) and field.lighten:
                    move_type = party.active_field.move(party, field, x, y)
                    print(move_type)
                    party.active_field = None
                    for field in party.fields.values():
                        field.lighten = False
                        field.long_pawn_move = False
                        field.enpassant = False
                        field.castling = False
                    prior_flag = change_flag(prior_flag)
                    return (party, prior_flag, False)


def change_color(color):
    '''
    returns opposite color of *color*
    '''
    if color == 'black':
        return 'white'
    else:
        return 'black'


def event_handler_1(party, color, moves_window, surr_button, players_data):
    '''
    Multiplayer version of event_handler fuction. Takes *party* to handle,
    *moves_window* - Scroll_window object with moves. *surr_button* - button
    to surrender and *players_data* dictionary with usernames and ratings.
    '''
    finished = False
    finished_program = False
    if checkstalemate(color, party) and not checkmate(color, party):
        move = 'draw_win'
        return party, False, move
    if checkmate(color, party):
        move = change_color(color) + '_win'
        return party, False, move
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                finished_program = True
                move = change_color(color) + '_win'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for field_num in party.fields.keys():
                    field = party.fields[field_num]
                    x, y = field_num
                    if color == 'black':
                        y = 9 - y
                    if field_mouse_check(x, y) and (
                            color in field.figuretype):
                        if color == 'black':
                            y = 9 - y
                        steps = get_moves(field, party, x, y)
                        for field_ in party.fields.values():
                            field_.lighten = False
                            if field_ in steps:
                                field_.lighten = True
                        party.active_field = field
                    elif field_mouse_check(x, y) and field.lighten:
                        if color == 'black':
                            y = 9 - y
                        for i in party.fields.keys():
                            if party.active_field == party.fields[i]:
                                coords_1 = str(i[0]) + str(i[1])
                        coords_2 = str(field_num[0]) + str(field_num[1])
                        move = coords_1 + coords_2 + field.figuretype
                        rules_exept = party.active_field.move(
                            party, field, x, y)
                        if rules_exept == 'castling':
                            move += 'O-O'
                        if rules_exept == 'enpassant':
                            move += 'enpassant'
                        party.active_field = None
                        for field in party.fields.values():
                            field.lighten = False
                            field.long_pawn_move = False
                            field.enpassant = False
                            field.castling = False
                        finished = True
                if surr_button.check():
                    finished = True
                    move = change_color(color) + '_win'
            moves_window.event_handler(event)
        draw_party_1(party, color, moves_window, players_data)
        surr_button.draw()
        pygame.display.update()
    return party, finished_program, move


class InputBox:
    '''
    Box for inputting text.
    *x, y* - coordinates. *length* - length of the box.
    '''
    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.screen = get_screen()
        self.text = ''
        self.active = False
        self.length = length
        self.rect = pygame.Rect(self.x, self.y, length, 15)
        self.font = pygame.font.SysFont('Arial', int(45 * scale_x))

    def event_handler(self, event):
        '''
        Event handler for box taking *event* to handle.
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self):
        '''
        Function draws the box.
        '''
        dx = int(5 * scale_x)
        dy = int(5 * scale_y)
        x, y = write_text(
                self.text, (self.x, self.y), self.screen, self.font)
        width = max(x + 2 * dx, self.length)
        self.rect = pygame.Rect(
                self.x - dx, self.y - dx, width, y + 2 * dy)
        field_image = pygame.Surface((width, y + 2 * dy), pygame.SRCALPHA)
        if self.active:
            pygame.transform.smoothscale(
                    field_active_img, (width, y + 2 * dy), field_image)
        else:
            pygame.transform.smoothscale(
                    field_img, (width, y + 2 * dy), field_image)
        self.screen.blit(field_image, (self.x - dx, self.y - dy))
        write_text(self.text, (self.x, self.y), self.screen, self.font)


class button:
    '''
    Button with text *text*, coords *x, y*, font *font* and color *color*.
    '''
    def __init__(self, x, y, text, font):
        self.font = font
        self.x = x
        self.y = y
        self.text = text
        self.rect = pygame.Rect(0, 0, 0, 0)

    def check(self):
        '''
        Checks if mouse is in button
        '''
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self):
        '''
        Draws button
        '''
        dx = int(10 * scale_x)
        dy = int(10 * scale_y)
        x, y = write_text(self.text, (self.x, self.y), get_screen(), self.font)
        self.rect = pygame.Rect(
                self.x - dx, self.y - dy, x + 2 * dx, y + 2 * dy)
        x += 2 * dx
        y += 2 * dy
        button_image = pygame.Surface((x, y), pygame.SRCALPHA)
        if self.check():
            pygame.transform.smoothscale(
                    button_pushed_img, (x, y), button_image)
        else:
            pygame.transform.smoothscale(button_img, (x, y), button_image)
        get_screen().blit(button_image, (self.x - dx, self.y - dx))
        write_text(self.text, (self.x, self.y), get_screen(), self.font)


class Scroll_window:
    '''
    Scrolling window with *x*, *y* coords, *data* list of data represented,
    *width*, *height* size, and *clickable* bool to decide wether it is
    clickable.
    '''
    def __init__(self, x, y, data, font, width, height, clickable):
        self.x = x
        self.y = y
        self.data = data
        self.font = font
        self.screen = get_screen()
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.text_y = 0
        self.clickable = clickable
        self.elems = []
        self.field_h = 0
        self.height = height

    def event_handler(self, event):
        '''
        event handler for box taking *event* to handle
        '''
        if event.type == pygame.MOUSEWHEEL and self.rect.collidepoint(
                pygame.mouse.get_pos()):
            self.text_y += event.y * 5 * scale_y
            if self.text_y > 0:
                self.text_y = 0
            if self.text_y + self.field_h < self.height:
                self.text_y -= event.y * 5 * scale_y
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
                pygame.mouse.get_pos()) and self.clickable:
            for elem in range(len(self.elems)):
                if self.elems[elem].collidepoint(pygame.mouse.get_pos()):
                    return elem

    def draw(self):
        '''
        Draws window
        '''
        height = 0
        self.surface.fill((255, 255, 255, 0))
        self.elems = []
        for element in self.data:
            dy = int(5 * scale_y)
            x, y = write_text(element, (
                0, self.text_y + height + dy), self.surface, self.font)
            y += 2 * dy
            elem_surf = pygame.Surface((self.width, y), pygame.SRCALPHA)
            rect = pygame.Rect(
                    self.x, self.y + height + self.text_y, self.width, y)
            if rect.collidepoint(pygame.mouse.get_pos()) and self.clickable:
                pygame.transform.smoothscale(
                        field_img, (self.width, y), elem_surf)
            else:
                pygame.transform.smoothscale(
                        rect_img, (self.width, y), elem_surf)
            self.surface.blit(elem_surf, (0, self.text_y + height))
            self.elems.append(rect)
            write_text(element, (
                0, self.text_y + height + dy), self.surface, self.font)
            height += y
        self.field_h = height
        self.screen.blit(self.surface, (self.x, self.y))
