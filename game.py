from visual_module import *
import random
import time
import pygame

FPS = 30

def game(id, username):
    party = get_party(id)
    if username = party.user1:
        user1_game(id)
    else:
        user2_game(id)

def user1_game(id):
    party = get_party(id)
    if random.random():
        party.user1_color = 'black'
        party.user2_color = 'white'
    else:
        party.user1_color = 'white'
        party.user2_color = 'black'
    push_party(party)
    finished = False
    frame_iterator = 0
    while not finished:
        frame_iterator += 1
        if frame_iterator >= FPS:
           frame_iterator = 0
           party = get_party(id)
        if party.user1_color == party.priority_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    party.winner = party.user2_color
                    push_party(party, id)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    party = event_handler(party)
                    push_party(party, id)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                    party.winner = party.user2_color
                    push_party(party)
        draw_party_user_1(party, id)
        if party.winner != '':
            finished = True


def user2_game(id):
    party = get_party(id)
    finished = False
    frame_iterator = 0
    while not finished:
        frame_iterator += 1
        if frame_iterator >= FPS:
           frame_iterator = 0
           party = get_party(id)
        if party.user2_color == party.priority_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    party.winner = party.user1_color
                    push_party(party, id)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    party = event_handler(party)
                    push_party(party, id)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    party.winner = party.user2_color
                    push_party(party, id)
        draw_party_user_2(party)
        if party.winner != '':
            finished = True
