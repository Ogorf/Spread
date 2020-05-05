from SkillTree import *


class DefensePerk(Perk):
    def defense_modifier(self, info):
        return 0


class Base(DefensePerk):
    def __init__(self, values):
        tooltip = "Boost defense by {}"
        super(Base, self).__init__("Base", tooltip=tooltip, tier=0, values=values)

    def defense_modifier(self, info):
        if self.skilled > 0:
            return self.values[self.skilled-1][0]
        else:
            return 0


class Recover(DefensePerk):
    def __init__(self, values):
        tooltip = "Cell recovers {} viruses after a successful defense"
        super(Recover, self).__init__("Recover", tooltip=tooltip, tier=1, values=values)

    def get_value(self):
        if self.skilled > 0:
            return self.values[self.skilled-1][0]
        else:
            return 0

class Preparation(DefensePerk):
    def __init__(self, values):
        tooltip = "For every consecutive second a cell has neither received nor sent any bubble, it gains {} defense."
        super(Preparation, self).__init__("Preparation", tooltip=tooltip, tier=2, values=values)

    def defense_modifier(self, info):
        t = info["time"]
        attack_list = info["cell"].action_tracker.ordered_attacks
        defend_list = info["cell"].action_tracker.defended_attacks
        conquer_list = info["cell"].action_tracker.conquered_list
        result = ((t - max(0 if attack_list == [] else attack_list[-1][0], 0 if defend_list == [] else defend_list[-1][0], 0 if conquer_list == [] else conquer_list[-1][0])) * self.values[self.skilled-1][0]) / 1000
        return int(result)


class Membrane(DefensePerk):
    def __init__(self, values):
        tooltip = "The first {} attackers of every attacking enemy bubble die to the membrane before doing damage."
        super(Membrane, self).__init__("Membrane", tooltip=tooltip, tier=2, values=values)

    def get_value(self):
        if self.skilled > 0:
            return self.values[self.skilled-1][0]
        else:
            return 0


class DefenseSkill(Skill):
    def __init__(self, l):
        super(DefenseSkill, self).__init__("Defense", l)

    def defense_modifier(self, info):
        result = 0
        for perk in self.perks():
            result += perk.defense_modifier(info)
        return result


def empty():
    return DefenseSkill([Base([(0.1,), (0.2,), (0.3,)]), Recover([(5, )]), Preparation([(0.01, ), ]), Membrane([(10, )])])
