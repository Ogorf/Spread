from Utils import *


class MainMenu:
    def __init__(self, screen):
        self.running = True
        self.screen = screen
        self.buttons = [
            Button("Singleplayer", (550, 100, 200, 50)),
            Button("Multiplayer", (550, 200, 200, 50)),
            Button("Map Editor", (550, 300, 200, 50)),
            Button("Laboratory", (550, 400, 200, 50)),
            Button("Quit", (550, 500, 200, 50))
            ]

    def draw(self):
        self.screen.fill(dark_blue)
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.update()

    def loop(self):
        while True:
            print(clock)                    # delete later
            clock.tick(fps)                 # delete later

            for event in pygame.event.get():
                # close window
                if event.type == pygame.QUIT:
                    return "Quit"

                if event.type == pygame.MOUSEBUTTONUP:
                    for button in self.buttons:
                        if pygame.Rect(button.rect).collidepoint(event.pos):
                            return button.name
            self.draw()



