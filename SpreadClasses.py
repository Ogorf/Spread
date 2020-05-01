from Utils import *
import math
import SkillTree

pygame.init()

cell_img_path = 'img/cell1.png'
bubble_img_path = 'img/bubble1.png'
bubble_img_angle = -45


class PlayerActionTracker:
    def __init__(self, player):
        self.player = player
        self.cell_loose_history = [] # should contain pairs of (time, cell) where time is the time that passed until player lost cell
        self.cell_win_history = [] # should contain pairs of (time, cell) where time is the time that passed until player won cell
        self.ordered_attacks = [] # (time, bubble)
        self.received_attacks = [] # (time, cell, bubble)


class Player:

    def __init__(self, player_id, name, colors, velocity):
        self.id = player_id
        self.name = name
        self.colors = colors
        self.velocity = velocity
        self.action_tracker = PlayerActionTracker(self)
        self.skilltree = SkillTree.empty()

    def attack_modifier(self, bubble):
        t = pygame.time.get_ticks()
        info = {"bubble": bubble, "time": t, "player": self}
        return self.skilltree.attack_modifier(info)

    def defense_modifier(self, cell):
        t = pygame.time.get_ticks()
        info = {"cell": cell, "time": t, "player": self}
        return self.skilltree.defense_modifier(info)

    def growth_modifier(self, cell):
        t = pygame.time.get_ticks()
        info = {"cell": cell, "time": t, "player": self}
        return self.skilltree.growth_modifier(info)

    def clear_action_tracker(self):
        self.action_tracker = PlayerActionTracker(self)

def get_angle(p):
    angle = math.acos(p[0]/math.sqrt(p[0]**2+p[1]**2))*180/math.pi
    print(p, angle)
    if p[1] < 0:
        return 360-angle
    else:
        return angle


class Bubble:

    def __init__(self, destination, mother, time, population):
        self.creation_time = time
        self.center = mother.center
        self.colour = mother.get_player().colors[2]
        self.destination = destination
        self.velocity = mother.player_stats.velocity
        self.player = mother.get_player()
        self.population = population
        self.radius = population_to_radius(self.population)
        self.mother = mother
        self.images = [
            pygame.transform.scale(pygame.image.load(bubble_img_path).convert_alpha(), (self.radius * 4, self.radius * 4)),
        ]
        angle = get_angle((self.destination[0]-self.center[0], self.destination[1]-self.center[1]))
        angle -= bubble_img_angle
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.rotate(self.images[i], -angle)

    def update_radius(self):
        self.radius = population_to_radius(self.population)

    def move(self, dt):
        radians = math.atan2(self.destination[1] - self.center[1], self.destination[0] - self.center[0])
        direction = (math.cos(radians), math.sin(radians))
        distance = math.hypot(self.center[0] - self.destination[0], self.center[1] - self.destination[1])
        if distance > self.velocity * dt:
            self.center = (self.center[0] + direction[0] * self.velocity * dt, self.center[1] + direction[1] * self.velocity * dt)

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (round(self.center[0]), round(self.center[1])), self.radius)
        screen.blit(self.images[0], (self.center[0] - self.radius, self.center[1] - self.radius))

    def collide_with_bubble(self, bubble):     # return winner
        if self.player != bubble.player:
            attack_modifier = self.player.attack_modifier(self)-bubble.player.attack_modifier(self)
            result = fight(self.population, bubble.population, attack_modifier)
            print(self.population, bubble.population, result)
            if result >= 0:
                bubble.population = result
                bubble.update_radius()
                return bubble
            else:
                self.population = -result
                self.update_radius()
                return self
        else:
            return None

    def collide_with_cell(self, cell):
        if self.player.id == cell.player_id:
            cell.population += self.population
        else:
            perk = cell.get_player().skilltree.find_perk("Defense", "Membrane")
            if perk is not None and perk.get_value():
                self.population = max(self.population - perk.get_value(), 0)
            attack_modifier = self.player.attack_modifier(self)-cell.get_player().defense_modifier(cell)
            result = fight(self.population, cell.population, attack_modifier)
            if result >= 0:
                cell.population = result
                cell.defended(self)
                perk = cell.get_player().skilltree.find_perk("Defense", "Recover")
                if perk is not None and perk.get_value():
                    cell.population += perk.get_value()

            else:
                cell.population = -result
                cell.switch_player(self.player)


class CellActionTracker:

    def __init__(self, cell):
        self.cell = cell
        self.ordered_attacks = [] # (time, bubble)
        self.defended_attacks = [] # (time, bubble)
        self.conquered_list = [] # (time, player)


class CellPlayer:
    def __init__(self, cell, player):
        self.player = player
        self.cell = cell
        self.velocity = player.velocity
        self.capacity = self.cap()

    def cap(self):
        perk = self.player.skilltree.find_perk("Population", "Capacity")
        bonus = 0
        if perk is not None:
            bonus = perk.get_value()
        return int(pow(self.cell.radius, 2) / 100) + bonus

class Cell:

    def __init__(self, center, radius, player_id, population, img_path=cell_img_path):
        self.center = center
        self.radius = 0
        self.img_path = img_path
        self.time_cycle = 0
        self.action_tracker = CellActionTracker(self)
        self.population = population
        #self.velocity = None
        #self.player = None
        #self.capacity = None
        #self.player = None
        self.player_id = player_id
        self.player_stats = None
        self.img = None
        self.cycle_interval = None
        self.update_radius(radius)

    def update_radius(self, radius):
        self.radius = radius
        self.cycle_interval = int(50000/self.radius)
        self.img = pygame.transform.scale(pygame.image.load(self.img_path).convert_alpha(), (radius * 2, radius * 2))

    def code(self):
        result = ""
        l = (self.center[0], self.center[1], self.radius, self.player_id, self.population, self.img_path)
        for i in l:
            result += str(i)+", "
        return result

    @staticmethod
    def decode(s): # inverse function to 'code'
        l = s.split(", ")[:-1]
        return Cell((int(l[0]), int(l[1])), int(l[2]), int(l[3]), int(l[4]), l[5])

    def init_player(self, player):
        self.set_player(player)
        self.population = self.start_pop(self.population)

    def get_player(self):
        if self.player_stats != None:
            return self.player_stats.player
        else:
            return None

    def get_attack_population(self):
        return min(int(self.population / 2), int(pow(self.radius, 2) / 100))

    def attack(self, enemypos):
        attack_pop = self.get_attack_population()
        if attack_pop > 0:
            time = pygame.time.get_ticks()
            b = Bubble(enemypos, self, time, attack_pop)
            self.population -= attack_pop
            self.action_tracker.ordered_attacks += [(time, b)]
            self.get_player().action_tracker.ordered_attacks += [(time, b)]
            return b
        else:
            return None

    def draw(self, window):
        pygame.draw.circle(window, self.get_player().colors[0], self.center, self.radius)
        pygame.draw.circle(window, self.get_player().colors[1], self.center,
                           min(self.radius, int(math.sqrt(self.population) * 10)))
        if self.get_player().colors[1] != grey:                                         # checks if player is neutral
            pygame.draw.circle(window, self.get_player().colors[2], self.center,
                               min(self.radius, int(math.sqrt(self.population / 2) * 10)))
        poptext = font.render(str(self.population), 1, (0, 0, 0))
        window.blit(poptext, (self.center[0] - 3, self.center[1] - 5))
        window.blit(self.img, (self.center[0] - self.radius, self.center[1] - self.radius))

    def grow(self, dt, current_time):
        self.time_cycle += dt * (1 + self.get_player().growth_modifier(self))
        if self.population > self.player_stats.capacity:
            self.population = self.player_stats.capacity
        else:
            if self.time_cycle > self.cycle_interval:
                cycles = int(self.time_cycle / self.cycle_interval)
                self.time_cycle %= self.cycle_interval
                for (t, b) in self.action_tracker.defended_attacks:   # TODO: fix iteration über länger werdende liste
                    info = {"current_time": current_time, "arrival_time": t, "bubble": b}
                    perk = b.player.skilltree.find_perk("Infection", "Base")
                    if perk is not None and perk.get_value(info):
                        return
                if self.population < self.player_stats.capacity and self.player_id != 0:
                    self.population += cycles

    def start_pop(self, population):
        perk = self.get_player().skilltree.find_perk("Population", "Reinforcements")
        if perk is not None and perk.get_value():
            return population + perk.get_value()
        else:
            return population

    def defended(self, bubble):
        passed_time = pygame.time.get_ticks()
        self.action_tracker.defended_attacks += [(passed_time, bubble)]
        self.get_player().action_tracker.received_attacks += [(passed_time, self, bubble)]

    def set_player(self, new_player):
        self.player_id = new_player.id
        self.player_stats = CellPlayer(self, new_player)
        #self.player = new_player
        #self.velocity = new_player.velocity
        #self.capacity = self.cap()

    def switch_player(self, new_player):
        passed_time = pygame.time.get_ticks()
        self.action_tracker.conquered_list += [(passed_time, new_player)]
        new_player.action_tracker.cell_win_history += [(passed_time, self)]
        self.get_player().action_tracker.cell_loose_history += [(passed_time, self)]
        self.set_player(new_player)
        perk = self.get_player().skilltree.find_perk("Attack", "Slavery")
        if perk is not None and perk.skilled > 0:
            self.population += perk.get_value()

    def blow(self, cell_list):
        enough_space = True
        for cell in filter(lambda x: x != self, cell_list):
            if math.hypot(self.center[0] - cell.center[0], self.center[1] - cell.center[1]) < cell.radius + self.radius + 5:
                enough_space = False
        if enough_space:
            self.update_radius(self.radius+1)


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
