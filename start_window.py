from visual_module import *
from windows import *

init()

start, username = start_window()
if start:
    main_menu(username)
quit()
