import math
import spread_classes
import pygame


class Map:
    map_dir = "maps/"
    map_ending = ".map"

    # uninitialized cells loaded from a file, or mb just pass the file
    def __init__(self, name, cell_list):
        self.name = name
        self.cells = cell_list

    @classmethod
    def new(cls, map_name="new"):
        return cls(map_name, [])

    @classmethod
    def load(cls, map_name):
        with open(Map.map_dir + map_name + Map.map_ending, "r") as f:
            lines = f.readlines()
            name = lines[0]
            cell_list = []
            for s in lines[1:]:
                cell_list += [spread_classes.Cell.decode(s)]
        return cls(name, cell_list)

    def save(self, name):
        self.name = name
        with open(Map.map_dir + self.name + Map.map_ending, 'w') as f:
            f.write(self.name + "\n")
            for cell in self.cells:
                f.write(cell.code() + "\n")

    def init_players(self, player_list):
        for cell in self.cells:
            for player in player_list:
                if player.id == cell.player_id:
                    cell.init_player(player)
                    break

    def get_player_slots(self):
        players = []
        for cell in self.cells:
            if cell.player_id not in players:
                players += [cell.player_id]
        players.sort()
        return players


class GameState:
    def __init__(self, cells, bubbles):
        self.cells = cells
        self.bubbles = bubbles

    def draw(self, window):
        for cell in self.cells:
            cell.draw(window)
        for bubble in self.bubbles:
            bubble.draw(window)

    def tick(self, dt, current_time):
        # grow cells
        for cell in self.cells:
            cell.grow(dt, current_time)
        # moves bubbles
        for bubble in self.bubbles:
            bubble.move(dt)
        # check bubble-bubble-collision
        new_bubbles = []
        while self.bubbles:
            bubble = self.bubbles.pop()
            fought = False
            for b in new_bubbles:
                if spread_classes.collides(bubble.center, b.center, bubble.radius, b.radius):
                    winner_bubble = b.collide_with_bubble(bubble)
                    if winner_bubble == bubble:
                        new_bubbles.remove(b)
                        new_bubbles += [winner_bubble]
                    elif winner_bubble is None:
                        continue
                    fought = True
                    break
            if not fought:
                new_bubbles += [bubble]
        self.bubbles = new_bubbles

        # checks if bubble collides with desti_cell and calls collide function
        for bubble in self.bubbles:
            if spread_classes.collides(bubble.center, bubble.desti_cell.center, bubble.radius, bubble.desti_cell.radius):
                bubble.collide_with_cell(bubble.desti_cell, current_time)
                self.bubbles.remove(bubble)

        # checks if bubble should bounce and calls bounce function
        for bubble in self.bubbles:
            for cell in filter(lambda x: x != bubble.desti_cell, self.cells):
                down = (cell.center[0] - bubble.center[0] + bubble.direction[0],
                        cell.center[1] - bubble.center[1] + bubble.direction[1])
                up = (- cell.center[0] + bubble.center[0] + bubble.direction[0],
                      - cell.center[1] + bubble.center[1] + bubble.direction[1])
                down = down[0] ** 2 + down[1] ** 2
                up = up[0] ** 2 + up[1] ** 2
                if math.sqrt((bubble.center[0] - cell.center[0]) ** 2 + (bubble.center[1] - cell.center[1]) ** 2) < bubble.radius + cell.radius and down > up:
                    bubble.bounce(cell, current_time)

import maps
class Game:
    def __init__(self, m: Map, player_list):
        self.time = pygame.time.get_ticks()
        self.start_time = self.time
        self.players = player_list
        m.init_players(self.players)
        self.game_state = GameState(m.cells, [])

    def get_game_state(self):
        return self.game_state

    def update_game_state(self, game_state):
        self.game_state = game_state

    def order_attacks(self, cell_list, cell):
        for c in filter(lambda x: x != cell, cell_list):
            b = c.attack(cell, pygame.time.get_ticks() - self.start_time)
            if b is not None:
                self.game_state.bubbles += [b]

    def tick(self, dt):
        self.time += dt
        self.game_state.tick(dt, self.time - self.start_time)

    def draw(self, window):
        self.game_state.draw(window)
