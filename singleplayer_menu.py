from utils import *
from pathlib import Path


class SingleplayerMenu:
    def __init__(self, screen):  # add: profile, virus
        self.screen = screen
        self.map_name = ""
        self.buttons = [
            Button("Custom Game", (10, window_height - 50, 160, 40)),
            Button("Exit", (window_width - 60, 0, 60, 30))
        ]
        self.map_buttons = []
        self.box = []

    def draw(self):
        self.screen.fill(dark_blue)
        for box in self.box:
            box.draw(self.screen)
        for button in self.buttons:
            button.draw(self.screen)
        for button in self.map_buttons:
            button.draw(self.screen)
        pygame.display.update()

    def reset_buttons(self):
        self.box.clear()
        self.buttons.clear()
        self.map_buttons.clear()
        self.buttons.append(Button("Exit", (window_width - 60, 0, 60, 30)))
        self.buttons.append(Button("Custom Game", (10, window_height - 50, 160, 40)))

    def button_effect(self, name):
        if name == "Custom Game":
            self.reset_buttons()
            height = 0
            entries = Path('maps/')
            for entry in entries.iterdir():
                self.map_buttons.append(
                    Button(entry.name[:-4], (window_width / 2 - 100, window_height / 2 - 120 + height, 200, 30)))
                height += 40
            self.buttons.append(Button("load", (window_width / 2 - 35, window_height / 2 - 120 + height, 70, 30)))
            self.buttons.append(Button("cancel", (window_width / 2 - 35, window_height / 2 - 90 + height, 70, 30)))
            self.box.append(Box((window_width / 2 - 110, window_height / 2 - 140, 220, height + 100), dim_grey))
        elif name == "cancel":
            self.reset_buttons()

    def map_button_effect(self, button):
        for map_button in self.map_buttons:
            map_button.colour = gold
        button.colour = yellow
        self.map_name = button.name

    def loop(self):
        clock = pygame.time.Clock()
        while True:
            print(clock)  # delete later
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
                            elif button.name == "load" and self.map_name != "":
                                return "SP" + self.map_name
                            else:
                                self.button_effect(button.name)

                    for button in self.map_buttons:
                        if pygame.Rect(button.rect).collidepoint(event.pos):
                            self.map_button_effect(button)
            self.draw()
