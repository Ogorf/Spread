from SkillTree import *


class PopulationPerk(Perk):
    def growth_modifier(self, info):
        return 0


class Base(PopulationPerk):
    def __init__(self, values):
        tooltip = "Boost growth by {}"
        super(Base, self).__init__("Base", tooltip=tooltip, tier=0, values=values)

    def growth_modifier(self, info):
        if self.skilled > 0:
            return self.values[self.skilled-1][0]
        else:
            return 0


class Capacity(PopulationPerk):
    def __init__(self, values):
        tooltip = "Capacity of your cells is increased by {}"
        super(Capacity, self).__init__("Capacity", tooltip=tooltip, tier=0, values=values)

    def get_value(self):
        if self.skilled > 0:
            return self.values[self.skilled-1][0]
        else:
            return 0


class Reinforcements(PopulationPerk):
    def __init__(self, values):
        tooltip = "At the beginning, every friendly cell starts with +{} population."
        super(Reinforcements, self).__init__("Reinforcements", tooltip=tooltip, tier=1, values=values)
        
    def get_value(self):
        if self.skilled > 0:
            return self.values[self.skilled-1][0]
        else:
            return 0


class PopulationSkill(Skill):
    def __init__(self, l):
        super(PopulationSkill, self).__init__("Population", l)

    def growth_modifier(self, info):
        result = 0
        for perk in self.perks():
            result += perk.growth_modifier(info)
        return result


def empty():
    return PopulationSkill([Base([(0.06,), (0.12,), (0.18,)]), Capacity([(20, ), (40, ), (60, )]), Reinforcements([(5, ), (10, ), (15, )])])
