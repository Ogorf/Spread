from SkillTree import *


class InfectionPerk(Perk):
    pass

class Base(InfectionPerk):
    def __init__(self, values):
        tooltip = "Cells you attacked stop growing for attacker divided by {} of seconds"
        super(Base, self).__init__("Base", tooltip=tooltip, tier=0, values=values)

    def get_value(self, info):
        if self.skilled > 0 and info["current_time"]-info["arrival_time"] <= info["bubble"].population/self.values[self.skilled-1][0]:
            return 1
        else:
            return 0

class InfectionSkill(Skill):
    def __init__(self, l):
        super(InfectionSkill, self).__init__("Infection", l)

def empty():
    return InfectionSkill([Base([(50,), (33,), (25,)])])
