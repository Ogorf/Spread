import math
from utils import *

pygame.init()

img_path = 'img/cell1.png'

# classes for gameloop ------------------------------------------------------------------------------------------------
class Player:
    _registry = []

    def __init__(self, name, cell_colour, pop_colour, core_colour, velocity, startpop):
        self._registry.append(self)
        self.name = name
        self.cell_colour = cell_colour
        self.pop_colour = pop_colour
        self.core_colour = core_colour
        self.velocity = velocity
        self.startpop = startpop


class Bubble:
    _registry = []

    def __init__(self, destination, mother):
        self._registry.append(self)
        self.xcord = mother.xcord
        self.ycord = mother.ycord
        self.radius = int(math.sqrt(mother.population / 2) * 10)
        self.colour = mother.core_colour
        self.destination = destination
        self.velocity = mother.velocity
        self.player = mother.player
        self.population = int(mother.population / 2)
        self.mother = mother

    def move(self):
        radians = math.atan2(self.destination[1] - self.ycord, self.destination[0] - self.xcord)
        direction = (math.cos(radians), math.sin(radians))
        distance = math.hypot(self.xcord - self.destination[0], self.ycord - self.destination[1])
        if distance > self.velocity:
            self.xcord += direction[0] * self.velocity
            self.ycord += direction[1] * self.velocity

    def draw(self, window):
        pygame.draw.circle(window, self.colour, [int(self.xcord), int(self.ycord)], self.radius)

    def delete(self):
        self._registry.remove(self)
        del self


class Cell:
    _registry = []


    def __init__(self, center, radius, player, population, img_path = img_path):
        self._registry.append(self)
        self.img = pygame.transform.scale(pygame.image.load(img_path).convert_alpha(), (radius*2, radius*2))
        self.xcord = center[0]
        self.ycord = center[1]
        self.radius = radius
        self.cell_colour = player.cell_colour
        self.pop_colour = player.pop_colour
        self.core_colour = player.core_colour
        self.velocity = player.velocity
        self.player = player
        self.population = population
        self.counter = 0               # counts the amount of times the cell grew
        self.capacity = int(pow(radius, 2) / 100)

    def attack(self, enemypos):
        Bubble(enemypos, self)
        self.population = math.ceil(self.population / 2)

    def draw(self, window):
        pygame.draw.circle(window, self.cell_colour, (int(self.xcord), int(self.ycord)), self.radius)
        pygame.draw.circle(window, self.pop_colour, (int(self.xcord), int(self.ycord)),
                           int(math.sqrt(self.population) * 10))
        if self.pop_colour != grey:                                         # checks if player is neutral
            pygame.draw.circle(window, self.core_colour, [int(self.xcord), int(self.ycord)],
                               int(math.sqrt(self.population / 2) * 10))
        window.blit(self.img, (self.xcord-self.radius, self.ycord-self.radius))

    def grow(self, current_time):
        if self.population > self.capacity:
            self.population = self.capacity
        if current_time > 50000 * self.counter / self.radius:
            self.counter += 1
            if self.population < self.capacity and self.pop_colour != grey:  # last condition checks if player is neutral
                self.population += 1

    def switch_player(self, new_player):
        self.player = new_player
        self.cell_colour = new_player.cell_colour
        self.pop_colour = new_player.pop_colour
        self.core_colour = new_player.core_colour
        self.velocity = new_player.velocity

    def blow(self):
        enough_space = True
        for cell in filter(lambda x: x != self, Cell._registry):
            if math.hypot(self.xcord - cell.xcord, self.ycord - cell.ycord) < cell.radius + self.radius + 5:
                enough_space = False
        if enough_space:
            self.radius += 1


# classes for mapeditor ---------------------------------------------------------------------------------------------
class AdjustRect:
    _registry = []

    def __init__(self, rect, cell):
        self._registry.append(self)
        self.rect = rect
        TextBox("X-Coordinate: ", (rect[0] + rect[3] - 170, rect[1] + 20, 70, 20), cell.xcord, grey, (255, 255, 255))
        TextBox("Y-Coordinate: ", (rect[0] + rect[3] - 170, rect[1] + 60, 70, 20), cell.ycord, grey, (255, 255, 255))
        TextBox("Radius: (0 to remove)", (rect[0] + rect[3] - 170, rect[1] + 100, 70, 20), cell.radius, grey, (255, 255, 255))
        TextBox("Player: ", (rect[0] + rect[3] - 170, rect[1] + 140, 70, 20), cell.player.name, grey, (255, 255, 255))
        TextBox("Population: ", (rect[0] + rect[3] - 170, rect[1] + 180, 70, 20), cell.population, grey, (255, 255, 255))
        EditorButton("OK", (rect[0] + 150, rect[1] + 360, 50, 30), golden_rod, dark_golden_rod)

    def draw(self, window):
        pygame.draw.rect(window, dark_golden_rod, self.rect, 5)
        pygame.draw.rect(window, gold, (self.rect[0] + 5, self.rect[1] + 5, self.rect[2] - 10, self.rect[3] - 10))


class TextBox:
    _registry = []

    def __init__(self, name, rect, text, colour, active_colour):
        self._registry.append(self)
        self.name = name
        self.rect = rect
        self.colour = colour
        self.active_colour = active_colour
        self.active = False
        self.text = str(text)

    def draw(self, window):
        if self.active:
            pygame.draw.rect(window, self.active_colour, self.rect)
        else:
            pygame.draw.rect(window, self.colour, self.rect)
        font = pygame.font.SysFont("comincsans", 25)
        name = font.render(self.name, 1, (0, 0, 0))
        window.blit(name, (self.rect[0] - 180, self.rect[1]))
        text = font.render(self.text, 1, (0, 0, 0))
        window.blit(text, (self.rect[0] + 5, self.rect[1] + 2))

    def add_text(self, key):
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


class EditorButton:
    _registry = []

    def __init__(self, name, rect, colour, edge_colour):
        self._registry.append(self)
        self.name = name
        self.rect = rect
        self.colour = colour
        self.edge_colour = edge_colour

    def effect(self):
        AdjustRect._registry.clear()
        EditorButton._registry.clear()
        TextBox._registry.clear()

    def draw(self, window):
        pygame.draw.rect(window, self.edge_colour, (self.rect[0] - 5, self.rect[1] - 5, self.rect[2] + 10, self.rect[3] + 10))
        pygame.draw.rect(window, self.colour, self.rect)
        font = pygame.font.SysFont("comincsans", 25)
        text = font.render(self.name, 1, (0, 0, 0))
        window.blit(text, (self.rect[0] + 10, self.rect[1] + 7))


# classes for main menu -----------------------------------------------------------------------------------------------
class MainButton:
    _registry = []

    def __init__(self, name, xcord, ycord, width, height):
        self._registry.append(self)
        self.name = name
        self.xcord = xcord
        self.ycord = ycord
        self.width = width
        self.height = height

    def draw(self, window):
        pygame.draw.rect(window, dark_golden_rod, (self.xcord, self.ycord, self.width, self.height), 5)
        pygame.draw.rect(window, gold, (self.xcord + 5, self.ycord + 5, self.width - 10, self.height - 10))
        font = pygame.font.SysFont("comincsans", 40)
        text = font.render(self.name, 1, (0, 0, 0))
        window.blit(text, (self.xcord + 8, self.ycord + 12))

