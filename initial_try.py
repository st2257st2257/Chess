from show_part import *
from game_objects import *

init()

party = Party

def main():
    prior_flag = 'white'
    finished = False
    while not finished:
        party, prior_flag, finished = event_handler(party, prior_flag)
        draw_party(party)
main()
quit()