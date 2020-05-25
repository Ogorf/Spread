from utils import *
from pathlib import Path
import game
import spread_classes
import ai
import singleplayer
import options


class SingleplayerMenu:
    def __init__(self, screen):
        self.screen = screen
        self.map_name = ""
        self.selected_player_id = 0
        self.buttons = [
            Button("Custom Game", (10, window_height - 50, 160, 40)),
            Button("Exit", (window_width - 60, 0, 60, 30))
        ]
        self.map_buttons = []
        self.player_buttons = []
        self.phage_buttons = []
        self.load_phage_button = []
        self.box = []
        self.writings = []
        self.colour_box = []

    def colour_box_to_list(self):
        colours = []
        for box in self.colour_box:
            colours += [colour_dict[box.colour]]
        return colours

    def player_list(self):
        player_list = []
        colours = self.colour_box_to_list()
        slots = game.Map.load(self.map_name).get_player_slots()
        if slots[0] == 0:
            player_list += [spread_classes.Player.neutral()]
            slots.remove(0)
        i = 0
        for button in self.player_buttons:
            if button.name == "Player" or button.name == options.current_settings.profile_name:
                player_list += [spread_classes.Player(slots[i], str(i), colours[i], 0.2)]
            elif button.name == "AI":
                player_list += [ai.Basic(slots[i], str(i), colours[i], 0.3)]
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
        for box in self.colour_box:
            box.draw(self.screen)
        for button in self.phage_buttons:
            button.draw(self.screen)
        for button in self.load_phage_button:
            button.draw(self.screen)
        pygame.display.update()

    def reset_buttons(self):
        self.box.clear()
        self.buttons.clear()
        self.map_buttons.clear()
        self.player_buttons.clear()
        self.phage_buttons.clear()
        self.load_phage_button.clear()
        self.writings.clear()
        self.colour_box.clear()
        self.load_phage_button.clear()
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
        self.reset_buttons()
        self.button_effect("Custom Game")
        for b in self.map_buttons:
            b.active = False
        button.active = True
        self.map_name = button.name
        self.box[0] = Box((10, self.box[0].rect[1], 720, self.box[0].rect[3]))
        self.writings += [Writing("Players:", 280, self.box[0].rect[1] + 5, 30, (255, 255, 255))]
        height = 0
        colours = [orange_red, yellow_green, medium_violet_red, lime_green]
        for slot_id in game.Map.load(self.map_name).get_player_slots():
            if slot_id != 0:
                self.player_buttons.append(Button("AI", (280, self.box[0].rect[1] + 35 + height, 150, 30)))
                self.colour_box.append(Box((450, self.box[0].rect[1] + 35 + height, 30, 30), colours[slot_id - 1], (0, 0, 0)))
                self.phage_buttons.append(Button("None", (500, self.box[0].rect[1] + 35 + height, 150, 30), dim_grey, light_grey, light_cyan, slot_id))
                height += 40
        if self.player_buttons:
            self.player_buttons[0].name = options.current_settings.profile_name
        self.buttons.append(Button("Play", (400, window_height - 100, 70, 30)))

    def phage_button_effect(self, button):
        self.load_phage_button.clear()
        height = 0
        entries = Path('profiles/' + options.current_settings.profile_name + "/phages/")
        for entry in entries.iterdir():
            self.load_phage_button.append(Button(entry.name[:-4], (window_width / 2 - 100, window_height / 2 - 90 + height, 200, 30)))
            height += 40
        self.buttons.append(Button("ok", (window_width / 2 - 35, window_height / 2 - 90 + height, 70, 30)))
        self.box.append(Box((window_width / 2 - 110, window_height / 2 - 100, 220, height + 90), dim_grey))
        self.selected_player_id = button.id

    def load_phage_button(self, name):
        pass

    @staticmethod
    def player_button_effect(button):
        if button.name == "Player":
            button.name = "AI"
        elif button.name == "AI":
            button.name = "Player"

    @staticmethod
    def colour_box_effect(box):
        box.colour = colour_list[(colour_list.index(box.colour) + 1) % len(colour_list)]

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

                    for button in self.phage_buttons:
                        if pygame.Rect(button.rect).collidepoint(event.pos):
                            self.phage_button_effect(button)

                    for box in self.colour_box:
                        if pygame.Rect(box.rect).collidepoint(event.pos):
                            self.colour_box_effect(box)

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

            for button in self.phage_buttons:
                if pygame.Rect(button.rect).collidepoint(x, y):
                    button.active = True
                else:
                    button.active = False
            self.draw()
