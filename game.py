from visual_module import *
import random
import time
import pygame
from Web import client_local as cl
from game_objects import *

def figures_to_string(cf_dict):
    '''
    Transforms *cf_dict* into database format. *cf_dict* - dictionary
    of fields in party (party.fields attribute).
    '''
    output = ''
    for number in cf_dict.keys():
        x, y = number
        field = cf_dict[number]
        pm = str(int(field.pawn_moved))
        output += str(x) + str(y) + ',' + field.figuretype + ',' + pm + ';'
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
        field = cf_dict[coords]
        field.figuretype = data[1]
        field.pawn_moved = bool(data[2])
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
    players_data = {'player':username, 'player_rating': str(cl.check_rate(username))}
    finished = False
    moves_font = pygame.font.SysFont('FreeSerif', int(80 * scale_x))
    button_font = pygame.font.SysFont('Arial', int(50 * scale_x))
    moves_vis = Scroll_window(0, 0, [], moves_font, int(desk_x_coord), int(450 * scale_y), False)
    surrender_button = button(int(50 * scale_x), int(500 * scale_y), 'Surrender', button_font)
    white = cl.get_white(id)
    if white == username:
        color = 'white'
        black = cl.get_black(id)
        players_data.update({'opponent':black, 'opponent_rating': str(cl.check_rate(black))})
    else:
        color = 'black'
        players_data.update({'opponent':white, 'opponent_rating': str(cl.check_rate(white))})
    while not finished:
        if cl.check_flag(id, username):
            party, finished_program, move = event_handler_1(
                    party, color, moves_vis, surrender_button, players_data)
            if 'win' in cl.get_last_move(id):
                break
            cl.update_party_figures(id, figures_to_string(party.fields))
            cl.add_move(id, move)
            if 'win' in move:
                if 'draw' in move:
                    cl.update_rate(username, players_data['opponent'], 0)
                else:
                    cl.update_rate(username, players_data['opponent'], 2)
            if finished_program:
                raise SystemExit
            moves_vis.data.append(move)
        else:
            finished_1 = False
            frame_counter = 0
            while not finished_1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        finished_1 = True
                        cl.add_move(id, change_color(color) + '_win')
                        cl.update_rate(username, players_data['opponent'], 2)
                        raise SystemExit
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if surrender_button.check():
                            cl.add_move(id, change_color(color) + '_win')
                            cl.update_rate(username, players_data['opponent'], 2)
                    moves_vis.event_handler(event, None)
                draw_party_1(party, color, moves_vis, players_data)
                surrender_button.draw()
                pygame.display.update()
                frame_counter += 1
                if frame_counter >= FPS:
                    frame_counter = 0
                    finished_1 = cl.check_flag(id, username)
                    if 'win' in cl.get_last_move(id):
                        finished_1 = True
                        finished = True
                    if finished_1 and not finished:
                        last_move = cl.get_last_move(id)
                        moves_vis.data.append(last_move)
                        if 'pawn' in party.fields[(int(last_move[0]), int(last_move[1]))].figuretype and abs(int(last_move[3]) - int(last_move[1])) == 2:
                            party.last_pawn = party.fields[(int(last_move[2]), int(last_move[3]))]
                        party.fields = string_to_figures(cl.get_party_figures(id), party.fields)
    post_game_lobby(id, color, party)


def post_game_lobby(id, color, party):
    moves = cl.get_moves(id).split('\', \'')
    moves.remove('[\'')
    moves.remove('')
    moves.pop()
    party.fields = string_to_figures(cl.get_party_figures(id), party.fields)
    moves_font = pygame.font.SysFont('FreeSerif', int(80 * scale_x))
    button_font = pygame.font.SysFont('Arial', int(50 * scale_x))
    to_main_button = button(int(10 * scale_x), int(500 * scale_y), 'Back to main menu', button_font)
    states = [figures_to_string(party.fields)]
    for move in moves[::-1]:
        fig = move[4:]
        if 'enpassant' in move:
            fig = 'empty'
            if int(move[3]) > int(move[1]):
                fig_killed = 'black_pawn'
            else:
                fig_killed = 'white_pawn'
            party.fields[int(move[3]), int(move[0])].figuretype = fig_killed
        if 'O-O' in move:
            if move[2] == '7':
                party.fields[8, int(move[1])].figuretype = party.fields[6, int(move[1])].figuretype
                party.fields[6, int(move[1])].figuretype = 'empty'
            else:
                party.fields[1, int(move[1])].figuretype = party.fields[4, int(move[1])].figuretype
                party.fields[4, int(move[1])].figuretype = 'empty'
            fig = 'empty'
        party.fields[int(move[0]), int(move[1])].figuretype = party.fields[int(move[2]), int(move[3])].figuretype
        party.fields[int(move[2]), int(move[3])].figuretype = fig
        states.insert(0, figures_to_string(party.fields))
    finished = False
    moves_visual = Scroll_window(0, 0, moves, moves_font, int(desk_x_coord), 450 * scale_y, True)
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if to_main_button.check():
                    finished = True
            state_num = moves_visual.event_handler(event, None)
            if state_num != None:
                party.fields = string_to_figures(states[state_num + 1], party.fields)
        draw_party_1(party, color, moves_visual)
        to_main_button.draw()
        pygame.display.update()

