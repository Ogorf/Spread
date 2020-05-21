from utils import *
from pathlib import Path
import game
import spread_classes
import ai
import singleplayer


class SingleplayerMenu:
    def __init__(self, screen):  # add: profile, virus
        self.screen = screen
        self.map_name = ""
        self.buttons = [
            Button("Custom Game", (10, window_height - 50, 160, 40)),
            Button("Exit", (window_width - 60, 0, 60, 30))
        ]
        self.map_buttons = []
        self.player_buttons = []
        self.box = []
        self.writings = []

    def player_list(self):
        player_list = []
        colours = [(olive, yellow_green, yellow), (maroon, brown, peru), (indian_red, light_coral, light_salmon), (dark_magenta, medium_violet_red, magenta)]
        slots = game.Map.load(self.map_name).get_player_slots()
        if slots[0] == 0:
            player_list += [spread_classes.Player.neutral()]
            slots.remove(0)
        i = 0
        for button in self.player_buttons:
            if button.name == "Player":
                player_list += [spread_classes.Player(slots[i], str(i), colours[i], 0.5)]
            elif button.name == "AI":
                player_list += [ai.Basic(slots[i], str(i), colours[i], 0.5)]
            i += 1
        return player_list

    def draw(self):
        self.screen.fill(dark_grey_bt)
        for box in self.box:
            box.draw(self.screen)
        for button in self.buttons:
            button.draw(self.screen)
        for button in self.map_buttons:
            button.draw(self.screen)
        for button in self.player_buttons:
            button.draw(self.screen)
        for writing in self.writings:
            writing.draw(self.screen)
        pygame.display.update()

    def reset_buttons(self):
        self.box.clear()
        self.buttons.clear()
        self.map_buttons.clear()
        self.player_buttons.clear()
        self.writings.clear()
        self.buttons.append(Button("Exit", (window_width - 60, 0, 60, 30)))
        self.buttons.append(Button("Custom Game", (10, window_height - 50, 160, 40)))

    def button_effect(self, name):
        if name == "Custom Game":
            self.reset_buttons()
            height = 0
            entries = Path('maps/')
            for entry in entries.iterdir():
                self.map_buttons.append(
                    Button(entry.name[:-4], (20, window_height - 145 - height, 200, 30)))
                height += 40
            self.buttons.append(Button("cancel", (50, window_height - 100, 100, 30)))
            self.box.append(Box((10, window_height - height - 120, 240, max(height + 110, 200))))
        elif name == "cancel":
            self.reset_buttons()
            self.map_name = ""

    def map_button_effect(self, button):
        for b in self.map_buttons:
            b.active = False
        button.active = True
        self.map_name = button.name
        self.box[0] = Box((10, self.box[0].rect[1], 720, self.box[0].rect[3]))
        self.writings += [Writing("Players:", 280, self.box[0].rect[1] + 5, 30, (255, 255, 255))]
        height = 0
        self.player_buttons.clear()
        for slot_id in game.Map.load(self.map_name).get_player_slots():
            if slot_id != 0:
                self.player_buttons.append(Button("AI", (280, self.box[0].rect[1] + 35 + height, 100, 30)))
                height += 40
        if self.player_buttons:
            self.player_buttons[0].name = "Player"
        self.buttons.append(Button("Play", (400, window_height - 100, 70, 30)))

    @staticmethod
    def player_button_effect(button):
        if button.name == "Player":
            button.name = "AI"
        elif button.name == "AI":
            button.name = "Player"

    def loop(self):
        clock = pygame.time.Clock()
        while True:
            # print(clock)  # delete later
            clock.tick(fps)
            for event in pygame.event.get():

                # closes window
                if event.type == pygame.QUIT:
                    return "Quit"

                # triggers effect for clicked button
                if event.type == pygame.MOUSEBUTTONUP:
                    for button in self.buttons:
                        if pygame.Rect(button.rect).collidepoint(event.pos):
                            if button.name == "Exit":
                                return "MainMenu"
                            elif button.name == "Play" and self.map_name != "":
                                goto = singleplayer.Singleplayer(self.screen, self.map_name, self.player_list()).loop()
                                return goto
                            else:
                                self.button_effect(button.name)

                    for button in self.map_buttons:
                        if pygame.Rect(button.rect).collidepoint(event.pos):
                            self.map_button_effect(button)
                    for button in self.player_buttons:
                        if pygame.Rect(button.rect).collidepoint(event.pos):
                            self.player_button_effect(button)


            # activate buttons
            x, y = pygame.mouse.get_pos()
            for button in self.buttons:
                if pygame.Rect(button.rect).collidepoint(x, y):
                    button.active = True
                else:
                    button.active = False

            for button in filter(lambda x: x.name != self.map_name, self.map_buttons):
                if pygame.Rect(button.rect).collidepoint(x, y):
                    button.active = True
                else:
                    button.active = False

            for button in self.player_buttons:
                if pygame.Rect(button.rect).collidepoint(x, y):
                    button.active = True
                else:
                    button.active = False
            self.draw()
