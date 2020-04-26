from SkillTree import *


class AttackPerk(Perk):
    pass
    #def attack_modifier(self, info):
    #    return 0


class Base(AttackPerk):
    def __init__(self, values):
        #tooltip = "Boost attack by "+"%/".join(map(lambda x: str(int(x*100)), values))+"%"
        tooltip = "Boost attack by {}%"
        super(Base, self).__init__("Base", tooltip=tooltip, tier=0, values=values)

    def attack_modifier(self, info):
        if self.skilled > 0:
            return self.values[self.skilled-1][0]
        else:
            return 0


class Rage(AttackPerk):
    def __init__(self, values):
        #tooltip = "Whenever a friendly cell is lost, attack is shortly (" + str(value[0]) + " seconds) increased by " + str(int(100*value[1])) + "%"
        tooltip = "Whenever a friendly cell is lost, attack is shortly ({} seconds) increased by {}%"
        super(Rage, self).__init__("Rage", tooltip=tooltip, tier=0, values=values)

    #TODO:
    def condition(self, player, time):
        return len(list(filter(lambda time_cell: time-time_cell[0] <= 1000*self.get_condition_value(), player.action_tracker.cell_loose_history))) > 0

    def get_condition_value(self):
        if self.skilled > 0:
            return self.values[self.skilled-1][0]
        else:
            return 0

    def get_value(self):
        if self.skilled > 0:
            return self.values[self.skilled-1][1]
        else:
            return 0

    def attack_modifier(self, info):
        if self.condition(info["player"], info["time"]):
            return self.get_value()
        else:
            return 0


class Berserker(AttackPerk):
    def __init__(self, values):
        #tooltip = "For every consecutive (within " + str(value[0]) + " seconds after the last) attack a cell orders, it's attack increases by " + str(int(100*value[1])) + "%"
        tooltip = "For every consecutive (within {} seconds after the last) attack a cell orders, it's attack increases by {}%"
        super(Berserker, self).__init__("Berserker", tooltip=tooltip, tier=1, values=values)

    def get_condition_value(self):
        if self.skilled > 0:
            return self.values[self.skilled-1][0]

    def get_value(self):
        if self.skilled > 0:
            return self.values[self.skilled-1][1]
        else:
            return 0

    def attack_modifier(self, info):
        l = filter(lambda time_bubble: 0 < info["bubble"].creation_time-time_bubble[0] <= 1000*self.get_condition_value() and time_bubble[1].mother == info["bubble"].mother, info["player"].action_tracker.ordered_attacks)
        n = len(list(l))      # subtract the order itself
        return self.get_value()*n


class Slavery(AttackPerk):
    def __init__(self, values):
        #tooltip = "Every newly conquered cell gains " + str(value) + " pop"
        tooltip = "Every newly conquered cell gains {} population"
        super(Slavery, self).__init__("Slavery", tooltip=tooltip, tier=2, values=values)

    def get_value(self):
        if self.skilled > 0:
            return self.values[self.skilled-1][0]
        else:
            return 0


class AttackSkill(Skill):
    def __init__(self, l):
        super(AttackSkill, self).__init__("Attack", l)

    def attack_modifier(self, info):
        result = 0
        for perk in self.perks():
            result += perk.attack_modifier(info)
        return result
