from Utils import *
from Game import *
from SpreadClasses import Cell

background_img_path = 'img/background.PNG'


class Singleplayer:

    def __init__(self, screen, map_name="new", player_list=None):
        if player_list is None:
            player_list = Maps.player_list()
        self.map_name = map_name
        self.game = Game(Map.load(map_name), player_list)
        self.screen = screen
        self.buttons = [
            Button("Exit", (window_width - 60, 0, 60, 30))
        ]
        self.img = pygame.transform.scale(pygame.image.load(background_img_path).convert_alpha(), (
            int(math.sqrt(math.pow(window_width, 2) + math.pow(window_height, 2))),
            int(math.sqrt(math.pow(window_width, 2) + math.pow(window_height, 2)))))
        self.images = []
        for angle in range(90):
            self.images.append(pygame.transform.rotate(self.img, angle / 2))

    def draw(self, selected, angle):
        self.screen.blit(self.images[angle % 90], (window_width / 2 - int(self.images[angle % 90].get_width()) / 2,
                                                   window_height / 2 - int(self.images[angle % 90].get_height() / 2)))

        for obj in selected:
            pygame.draw.circle(self.screen, (255, 255, 255), obj.center, obj.radius + 4)

        for button in self.buttons:
            button.draw(self.screen)

        self.game.draw(self.screen)

        pygame.display.update()

    def reset(self):
        self.game = Game(Map.load(self.map_name), self.game.players)

    def loop(self):
        self.reset()
        selected = []
        angle = 0
        t_before_loop = pygame.time.get_ticks()

        while True:
            print(clock)  # delete later
            dt = clock.tick(fps)
            angle += (pygame.time.get_ticks() - t_before_loop) / 300000 + 0.15

            for event in pygame.event.get():

                # close window
                if event.type == pygame.QUIT:
                    return "Quit"

                # initiating attack/transfer
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for c in self.game.game_state.cells:
                        if math.hypot(pos[0] - c.center[0], pos[1] - c.center[1]) < c.radius:
                            self.game.order_attacks(selected, c)
                            break

                    for button in self.buttons:
                        if pygame.Rect(button.rect).collidepoint(event.pos):
                            if button.name == "Exit":
                                return "MainMenu"

            # selecting Cells
            if pygame.mouse.get_pressed():
                pos = pygame.mouse.get_pos()
                for c in self.game.game_state.cells:
                    if math.hypot(c.center[0] - pos[0], c.center[1] - pos[1]) < c.radius:
                        if c not in selected:  # add (later) and obj.player == p1
                            selected.append(c)

            if not pygame.mouse.get_pressed()[0]:
                selected.clear()

            self.game.tick(dt)

            self.draw(selected, int(angle))
