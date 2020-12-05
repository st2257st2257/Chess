from visual_module import *
import random
import time
import pygame
from Web import client as cl
from game_objects import *

FPS = 30

def figures_to_string(cf_dict):
    output = ''
    for number in cf_dict.keys():
        x, y = number
        field = cf_dict[number]
        output += str(x) + str(y) + ',' + field.figuretype + ';'
    return output[:-1]


def string_to_figures(string, cf_dict):
    figs = string.split(';')
    output = {}
    for fig in figs:
        data = fig.split(',')
        coords = (int(data[0][0]), int(data[0][1]))
        field = Field(data[1])
        field.figmoved = cf_dict[coords].figmoved
        output.update({coords:field})
    return output


def game(id, username):
    party = Party()
    finished = False
    if cl.get_white(id) == username:
        color = 'white'
    else:
        color = 'black'
    while not finished:
        if cl.check_flag(id, username):
            party, finished, move = event_handler_1(party, color)
            cl.update_party_figures(id, figures_to_string(party.fields))
            cl.add_move(id, move)
        else:
            finished_1 = False
            frame_counter = 0
            while not finished_1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        finished_1 = True
                        finished = True
                draw_party_1(party, color)
                frame_counter += 1
                if frame_counter >= FPS:
                    frame_counter = 0
                    finished_1 = cl.check_flag(id, username)
                    if finished_1:
                        party.fields = string_to_figures(cl.get_party_figures(id), party.fields)
                
