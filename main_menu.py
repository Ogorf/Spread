from utils import *


class MainMenu:
    def __init__(self, screen):
        self.running = True
        self.screen = screen
        self.buttons = [
            Button("Singleplayer", (window_width/2 - 100, 100, 200, 50)),
            Button("Multiplayer", (window_width/2 - 100, 200, 200, 50)),
            Button("Map Editor", (window_width/2 - 100, 300, 200, 50)),
            Button("Laboratory", (window_width/2 - 100, 400, 200, 50)),
            Button("Options", (window_width/2 - 100, 500, 200, 50)),
            Button("Quit", (window_width/2 - 100, 600, 200, 50))
            ]

    def draw(self):
        self.screen.fill(dark_grey_bt)
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.update()

    def loop(self):
        clock = pygame.time.Clock()
        while True:
            print(clock)                    # delete later
            clock.tick(fps)

            for event in pygame.event.get():
                # close window
                if event.type == pygame.QUIT:
                    return "Quit"

                if event.type == pygame.MOUSEBUTTONUP:
                    for button in self.buttons:
                        if pygame.Rect(button.rect).collidepoint(event.pos):
                            return button.name
            self.draw()



