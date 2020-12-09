from visual_module import *
import pyganim
import pygame
from game import *
from Web import client_local as cl
import random
import _thread

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
    Draws window for creating new user.
    '''
    field_x = (window_width - field_len) // 3 * 2
    field_y = window_height // 2 - 100
    username_field = InputBox(field_x, field_y, field_len)
    pass_field = InputBox(field_x, field_y + 100, field_len)
    rep_pass_field = InputBox(field_x, field_y + 200, field_len)
    screen = get_screen()
    finished = False
    header_font = pygame.font.SysFont('Arial', 80)
    button_font = pygame.font.SysFont('Arial', 50)
    reg_button = button(
            field_x, window_height * 4 // 5, 
            'Add user', button_font, BUTTON_COLOR
    )
    back_button = button(
            field_x + field_len // 2, window_height * 4 // 5, 
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
                    if pass_field.text != rep_pass_field.text:
                        error_text = 'Passwords do not match'
                    elif cl.check_user(username_field.text):
                        error_text = 'User exists'
                    else:
                        cl.create_user(username_field.text, pass_field.text)
                        finished = True
                if back_button.check():
                    finished = True
            username_field.event_handler(event)
            pass_field.event_handler(event)
            rep_pass_field.event_handler(event)
        password = pass_field.text
        pass_repeat = rep_pass_field.text
        pass_field.text = '*' * len(pass_field.text)
        rep_pass_field.text = '*' * len(rep_pass_field.text)
        username_field.draw()
        pass_field.draw()
        reg_button.draw()
        back_button.draw()
        rep_pass_field.draw()
        pass_field.text = password
        rep_pass_field.text = pass_repeat
        write_text('Password', (field_x, 
            pass_field.y - 30), screen, text_font)
        write_text('Username', (
            field_x, username_field.y - 30), screen, text_font)
        write_text('Repeat password', (
            field_x, rep_pass_field.y - 30), screen, text_font)
        write_text(error_text, (
            field_x, rep_pass_field.y + 50), screen, text_font)
        clock.tick(FPS)
        pygame.display.update()
        fill()
    return finish_program


def start_window():
    '''
    Creates main window for entering password and username. 
    '''
    field_x = (window_width - field_len) // 3 * 2
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
            field_x + field_len // 2, window_height * 4 // 5, 
            'Sign up', button_font, BUTTON_COLOR
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
                    if cl.check_user_lp(username_field.text, pass_field.text):
                        finished = True
                        start = True
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
        write_text(error_text, (
            field_x, pass_field.y + 50), screen, text_font)
        clock.tick(FPS)
        pygame.display.update()
        fill()
    if start:
        main_menu(username_field.text)


def main_menu(username):
    '''
    Draws main menu for creating or entering game. Takes 
    *username* - username of user entering main menu.
    '''
    x = window_width // 5
    y = window_height // 5
    text_font = pygame.font.SysFont('Arial', 40)
    button_font = pygame.font.SysFont('Arial', 50)
    header_font = pygame.font.SysFont('Arial', 80)
    screen = get_screen()
    create_game = button(x * 3, y * 2, 'Create game', button_font, BUTTON_COLOR)
    join_game = button(x * 3, y * 3, 'Join game', button_font, BUTTON_COLOR)
    id_field = InputBox(x * 3 + 150, y * 3, field_len)
    finished = False
    error_text = ''
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if join_game.check():
                    if cl.check_user_party(id_field.text, 'wait') != 0:
                        id = id_field.text
                        print('ure wonderful')
                        colors_gen = random.randint(0, 1)
                        if colors_gen:
                            cl.set_black(id, username)
                        else:
                            cl.set_black(id, cl.get_white(id))
                            cl.set_white(id, username)
                        cl.add_move(id, '')
                        cl.add_move(id, '')
                        game(id, username)
                    else:
                        error_text = 'Unable to find game'
                if create_game.check():
                    id = cl.create_party(username, 'wait', 0)
                    waiting_room(id, username)
            id_field.event_handler(event)
        create_game.draw()
        join_game.draw()
        id_field.draw()
        write_text(error_text, (x * 3 + 150, y * 3 + 35), screen, text_font)
        write_text('Enter id', (x * 3 + 150, y * 3 - 30), screen, text_font)
        write_text(username, (x * 4, y * 2), screen, header_font)
        clock.tick(FPS)
        pygame.display.update()
        fill()

def check_start(id, a):
    global start, finished
    finished = not cl.check_user_party(id, 'wait')
    start = finished

def waiting_room(id, username):
    '''
    Draws waiting room with *id* number. *Username* - username of
    user creating game with id number.
    '''
    global start, finished
    finished = False
    header_font = pygame.font.SysFont('Arial', 80)
    text_font = pygame.font.SysFont('Arial', 40)
    load_anim.play()
    screen = get_screen()
    raw_time = 0
    time = 0
    start = False
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        raw_time += 1 / FPS
        if raw_time > time + 1:
            _thread.start_new_thread(check_start, (id, 0))
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
    if start:
        game(id, username)

