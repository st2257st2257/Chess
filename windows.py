from visual_module import *
import pygame

field_len = 400

FPS = 30

window_width = 1000

window_height = 600

clock = pygame.time.Clock()

BUTTON_COLOR = (255, 99, 0)


def register_window():
    '''
    '''
    field_x = (window_width - field_len) // 2
    field_y = window_height // 2 - 100
    username_field = InputBox(field_x, field_y, field_len)
    pass_field = InputBox(field_x, field_y + 100, field_len)
    email_field = InputBox(field_x, field_y + 200, field_len)
    screen = get_screen()
    finished = False
    header_font = pygame.font.SysFont('Arial', 80)
    button_font = pygame.font.SysFont('Arial', 50)
    reg_button = button(
            field_x, window_height * 4 // 5, 
            'Register', button_font, BUTTON_COLOR
    )
    back_button = button(
            window_width // 2, window_height * 4 // 5, 
            'Back', button_font, BUTTON_COLOR
    )
    text_font = pygame.font.SysFont('Arial', 40)
    finish_program = False
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                finish_program = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if reg_button.check():
                    finished = True
                if back_button.check():
                    finished = True
            username_field.event_handler(event)
            pass_field.event_handler(event)
            email_field.event_handler(event)
        password = pass_field.text
        pass_field.text = '*' * len(pass_field.text)
        username_field.draw()
        pass_field.draw()
        reg_button.draw()
        back_button.draw()
        email_field.draw()
        pass_field.text = password
        write_text('Password', (field_x, 
            pass_field.y - 30), screen, text_font)
        write_text('Username', (
            field_x, username_field.y - 30), screen, text_font)
        write_text('Phystech.Chess', (
            field_x, window_height // 10), screen, header_font)
        write_text('Registration', (
            field_x, window_height // 10 + 50), screen, text_font)
        write_text('Email', (
            field_x, email_field.y - 30), screen, text_font)
        clock.tick(FPS)
        pygame.display.update()
        fill()
    return finish_program


def start_window():
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
    reg_button = button(
            window_width // 2, window_height * 4 // 5, 
            'Register', button_font, BUTTON_COLOR
    )
    text_font = pygame.font.SysFont('Arial', 40)
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.check():
                    finished = True
                if reg_button.check():
                    exit_flag = register_window()
                    if exit_flag:
                        finished = True
            username_field.event_handler(event)
            pass_field.event_handler(event)
        password = pass_field.text
        pass_field.text = '*' * len(pass_field.text)
        username_field.draw()
        pass_field.draw()
        start_button.draw()
        reg_button.draw()
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
