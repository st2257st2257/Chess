from visual_module import *
import pyganim
import pygame

field_len = 400

FPS = 30

window_width = 1600

window_height = 900

clock = pygame.time.Clock()

BUTTON_COLOR = (255, 99, 0)

load_anim = []

anim_delay = 50

for i in range(9):
    load_anim.append(('load_anim/load_' + str(i) + '.png', anim_delay))
load_anim = pyganim.PygAnimation(load_anim)

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
            'Add user', button_font, BUTTON_COLOR
    )
    back_button = button(
            window_width // 2, window_height * 4 // 5, 
            'Back', button_font, BUTTON_COLOR
    )
    text_font = pygame.font.SysFont('Arial', 40)
    finish_program = False
    error_text = ''
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                finish_program = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if reg_button.check():
                    error_text = ''
                    try:
                        add_player(
                                username_field.text, 
                                pass_field.text, email_field.text
                        )
                    except Exception:
                        error_text = 'Unable to create user'
                    else:
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
        write_text(error_text, (
            field_x, email_field.y + 50), screen, text_font)
        clock.tick(FPS)
        pygame.display.update()
        fill()
    return finish_program


def start_window():
    '''
    Creates main window for entering password and username. 
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
    start = False
    error_text = ''
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.check():
                    id = check_player(username_field.text, pass_field.text)
                    if id != 0:
                        start = True
                        finished = True
                    else:
                        error_text = 'Wrong password or username'
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
        write_text(error_text, (
            field_x, pass_field.y + 50), screen, text_font)
        clock.tick(FPS)
        pygame.display.update()
        fill()
    return start, username_field.text


def main_menu(username):
    x = window_width // 5
    y = window_height // 5
    text_font = pygame.font.SysFont('Arial', 40)
    button_font = pygame.font.SysFont('Arial', 50)
    header_font = pygame.font.SysFont('Arial', 80)
    screen = get_screen()
    create_game = button(x, y * 2, 'Create game', button_font, BUTTON_COLOR)
    join_game = button(x, y * 3, 'Join game', button_font, BUTTON_COLOR)
    id_field = InputBox(x + 150, y * 3, field_len)
    finished = False
    error_text = 'test'
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if join_game.check():
                    if check_id(id_field.text):
                        id = id_field.text
                        party = get_party(id)
                        party.user2 = username
                        push_party(party, id)
                        game(id, username)
                    else:
                        error_text = 'Unable to find game'
                if create_game.check():
                    id = create_new_party(username)
                    waiting_room(id)
                    game(id, username)
            id_field.event_handler(event)
        create_game.draw()
        join_game.draw()
        id_field.draw()
        write_text(error_text, (x + 150, y * 3 + 35), screen, text_font)
        write_text('Enter id', (x + 150, y * 3 - 30), screen, text_font)
        write_text(username, (x * 2, y * 2), screen, header_font)
        clock.tick(FPS)
        pygame.display.update()
        fill()


def waiting_room(id):
    finished = False
    header_font = pygame.font.SysFont('Arial', 80)
    text_font = pygame.font.SysFont('Arial', 40)
    load_anim.play()
    screen = get_screen()
    raw_time = 0
    time = 0
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        raw_time += 1 / FPS
        if raw_time > time + 1:
            party = get_party(id)
            user2 = party.user2
            if user2 != 'wait':
                finished = True
        time = int(raw_time)
        write_text('Waiting for another player to join: ' + str(time), (
            window_width // 2 - 320, window_height // 5), screen, header_font)
        write_text('Your game id is ' + str(id), (
            window_width // 2 - 120, window_height // 5 + 50), screen, text_font)
        load_anim.blit(screen, (window_width // 2 - 100, window_height // 3 + 50))
        clock.tick(FPS)
        pygame.display.update()
        fill()
    load_anim.stop()

