from spread_classes import Player
from utils import *
import skilltree
import ai


pygame.display.set_mode((window_width, window_height))

p0 = Player(0, "0", (dim_grey, grey, light_grey), 0.03)      # id 0 stands for NeutralPlayer
p1 = ai.Basic(1, "1", (olive, yellow_green, yellow), 1)
p2 = ai.Basic(2, "2", (maroon, brown, peru), 0.3)
p3 = ai.Basic(3, "3", (indian_red, light_coral, light_salmon), 0.3)
p4 = ai.Basic(4, "4", (dark_magenta, medium_violet_red, magenta), 0.1)

#p1.skilltree = SkillTree.SkillTree.load("firstphage")

def player_list():
    return [p0, p1, p2, p3, p4]
