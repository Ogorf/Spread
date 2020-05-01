import math
import SpreadClasses
import pygame


class Map:
    map_dir = "maps/"
    map_ending = ".map"
    # uninitialized cells loaded from a file, or mb just pass the file
    def __init__(self, name, cell_list):
        self.name = name
        self.cells = cell_list

    @staticmethod
    def new(map_name="new"):
        return Map("new", [])

    @staticmethod
    def load(map_name):
        with open(Map.map_dir+map_name+Map.map_ending, "r") as f:
            lines = f.readlines()
            name = lines[0]
            cell_list = []
            for s in lines[1:]:
                cell_list += [SpreadClasses.Cell.decode(s)]
        return Map(name, cell_list)

    def save(self):
        with open(Map.map_dir+self.name+Map.map_ending, 'w') as f:
            f.write(self.name+"\n")
            for cell in self.cells:
                f.write(cell.code()+"\n")

    def init_players(self, player_list):
        for cell in self.cells:
            player = next(filter(lambda p: p.id == cell.player_id, player_list), None)
            if player == None:
                print("unowned cell!")
                # mb interrupt here or set default to neutral
            else:
                cell.init_player(player)


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
        while self.bubbles != []:
            bubble = self.bubbles.pop()
            fought = False
            for b in new_bubbles:
                if SpreadClasses.collides(bubble.center, b.center, bubble.radius, b.radius):
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

        # checks if bubble collides with cell and calls collide function
        for bubble in self.bubbles:
            for cell in filter(lambda x: x != bubble.mother, self.cells):
                if SpreadClasses.collides(bubble.center, cell.center, bubble.radius, cell.radius):
                    bubble.collide_with_cell(cell)
                    self.bubbles.remove(bubble)

import Maps
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
            self.game_state.bubbles += [c.attack(cell.center)]

    def tick(self, dt):
        self.time += dt
        self.game_state.tick(dt, self.time-self.start_time)

    def draw(self, window):
        self.game_state.draw(window)
