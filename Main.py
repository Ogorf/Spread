from MainMenu import *
from Singleplayer import *

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
    elif goto == "Mapeditor":
        goto = Mapeditor(window).loop()
    elif goto == "Laboratory":
        goto = Laboratory(window).loop()
    elif goto == "Quit":
        running = False
