import pygame
from pygame.draw import *
from game_objects import *
from show_part import *
from options import *
pygame.init()


screen = pygame.display.set_mode((screen_w_max, screen_h_max))

# files setting
data_file_name = "data_party.txt"
data_players = "data_players.txt"


# party settings
player_1 = Player(color="white", rate=2400)
player_2 = Player(color="black", rate=2500)

first_party = Party(player_1, player_2, "30min")


"""Настраиваем основные параметры"""
pygame.display.update()
clock = pygame.time.Clock()
finished = False

data = Party.create_party_fron_RGN(data_file_name)
print("data: ", data)
"""  создаём партию из нашего файла: нужно для того, чтобы расставить фигуры  """

base_font = pygame.font.Font(None, 32)


counter = 0
# индикатор этапов партии


def read_players(file_name):
    """
    1) считываем данные из файла
    2) разделяем строки по пробелу
    3) преобразуем строки в объекты типа Player по массиву
    4) возвращаем массив игроков
    """

    players_data = str(open(file_name, 'r')).split()
    return [Player(pl_i.split(",")) for pl_i in players_data]


def main():
    global counter, FPS, BLACK
    while finished == 0:
        """
        Рассматриваем разные этапы запуска программы:
        0) ввод имени первого пользователя
        1) проверка пользователя 1 в базе данных
        2) ввод имени второго пользователя
        3) проверка пользователя 2 в базе данных
        4) основной цикл отрисовки
        """
        p1_index = -1  # номер в массиве игроков первого игрока
        p2_index = -1  # номер в массиве игроков второго игрока
        if counter == 0:
            """(0) ввод имени player_1"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        """Обрабатываем удаление символа"""
                        player_1.name = player_1.name[:-1]
                    elif event.key == pygame.K_RETURN:
                        """Обрабатываем момент нажатия пользователем на кнопку ввода"""
                        counter += 1
                    else:
                        """Обрабатываем добавление символа в строку"""
                        player_1.name += event.unicode
            screen.fill((0, 0, 0))
            text_surface = base_font.render(player_1.name, 1, (255, 255, 255))
            general_text_surface = base_font.render("Enter name: ", 1, (255, 255, 255))

            screen.blit(text_surface, (250, 100))
            screen.blit(general_text_surface, (100, 100))

            pygame.display.flip()
            clock.tick(60)

        elif counter == 1:
            """(1) проверка пользователя player_2 в базе данных"""
            # check user in our data
            players_data = str(open(data_players, "r")).split()
            # FIXME: при считывании данных из файла берём все данные пользователя а нужны только имена
            # FIXME: добавить закрытие файла после взятия даных + ответить на вопрос что я вообще в этом модуле делаю
            try:
                """ проверяем наличие пользователя с заданным именем в базе данных """
                p1_index = players_data.index(player_1.name)
            except ValueError:
                """ если пользователя нет в базе, ставим ему последний индекс """
                p1_index = len(players_data)
            players_data.append(player_1.name)

            counter += 1

        elif counter == 2:
            """(2) ввод имени player_2"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        """Обрабатываем удаление символа"""
                        player_2.name = player_2.name[:-1]
                    elif event.key == pygame.K_RETURN:
                        """Обрабатываем момент нажатия пользователем на кнопку ввода"""
                        counter += 1
                    else:
                        """Обрабатываем добавление символа в строку"""
                        player_2.name += event.unicode
            screen.fill((0, 0, 0))
            text_surface = base_font.render(player_2.name, 1, (255, 255, 255))
            general_text_surface = base_font.render("Enter name: ", 1, (255, 255, 255))

            screen.blit(text_surface, (250, 100))
            screen.blit(general_text_surface, (100, 100))

            pygame.display.flip()
            clock.tick(60)

        elif counter == 3:
            """(3) проверка пользователя player_2 в базе данных"""
            # check user in our data
            players_data = str(open(data_players, "r")).split()
            # FIXME: при считывании данных из файла берём все данные пользователя а нужны только имена
            # FIXME: добавить закрытие файла после взятия даных + ответить на вопрос что я вообще в этом модуле делаю
            try:
                """ проверяем наличие пользователя с заданным именем в базе данных """
                p2_index = players_data.index(player_2.name)
            except ValueError:
                """ если пользователя нет в базе, ставим ему последний индекс """
                p2_index = len(players_data)
            players_data.append(player_2.name)

            counter += 1

        else:
            """(4) основной цикл отрисовки"""
            clock.tick(FPS)
            screen.fill((0, 0, 0))

            """Обрабатываем нажатия с клавиатуры"""
            for eevent in pygame.event.get():
                if eevent.type == pygame.QUIT:
                    pass
                elif eevent.type == pygame.MOUSEBUTTONDOWN:
                    print('Click! ', pygame.mouse.get_pos())
                    first_party.check_press(x=pygame.mouse.get_pos()[0], y=pygame.mouse.get_pos()[1])

            """ выводим доску """
            show_party(screen, first_party)

            pygame.display.update()
            screen.fill(BLACK)
            finished = first_party.indicator


print(first_party.print())
print("enter value: ")
iii = int(input())
pygame.quit()
"""
extra actions:
добавить матожидание выводом на экрон
добавить добавить возможные очки при проигрыше или выигрыше
добавить индикатор хода выводом на экран

добавить режим одного игрока:
вариант игры с компьютером 
вариант игры по онлайну

"""


if __name__ == '__main__':
    main()
