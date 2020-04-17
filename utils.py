import pygame

pygame.init()

font = pygame.font.SysFont("comincsans", 25)

# window size
window_width = 1300
window_height = 740

# colours
maroon = (128, 0, 0)
brown = (165, 42, 42)
crimson = (220, 20, 60)

red = (255, 0, 0)
orange_red = (255, 69, 0)
orange = (255, 165, 0)

indian_red = (205, 92, 92)
light_coral = (240, 128, 128)
light_salmon = (255, 160, 122)

dark_golden_rod = (184, 134, 11)
golden_rod = (218, 165, 32)
gold = (255, 215, 0)

olive = (128, 128, 0)
yellow_green = (154, 205, 50)
yellow = (255, 255, 0)

green = (0, 128, 0)
lime_green = (50, 205, 50)
lime = (0, 255, 0)

dark_cyan = (0, 139, 139)
cyan = (0, 255, 255)
light_cyan = (224, 255, 255)

dark_magenta = (139, 0, 139)
medium_violet_red = (199, 21, 133)
magenta = (255, 0, 255)

saddle_brown = (139, 69, 19)
chocolate = (210, 105, 30)
peru = (205, 133, 63)

dark_blue = (11, 11, 66)         # used for background
dim_grey = (105, 105, 105)       # used for neutrals
grey = (128, 128, 128)           # used for neutrals
light_grey = (211, 211, 211)     # used for neutrals

class MessageBox:
    _registry = []

    def __init__(self, screen, text, font, rect = (window_width / 2 - 140, window_height / 2 - 50, 280, 100)):
        self._registry.append(self)
        self.rect = rect
        self.screen = screen
        self.text = text
        self.font = font
        self.ok = (int(window_width / 2) - 25, int(window_height / 2) + 10, 50, 30)

    def draw(self, screen):
        pygame.draw.rect(screen, dark_golden_rod, self.rect, 5)
        pygame.draw.rect(screen, gold, (self.rect[0] + 5, self.rect[1] + 5, self.rect[2] - 10, self.rect[3] - 10))
        text = font.render(self.text, 1, (0, 0, 0))
        screen.blit(text, (self.rect[0] + 10, self.rect[1] + 10))
        pygame.draw.rect(screen, dark_golden_rod,
                         (self.ok[0] - 5, self.ok[1] - 5, self.ok[2] + 10, self.ok[3] + 10))
        pygame.draw.rect(screen, golden_rod, self.ok)
        ok = font.render("OK", 1, (0, 0, 0))
        screen.blit(ok, (self.ok[0] + 10, self.ok[1] + 7))
