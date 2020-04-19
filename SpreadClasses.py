from Utils import *

pygame.init()

img_path = 'img/cell1.png'


class Player:

    def __init__(self, name, cell_colour, pop_colour, core_colour, velocity, startpop):
        self.name = name
        self.cell_colour = cell_colour
        self.pop_colour = pop_colour
        self.core_colour = core_colour
        self.velocity = velocity
        self.startpop = startpop


class Bubble:

    def __init__(self, destination, mother):
        self.xcord = mother.xcord
        self.ycord = mother.ycord
        self.radius = int(math.sqrt(mother.population) * 10)
        self.colour = mother.core_colour
        self.destination = destination
        self.velocity = mother.velocity
        self.player = mother.player
        self.population = int(mother.population)
        self.mother = mother

    def move(self, dt):
        radians = math.atan2(self.destination[1] - self.ycord, self.destination[0] - self.xcord)
        direction = (math.cos(radians), math.sin(radians))
        distance = math.hypot(self.xcord - self.destination[0], self.ycord - self.destination[1])
        if distance > self.velocity * dt:
            self.xcord += direction[0] * self.velocity * dt
            self.ycord += direction[1] * self.velocity * dt

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.xcord), int(self.ycord)), self.radius)

    def collide(bubble, cell):
        if bubble.player == cell.player:
            cell.population += bubble.population
        else:
            if cell.population >= bubble.population:
                cell.population -= bubble.population
            else:
                cell.population = bubble.population - cell.population
                cell.switch_player(bubble.player)


class Cell:

    def __init__(self, center, radius, player, population, img_path=img_path):
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
        self.img = pygame.transform.scale(pygame.image.load(img_path).convert_alpha(), (radius * 2, radius * 2))

    def attack(self, enemypos):
        self.population = math.ceil(self.population / 2)
        return Bubble(enemypos, self)

    def draw(self, window):
        pygame.draw.circle(window, self.cell_colour, (int(self.xcord), int(self.ycord)), self.radius)
        pygame.draw.circle(window, self.pop_colour, (int(self.xcord), int(self.ycord)),
                           int(math.sqrt(self.population) * 10))
        if self.pop_colour != grey:                                         # checks if player is neutral
            pygame.draw.circle(window, self.core_colour, [int(self.xcord), int(self.ycord)],
                               int(math.sqrt(self.population / 2) * 10))
        poptext = font.render(str(self.population), 1, (0, 0, 0))
        window.blit(poptext, (self.xcord - 3, self.ycord - 5))
        window.blit(self.img, (self.xcord - self.radius, self.ycord - self.radius))

    def grow(self, current_time):
        if self.population > self.capacity:
            self.population = self.capacity
        if current_time > 50000 * self.counter / self.radius:
            self.counter += 1
            if self.population < self.capacity and self.player.name != "0":
                self.population += 1

    def switch_player(self, new_player):
        self.player = new_player
        self.cell_colour = new_player.cell_colour
        self.pop_colour = new_player.pop_colour
        self.core_colour = new_player.core_colour
        self.velocity = new_player.velocity

    def blow(self, cell_list):
        enough_space = True
        for cell in filter(lambda x: x != self, cell_list):
            if math.hypot(self.xcord - cell.xcord, self.ycord - cell.ycord) < cell.radius + self.radius + 5:
                enough_space = False
        if enough_space:
            self.radius += 1