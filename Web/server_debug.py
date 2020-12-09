import socket
import json
import sqlite3
from functions import *


init()
cancel()

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
print(9)
serv_sock.bind(('', 11111))
print(9)
serv_sock.listen(10)
print(9)

while True:
    # Бесконечно обрабатываем входящие подключения
    client_sock, client_addr = serv_sock.accept()
    print('Connected by', client_addr)

    while True:
        # Пока клиент не отключился, читаем передаваемые
        # им данные и отправляем их обратно
        """
        format:
        message(function_number, param_list)
        """
        try:
            data = json.loads(client_sock.recv(1024))
        except Exception:
            print("JSON Error")
            
        if not data:
            # Клиент отключился
            break
        print(data)
        
        """ decoding... """
        init()
        # 1:  add_move(472, "56-58" + ";")
        # 2:  create_party('white', 'black', 5)
        # 3:  get_last_move(id=476)
        # 4:  get_party_figures(472)
        # 5:  update_party_figures(472, "11,;21,black_knight;31,black_bishop;41,black_queen;51,black_knight;61,black_bishop;71,black_knight;81,black_rook;12,black_pawn;22,black_pawn;32,black_pawn;42,black_pawn;52,black_pawn;62,black_pawn;72,black_pawn;82,black_pawn;13,;23,;33,;43,;53,;63,;73,;83,;14,;24,;34,;44,;54,white_pawn;64,white_knight;74,;84,;15,;25,;35,;45,;55,;65,;75,;85,;16,;26,;36,;46,;56,;66,;76,;86,;17,white_pawn;27,white_pawn;37,white_pawn;47,white_pawn;57,;67,white_pawn;77,white_pawn;87,white_pawn;18,white_rook;28,white_knight;38,white_bishop;48,white_queen;58,white_king;68,white_bishop;78,;88,white_rook;")
        # 6:  set_white(472, "zvs")
        # 7:  set_black(472, "zvzvzs")
        # 8:  get_white(472)
        # 9:  get_black(472)
        # 10: check_user("ask")
        # 11: check_user_party(472, "zvzvzs")
        # 12: check_user_lp('ask', 'srt')
        # 13: check_flag(472, "zvzvzs")
        # 14: create_user()
        # 15: execute_sql(string)
        # 16: get_moves(472)
        
        function_number = data[0]
        param_list = data[1]
        res = None
        
        try: 
            if function_number == 1:
                res = add_move(param_list[0], param_list[1] + ";")
                
            elif function_number == 2:
                res = create_party(param_list[0], param_list[1], param_list[2])
                
            elif function_number == 3:
                res = get_last_move(param_list[0])
                
            elif function_number == 4:
                res = get_party_figures(param_list[0])
                
            elif function_number == 5:
                res = update_party_figures(param_list[0], param_list[1])
                
            elif function_number == 6:
                res = set_white(param_list[0], param_list[1])
                
            elif function_number == 7:
                res = set_black(param_list[0], param_list[1])
                
            elif function_number == 8:
                res = get_white(param_list[0])
                
            elif function_number == 9:
                res = get_black(param_list[0])
                
            elif function_number == 10:
                res = check_user(param_list[0])
                
            elif function_number == 11:
                res = check_user_party(param_list[0], param_list[1])
                
            elif function_number == 12:
                res = check_user_lp(param_list[0], param_list[1])
                
            elif function_number == 13:
                res = check_flag(param_list[0], param_list[1])
            
            elif function_number == 14:
                res = create_user(param_list[0], param_list[1])
                
            elif function_number == 15:
                res = execute_sql(param_list[0], param_list[1])
                
            elif function_number == 16:
                res = get_moves(param_list[0])
                
            elif function_number == 17:
                res = get_last_move_number(param_list[0])
                
                    
        except Exception:
            res = "Error in DB access"
            
        cancel()
        print()
        try:
            client_sock.send(json.dumps(res).encode())  # json.dumps(data).encode())
            break
        except Exception:
            client_sock.send(b'Error in JSON file')
            print("Error in JSON file")
            break

    client_sock.close()
