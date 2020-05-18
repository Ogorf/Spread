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


class OptionsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = [
            Button("Exit", (window_width - 60, 0, 60, 30)),
            Button("Video", (30, 100, 150, 50)),
            Button("Audio", (30, 200, 150, 50)),
            Button("Profile", (30, 300, 150, 50)),
            Button("Gameplay", (30, 400, 150, 50)),
        ]
        self.box = []
        self.textbox = []

    def reset_buttons(self):
        self.box.clear()
        self.buttons.clear()
        self.textbox.clear()
        self.buttons.append(Button("Exit", (window_width - 60, 0, 60, 30)))
        self.buttons.append(Button("Video", (30, 100, 150, 50)))
        self.buttons.append(Button("Audio", (30, 200, 150, 50)))
        self.buttons.append(Button("Profile", (30, 300, 150, 50)))
        self.buttons.append(Button("Gameplay", (30, 400, 150, 50)))
        for button in self.buttons:
            button.colour = gold


    def button_effect(self, button):
        if button.name == "Profile":
            self.reset_buttons()
            self.buttons.append(Button("new profile", (280, 10, 120, 30)))
            self.buttons.append(Button("open profile", (430, 10, 120, 30)))
        elif button.name == "Close menu":
            self.reset_buttons()
        elif button.name == "new profile":
            self.reset_buttons()
            self.buttons.append(Button("new profile", (280, 10, 120, 30)))
            self.buttons.append(Button("open profile", (430, 10, 120, 30)))
            self.buttons.append(Button("create profile", (window_width/2 - 70, window_height/2 + 30, 140, 30)))
            self.buttons.append(Button("cancel", (window_width / 2 - 32, window_height / 2 + 70, 64, 30)))
            self.textbox.append(TextBox("name:", (window_width/2 - 50, window_height/2, 210, 20), "new", True, 100))
            self.box.append(Box((window_width/2 - 180, window_height/2 - 10, 360, 120)))
        elif button.name == "create profile":
            Profile(self.textbox[0].text)
            self.reset_buttons()
        elif button.name == "cancel":
            self.reset_buttons()

    def draw(self):
        self.screen.fill(dim_grey_bt)
        pygame.draw.rect(self.screen, dark_grey_bt, (0, 0, 210, window_height))
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
                            else:
                                self.button_effect(button)
            self.draw()