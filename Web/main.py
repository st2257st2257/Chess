import requests
from requests.exceptions import HTTPError
from getpass import getpass
from gettext import gettext
import yaml

"""for url in ['http://kriel.xyz/menu/News/']:
    try:
        response = requests.get(url)
        print(response.text)
        response.json()
        # если ответ успешен, исключения задействованы не будут
        response.raise_for_status()
        print('Success!')
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
"""


class WedUser:
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def ddd(self):
        pass


session = requests.Session()

# session.headers.update = {'X-Request-ID': 'c8b50f7200e75f2bd3759ce8b09faaf8'}
# print(session.headers.update)

# session.auth = ('username', getpass())
# response = session.post("http://kriel.xyz/text/s_get.php", data={'text': 'aabbcc'}, timeout=1)
# response = session.post("http://kriel.xyz/text/s_get.php", data={'text': 'aabbcc'}, timeout=1)
# print(response.headers)
# print(response.json())


def add_player(login, password):
    # FIXME: добавить проверку наличия пользователя в БД
    local_response = session.post("http://kriel.xyz/Chess/php/add_player.php",
                                  data={'login': login, 'password': password},
                                  timeout=1)
    print("Player added: " + str(local_response.content))


def create_new_party(player_1_login, player_2_login, time):
    # FIXME: добавить проверку наличия пользователей в базе данных
    local_response = session.post("http://kriel.xyz/Chess/php/create_party.php",
                                  data={'white': player_1_login, 'black': player_2_login, 'time': str(time)},
                                  timeout=1)
    print(str(local_response.content)[3:-1:])
    return int(str(local_response.content)[3:-1:])


def update_figures(party_id=10, yaml_name="init_party.yaml"):
    figures_data_string = ""
    with open(yaml_name, 'r') as file:
        cf_dict = yaml.load(file, Loader=yaml.Loader)
    for elem in cf_dict:
        figures_data_string += str(elem) + ',' + str(cf_dict[elem]) + ";"
    local_response = session.post("http://kriel.xyz/Chess/php/update_party.php",
                                  data={'id': party_id, 'data': figures_data_string},
                                  timeout=1)
    print(str(local_response.content))


def get_figures(party_id=10):
    # FIXME: добавить умную проверку корректности строки
    local_response = session.post("http://kriel.xyz/Chess/php/get_figures.php",
                                  data={'id': party_id},
                                  timeout=1)
    try:
        cf_dict = {figure.split(',')[0]: figure.split(',')[1]
                   for figure in str(local_response.content)[3:-1:].split(";")[:-1]}
        return cf_dict
    except IndexError:
        print("List index out of range in 77 string")


def check_player(login, password):
    """
    Проверяет наличие пользователя в базе данных
    и возвращет его id если он есть, 0 -в противном случае
    """
    local_response = session.get("http://kriel.xyz/Chess/php/check_player.php",
                                 data={'login': login, 'password': password},
                                 timeout=1)
    return int(str(local_response.content)[2:-1:])


def get_move_number(party_id):
    """
    Проверяет изменённость данных на сервере:
    есди данные изменены, то выводит новый номер хода
    если нет выводит 0
    """
    local_response = session.post("http://kriel.xyz/Chess/php/check_change.php",
                                  data={'id': party_id},
                                  timeout=1)
    return int(str(local_response.content)[2:-1:])


def add_move(party_id=99, string="11-11"):
    """
    Вносит изменения в базу данны:
    1) в последовательность ходов добавляет ход
    2) увеличивает номер хода на 1
    """
    local_response = session.post("http://kriel.xyz/Chess/php/add_move.php",
                                  data={'id': str(party_id), 'move': string},
                                  timeout=1)
    print("New move: " + string)
    print(str(local_response.content))


def update_rate(player_login, string):
    pass


def get_moves(party_id):
    pass


# add_player(input('Login: '), getpass())

"""

Программа ждёт изменения хода на сервере
и не даёт пользователю делать ход.  
Когда ход на сервере меняется , программа обновляет данные 
и предлагает ввести значения вида ХХ-ХХ.
Когда значения введены, отправляет данные на
сервер и ЦИКЛ СНОВА


"""
move_number = get_move_number(99)
party = 99
color = int(input("0-white, 1-black: "))

if color:
    party = int(input("Enter party id: "))
else:
    party = create_new_party("white", "black", 5)
    print("Party id: " + str(party))

not_finished = True


def main():
    global move_number, color, party
    count = 0
    while (count < 1000) & not_finished:
        if (get_move_number(party) == move_number) or ((color == 1) and (get_move_number(party) == 1)):
            print("<Waiting>")
        else:
            add_move(party, input("Enter your move(XX-XX): "))
            move_number = get_move_number(party)
            print("Waiting for enemy move...")
            color = 1
        count += 1


if __name__ == '__main__':
    main()


# create_new_party(input('Login_white: '), input('Login_black: '), 5)
# print(update_figures(50))

# requests.post("http://kriel.xyz/text/s_get.php", data={'text': 'aabbcc'}, timeout=1)
