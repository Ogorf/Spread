import skilltree


class OffensePerk(skilltree.Perk):
    def attack_modifier(self, info):
        return 0


class Base(OffensePerk):
    def __init__(self, values):
        tooltip = "Boost attack by {}%"
        super(Base, self).__init__("Base", tooltip=tooltip, tier=0, values=values)

    def attack_modifier(self, info):
        if self.skilled > 0:
            return self.values[self.skilled-1][0]
        else:
            return 0


class Rage(OffensePerk):
    def __init__(self, values):
        tooltip = "Whenever a friendly cell is lost, attack is shortly ({} seconds) increased by {}"
        super(Rage, self).__init__("Rage", tooltip=tooltip, tier=1, values=values)

    # TODO:
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


class Berserker(OffensePerk):
    def __init__(self, values):
        tooltip = "For every attack a cell has ordered within the last {} seconds, it's attack increases by {}"
        super(Berserker, self).__init__("Berserker", tooltip=tooltip, tier=1, values=values)

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
        l = filter(lambda time_bubble: 0 < info["bubble"].creation_time-time_bubble[0] <= 1000*self.get_condition_value() and time_bubble[1].mother == info["bubble"].mother, info["player"].action_tracker.ordered_attacks)
        n = len(list(l))      # subtract the order itself
        return self.get_value()*n


class Slavery(OffensePerk):
    def __init__(self, values):
        # tooltip = "Every newly conquered cell gains " + str(value) + " pop"
        tooltip = "Every newly conquered cell gains {} population"
        super(Slavery, self).__init__("Slavery", tooltip=tooltip, tier=2, values=values)

    def get_value(self):
        if self.skilled > 0:
            return self.values[self.skilled-1][0]
        else:
            return 0


class OffenseSkill(skilltree.Skill):
    def __init__(self, l):
        super(OffenseSkill, self).__init__("Offense", l)

    def attack_modifier(self, info):
        result = 0
        for perk in self.perks():
            result += perk.attack_modifier(info)
        return result


def empty():
    return OffenseSkill([Base([(0.1,), (0.2,), (0.3,)]), Rage([(3, 0.2)]), Berserker([(5, 0.05)]), Slavery([(10,)])])
