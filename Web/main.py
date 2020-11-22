import requests
from requests.exceptions import HTTPError
from getpass import getpass
from gettext import gettext
import yaml


"""
Создание сессии от лица которй делаются GET и POST запросы
"""
session = requests.Session()


def check_player(login, password):
    """
    Проверяет наличие пользователя в базе данных
    и возвращет его id если он есть, 0 -в противном случае
    """
    local_response = session.get("http://kriel.xyz/Chess/php/check_player.php",
                                 data={'login': login, 'password': password},
                                 timeout=1)
    return int(str(local_response.content)[2:-1:])

"""
Добавление игрока вы базу данных(таблицу chess_players) с параметрами:
Name	    Type	        CollationAttributes		Default	
idPrimary	int(11)			No      	            None		AUTO_INCREMENT	
login	    varchar(255)	utf8_unicode_ci  		No	None		
password	varchar(255)	utf8_unicode_ci	    	No	None	
rate	    int(11)			No	                    None				
Если такой пользователь уже существует, то возвращаемое значение 1
Если пользователя нет, то возвращаемое значение 0
"""
def add_player(login, password):
    if check_player(login, password):
        return 0
    else:
        local_response = session.post("http://kriel.xyz/Chess/php/add_player.php",
                                     data={'login': login, 'password': password},
                                      timeout=1)
        return 1  # int(str(local_response.content)[3:-1:])
    
        
"""
Создаёт партию по двум лгинам и времени игры:
запись на сервер новой строчки в таблицу chess с параметрами:
	Name	Type	            CollationAttributes	    	Default
	1	    idPrimary	        int(11)			            No	None		AUTO_INCREMENT	
	2	    party_figures	    text	utf8_unicode_ci		Yes				
	3	    party_moves	text	utf8_unicode_ci		        Yes				
	4	    player_white_login	varchar(255)	            utf8_unicode_ci		
	5	    player_black_login	varchar(255)	            utf8_unicode_ci			
	6	    time	            int(11)			            None			
	7	    move_number     	int(11)			            0			
	8   	finished
""""
def create_new_party(player_1_login, player_2_login, time):
    # FIXME: добавить проверку наличия пользователей в базе данных
    local_response = session.post("http://kriel.xyz/Chess/php/create_party.php",
                                  data={'white': player_1_login, 'black': player_2_login, 'time': str(time)},
                                  timeout=1)
    print(str(local_response.content)[3:-1:])
    return int(str(local_response.content)[3:-1:])



"""
Обновляет данные на сервере по ямл файлу:
на вход подаётся имя файла и ID базы данных
"""
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


    
"""
Получение фигур из бызы данных словарь (возвращение словарая)
"""
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



"""Получение последнего номера хода из БД"""
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
    """Добавление хода в соблюдённом формате:
    AB-CD
    Где:
    A - Номер колонки начальной позиции (считая слева)
    B - Номер ряда начальной позиции (считая сверху (так надо))
    C - Номер колонки конечной позиции (считая слева)
    D - Номер ряда конечной позиции (считая сверху (так надо))
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



"""
Программа ждёт изменения хода на сервере
и не даёт пользователю делать ход.  
Когда ход на сервере меняется , программа обновляет данные 
и предлагает ввести значения вида ХХ-ХХ.
Когда значения введены, отправляет данные на
сервер и ЦИКЛ СНОВА
-пробная версия программы 
-использовать для разработки ивэнт мэреджера
"""


party = 476  # Дефолтный ID партии строка с этим  ID имеет вид:
# 476   11,;21,;31,;41,;51,;61,;71,;81,black_rook;12,;22,;...    55-57;66-78;54-66;62-54;41-62;22-41;43-22;51-43;63...
# xfgsdfg     wait   5   31   0
move_number = get_move_number(party)

# Создаём партию если пользователь играет беслыми и вступаем в партияю если пользователь играет чёрными
# начтраиваем индетефикатор партии
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
        """
        ЕСЛИ пользователь играет чёрными и первый ход ИЛИ ЕСЛИ пользователь сделал жод ЖДЁМ
        """
        if (get_move_number(party) == move_number) or ((color == 1) and (get_move_number(party) == 0)):
            print("<Waiting>")
        else:
            """Заставляем пользователя ввести ход"""
            add_move(party, input("Enter your move(XX-XX): "))
            move_number = get_move_number(party)
            print("Waiting for enemy move...")
            color = 1
        count += 1


if __name__ == '__main__':
    main()
