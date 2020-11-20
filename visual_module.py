# coding: utf-8
import pygame
import yaml 

field_len = 400

FPS = 30

window_width = 1000

window_height = 600

field_size = window_height / 8

desk_x_coord = (window_width - window_height) / 2 

black = (0, 0, 0)
white = (255, 255, 255)
lighten = (255, 218, 185)
COLOR_ACTIVE = (0, 0, 0)
COLOR_INACTIVE = (0, 0, 255)
BUTTON_COLOR = (255, 99, 71)

clock = pygame.time.Clock()

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
    fig_images.update({figure : set_image(fig_images[figure][0])})
fig_images.update({'' : pygame.Surface((0, 0))})


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
    Заливает главный экран белым цветом
    '''
    screen = get_screen()
    screen.fill(white)


def quit():
    '''
    Выходит из модуля pygame.
    '''
    pygame.quit()


def draw_field(field, field_x, field_y):
    '''
    Отрисовывает поле *field* шахматной доски.
    '''
    screen = get_screen()
    size = (int(field_size), int(field_size))
    x = int(desk_x_coord + (field_x - 1) * field_size)
    y = int((8 - field_y) *  field_size)
    rectan = (x, y, *size)
    color_rgb = (field_x + field_y) % 2 * 150 + 100
    color = (color_rgb, color_rgb, color_rgb)
    if field.lighten:
        color = lighten
    pygame.draw.rect(screen, color, rectan)
    screen.blit(fig_images[field.figuretype], (x, y))
    
    
def field_mouse_check(field, field_x, field_y):
    '''
    Возвращает True если мышь в поле *field* и False если нет.
    '''
    x0 = desk_x_coord + (field_x - 1) * field_size
    y0 = (8 - field_y) *  field_size
    x, y = pygame.mouse.get_pos()
    return (x > x0) and (x < x0 + field_size) and (
        y > y0) and (y < y0 + field_size)


def write_text(text, coords, surface, font):
    '''
    Отображает текст *text* на поверхности *surface* с координатами *(x, y)*.
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
    
    
def show_moves(moves):
    '''
    Отображает массив ходов *moves*.
    '''
    a = 0
    screen = get_screen()
    size = (int(desk_x_coord), window_height // 2)
    moves_surface = pygame.Surface(size, pygame.SRCALPHA)
    for move in moves[::-1]:
        write_text(move.text, (0, a * 25), moves_surface)
        a += 1
    coords = (int(screen_width - desk_x_coord), 0)
    screen.blit(moves_surface, coords)


def draw_party(party):
    '''
    Прорисовка всех составляющих игры *party*.
    '''
    fill()
    for field_num in party.fields.keys():
        field = party.fields[field_num]
        x, y = divmod(field_num, 10)
        draw_field(field, x, y)
    #show_moves(moves)
    pygame.display.update()
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
                x, y = divmod(field_num, 10)
                if field_mouse_check(field, x, y) and (
                    prior_flag in field.figuretype):
                    steps = field.get_possible_steps(party, x, y)
                    for field_ in party.fields.values():
                        field_.lighten = False
                        if field_ in steps:
                            field_.lighten = True
                    party.active_field = field
                    return (party, prior_flag, False)
                elif field_mouse_check(field, x, y) and field.lighten:
                    party = field.move(party)
                    prior_flag = change_flag(prior_flag)
                    return (party, prior_flag, False)
                    
class InputBox:
    '''
    Box for inputting text. 
    *x, y* - coordinates. *length* - length of the box.
    '''
    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.color = COLOR_INACTIVE
        self.screen = get_screen()
        self.text = ''
        self.active = False
        self.length = length
        self.rect = pygame.Rect(self.x, self.y, length, 15)
        self.font = pygame.font.SysFont('Arial', 45)

    def event_handler(self, event):
        '''
        event handler for box.
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            if self.active:
                self.color = COLOR_ACTIVE
            else:
                self.color = COLOR_INACTIVE
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
        x, y = write_text(
                self.text, (self.x, self.y), self.screen, self.font)
        self.rect = pygame.Rect(
                self.x - 5, self.y - 5, max(x + 10, self.length), y + 10)
        pygame.draw.rect(self.screen, self.color, self.rect, 5)


class button:
    '''
    button with text *text*, coords *x, y*, font *font* and color *color*.
    '''
    def __init__(self, x, y, text, font, color):
        self.color = color
        self.font = font
        self.x = x
        self.y = y
        self.text = text
        self.rect = pygame.Rect(0, 0, 0, 0)

    def check(self):
        '''
        checks if mouse is in button
        '''
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self):
        '''
        draws button
        '''
        x, y = write_text(self.text, (self.x, self.y), get_screen(), self.font)
        self.rect = pygame.Rect(self.x - 10, self.y - 10, x + 20, y + 20)
        pygame.draw.rect(get_screen(), self.color, self.rect, 5)
        if self.check():
            pygame.draw.rect(get_screen(), self.color, self.rect)
        write_text(self.text, (self.x, self.y), get_screen(), self.font)


def main_window():
    '''
    Creates main window for entering password and username. 
    NOT FINISHED. NEED TO ADD FURTHER TASK.
    '''
    field_x = (window_width - field_len) // 2
    field_y = window_height // 2 - 50
    username_field = InputBox(field_x, field_y, field_len)
    pass_field = InputBox(field_x, field_y + 100, field_len)
    screen = get_screen()
    finished = False
    header_font = pygame.font.SysFont('Arial', 80)
    button_font = pygame.font.SysFont('Arial', 50)
    start_button = button(
            field_x, window_height * 4 // 5, 'Play', button_font, BUTTON_COLOR)
    text_font = pygame.font.SysFont('Arial', 40)
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.check():
                    finished = True
            username_field.event_handler(event)
            pass_field.event_handler(event)
        password = pass_field.text
        pass_field.text = '*' * len(pass_field.text)
        username_field.draw()
        pass_field.draw()
        start_button.draw()
        pass_field.text = password
        write_text('Password', (field_x, 
            pass_field.y - 30), screen, text_font)
        write_text('Username', (
            field_x, username_field.y - 30), screen, text_font)
        write_text('Phystech.Chess', (
            field_x, window_height // 5), screen, header_font)
        clock.tick(FPS)
        pygame.display.update()
        fill()
