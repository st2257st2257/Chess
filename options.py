# base setting
FPS = 5
""" частота обновления экрана """

screen_h_min = 0
screen_h_max = 500
screen_w_min = 0
screen_w_max = 500
""" настроцки положения экрана """

board_x = 50
board_y = 50
""" координаты левого верхнего края доски """

board_width = 400
board_height = board_width
""" ширина и высота доски """

game_mode = 0
""" режим игры: 0 - два игрокаб 1 - один игрок """

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
""" цвета для отображения на экране """

CF_width = board_width / 8
CF_height = board_width / 8
""" ширина и высота изображения шахматной фигуры на доске """
