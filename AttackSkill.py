from SkillTree import *


class AttackPerk(Perk):
    def attack_modifier(self, info):
        return 0


class Base(AttackPerk):
    def __init__(self, values):
        tooltip = "Boost attack by "+"%/".join(map(lambda x: str(int(x*100)), values))+"%"
        super(Base, self).__init__("Base", tooltip=tooltip, tier=0, levels=len(values), values=values)

    def attack_modifier(self, info):
        return self.values[self.skilled]


class Rage(AttackPerk):
    def __init__(self, value):
        tooltip = "Whenever a friendly cell is lost, attack is shortly (" + str(value[0]) + " seconds) increased by " + str(int(100*value[1])) + "%"
        super(Rage, self).__init__("Rage", tooltip=tooltip, tier=0, levels=1, value=value)

    #TODO:
    def condition(self, player, time):
        return len(list(filter(lambda time_cell: time-time_cell[0] <= 1000*self.get_condition_value(), player.action_tracker.cell_loose_history))) > 0

    def get_condition_value(self):
        return self.value[0]

    def get_value(self):
        return self.value[1]

    def attack_modifier(self, info):
        if self.condition(info["player"], info["time"]):
            return self.get_value()
        else:
            return 0


class Berserker(AttackPerk):
    def __init__(self, value):
        tooltip = "For every consecutive (within " + str(value[0]) + " seconds after the last) attack a cell orders, it's attack increases by " + str(int(100*value[1])) + "%"
        super(Berserker, self).__init__("Berserker", tooltip=tooltip, tier=1, levels=1, value=value)

    def get_condition_value(self):
        return self.value[0]

    def get_value(self):
        if self.skilled > 0:
            return self.value[1]
        else:
            return 0

    def attack_modifier(self, info):
        l = filter(lambda time_bubble: 0 < info["bubble"].creation_time-time_bubble[0] <= 1000*self.get_condition_value() and time_bubble[1].mother == info["bubble"].mother, info["player"].action_tracker.ordered_attacks)
        n = len(list(l))      # subtract the order itself
        return self.get_value()*n


class Slavery(AttackPerk):
    def __init__(self, value):
        tooltip = "Every newly conquered cell gains " + str(value) + " pop"
        super(Slavery, self).__init__("Slavery", tooltip=tooltip, tier=2, levels=1, value=value)

    def get_value(self):
        return self.value


class AttackSkill(Skill):
    def __init__(self, l):
        super(AttackSkill, self).__init__("Attack", l)

    def attack_modifier(self, info):
        result = 0
        for perk in self.perks():
            result += perk.attack_modifier(info)
        return result
