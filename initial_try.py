from show_part import *
from game_objects import *

init()


def main():
    party = Party()
    prior_flag = 'white'
    finished = False
    while not finished:
        try:
            party, prior_flag, finished = event_handler(party, prior_flag)
        except TypeError:
            pass
        draw_party(party)
main()
quit()
