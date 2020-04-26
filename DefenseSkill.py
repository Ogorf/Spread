from SkillTree import *


class DefensePerk(Perk):
    def defense_modifier(self, info):
        return 0


class Base(DefensePerk):
    def __init__(self, values):
        # tooltip = "Boost defense by "+"%/".join(map(lambda x: str(int(x*100)), values))+"%"
        tooltip = "Boost defense by {}%"
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
        tooltip = "For every consecutive second a cell has neither defended nor attacked, it gains {}% defense."
        super(Preparation, self).__init__("Preparation", tooltip=tooltip, tier=2, values=values)





class DefenseSkill(Skill):
    def __init__(self, l):
        super(DefenseSkill, self).__init__("Defense", l)

    def defense_modifier(self, info):
        result = 0
        for perk in self.perks():
            result += perk.defense_modifier(info)
        return result


def empty():
    return DefenseSkill([Base([(0.1,), (0.2,), (0.3,)]), Recover([(5, )]), ])
