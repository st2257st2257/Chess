import socket
import json
from time import sleep

vis = 1


# 1:  add_move(472, "56-58" + ";")
def add_move(party_id=472, move="56-58" + ";"):
    global vis
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('46.138.245.249', 11111))
    client_sock.sendall(json.dumps([1, [party_id, move]]).encode())
    data = json.loads(client_sock.recv(1024))
    client_sock.close()
    if vis:
        print('New move was added')
    return str(data)


# 2
def create_party(white='white', black='black', time=5):
    global vis
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('46.138.245.249', 11111))
    client_sock.sendall(json.dumps([2, [white, black, time]]).encode())
    data = json.loads(client_sock.recv(1024))
    client_sock.close()
    if vis:
        print('New party id =', str(data))
    return int(data)


# 3:  get_last_move(id=476)
def get_last_move(party_id=476):
    global vis
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('46.138.245.249', 11111))
    client_sock.sendall(json.dumps([3, [party_id]]).encode())
    data = json.loads(client_sock.recv(1024))
    client_sock.close()
    if vis:
        print('Last move with party id =', str(party_id), "  move:", repr(data))
    return str(data)


# 4
def get_party_figures(party_id=472):
    global vis
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('46.138.245.249', 11111))
    client_sock.sendall(json.dumps([4, [party_id]]).encode())
    data = json.loads(client_sock.recv(1024))
    client_sock.close()
    if vis:
        print('Party figures with party id =', str(party_id), "  figures: ", repr(data))
    return str(data)


# 5
def update_party_figures(party_id=472, figures="11,;21,"):
    global vis
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('46.138.245.249', 11111))
    client_sock.sendall(json.dumps([5, [party_id, figures]]).encode())
    data = json.loads(client_sock.recv(1024))
    client_sock.close()
    if vis:
        print('Party figures was updated with party id =', str(party_id), "  data: ", figures)
    return str(data)


# 6
def set_white(party_id, name="white"):
    global vis
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('46.138.245.249', 11111))
    client_sock.sendall(json.dumps([6, [party_id, name]]).encode())
    data = json.loads(client_sock.recv(1024))
    client_sock.close()
    if vis:
        print('White player with party id =', str(party_id), "  login:", repr(data))
    return str(data)


# 7
def set_black(party_id, name="black"):
    global vis
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('46.138.245.249', 11111))
    client_sock.sendall(json.dumps([7, [party_id, name]]).encode())
    data = json.loads(client_sock.recv(1024))
    client_sock.close()
    if vis:
        print('Black player with party id =', str(party_id), "  login:", repr(data))
    return str(data)


# 8
def get_white(party_id):
    global vis
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('46.138.245.249', 11111))
    client_sock.sendall(json.dumps([8, [party_id]]).encode())
    data = json.loads(client_sock.recv(1024))
    client_sock.close()
    if vis:
        print('White player with party id =', str(party_id), "  login:", repr(data))
    return str(data)


# 9
def get_black(party_id):
    global vis
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('46.138.245.249', 11111))
    client_sock.sendall(json.dumps([9, [party_id]]).encode())
    data = json.loads(client_sock.recv(1024))
    client_sock.close()
    if vis:
        print('Black player with party id =', str(party_id), "  login:", repr(data))
    return str(data)


# 10
def check_user(name="ask"):
    global vis
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('46.138.245.249', 11111))
    client_sock.sendall(json.dumps([10, [name]]).encode())
    data = json.loads(client_sock.recv(1024))
    client_sock.close()
    if vis:
        print('User is in DB: ', int(data))
    return int(data)


# 11
def check_user_party(party_id=472, name="zvzvzs"):
    global vis
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('46.138.245.249', 11111))
    client_sock.sendall(json.dumps([11, [party_id, name]]).encode())
    data = json.loads(client_sock.recv(1024))
    client_sock.close()
    if vis:
        print("check_user_party answer: ", data, "  0-no user 1-white 2-black")
    return int(data)


# 12
def check_user_lp(login='ask', password='srt'):
    global vis
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('46.138.245.249', 11111))
    client_sock.sendall(json.dumps([12, [login, password]]).encode())
    data = json.loads(client_sock.recv(1024))
    client_sock.close()
    if vis:
        print("check_user_lp answer: ", data, "  0-wrong LogPass 1-right LogPass")
    return int(data)


# 13
def check_flag(party_id=472, name="white"):
    global vis
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('46.138.245.249', 11111))
    client_sock.sendall(json.dumps([13, [party_id, name]]).encode())
    data = json.loads(client_sock.recv(1024))
    client_sock.close()
    if vis:
        print('Flag for ' + name + ": " + str(data))
    return int(data)


# 14
def create_user(login="New_user", password="New_password"):
    global vis
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('46.138.245.249', 11111))
    client_sock.sendall(json.dumps([14, [login, password]]).encode())
    data = json.loads(client_sock.recv(1024))
    client_sock.close()
    if vis:
        print('New user id =', str(data))
    return int(data)


# 15
def execute_sql(string="SQL", password="password"):
    global vis
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('46.138.245.249', 11111))
    client_sock.sendall(json.dumps([15, [string, password]]).encode())
    data = json.loads(client_sock.recv(1024))
    client_sock.close()
    if vis:
        print('Answer: ', str(data))
    return str(data)


# 16
def get_moves(party_id=472):
    global vis
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('46.138.245.249', 11111))
    client_sock.sendall(json.dumps([16, [party_id]]).encode())
    data = json.loads(client_sock.recv(1024))
    client_sock.close()
    if vis:
        print('Moves: ', str(data))
    return str(data)


# 17
def get_last_move_number(party_id=472):
    global vis
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('46.138.245.249', 11111))
    client_sock.sendall(json.dumps([17, [party_id]]).encode())
    data = json.loads(client_sock.recv(1024))
    client_sock.close()
    if vis:
        print('Last move number =', str(data))
    return int(data)


# set_black(472, "abcc")
# check_user()
# check_user_party(472, "abcc")
# check_user_lp("sdf", "sdf")
# check_flag(472, "abcc")
# get_party_figures()
# create_party("asdf", "DFds", 5)
# add_move(472, "76-58" + ";")

get_last_move()
