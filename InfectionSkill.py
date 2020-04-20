from SkillTree import *


class InfectionPerk(Perk):
    pass

class Base(InfectionPerk):
    def __init__(self, values):
        tooltip = "Cells u attacked stop growing for {} of seconds".format("attacker/".join(map(lambda i: str(i), values))[:-1])
        super(Base, self).__init__("Base", tooltip=tooltip, tier=0, levels=len(values), values=values)
