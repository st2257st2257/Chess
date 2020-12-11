from visual_module import *
import random
import time
import pygame
from Web import client as cl
from game_objects import *

FPS = 30

def figures_to_string(cf_dict):
    '''
    Transforms *cf_dict* into database format. *cf_dict* - dictionary
    of fields in party (party.fields attribute).
    '''
    output = ''
    for number in cf_dict.keys():
        x, y = number
        field = cf_dict[number]
        output += str(x) + str(y) + ',' + field.figuretype + ';'
    return output[:-1]


def string_to_figures(string, cf_dict):
    '''
    Transforms string in database into dictionary of fields in party.
    Takes *string* and *cf_dict* - dictionary of fields on computer to
    keep *figmoved* attribute on computer.
    '''
    figs = string.split(';')
    output = {}
    for fig in figs:
        data = fig.split(',')
        coords = (int(data[0][0]), int(data[0][1]))
        field = Field(data[1])
        field.figmoved = cf_dict[coords].figmoved
        output.update({coords:field})
    return output

def change_color(color):
    if color == 'black':
        return 'white'
    else:
        return 'black'


def game(id, username):
    '''
    Game itself with *id* id and *username* - username of user entering game.
    '''
    party = Party()
    finished = False
    moves_font = pygame.font.SysFont('FreeSerif', 80)
    button_font = pygame.font.SysFont('Arial', 80)
    moves_vis = Scroll_window(0, 0, [], moves_font, 300, 500, False)
    surrender_button = button(000, 700, 'Surrender', button_font, 0)
    if cl.get_white(id) == username:
        color = 'white'
    else:
        color = 'black'
    while not finished:
        if cl.check_flag(id, username):
            party, finished, move = event_handler_1(party, color, moves_vis, surrender_button)
            if 'win' in cl.get_last_move(id):
                break
            cl.update_party_figures(id, figures_to_string(party.fields))
            cl.add_move(id, move)
            moves_vis.data.append(move)
        else:
            finished_1 = False
            frame_counter = 0
            while not finished_1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        finished_1 = True
                        finished = True
                        cl.add_move(id, change_color(color) + '_win')
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if surrender_button.check():
                            cl.add_move(id, change_color(color) + '_win')
                    moves_vis.event_handler(event, None)
                draw_party_1(party, color, moves_vis)
                surrender_button.draw()
                pygame.display.update()
                frame_counter += 1
                if frame_counter >= FPS:
                    frame_counter = 0
                    finished_1 = cl.check_flag(id, username)
                    if 'win' in cl.get_last_move(id):
                        finished_1 = True
                        finished = True
                    if finished_1:
                        party.fields = string_to_figures(cl.get_party_figures(id), party.fields)
                        moves_vis.data.append(cl.get_last_move(id))
    post_game_lobby(id, color, party)


def post_game_lobby(id, color, party):
    moves = cl.get_moves(id).split('\', \'')
    moves.remove('[\'')
    moves.remove('')
    moves.pop()
    party.fields = string_to_figures(cl.get_party_figures(id), party.fields)
    moves_font = pygame.font.SysFont('FreeSerif', 80)
    states = [figures_to_string(party.fields)]
    for move in moves[::-1]:
        fig = move[4:]
        party.fields[int(move[0]), int(move[1])].figuretype = party.fields[int(move[2]), int(move[3])].figuretype
        party.fields[int(move[2]), int(move[3])].figuretype = fig
        states.insert(0, figures_to_string(party.fields))
    finished = False
    moves_visual = Scroll_window(0, 0, moves, moves_font, 300, 500, True)
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            state_num = moves_visual.event_handler(event, None)
            if state_num != None:
                party.fields = string_to_figures(states[state_num + 1], party.fields)
        draw_party_1(party, color, moves_visual)
        pygame.display.update()

