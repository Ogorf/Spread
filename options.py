from utils import *
from pathlib import Path
import skilltree


class Settings:
    def __init__(self, profile_name="Username"):
        self.profile_name = profile_name

    def switch_profile(self, profile_name):
        self.profile_name = Profile.load(profile_name)[0]


current_settings = Settings("frogo")


class Profile:
    profile_dir = "profiles/"

    def __init__(self, name: str):
        self.name = name
        self.phage = skilltree.empty()

        p = Path('profiles')
        p = p / self.name / 'phages'
        p.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def load(profile_name):
        entries = Path('profiles/')
        for entry in entries.iterdir():
            if entry.name == profile_name:
                return [entry.name]             # In diese Liste kommen alle Profil abhängigen parameter (name, lvl, progress, achievements...)

class OptionsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.selected_profile_name = ""
        self.buttons = [
            Button("Exit", (window_width - 60, 0, 60, 30)),
            Button("Video", (30, 100, 150, 50)),
            Button("Audio", (30, 200, 150, 50)),
            Button("Profile", (30, 300, 150, 50)),
            Button("Gameplay", (30, 400, 150, 50)),
        ]
        self.box = []
        self.textbox = []
        self.profile_buttons = []
        self.load_profile_buttons = []

    def reset_buttons(self):
        self.box.clear()
        self.textbox.clear()
        self.profile_buttons.clear()
        self.load_profile_buttons.clear()

    def button_effect(self, button):
        if button.name == "Profile":
            self.reset_buttons()
            self.profile_buttons.append(Button("new profile", (280, 10, 120, 30)))
            self.profile_buttons.append(Button("open profile", (430, 10, 120, 30)))
        elif button.name == "Video":
            self.reset_buttons()
        elif button.name == "Audio":
            self.reset_buttons()
        elif button.name == "Gameplay":
            self.reset_buttons()

    def profile_button_effect(self, button):
        if button.name == "new profile":
            self.reset_buttons()
            self.profile_buttons.append(Button("new profile", (280, 10, 120, 30)))
            self.profile_buttons.append(Button("open profile", (430, 10, 120, 30)))
            self.profile_buttons.append(Button("create profile", (window_width / 2 - 70, window_height / 2 + 30, 140, 30)))
            self.profile_buttons.append(Button("cancel", (window_width / 2 - 32, window_height / 2 + 70, 64, 30)))
            self.textbox.append(TextBox("name:", (window_width / 2 - 50, window_height / 2, 210, 20), "new", True, 100))
            self.box.append(Box((window_width / 2 - 180, window_height / 2 - 10, 360, 120)))
        elif button.name == "create profile":
            Profile(self.textbox[0].text)
            self.reset_buttons()
            self.profile_buttons.append(Button("new profile", (280, 10, 120, 30)))
            self.profile_buttons.append(Button("open profile", (430, 10, 120, 30)))
        elif button.name == "open profile":
            self.reset_buttons()
            self.profile_buttons.append(Button("new profile", (280, 10, 120, 30)))
            self.profile_buttons.append(Button("open profile", (430, 10, 120, 30)))
            height = 0
            entries = Path('profiles/')
            for entry in entries.iterdir():
                self.load_profile_buttons.append(Button(entry.name, (window_width / 2 - 100, window_height / 2 - 90 + height, 200, 30)))
                height += 40
            self.profile_buttons.append(Button("ok", (window_width / 2 - 23, window_height / 2 - 90 + height, 46, 30)))
            self.box.append(Box((window_width / 2 - 110, window_height / 2 - 100, 220, height + 50), dim_grey))
        elif button.name == "cancel":
            self.reset_buttons()
            self.profile_buttons.append(Button("new profile", (280, 10, 120, 30)))
            self.profile_buttons.append(Button("open profile", (430, 10, 120, 30)))
        elif button.name == "ok":
            self.reset_buttons()
            self.profile_buttons.append(Button("new profile", (280, 10, 120, 30)))
            self.profile_buttons.append(Button("open profile", (430, 10, 120, 30)))

    def load_profile_button_effect(self):
        return

    def draw(self):
        self.screen.fill(dim_grey_bt)
        pygame.draw.rect(self.screen, dark_grey_bt, (0, 0, 210, window_height))
        for box in self.box:
            box.draw(self.screen)
        for button in self.buttons:
            button.draw(self.screen)
        for box in self.textbox:
            box.draw(self.screen)
        for button in self.profile_buttons:
            button.draw(self.screen)
        for button in self.load_profile_buttons:
            button.draw(self.screen)
        pygame.display.update()

    def loop(self):
        clock = pygame.time.Clock()
        while True:
            #print(clock)  # delete later
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
                    # activates textboxes
                    for box in self.textbox:
                        if pygame.Rect(box.rect).collidepoint(event.pos):
                            box.active = True
                            box.text = ""
                        else:
                            box.active = False

                    for button in self.profile_buttons:
                        if pygame.Rect(button.rect).collidepoint(event.pos):
                            self.profile_button_effect(button)

                # writes in active textbox
                if event.type == pygame.KEYDOWN:
                    for box in self.textbox:
                        if box.active:
                            box.add_text(event.key)

            # activate buttons
            x, y = pygame.mouse.get_pos()
            for button in self.buttons:
                if pygame.Rect(button.rect).collidepoint(x, y):
                    button.active = True
                else:
                    button.active = False

            for button in self.profile_buttons:
                if pygame.Rect(button.rect).collidepoint(x, y):
                    button.active = True
                else:
                    button.active = False

            for button in filter(lambda x: x.name != self.selected_profile_name, self.load_profile_buttons):
                if pygame.Rect(button.rect).collidepoint(x, y):
                    button.active = True
                else:
                    button.active = False

            self.draw()
