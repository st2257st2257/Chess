from visual_module import *
import pyganim
import pygame
from game import *
from Web import client_local as cl
import random
import _thread

clock = pygame.time.Clock()

field_len = int(400 * scale_x)

x0 = int(800 * scale_x)

load_anim = []

anim_delay = 50

for i in range(9):
    load_anim.append(('load_anim/load_' + str(i) + '.png', anim_delay))
load_anim = pyganim.PygAnimation(load_anim)

def register_window():
    '''
    Draws window for creating new user.
    '''
    username_field = InputBox(x0, int(350 * scale_y), field_len)
    pass_field = InputBox(x0, 450 * scale_y, field_len)
    rep_pass_field = InputBox(x0, 550 * scale_y, field_len)
    screen = get_screen()
    finished = False
    header_font = pygame.font.SysFont('Arial', int(scale_x * 80))
    button_font = pygame.font.SysFont('Arial', int(scale_x * 50))
    reg_button = button(
            x0, int(720 * scale_y), 
            'Add user', button_font
    )
    back_button = button(
            int(1000 * scale_x), int(720 * scale_y), 
            'Back', button_font
    )
    text_font = pygame.font.SysFont('Arial', int(40 * scale_x))
    error_text = ''
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if reg_button.check():
                    error_text = ''
                    if len(username_field.text) < 5:
                        error_text = 'Username is too short'
                    elif len(pass_field.text) < 5:
                        error_text = 'Password is too short'
                    elif pass_field.text != rep_pass_field.text:
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
        write_text('Password', (x0, 
            int(420 * scale_y)), screen, text_font)
        write_text('Username', (
            x0, int(320 * scale_y)), screen, text_font)
        write_text('Repeat password', (
            x0, int(520 * scale_y)), screen, text_font)
        write_text(error_text, (
            x0, int(600 * scale_y)), screen, text_font)
        clock.tick(FPS)
        pygame.display.update()
        login_fill()


def start_window():
    '''
    Creates main window for entering password and username. 
    '''
    username_field = InputBox(x0, 400 * scale_y, field_len)
    pass_field = InputBox(x0, 500 * scale_y, field_len)
    screen = get_screen()
    finished = False
    header_font = pygame.font.SysFont('Arial', int(scale_x * 80))
    button_font = pygame.font.SysFont('Arial', int(scale_x * 50))
    start_button = button(
            x0, int(720 * scale_y), 'Play', button_font)
    reg_button = button(
            int(1000 * scale_x), int(720 * scale_y), 
            'Sign up', button_font
    )
    text_font = pygame.font.SysFont('Arial', int(40 * scale_x))
    error_text = ''
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.check():
                    if len(username_field.text) < 5:
                        error_text = 'Username is too short'
                    elif len(pass_field.text) < 5:
                        error_text = 'Password is too short'
                    elif not cl.check_user_lp(username_field.text, pass_field.text):
                        error_text = 'Wrong password or username'
                    else:
                        finished = True
                if reg_button.check():
                    error_text = ''
                    pass_field.text = ''
                    username_field.text = ''
                    register_window()
            username_field.event_handler(event)
            pass_field.event_handler(event)
        password = pass_field.text
        pass_field.text = '*' * len(pass_field.text)
        username_field.draw()
        pass_field.draw()
        start_button.draw()
        reg_button.draw()
        pass_field.text = password
        write_text('Password', (x0, 
            int(470 * scale_y)), screen, text_font)
        write_text('Username', (
            x0, int(370 * scale_y)), screen, text_font)
        write_text(error_text, (
            x0, int(320 * scale_y)), screen, text_font)
        clock.tick(FPS)
        pygame.display.update()
        login_fill()
    main_menu(username_field.text)


def main_menu(username):
    '''
    Draws main menu for creating or entering game. Takes 
    *username* - username of user entering main menu.
    '''
    text_font = pygame.font.SysFont('Arial', int(scale_x * 40))
    button_font = pygame.font.SysFont('Arial', int(scale_x * 50))
    header_font = pygame.font.SysFont('Arial', int(scale_x * 80))
    screen = get_screen()
    create_game = button(int(960 * scale_x), int(360 * scale_y), 'Create game', button_font)
    join_game = button(int(960 * scale_x), int(540 * scale_y), 'Join game', button_font)
    id_field = InputBox(int(1110 * scale_x), int(540 * scale_y), field_len)
    error_text = ''
    finished = False
    rate = cl.check_rate(username)
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if join_game.check():
                    if cl.check_user_party(id_field.text, 'wait') != 0:
                        id = id_field.text
                        colors_gen = random.randint(0, 1)
                        if colors_gen:
                            cl.set_black(id, username)
                        else:
                            cl.set_black(id, cl.get_white(id))
                            cl.set_white(id, username)
                        cl.add_move(id, '')
                        cl.add_move(id, '')
                        game(id, username)
                        error_text = ''
                        rate = cl.check_rate(username)
                    else:
                        error_text = 'Unable to find game'
                    id_field.text = ''
                if create_game.check():
                    id_field.text = ''
                    error_text = ''
                    id = cl.create_party(username, 'wait', 0)
                    waiting_room(id, username)
                    rate = cl.check_rate(username)
            id_field.event_handler(event)
        create_game.draw()
        join_game.draw()
        id_field.draw()
        write_text(error_text, (int(1110 * scale_x), int(575 * scale_y)), screen, text_font)
        write_text('Enter id', (int(1110 * scale_x), int(510 * scale_y)), screen, text_font)
        write_text(username + '|' + str(rate), (int(1280 * scale_x), int(360 * scale_y)), screen, header_font)
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
    header_font = pygame.font.SysFont('Arial', int(scale_x * 80))
    button_font = pygame.font.SysFont('Arial', int(scale_x * 50))
    text_font = pygame.font.SysFont('Arial', int(scale_x * 40))
    back_button = button(int(100 * scale_x), int(100 * scale_x), 'Back', button_font)
    load_anim.play()
    screen = get_screen()
    raw_time = 0
    time = 0
    start = False
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cl.set_black(id, 'None')
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check():
                    cl.set_black(id, 'None')
                    finished = True
                    start = False
        raw_time += 1 / FPS
        if raw_time > time + 1:
            _thread.start_new_thread(check_start, (id, 0))
        time = int(raw_time)
        write_text('Waiting for another player to join: ' + str(time), (
            int(480 * scale_x), int(180 * scale_y)), screen, header_font)
        write_text('Your game id is ' + str(id), (
            int(680 * scale_x), int(230 * scale_y)), screen, text_font)
        back_button.draw()
        load_anim.blit(screen, (int(700 * scale_x), int(350 * scale_y)))
        clock.tick(FPS)
        pygame.display.update()
        fill()
    load_anim.stop()
    if start:
        game(id, username)

