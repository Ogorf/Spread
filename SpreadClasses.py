from Utils import *
import math
import SkillTree

pygame.init()

img_path = 'img/cell1.png'


class ActionTracker:
    def __init__(self, player):
        self.player = player
        self.cell_loose_history = [] # should contain pairs of (time, cell) where time is the time that passed until player lost cell
        self.cell_win_history = [] # should contain pairs of (time, cell) where time is the time that passed until player won cell
        self.ordered_attacks = [] # (time, bubble)
        self.received_attacks = [] # (time, cell, bubble)


class Player:

    def __init__(self, name, cell_colour, pop_colour, core_colour, velocity, startpop):
        self.name = name
        self.cell_colour = cell_colour
        self.pop_colour = pop_colour
        self.core_colour = core_colour
        self.velocity = velocity
        self.startpop = startpop
        self.action_tracker = ActionTracker(self)
        self.skilltree = SkillTree.empty()

    def attack_modifier(self, bubble):
        t = pygame.time.get_ticks()
        info = {"bubble": bubble, "time": t, "player": self}
        return self.skilltree.attack_modifier(info)

    def defense_modifier(self):
        return 0

    def clear_action_tracker(self):
        self.action_tracker = ActionTracker(self)

class Bubble:

    def __init__(self, destination, mother, time):
        self.creation_time = time
        self.center = mother.center
        self.colour = mother.core_colour
        self.destination = destination
        self.velocity = mother.velocity
        self.player = mother.player
        self.population = int(mother.population)
        self.radius = population_to_radius(self.population)
        self.mother = mother

    def update_radius(self):
        self.radius = population_to_radius(self.population)

    def move(self, dt):
        radians = math.atan2(self.destination[1] - self.center[1], self.destination[0] - self.center[0])
        direction = (math.cos(radians), math.sin(radians))
        distance = math.hypot(self.center[0] - self.destination[0], self.center[1] - self.destination[1])
        if distance > self.velocity * dt:
            self.center = (int(self.center[0]+direction[0]*self.velocity*dt), int(self.center[1]+direction[1]*self.velocity*dt))

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, self.center, self.radius)

    def collide_with_bubble(self, bubble): # return winner
        if self.player != bubble.player:
            attack_modifier = self.player.attack_modifier(self)-bubble.player.attack_modifier(self)
            result = fight(self.population, bubble.population, attack_modifier)
            if result >= 0:
                bubble.population = result
                bubble.update_radius()
                return bubble
            else:
                self.population = -result
                self.update_radius()
                return self

    def collide_with_cell(self, cell):
        if self.player == cell.player:
            cell.population += self.population
        else:
            attack_modifier = self.player.attack_modifier(self)-cell.player.defense_modifier()
            result = fight(self.population, cell.population, attack_modifier)
            if result >= 0:
                cell.population = result
                cell.defended(self)
            else:
                cell.population = -result
                cell.switch_player(self.player)


class Cell:

    def __init__(self, center, radius, player, population, img_path=img_path):
        self.center = center
        self.radius = radius
        self.cell_colour = player.cell_colour
        self.pop_colour = player.pop_colour
        self.core_colour = player.core_colour
        self.velocity = player.velocity
        self.player = player
        self.population = population
        self.capacity = int(pow(radius, 2) / 100)
        self.img = pygame.transform.scale(pygame.image.load(img_path).convert_alpha(), (radius * 2, radius * 2))
        self.time_cycle = 0
        self.cycle_interval = int(50000/self.radius)

    def attack(self, enemypos):
        self.population = math.ceil(self.population / 2)
        time = pygame.time.get_ticks()
        b = Bubble(enemypos, self, time)
        self.player.action_tracker.ordered_attacks += [(time, b)]
        return b

    def draw(self, window):
        pygame.draw.circle(window, self.cell_colour, self.center, self.radius)
        pygame.draw.circle(window, self.pop_colour, self.center,
                           int(math.sqrt(self.population) * 10))
        if self.pop_colour != grey:                                         # checks if player is neutral
            pygame.draw.circle(window, self.core_colour, self.center,
                               int(math.sqrt(self.population / 2) * 10))
        poptext = font.render(str(self.population), 1, (0, 0, 0))
        window.blit(poptext, (self.center[0] - 3, self.center[1] - 5))
        window.blit(self.img, (self.center[0] - self.radius, self.center[1] - self.radius))

    def grow(self, dt):
        self.time_cycle += dt
        if self.population > self.capacity:
            self.population = self.capacity
        else:
            if self.time_cycle > self.cycle_interval:
                current_time = pygame.time.get_ticks()
                cycles = int(self.time_cycle / self.cycle_interval)
                self.time_cycle %= self.cycle_interval
                for (t, c, b) in self.player.action_tracker.received_attacks:
                    if c == self:
                        info = {"current_time": current_time, "arrival_time": t, "bubble": b}
                        perk = b.player.skilltree.find_perk("Infection", "Base")
                        if perk is not None and perk.get_value(info):
                            return
                if self.population < self.capacity and self.player.name != "0":
                    self.population += cycles


    def defended(self, bubble):
        passed_time = pygame.time.get_ticks()
        self.player.action_tracker.received_attacks += [(passed_time, self, bubble)]

    def switch_player(self, new_player):
        passed_time = pygame.time.get_ticks()
        new_player.action_tracker.cell_win_history += [(passed_time, self)]
        self.player.action_tracker.cell_loose_history += [(passed_time, self)]
        self.player = new_player
        self.cell_colour = new_player.cell_colour
        self.pop_colour = new_player.pop_colour
        self.core_colour = new_player.core_colour
        self.velocity = new_player.velocity
        perk = self.player.skilltree.find_perk("Attack", "Slavery")
        if perk != None and perk.skilled > 0:
            self.population += perk.get_value()

    def blow(self, cell_list):
        enough_space = True
        for cell in filter(lambda x: x != self, cell_list):
            if math.hypot(self.center[0] - cell.center[0], self.center[1] - cell.center[1]) < cell.radius + self.radius + 5:
                enough_space = False
        if enough_space:
            self.radius += 1


def fight(a, d, am):
    if am >= 0:
        if int(a*(1+am))-d >= 1:
            return -int(a-d/(1+am))
        else:
            return d-int(a*(1+am))
    elif am < 0:
        if a-int(d*(1-am)) >= 1:
            return -(a-int(d*(1-am)))
        else:
            return int(d-a/(1-am))

def collides(center1, center2, radius1, radius2):
    return (center1[0]-center2[0])**2+(center1[1]-center2[1])**2 <= max(radius1, radius2)**2

def population_to_radius(n):
    return int(math.sqrt(n) * 10)

