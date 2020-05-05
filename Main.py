from MainMenu import *
from Singleplayer import *
from MapEditor import *
from SkillTree import *
from MultiplayerClient import *

# name window
pygame.display.set_caption("Spread")

# create the game window, size in utils.py
window = pygame.display.set_mode((window_width, window_height))

goto = "MainMenu"
running = True
while running:
    if goto == "MainMenu":
        goto = MainMenu(window).loop()
    elif goto == "Singleplayer":
        goto = Singleplayer(window).loop()
    elif goto == "Multiplayer":
        goto = Multiplayer(window).loop()
    elif goto == "Map Editor":
        goto = MapEditor(window).loop()
    elif goto == "Laboratory":
        goto = skilltree_loop(window)
    elif goto == "Quit":
        running = False
