from utils import *
import math
import skilltree

pygame.init()

cell_img_path = 'img/cell1.png'
bubble_img_path = 'img/bubble1.png'


class PlayerActionTracker:
    def __init__(self, player):
        self.player = player
        self.cell_loose_history = []  # should contain pairs of (time, cell) where time is the time that passed until player lost cell
        self.cell_win_history = []  # should contain pairs of (time, cell) where time is the time that passed until player won cell
        self.ordered_attacks = []  # (time, bubble)
        self.received_attacks = []  # (time, cell, bubble)


class Player:

    def __init__(self, player_id, name, colors, velocity):
        self.id = player_id
        self.name = name
        self.colors = colors
        self.velocity = velocity
        self.isAI = False
        self.action_tracker = PlayerActionTracker(self)
        self.skilltree = skilltree.empty()

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
    angle = math.acos(p[0] / math.sqrt(p[0] ** 2 + p[1] ** 2))
    if p[1] < 0:
        return 2 * math.pi - angle
    else:
        return angle


def get_angle_two_vectors(v, w):
    v = get_angle(v)
    w = get_angle(w)
    return w - v


class MoveObject:
    def __init__(self, center, direction, velocity):
        self.center = center
        self.direction = direction
        self.velocity = velocity

    def update_center(self, dt):
        self.center = (self.center[0] + self.direction[0] * self.velocity * dt,
                       self.center[1] + self.direction[1] * self.velocity * dt)

class Bubble(MoveObject):
    def __init__(self, desti_cell, mother, time, population):

        self.creation_time = time
        self.population = population
        self.radius = population_to_radius(self.population)
        self.colour = mother.get_player().colors[2]
        self.desti_cell = desti_cell
        self.destination = desti_cell.center
        self.player = mother.get_player()
        self.mother = mother
        self.epsilon = 0.03
        self.images = [
            pygame.transform.scale(pygame.image.load(bubble_img_path).convert_alpha(),
                                   (int(self.radius * 2.2), int(self.radius * 2.2))),
        ]
        super(Bubble, self).__init__(self.mother.center, (0, 0), self.mother.player_stats.velocity)

    def update_radius(self):
        self.radius = population_to_radius(self.population)
        self.images[0] = pygame.transform.scale(pygame.image.load(bubble_img_path).convert_alpha(),
                                                (int(self.radius * 2.2), int(self.radius * 2.2)))

    def direction_to_desti(self):
        radians = math.atan2(self.destination[1] - self.center[1], self.destination[0] - self.center[0])
        return math.cos(radians), math.sin(radians)

    def update_direction(self):
        self.direction = ((1 - self.epsilon) * self.direction[0] + self.epsilon * self.direction_to_desti()[0], (1 - self.epsilon) * self.direction[1] + self.epsilon * self.direction_to_desti()[1])

    def move(self, dt):
        self.update_center(dt)
        self.update_direction()

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (round(self.center[0]), round(self.center[1])), self.radius)
        screen.blit(self.images[0], (self.center[0] - int(self.radius * 1.1), self.center[1] - int(self.radius * 1.1)))

    def bounce(self, cell, time):
        beta = get_angle_two_vectors(self.direction, (cell.center[0] - self.center[0], cell.center[1] - self.center[1]))
        alpha = math.pi + 2 * beta
        self.bounce_dmg(cell, time)
        self.direction = (math.cos(alpha) * self.direction[0] - math.sin(alpha) * self.direction[1], math.sin(alpha) * self.direction[0] + math.cos(alpha) * self.direction[1])

    def bounce_dmg(self, cell, time):
        if self.population > 1:
            self.population -= 1
            self.update_radius()
            if self.player.id == cell.player_id:
                cell.population += 1
            else:
                if cell.population > 0:
                    cell.population -= 1
                else:
                    cell.switch_player(self.player, time)
                    cell.population = 1

    def collide_with_bubble(self, bubble):  # return winner
        if self.player != bubble.player:
            attack_modifier = self.player.attack_modifier(self) - bubble.player.attack_modifier(self)
            result = fight(self.population, bubble.population, attack_modifier)
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

    def collide_with_cell(self, cell, time):
        if self.player.id == cell.player_id:
            cell.population += self.population
        else:
            perk = cell.get_player().skilltree.find_perk("Defense", "Membrane")
            if perk is not None and perk.get_value():
                self.population = max(self.population - perk.get_value(), 0)
            attack_modifier = self.player.attack_modifier(self) - cell.get_player().defense_modifier(cell)
            result = fight(self.population, cell.population, attack_modifier)
            if result >= 0:
                cell.population = result
                cell.defended(self, time)
                perk = cell.get_player().skilltree.find_perk("Defense", "Recover")
                if perk is not None and perk.get_value():
                    cell.population += perk.get_value()

            else:
                cell.population = -result
                cell.switch_player(self.player, time)


class CellActionTracker:
    def __init__(self, cell):
        self.cell = cell
        self.ordered_attacks = []  # (time, bubble)
        self.defended_attacks = []  # (time, bubble)
        self.conquered_list = []  # (time, player)


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
            print(bonus)
        return int(pow(self.cell.radius, 2) / 100) + bonus


class Cell(MoveObject):
    def __init__(self, center, radius, player_id, population, img_path=cell_img_path):
        self.radius = 0
        self.img_path = img_path
        self.time_cycle = 0
        self.action_tracker = CellActionTracker(self)
        self.population = population
        # self.velocity = None
        # self.player = None
        # self.capacity = None
        self.player_id = player_id
        self.player_stats = None
        self.img = None
        self.cycle_interval = None
        self.update_radius(radius)
        super(Cell, self).__init__(center, (0, 0), 0)

    def update_radius(self, radius):
        self.radius = radius
        self.cycle_interval = int(50000 / self.radius)
        self.img = pygame.transform.scale(pygame.image.load(self.img_path).convert_alpha(), (radius * 2, radius * 2))

    def code(self):
        result = ""
        l = (self.center[0], self.center[1], self.radius, self.player_id, self.population, self.img_path)
        for i in l:
            result += str(i) + ", "
        return result

    @classmethod
    def decode(cls, s):  # inverse function to 'code'
        l = s.split(", ")[:-1]
        return cls((int(l[0]), int(l[1])), int(l[2]), int(l[3]), int(l[4]), l[5])

    def init_player(self, player):
        self.set_player(player)
        self.population = self.start_pop(self.population)

    def get_player(self):
        if self.player_stats is not None:
            return self.player_stats.player
        else:
            return None

    def get_attack_population(self):
        return min(int(self.population / 2), int(pow(self.radius, 2) / 100))

    def attack(self, cell, time):
        attack_pop = self.get_attack_population()
        if attack_pop > 0:
            b = Bubble(cell, self, time, attack_pop)
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
        if self.get_player().colors[1] != grey:  # checks if player is neutral
            pygame.draw.circle(window, self.get_player().colors[2], self.center,
                               min(self.radius, int(math.sqrt(self.population / 2) * 10)))
        poptext = font.render(str(self.population), 1, (0, 0, 0))
        window.blit(poptext, (self.center[0] - 3, self.center[1] - 5))
        window.blit(self.img, (self.center[0] - self.radius, self.center[1] - self.radius))

    def grow(self, dt, current_time):
        if self.population <= self.player_stats.capacity:
            self.time_cycle += dt * (1 + self.get_player().growth_modifier(self))
            if self.time_cycle > self.cycle_interval:
                cycles = int(self.time_cycle / self.cycle_interval)
                self.time_cycle %= self.cycle_interval
                for (t, b) in self.action_tracker.defended_attacks:  # TODO: fix iteration über länger werdende liste
                    info = {"current_time": current_time, "arrival_time": t, "bubble": b}
                    perk = b.player.skilltree.find_perk("Infection", "Base")
                    if perk is not None and perk.get_value(info):
                        return
                if self.population < self.player_stats.capacity and self.player_id != 0:
                    self.population += cycles

    def start_pop(self, population):
        perk = self.get_player().skilltree.find_perk("Population", "Reinforcements")
        if perk is not None and perk.skilled > 0:
            return population + perk.get_value()
        else:
            return population

    def defended(self, bubble, time):
        self.action_tracker.defended_attacks += [(time, bubble)]
        self.get_player().action_tracker.received_attacks += [(time, self, bubble)]

    def set_player(self, new_player):
        self.player_id = new_player.id
        self.player_stats = CellPlayer(self, new_player)

    def switch_player(self, new_player, time):
        self.action_tracker.conquered_list += [(time, new_player)]
        new_player.action_tracker.cell_win_history += [(time, self)]
        self.get_player().action_tracker.cell_loose_history += [(time, self)]
        self.set_player(new_player)
        perk = self.get_player().skilltree.find_perk("Attack", "Slavery")
        if perk is not None and perk.skilled > 0:
            self.population += perk.get_value()

    def blow(self, cell_list):
        enough_space = True
        for cell in filter(lambda x: x != self, cell_list):
            if math.hypot(self.center[0] - cell.center[0],
                          self.center[1] - cell.center[1]) < cell.radius + self.radius + 5:
                enough_space = False
        if enough_space:
            self.update_radius(self.radius + 1)


def fight(a, d, am):
    if am >= 0:
        if int(a * (1 + am)) - d >= 1:
            return -int(a - d / (1 + am))
        else:
            return d - int(a * (1 + am))
    elif am < 0:
        if a - int(d * (1 - am)) >= 1:
            return -(a - int(d * (1 - am)))
        else:
            return int(d - a / (1 - am))


def collides(center1, center2, radius1, radius2):
    return (center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2 <= max(radius1, radius2) ** 2


def population_to_radius(n):
    return int(math.sqrt(n) * 10)
