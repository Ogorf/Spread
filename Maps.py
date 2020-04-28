from SpreadClasses import Player
from Utils import *
from ManualTest import skilltree1, skilltree2


pygame.display.set_mode((window_width, window_height))

p0 = Player("0", dim_grey, grey, light_grey, 0.03)
p1 = Player("1", maroon, brown, peru, 0.12)
p2 = Player("2", olive, yellow_green, yellow, 0.4)
p3 = Player("3", indian_red, light_coral, light_salmon, 0.2)
p4 = Player("4", dark_magenta, medium_violet_red, magenta, 0.1)
p1.skilltree = skilltree1
p2.skilltree = skilltree2


map_name = [
((888, 354), 100, p2, 0),
((644, 116), 54, p0, 0),
((1006, 102), 67, p4, 0),
((1220, 504), 39, p0, 0),
((96, 568), 37, p0, 0),
((120, 690), 38, p3, 0),
((366, 654), 39, p0, 0),
((100, 92), 59, p0, 0),
((80, 300), 50, p0, 0),
((1038, 672), 31, p0, 0),
((1258, 278), 74, p0, 0),
((388, 354), 100, p1, 0)]
