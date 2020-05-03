from SpreadClasses import Player
from Utils import *
from ManualTest import skilltree1, skilltree2


pygame.display.set_mode((window_width, window_height))

p0 = Player(0, "0", (dim_grey, grey, light_grey), 0.03) # id 0 stands for NeutralPlayer
p1 = Player(1, "1", (maroon, brown, peru), 0.12)
p2 = Player(2, "2", (olive, yellow_green, yellow), 0.4)
p3 = Player(3, "3", (indian_red, light_coral, light_salmon), 0.2)
p4 = Player(4, "4", (dark_magenta, medium_violet_red, magenta), 0.1)
p1.skilltree = skilltree1
p2.skilltree = skilltree2

def player_list():
    return [p0, p1, p2, p3, p4]
