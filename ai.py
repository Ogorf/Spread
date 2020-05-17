import spread_classes
from utils import *
import math


def get_distance(cell1, cell2):
    return math.sqrt((cell1.center[0] - cell2.center[0]) ** 2 + (cell1.center[1] - cell2.center[1]) ** 2)


class AI(spread_classes.Player):
    def __init__(self, player_id, name, colors, velocity):
        super(AI, self).__init__(player_id, name, colors, velocity)


class Basic(AI):
    def __init__(self, player_id, name, colors, velocity, distant_expansion=50, aggressive=1):
        super(AI, self).__init__(player_id, name, colors, velocity)
        self.isAI = True
        self.distant_expansion = distant_expansion
        self.aggressive = aggressive

    def order(self, game_state, time):
        distance = 50
        while distance < math.sqrt(window_width ** 2 + window_height ** 2):
            for friend_cell in filter(lambda x: x.player_id == self.id, game_state.cells):
                if friend_cell.action_tracker.ordered_attacks:
                    last_attack = friend_cell.action_tracker.ordered_attacks[-1][0]
                else:
                    last_attack = 0
                if time - last_attack > 1000:
                    if friend_cell.population >= friend_cell.player_stats.capacity:
                        for enemy_cell in filter(lambda x: x.player_id != self.id, game_state.cells):
                            if get_distance(friend_cell, enemy_cell) < distance:
                                return [friend_cell], enemy_cell
                    else:
                        for enemy_cell in filter(lambda x: x.player_id != self.id, game_state.cells):
                            if get_distance(friend_cell, enemy_cell) < distance:
                                if enemy_cell.get_player().name != "0":
                                    aggro = self.aggressive
                                else:
                                    aggro = 1
                                if friend_cell.population * aggro > enemy_cell.population * 2 + distance / self.distant_expansion:
                                    return [friend_cell], enemy_cell
            distance += 50
