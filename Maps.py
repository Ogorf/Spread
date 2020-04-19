from SpreadClasses import Cell
from SpreadClasses import Player
from Utils import *

pygame.display.set_mode((window_width, window_height))

p0 = Player("0", dim_grey, grey, light_grey, 0.03, 20)
p1 = Player("1", maroon, brown, peru, 0.12, 30)
p2 = Player("2", olive, yellow_green, yellow, 0.4, 70)
p3 = Player("3", indian_red, light_coral, light_salmon, 0.2, 0)
p4 = Player("4", dark_magenta, medium_violet_red, magenta, 0.1, 10)

map_name = [
    Cell((536, 126), 94, p2, 44),
    Cell((1090, 140), 82, p3, 0),
    Cell((792, 382), 92, p0, 0),
    Cell((826, 122), 44, p0, 0),
    Cell((482, 650), 58, p0, 0),
    Cell((1190, 590), 95, p4, 22),
    Cell((128, 66), 65, p0, 0),
    Cell((110, 662), 49, p0, 0),
    Cell((192, 392), 94, p1, 22)]
