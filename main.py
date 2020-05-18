import main_menu
import singleplayer
import map_editor
import skilltree
import multiplayer_client
import singleplayer_menu
import profile
import options
from utils import *


class Spread:
    pygame.display.set_caption("Spread")

    def __init__(self):
        self.window = pygame.display.set_mode((window_width, window_height))

    def loop(self):
        goto = "MainMenu"
        running = True
        while running:
            if goto == "MainMenu":
                goto = main_menu.MainMenu(self.window).loop()
            elif goto == "Singleplayer":
                goto = singleplayer_menu.SingleplayerMenu(self.window).loop()
            elif goto == "Multiplayer":
                goto = multiplayer_client.Multiplayer(self.window).loop()
            elif goto == "Map Editor":
                goto = map_editor.MapEditor(self.window).loop()
            elif goto == "Laboratory":
                goto = skilltree.SkilltreeMenu(self.window).skilltree_loop()
            elif goto[:2] == "SP":
                goto = singleplayer.Singleplayer(self.window, goto[2:]).loop()
            elif goto == "Options":
                goto = options.OptionsMenu(self.window).loop()
            elif goto == "Quit":
                running = False


Spread().loop()
