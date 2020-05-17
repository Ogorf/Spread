import pygame
import main_menu
import singleplayer
import map_editor
import skilltree
import multiplayer_client
import singleplayer_menu
import profile
from utils import *

# name window
pygame.display.set_caption("Spread")

# create the game window, size in utils.py
window = pygame.display.set_mode((window_width, window_height))

goto = "MainMenu"
running = True
while running:
    if goto == "MainMenu":
        goto = main_menu.MainMenu(window).loop()
    elif goto == "Singleplayer":
        goto = singleplayer_menu.SingleplayerMenu(window).loop()
    elif goto == "Multiplayer":
        goto = multiplayer_client.Multiplayer(window).loop()
    elif goto == "Map Editor":
        goto = map_editor.MapEditor(window).loop()
    elif goto == "Laboratory":
        goto = skilltree.SkilltreeMenu(window).skilltree_loop()
    elif goto[:2] == "SP":
        goto = singleplayer.Singleplayer(window, goto[2:]).loop()
    elif goto == "Profile":
        goto = profile.ProfileMenu(window).loop()
    elif goto == "Quit":
        running = False
