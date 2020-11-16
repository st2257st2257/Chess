# coding: utf-8
import pygame
import yaml

FPS = 30

window_width = 800

window_height = 600

field_size = window_height / 8

desk_x_coord = (window_width - window_height) / 2

black = (0, 0, 0)
white = (255, 255, 255)
lighten = (0, 255, 255)

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


def draw_field(field):
    '''
    Отрисовывает поле *field* шахматной доски.
    '''
    screen = get_screen()
    size = (int(field_size), int(field_size))
    x = int(desk_x_coord + (field.x - 1) * field_size)
    y = int((9 - field.y) *  field_size)
    rectan = (x, y, *size)
    color_rgb = (field.x + field.y) % 2 * 255
    color = (color_rgb, color_rgb, color_rgb)
    if field.lighten:
        color = lighten
    pygame.draw.rect(screen, color, rectan)
    screen.blit(fig_images[field.figure], (x, y))
    
    
def field_mouse_check(field):
    '''
    Возвращает True если мышь в поле *field* и False если нет.
    '''
    x0 = desk_x_coord + (field.x - 1) * field_size
    y0 = (9 - field.y) *  field_size
    x, y = pygame.mouse.get_pos()
    return (x > x0) and (x < x0 + field_size) and (
        y > y0) and (y < y0 + field_size)


def write_text(text, coords, surface):
    '''
    Отображает текст *text* на поверхности *surface* с координатами *(x, y)*.
    '''
    myfont = pygame.font.SysFont('Arial', 40)
    textsurface = myfont.render(text, False, (255, 255, 255))
    x, y = textsurface.get_size()
    surf = pygame.Surface(textsurface.get_size(), pygame.SRCALPHA)
    surfscaled = pygame.Surface(
            (x // 2, y // 2), pygame.SRCALPHA)
    surf.blit(textsurface, (0, 0))
    pygame.transform.smoothscale(
            surf, (x // 2, y // 2), surfscaled)
    surface.blit(surfscaled, coords)
    
    
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
    for field in party.fields.values():
        draw_field(field)
    show_moves(moves)
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            for field in party.fields.values():
                if field_mouse_check(field) and (prior_flag in field.figure):
                    for moves in field.get_possible_moves():
                        moves.lighten = True
                    party.active_field = field
                    return (party, prior_flag, False)
                if field_mouse_check(field) and field.lighten:
                    party = field.move(party)
                    prior_flag = change_flag(prior_flag)
                    return (party, prior_flag, False)
                    
            
