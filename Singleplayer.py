from Utils import *
from Maps import map_name
from Game import *


class Singleplayer:

    def __init__(self, screen):
        self.cells = map_name[:]
        self.game = Game(self.cells)
        self.screen = screen
        self.buttons = [
            Button("Exit", (window_width - 60, 0, 60, 30))
        ]

    def draw(self, selected):
        self.screen.fill(dark_blue)

        for obj in selected:
            pygame.draw.circle(self.screen, (255, 255, 255), (obj.xcord, obj.ycord), obj.radius + 2)

        for button in self.buttons:
            button.draw(self.screen)

        self.game.draw(self.screen)

        pygame.display.update()

    def loop(self):

        time_before_loop = pygame.time.get_ticks()
        selected = []

        while True:
            print(clock)                # delete later
            dt = clock.tick(fps)

            for event in pygame.event.get():

                # close window
                if event.type == pygame.QUIT:
                    return "Quit"

                # initiating attack/transfer
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for c in self.cells:
                        if math.hypot(pos[0] - c.xcord, pos[1] - c.ycord) < c.radius:
                            self.game.order_attacks(selected, c)
                            break

                    for button in self.buttons:
                        if pygame.Rect(button.rect).collidepoint(event.pos):
                            if button.name == "Exit":
                                return "MainMenu"

            # selecting Cells
            if pygame.mouse.get_pressed():
                pos = pygame.mouse.get_pos()
                for c in self.cells:
                    if math.hypot(c.xcord - pos[0], c.ycord - pos[1]) < c.radius:
                        if c not in selected:           # add (later) and obj.player == p1
                            selected.append(c)

            if not pygame.mouse.get_pressed()[0]:
                selected.clear()

            self.game.tick(dt, pygame.time.get_ticks() - time_before_loop)

            self.draw(selected)