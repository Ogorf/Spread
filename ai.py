import spread_classes
from utils import *
import math


def get_distance(cell1, cell2):
    return math.sqrt((cell1.center[0] - cell2.center[0]) ** 2 + (cell1.center[1] - cell2.center[1]) ** 2)


class AI(spread_classes.Player):
    def __init__(self, player_id, name, colors, velocity):
        super(AI, self).__init__(player_id, name, colors, velocity)


class Basic(AI):
    def __init__(self, player_id, name, colors, velocity=0.2, distant_expansion=50, aggressive=1, ffa_balance=1):
        super(AI, self).__init__(player_id, name, colors, velocity)
        self.isAI = True
        self.distant_expansion = distant_expansion  # in R+, neutral = +infinity
        self.aggressive = aggressive  # in R+, neutral = 1
        self.ffa_balance = ffa_balance
        self.map_strength = 0

    def calc_map_strength(self, game_state):
        for cell in game_state.cells:
            self.map_strength += cell.radius

    @staticmethod
    def calc_player_strength(player, game_state_cells):
        player_strength = 0
        for cell in filter(lambda x: x.player_id == player, game_state_cells):
            player_strength += cell.radius
        return player_strength

    def order(self, game_state, time):
        for friend_cell in filter(lambda x: x.player_id == self.id, game_state.cells):
            if friend_cell.action_tracker.ordered_attacks:
                last_attack = friend_cell.action_tracker.ordered_attacks[-1][0]
            else:
                last_attack = 0
            if time - last_attack > 1000:
                if friend_cell.population >= friend_cell.player_stats.capacity:
                    distance = 2000
                    for enemy_cell in filter(lambda x: x.player_id != self.id, game_state.cells):
                        if get_distance(friend_cell, enemy_cell) < distance:
                            distance = get_distance(friend_cell, enemy_cell)
                            target_cell = enemy_cell
                    if distance < 2000:
                        return [friend_cell], target_cell
                else:
                    for enemy_cell in filter(lambda x: x.player_id != self.id, game_state.cells):
                        enemy_player = enemy_cell.get_player().name
                        if enemy_player != "0":
                            aggro = self.aggressive
                        else:
                            aggro = 1
                        if friend_cell.population * aggro > enemy_cell.population * 2 + get_distance(friend_cell,
                                                                                                     enemy_cell) / self.distant_expansion:
                            return [friend_cell], enemy_cell
