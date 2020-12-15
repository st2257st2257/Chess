import socket
import json
import sqlite3
from functions import *
import datetime

init()
cancel()

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
print(9)
serv_sock.bind(('', 11111))
print(9)
serv_sock.listen(10)
print(9)
vis = 0


while True:
    # Бесконечно обрабатываем входящие подключения
    client_sock, client_addr = serv_sock.accept()
    if vis:
        print('Connected by', client_addr)
    current_time = datetime.datetime.now()
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
        if vis:
            print(data)
        
        """ decoding... """
        init()

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
            
        try:
            print_request(str(client_addr[0]), str(data).split("'"), res,
                          datetime.datetime.now() - current_time) 
        except Exception:
            print("Printing Error")
        
        cancel()
        try:
            client_sock.send(json.dumps(res).encode())  # json.dumps(data).encode())
            break
        except Exception:
            client_sock.send(b'Error in JSON file')
            print("Error in JSON file")
            break

    client_sock.close()
