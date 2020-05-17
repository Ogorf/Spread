from utils import *
from pathlib import Path


# TODO: add cell where you can select profile colour

class Profile:

    def __init__(self, name: str, colour=(red, orange_red, orange)):
        self.name = name
        self.colour = colour

        p = Path('profiles')
        p = p / self.name / 'phages'
        p.mkdir(parents=True, exist_ok=True)


class ProfileMenu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = [
            Button("Menu", (window_width - 60, 0, 60, 30))
        ]
        self.box = []
        self.textbox = []

    def reset_buttons(self):
        self.box.clear()
        self.buttons.clear()
        self.textbox.clear()
        self.buttons.append(Button("Menu", (window_width - 60, 0, 60, 30)))

    def button_effect(self, name):
        if name == "Menu":
            self.box.clear()
            self.textbox.clear()
            self.buttons.clear()
            self.buttons.append(Button("Close menu", (window_width - 110, 0, 110, 30)))
            self.buttons.append(Button("new profile", (window_width - 110, 30, 110, 30)))
            self.buttons.append(Button("open profile", (window_width - 110, 60, 110, 30)))
            self.buttons.append(Button("Exit", (window_width - 110, 90, 110, 30)))
        elif name == "Close menu":
            self.reset_buttons()
        elif name == "new profile":
            self.reset_buttons()
            self.buttons.append(Button("create profile", (window_width/2 - 70, window_height/2 + 30, 140, 30)))
            self.buttons.append(Button("cancel", (window_width / 2 - 32, window_height / 2 + 70, 64, 30)))
            self.textbox.append(TextBox("name:", (window_width/2 - 50, window_height/2, 210, 20), "new", True, 100))
            self.box.append(Box((window_width/2 - 180, window_height/2 - 10, 360, 120)))
        elif name == "create profile":
            Profile(self.textbox[0].text)
            self.reset_buttons()
        elif name == "cancel":
            self.reset_buttons()

    def draw(self):
        self.screen.fill(dark_blue)
        for box in self.box:
            box.draw(self.screen)
        for button in self.buttons:
            button.draw(self.screen)
        for box in self.textbox:
            box.draw(self.screen)
        pygame.display.update()

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
                            else:
                                self.button_effect(button.name)
            self.draw()
