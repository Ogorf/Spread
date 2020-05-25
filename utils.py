import pygame

pygame.init()

# window size
window_width = 1366
window_height = 768

font = pygame.font.SysFont("comincsans", 25)

fps = 100

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

dark_blue = (11, 11, 66)  # used for UI
dark_grey_bt = (35, 35, 65)    # used for UI
dim_grey_bt = (80, 80, 120)     # used for UI
dim_grey = (105, 105, 105)  # used for neutrals
grey = (128, 128, 128)  # used for neutrals
light_grey = (211, 211, 211)  # used for neutrals

colour_list = [brown, orange_red, light_coral, golden_rod, yellow_green, lime_green, cyan, medium_violet_red, chocolate]

colour_dict = {
    brown: (maroon, brown, crimson),
    orange_red: (red, orange_red, orange),
    light_coral: (indian_red, light_coral, light_salmon),
    golden_rod: (dark_golden_rod, golden_rod, gold),
    yellow_green: (olive, yellow_green, yellow),
    lime_green: (green, lime_green, lime),
    cyan: (dark_cyan, cyan, light_cyan),
    medium_violet_red: (dark_magenta, medium_violet_red, magenta),
    chocolate: (saddle_brown, chocolate, peru),
}


class Box:
    def __init__(self, rect, colour=dark_blue, edge_colour=dark_golden_rod):
        self.rect = rect
        self.colour = colour
        self.edge_colour = edge_colour

    def draw(self, screen):
        pygame.draw.rect(screen, self.edge_colour, (self.rect[0], self.rect[1], self.rect[2], self.rect[3]), 5)
        pygame.draw.rect(screen, self.colour, (self.rect[0] + 5, self.rect[1] + 5, self.rect[2] - 10, self.rect[3] - 10))


class Button:
    def __init__(self, name, rect,  colour=dim_grey, edge_colour=light_grey, active_colour=light_cyan, id=0):
        self.name = name
        self.rect = rect
        self.colour = colour
        self.edge_colour = edge_colour
        self.active_colour = active_colour
        self.active = False
        self.id = id

    def draw(self, screen):
        if not self.active:
            pygame.draw.rect(screen, self.edge_colour, (self.rect[0], self.rect[1], self.rect[2], self.rect[3]), 5)
            pygame.draw.rect(screen, self.colour, (self.rect[0] + 5, self.rect[1] + 5, self.rect[2] - 10, self.rect[3] - 10))
            text = font.render(self.name, 1, (255, 255, 255))
            screen.blit(text, (self.rect[0] + 8, self.rect[1] + self.rect[3] / 2 - 8))
        else:
            pygame.draw.rect(screen, self.edge_colour, (self.rect[0], self.rect[1], self.rect[2], self.rect[3]), 5)
            pygame.draw.rect(screen, self.active_colour, (self.rect[0] + 5, self.rect[1] + 5, self.rect[2] - 10, self.rect[3] - 10))
            text = font.render(self.name, 1, (0, 0, 0))
            screen.blit(text, (self.rect[0] + 8, self.rect[1] + self.rect[3] / 2 - 8))


class TextBox:
    def __init__(self, name, rect, text, letters=False, space=180, colour=grey, active_colour=(255, 255, 255), max_len=20):
        self.name = name
        self.rect = rect
        self.colour = colour
        self.active_colour = active_colour
        self.active = False
        self.text = str(text)
        self.letters = letters
        self.space = space
        self.max_len = max_len + 1

    def draw(self, window):
        if self.active:
            pygame.draw.rect(window, self.active_colour, self.rect)
        else:
            pygame.draw.rect(window, self.colour, self.rect)
        name = font.render(self.name, 1, (0, 0, 0))
        window.blit(name, (self.rect[0] - self.space, self.rect[1]))
        text = font.render(self.text, 1, (0, 0, 0))
        window.blit(text, (self.rect[0] + 5, self.rect[1] + 2))

    def add_text(self, key):
        if len(self.text) < self.max_len:
            if key in range(1073741913, 1073741922):
                key = int(key)
                key -= 1073741912
                text = list(self.text)
                text.append(str(key))
                self.text = "".join(text)
            elif key == 1073741922:
                text = list(self.text)
                text.append("0")
                self.text = "".join(text)
            elif key in range(48, 58):
                text = list(self.text)
                text.append(chr(key))
                self.text = "".join(text)
            elif key == 8:
                text = list(self.text)
                if text:
                    text = list(self.text)
                    text.pop()
                self.text = "".join(text)
            elif self.letters and key in range(pygame.K_a, pygame.K_z + 1):
                text = list(self.text)
                text.append(chr(key))
                self.text = "".join(text)


class MessageBox:
    def __init__(self, screen, text, font, rect=(window_width / 2 - 140, window_height / 2 - 50, 280, 100)):
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


class Writing:
    def __init__(self, text, xcord, ycord, size=25, colour=(0, 0, 0), wfont="comicsans",):
        self.text = text
        self.xcord = xcord
        self.ycord = ycord
        self.font = pygame.font.SysFont(wfont, size)
        self.colour = colour

    def draw(self, screen):
        text = font.render(self.text, 1, self.colour)
        screen.blit(text, (self.xcord, self.ycord))
