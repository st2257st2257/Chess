# coding: utf-8
import pygame

window_width = 800

window_height = 600

field_size = window_height / 8

desk_x_coord = (window_width - window_height) / 2

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
    screen.fill((255, 255, 255))


def quit():
    '''
    Выходит из модуля pygame.
    '''
    pygame.quit()


def set_figure_image(file):
    '''
    Создает поверхность с изображением из файла *file*. Размер поверхности
    равен размеру поля.
    '''
    size = (int(field_size), int(field_size))
    image = pygame.image.load(file)
    image = image.convert_alpha()
    surfscaled = pygame.Surface(size, pygame.SRCALPHA)
    pygame.transform.smoothscale(image, size, surfscaled)
    return surfscaled
    
    
def draw_figure(figure):
    '''
    Отрисовывает шахматную фигуру *figure*.
    '''
    x = int(desk_x_coord + (figure.x - 1) * field_size)
    y = int((9 - figure.y) *  field_size)
    screen = get_screen()
    screen.blit(figure.image, (x, y))
    

def draw_field(field):
    '''
    Отрисовывает поле *field* шахматной доски.
    '''
    screen = get_screen()
    size = (int(field_size), int(field_size))
    x = int(desk_x_coord + (field.x - 1) * field_size)
    y = int((9 - field.y) *  field_size)
    rectan = (x, y, *size)
    pygame.draw.rect(screen, field.color, rectan)
    
    
def field_mouse_check(field):
    '''
    Возвращает True если мышь в поле *field* и False если нет.
    '''
    x0 = desk_x_coord + (field.x - 1) * field_size
    y0 = (9 - field.y) *  field_size
    x, y = pygame.mouse.get_pos()
    return (x > x0) and (x < x0 + field_size) and (
        y > y0) and (y < y0 + field_size)
