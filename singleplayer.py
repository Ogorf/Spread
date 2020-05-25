from utils import *
from game import *

background_img_path = 'img/background.PNG'


class Singleplayer:
    def __init__(self, screen, map_name, player_list):
        self.player_list = player_list
        self.map_name = map_name
        self.game = Game(Map.load(map_name), self.player_list)
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
        for button in self.buttons:
            button.draw(self.screen)
        for obj in selected:
            pygame.draw.circle(self.screen, (255, 255, 255), obj.center, obj.radius + 6)

        self.game.draw(self.screen)

        pygame.display.update()

    def reset(self):
        self.game = Game(Map.load(self.map_name), self.game.players)

    def loop(self):
        self.reset()
        selected = []
        angle = 0
        t_before_loop = pygame.time.get_ticks()
        clock = pygame.time.Clock()

        while True:
            print(clock)  # delete later
            dt = clock.tick(fps)
            time = pygame.time.get_ticks() - t_before_loop
            angle += time / 300000 + 0.2

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
                                return "Singleplayer"

            # initiating AI orders
            for player in filter(lambda x: x.isAI, self.player_list):
                if player.order(self.game.game_state, time):
                    cell1, cell2 = player.order(self.game.game_state, time)
                    self.game.order_attacks(cell1, cell2)

            # selecting Cells
            if pygame.mouse.get_pressed():
                pos = pygame.mouse.get_pos()
                for c in self.game.game_state.cells:
                    if math.hypot(c.center[0] - pos[0], c.center[1] - pos[1]) < c.radius:
                        if c not in selected:  # add (later) and c.player == p1
                            selected.append(c)

            if not pygame.mouse.get_pressed()[0]:
                selected.clear()

            # activate buttons
            x, y = pygame.mouse.get_pos()
            for button in self.buttons:
                if pygame.Rect(button.rect).collidepoint(x, y):
                    button.active = True
                else:
                    button.active = False

            self.game.tick(dt)

            self.draw(selected, int(angle))
