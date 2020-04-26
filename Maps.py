from SpreadClasses import Player
from Utils import *
import SkillTree

pygame.display.set_mode((window_width, window_height))

p0 = Player("0", dim_grey, grey, light_grey, 0.03, 20)
p1 = Player("1", maroon, brown, peru, 0.12, 30)
p2 = Player("2", olive, yellow_green, yellow, 0.4, 70)
p3 = Player("3", indian_red, light_coral, light_salmon, 0.2, 0)
p4 = Player("4", dark_magenta, medium_violet_red, magenta, 0.1, 10)
p1.skilltree = SkillTree.empty()



map_name = [
((640, 344), 55, p1, 30),
((894, 376), 76, p0, 0),
((858, 542), 80, p0, 0),
((1040, 110), 95, p4, 55),
((484, 178), 58, p0, 0),
((268, 106), 61, p0, 0),
((328, 188), 20, p0, 0),
((618, 556), 57, p0, 0),
((1214, 686), 62, p0, 0),
((296, 444), 136, p2, 33)]

