import sqlite3
import json
import datetime

conn = None
cursor = None
vis = 0

def init():
    global vis, conn, cursor
    conn = sqlite3.connect('example.db')
    if vis:
        print("...Start connection...")
    cursor = conn.cursor()


def add_move(id, move):
    global vis, conn, cursor
    if vis:
        print("\nAdding move...")
    
    # base settings
    cursor.execute('SELECT * FROM chess WHERE id=' + str(id) + ';')
    answer = cursor.fetchone()
    if vis:
        print("    Answer id:", answer[0])
    
    
    new_last_move = 0
    new_moves_sequence = ""
    if answer[2] == None:
        new_moves_sequence = str(move)
    else:
        new_moves_sequence = str(str(answer[2]) + move)
    
    if int(answer[0]):
        new_last_move = int(answer[6]) + 1
    else:
        new_last_move = 1;
        
    # cursor.execute('UPDATE chess SET party_moves = ' + new_moves_sequence + ', move_number=' + new_last_move + ' WHERE id=470;')
    # print("UPDATE chess SET party_moves = '" + new_moves_sequence + "' WHERE id=470;")
    cursor.execute("UPDATE chess SET party_moves = '" + new_moves_sequence + "' WHERE id=" + str(id) + ";")
    cursor.execute("UPDATE chess SET move_number=" + str(new_last_move) + " WHERE id=" + str(id) + ";")
    
    if vis:
        print("    End adding")
        

def create_party(white='white', black='balck', time=5):
    global vis, conn, cursor
    if vis:
        print("\nCreating party...")
    
    cursor.execute("INSERT INTO chess (id, player_white_login, player_black_login, time) VALUES ((SELECT MAX(id) FROM chess)+1, '" +
                   str(white) + "','" + str(black) + "'," + str(time) + ");")
    cursor.execute("SELECT * FROM chess WHERE id = (SELECT MAX(id) FROM chess);");
    answer = cursor.fetchone()
    if vis:
        print("    New party: ", answer)
    return str(answer[0])
 
 
def get_last_move(id=472):
    global vis, conn, cursor
    if vis:
        print("\nGetting last move id=" +str(id)+ "...")
    
    cursor.execute("SELECT * FROM chess WHERE id = " + str(id) + ";");
    answer = str(cursor.fetchone()[2]).split(';')[-2]
    if vis:
        print("    Last move: ", answer)
    return answer


def get_moves(id=472):
    global conn, cursor
    if vis:
        print("\nGetting last move id=" +str(id)+ "...")
    
    cursor.execute("SELECT * FROM chess WHERE id = " + str(id) + ";");
    answer = str(cursor.fetchone()[2])[:-1].split(';')
    if vis:
        print("    Last move: ", answer)
    return answer

"""
def get_moves(id):
    id = int(id)
    global vis, conn, cursor
    if vis:
        print("\nGetting last move id=" +str(id)+ "...")
    
    cursor.execute("SELECT * FROM chess WHERE id = " + str(id) + ";");
    answer = str(cursor.fetchone()[2])[:-1].split(';')
    
    
    res =[]
    for i in answer:
        if len(i) > 0:
            res.append(i)
    
    if vis:
        print("    Moves: ", res)
    return res
"""
    
def get_last_move_number(id=472):
    return len(get_moves(id))


def get_party_figures(id):
    global vis, conn, cursor
    if vis:
        print("\nGetting party figures id=" +str(id)+ "...")
    
    cursor.execute("SELECT * FROM chess WHERE id = " + str(id) + ";");
    answer = str(cursor.fetchone()[1])
    if vis:
        print("    Party figures: ", answer)
    return answer


def update_party_figures(id, party_figures):
    global vis, conn, cursor
    if vis:
        print("\nUpdating party figures...")
    
    cursor.execute("UPDATE chess SET party_figures='"+party_figures+"' WHERE id=" + str(id) + ';')
    if vis:
        print("    End updating")
    
    
def get_white(id):
    global vis, conn, cursor
    if vis:
        print("\nGetting white id=" +str(id)+ "...")
    
    cursor.execute("SELECT * FROM chess WHERE id = " + str(id) + ";");
    answer = str(cursor.fetchone()[3])
    if vis:
        print("    Name: ", answer)
    return answer
    

def get_black(id):
    global vis, conn, cursor
    if vis:
        print("\nGetting black id=" +str(id)+ "...")
    
    cursor.execute("SELECT * FROM chess WHERE id = " + str(id) + ";");
    answer = str(cursor.fetchone()[4])
    if vis:
        print("    Name: ", answer)
    return answer


def set_white(id, name):
    global vis, conn, cursor
    if vis:
        print("\nSetting white id=" +str(id)+ "...")
    
    cursor.execute("UPDATE chess SET player_white_login='"+name+"' WHERE id=" + str(id) + ';')
    if vis:
        print("    New white name: ", name)
    

def set_black(id, name):
    global vis, conn, cursor
    if vis:
        print("\nSetting black id=" +str(id)+ "...")
    
    cursor.execute("UPDATE chess SET player_black_login='"+name+"' WHERE id=" + str(id) + ';')
    if vis:
        print("    New black name: ", name)


def check_user(login):
    global vis, conn, cursor
    if vis:
        print("\nChecking user login=" +str(login)+ "...")
    
    cursor.execute("SELECT * FROM chess_players WHERE login = '" + str(login) + "';");
    answer = str(cursor.fetchone())
    if answer != "None":
        if vis:
            print("    Here is a user with login: ", login)
            print("    User: ", answer)
        return 1
    else:
        if vis:
            print("    Here is no user with that login")
        return 0


def check_user_party(id, login):
    global vis, conn, cursor
    if vis:
        print("\nChecking user color in party=" +str(login)+ " login="+str(login)+"...")
    
    cursor.execute("SELECT * FROM chess WHERE id = " + str(id) + ";");
    answer = cursor.fetchone()
    if str(answer[3]) == login:
        if vis:
            print("    Here is a white user with login: ", login)
            print("    User: ", answer[3:])
        return 1
    elif str(answer[4]) == login:
        if vis:
            print("    Here is black user with that login: ", login)
            print("    User: ", answer[3:])
        return 2
    else:
        if vis:
            print("    No users with that login and party name")
            print("    Answer: ", answer[3:])
        return 0


def check_user_lp(login, password):
    global vis, conn, cursor
    if vis:
        print("\nChecking user login=" +str(login)+ "...")
    
    cursor.execute("SELECT * FROM chess_players WHERE login = '" + str(login) + "' AND password = '" + str(password) + "';");
    answer = str(cursor.fetchone())
    if answer != "None":
        if vis:
            print("    Here is a user with login: ", login, " and password: ", password)
            print("    User: ", answer)
        return 1
    else:
        if vis:
            print("    Here is no user with that login")
        return 0


def check_flag(id, login):
    global vis, conn, cursor
    if vis: 
        print("\nChecking user flag login=" +str(login)+ "...")
    
    color = check_user_party(id, login)
    last_move_number = get_last_move_number(id)
    
    if color == 0:
        if vis:
            print("Error: in getting user color")
        else:
            pass
    elif color == 1:
        if last_move_number%2:
            return 0
        else:
            return 1
    elif color == 2:
        if last_move_number%2:
            return 1
        else:
            return 0
    return 0


def create_user(login="New_user", password="New_password"):
    global vis, conn, cursor
    if vis:
        print("\nCreating user...")
    
    
    cursor.execute("INSERT INTO chess_players (id, login, password, rate) VALUES ((SELECT MAX(id) FROM chess_players)+1, '" +
                   str(login) + "','" + str(password) + "',800);")
    
    cursor.execute("SELECT * FROM chess_players WHERE id = (SELECT MAX(id) FROM chess_players);");
    answer = cursor.fetchone()
    if vis:
        print("    New party: ", answer)
    return str(answer[0])


def execute_sql(sql_string, password):
    global vis, conn, cursor
    if password == "askristal":
        cursor.execute(sql_string)
        answer = cursor.fetchone()
        if vis:
            print("    Answer: ", answer)
        return str(answer[0])
    else:
        return "wrong data"


def cancel():
    global vis 
    conn.commit()
    conn.close()
    if vis:
        print("\n...End   connection...")


def print_request(client_id="C_I", request="...", answer="...", ping="0"):
    global vis, conn, cursor
    
    text = ""
    try:
        if (len(request) > 0):
            text = "REQUEST: [" + str(request[0][1:-3:]) + ", " + str(request[1])  + "]  ANSWER: " + str(answer)
        else:
            text = "REQUEST: [" + str(request[0][1:-3:]) + "]  ANSWER: " + str(answer)
    except Exception:
        text = request + ' ' + answer
    if vis:
        print(text)
    
    cursor.execute("INSERT INTO History (id, client_id, request, time, ping) VALUES ((SELECT MAX(id) FROM History)+1, '" + str(client_id) + "', '" + text+ "', '" +
                   str(datetime.datetime.now()) + "','" + ping
                   + "');")
    
    cursor.execute("SELECT * FROM History WHERE id = (SELECT MAX(id) FROM History);");
    answer = cursor.fetchone()
    print(answer)

def check_rate(login):
    global vis, conn, cursor
    if vis: 
        print("\nChecking user rate login=" +str(login)+ "...")
    
    cursor.execute("SELECT * FROM chess_players WHERE login = '" + login + "';");
    answer = cursor.fetchone()
    if vis:
        print(answer[3])
    return answer[3]


def set_rate(login, value):
    global vis, conn, cursor
    if vis:
        print("Setting new rate:" + str(rate) + " for user " + login)
    cursor.execute("UPDATE chess_players SET rate="+str(value)+" WHERE login='" + login + "';")


def update_rate(login_1, login_2, flag):
    global vis, conn, cursor
    if vis: 
        print("\n Updating users rate login_0=" +str(login_1) + " login_1=" + str(login_2)+ "...")
    
    cursor.execute("SELECT * FROM chess_players WHERE login = '" + login_1 + "';");
    user_1 = cursor.fetchone()
    
    cursor.execute("SELECT * FROM chess_players WHERE login = '" + login_2 + "';");
    user_2 = cursor.fetchone()
    
    K = 0
    if min(user_2[3], user_1[3]) > 2500:
        K = 10
    elif min(user_2[3], user_1[3]) > 2000:
        K = 20
    elif min(user_2[3], user_1[3]) > 1500:
        K = 30
    else:
        K = 40
    
    vin_1 = 0.5
    vin_2 = 0.5
    if flag == 1:
        vin_1 = 1
        vin_2 = 0
    elif flag == 2:
        vin_1 = 0
        vin_2 = 1
    value_1 = user_1[3] + K*((vin_1) - (1/(1+10**((user_2[3] - user_1[3])/400))))
    value_2 = user_2[3] + K*((vin_2) - (1/(1+10**((user_1[3] - user_2[3])/400))))
    
    if vis:
        print("New rate: ", value_1, value_2)
    
    set_rate(login_1, int(value_1)+1)
    set_rate(login_2, int(value_2)+1)
    
# init()
# add_move(472, "56-58" + ";")
# create_party('white', 'black', 5)
# get_last_move(id=476)
# get_last_move_number(id=476)
# get_party_figures(472)
# update_party_figures(472, "11,;21,black_knight;31,black_bishop;41,black_queen;51,black_knight;61,black_bishop;71,black_knight;81,black_rook;12,black_pawn;22,black_pawn;32,black_pawn;42,black_pawn;52,black_pawn;62,black_pawn;72,black_pawn;82,black_pawn;13,;23,;33,;43,;53,;63,;73,;83,;14,;24,;34,;44,;54,white_pawn;64,white_knight;74,;84,;15,;25,;35,;45,;55,;65,;75,;85,;16,;26,;36,;46,;56,;66,;76,;86,;17,white_pawn;27,white_pawn;37,white_pawn;47,white_pawn;57,;67,white_pawn;77,white_pawn;87,white_pawn;18,white_rook;28,white_knight;38,white_bishop;48,white_queen;58,white_king;68,white_bishop;78,;88,white_rook;")
# set_white(472, "zvs")
# set_black(472, "zvzvzs")
# get_white(472)
# get_black(472)
# check_user("ask")
# check_user_party(472, "zvzvzs")
# check_user_lp('ask', 'srt')
# check_flag(472, "zvzvzs")
# create_user()
# print_request()
# print("ANSWER: ", get_moves(533))
# cancel()


