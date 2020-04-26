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
        return self.values[self.skilled][0]


class DefenseSkill(Skill):
    def __init__(self, l):
        super(DefenseSkill, self).__init__("Defense", l)

    def defense_modifier(self, info):
        result = 0
        for perk in self.perks():
            result += perk.defense_modifier(info)
        return result
