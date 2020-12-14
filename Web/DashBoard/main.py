# import pygame
import pygame
from numpy import pi
import numpy
import random
import socket
import sqlite3


conn = None
cursor = None
vis = 0


def init():
    global vis, conn, cursor
    conn = sqlite3.connect('example.db')
    if vis:
        print("...Start connection...")
    cursor = conn.cursor()

def cancel():
    global vis 
    conn.commit()
    conn.close()
    if vis:
        print("\n...End   connection...")


def get_users():
    global vis, conn, cursor
    cursor.execute("SELECT * FROM chess_players WHERE id = (SELECT MAX(id) FROM chess_players);");
    answer = cursor.fetchone()
    return str(answer[0])


def get_games():
    global vis, conn, cursor
    cursor.execute("SELECT * FROM chess WHERE id = (SELECT MAX(id) FROM chess);");
    answer = cursor.fetchone()
    return str(answer[0])


def get_request():
    return 5000 + 500*random.randint(0,10)


def get_ping():
    return random.randint(0,10)/5


def show_diagram(value, name, min_v, max_v, x, y, r, font_size = 12):
    
    new_font = pygame.font.SysFont('arial', font_size)
    angle = pi*int(value)/(max_v - min_v) 
    pygame.draw.arc(screen, WHITE,[x, y, r*2, r*2], 0, pi, 3)
    pygame.draw.line(screen, GREEN, [x + r, y + r], [x + r - r*numpy.cos(angle),
                                                y + r - r*numpy.sin(angle)], 5)
    text_1 = new_font.render(str(name) + ": " + str(value), False, (255, 255, 255))
    screen.blit(text_1, [x + r/2, y + r/2])
    text_2 = new_font.render(str((max_v-min_v)/2), False, (255, 255, 255))
    screen.blit(text_2, [x + 5*r/6, y - r/4])
    text_3 = new_font.render(str(min_v), False, (255, 255, 255))
    screen.blit(text_3, [x, y + 7*r/6])
    text_4 = new_font.render(str(max_v), False, (255, 255, 255))
    screen.blit(text_4, [x + r*2 - len(str(max_v)*5), y + 7*r/6])
    
    

# initialize game engine
pygame.init()
f2 = pygame.font.SysFont('arial', 24)
f3 = pygame.font.SysFont('arial', 36)
f1 = pygame.font.SysFont('arial', 12)
f4 = pygame.font.SysFont('arial', 30)
f5 = pygame.font.SysFont('arial', 18)




window_width=480
window_height=640

animation_increment=10
clock_tick_rate=20

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)


# Open a window
size = (window_width, window_height)
screen = pygame.display.set_mode(size)




# Set title to the window
pygame.display.set_caption("DASH BOARD")

dead=False

clock = pygame.time.Clock()
background_image = pygame.image.load("background_4").convert()


angle = pi/4
while(dead==False):
    init()
    # getting local IP
    a = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
    if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), 
    s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, 
    socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead = True
            
    b_b_image = pygame.image.load("b_1_1.jpg").convert()
    background = pygame.Surface((window_width-150, window_height-150))
    background.blit(b_b_image, [0, 0])
    
    
    
    adjusted_IP_text = f5.render("Adjusted IP: ", False, (255, 255, 255)) 
    adjusted_IP = f5.render("192.168.1.74", False, (255, 255, 255))
    real_IP_text = f5.render("   Real IP: ", False, (255, 255, 255))
    real_IP = f5.render(a, False, (255, 255, 255))
    background.blit(adjusted_IP, [150, 420])
    background.blit(real_IP, [150, 450])
    background.blit(adjusted_IP_text, [50, 420])
    background.blit(real_IP_text, [50, 450])
    
    
    # total users value
    text_u1 = f2.render("Total", False, (255, 255, 255))
    text_u2 = f2.render("Users: ", False, (255, 255, 255))
    text_g1 = f2.render("Total", False, (255, 255, 255))
    text_g2 = f2.render("Games: ", False, (255, 255, 255))
    
    background.blit(text_u1, [10, 10])
    background.blit(text_u2, [10, 30])
    text_value_u = f3.render(str(get_users()), False, (255, 255, 255))
    background.blit(text_value_u, [80, 20])
    
    # total games value
    background.blit(text_g1, [190, 10])
    background.blit(text_g2, [190, 30])
    text_value_u = f3.render(str(get_games()), False, (255, 255, 255))
    background.blit(text_value_u, [270, 20])
    
    
    screen.blit(background_image, [0, 0])
    screen.blit(background, [75, 75])
    pygame.draw.rect(screen, BLACK, [75, 75, window_width-150 , window_height-150], 3)
    
    # boards
    show_diagram(get_request(), "Requests", 0, 100000, 150, 250, 100, 18)
    show_diagram(get_ping(), "Ping", 0, 5, 270, 400, 50, 12)
    show_diagram(get_games(), "Party", 0, 1000, 120, 400, 50, 12)
    
    
    pygame.display.flip()
    clock.tick(clock_tick_rate)
    cancel()
