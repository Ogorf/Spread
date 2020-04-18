import pygame

pygame.init()

class Skill:
    _font = None
    _header_spacing = 0.1
    _line_width = 0.01
    def __init__(self, name: str, perks):
        self.name = name
        self.tier_perk_dict = {}
        for perk in perks:
            if perk.tier in self.tier_perk_dict:
                self.tier_perk_dict.update({perk.tier: self.tier_perk_dict[perk.tier] + [perk]})
            else:
                self.tier_perk_dict.update({perk.tier: [perk]})

    def draw(self, window):
        w, h = pygame.display.get_surface().get_size()
        if Skill._font == None:
            Skill._font = pygame.font.SysFont("comincsans", int(min(w, h)/10))
        text = Skill._font.render(self.name, 1, (0, 0, 0))
        w2, h2 = text.get_size()
        window.blit(text, ((w-w2)/2, h*Skill._header_spacing))
        pygame.draw.line(window, (0, 0, 0), (0, h2+2*h*Skill._header_spacing), (w, h2+2*h*Skill._header_spacing), width = int(min(w, h)*Skill._line_width))

        max_tier = len(self.tier_perk_dict)
        height_per_tier = (h-h2-2*h*Skill._header_spacing) / max_tier
        max_perks_per_tier = 0
        for perk_list in self.tier_perk_dict.values():
            if len(perk_list) > max_perks_per_tier:
                max_perks_per_tier = len(perk_list)
        perk_width = w/max_perks_per_tier
        perk_font = pygame.font.SysFont("comincsans", int(min(perk_width, height_per_tier)/5))
        # draw perks
        for (perk_tier, perk_list) in self.tier_perk_dict.items():
            y = h2 + 2*h*Skill._header_spacing + height_per_tier*(perk_tier+0.5)
            x = w/len(perk_list)/2
            for perk in perk_list:
                perk.draw(window, (x, y), (w/len(perk_list), height_per_tier), perk_font)
                x += w/len(perk_list)


class Perk:
    def __init__(self, name: str, tooltip: str, tier: int = 0, levels: int = 0, skilled: int = 0):
        self.tier = tier
        self.name = name
        self.tooltip = tooltip
        self.levels = levels
        self.skilled = skilled

    def level_up(self):
        self.skilled = (self.skilled+1)%self.levels

    def draw(self, window, center, box_size, font):
        text = font.render(self.name, 1, (0, 0, 0))
        a, b = text.get_size()
        window.blit(text, (center[0] - a/2, center[1] - b/2))
        pygame.draw.rect(window, (0, 0, 0), [center[0]-box_size[0]/2, center[1]-box_size[1]/2, box_size[0], box_size[1]], 3)


class SkillTree:
    def __init__(self, skills, player = None):
        self.skills = skills
        self.selected_index = 0
        self.font = None
        self.player = player

    def navigate(self, e: int):
        self.selected_index = (self.selected_index+e)%len(self.skills)

    def selected_skill(self):
        return self.skills[self.selected_index]

    def draw(self, window):
        self.selected_skill().draw(window)
        pygame.display.update()


perk1 = Perk("Enforce", "Boost attack by 5%")
perk2 = Perk("United", "Boost defense by 5%")
perk3 = Perk("Recover", "Revive 5% of fallen units")
perk4 = Perk("A", "blabla", 1)
perk5 = Perk("B", "asd", 2)
perk6 = Perk("C", "adgf", 2)
perk7 = Perk("D", "sljkhf", 2)
skill1 = Skill("Attack", [perk1])
skill2 = Skill("Defense", [perk2, perk3, perk4, perk5, perk6, perk7])
skilltree = SkillTree([skill2, skill1])
