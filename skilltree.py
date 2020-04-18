import pygame
from utils import *

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

    def perks(self):
        result = []
        for perk_list in self.tier_perk_dict.values():
            result += perk_list
        return result

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
    def __init__(self, name: str, tooltip: str, tier: int = 0, levels: int = 1, skilled: int = 0):
        self.tier = tier
        self.name = name
        self.tooltip = tooltip
        self.levels = levels
        self.skilled = skilled
        self.bbox = None
        self.rendered_tooltip = None
        self.rendered_text = None

    def draw_tooltip(self, window, x, y):
        if self.rendered_tooltip == None:
            self.rendered_tooltip = SkillTree._tooltip_font.render(self.tooltip, 1, (50, 50, 50))
        w, h = self.rendered_tooltip.get_size()
        window.blit(self.rendered_tooltip, (x-w, y-h))
        pygame.display.update()

    def level_up(self):
        self.skilled = (self.skilled+1)%(self.levels+1)
        self.rendered_text = None

    def draw(self, window, center, box_size, font):
        self.bbox = [center[0]-box_size[0]/2, center[1]-box_size[1]/2, box_size[0], box_size[1]]
        l = self.skilled/self.levels
        bg_color = (255-l*(255-dark_blue[0]), 255-l*(255-dark_blue[1]), 255-l*(255-dark_blue[2]))
        pygame.draw.rect(window, bg_color, self.bbox)
        if self.rendered_text == None:
            text = font.render(self.name + " ("+str(self.skilled)+"/"+str(self.levels)+")", 1, (0, 0, 0))
        a, b = text.get_size()
        window.blit(text, (center[0] - a/2, center[1] - b/2))
        pygame.draw.rect(window, (0, 0, 0), self.bbox, 3)


class SkillTree:
    _tooltip_font = pygame.font.SysFont("comincsans", 20)
    def __init__(self, skills, player = None):
        self.skills = skills
        self.selected_index = 0
        self.player = player
        self.rendered_tooltip = None

    def get_perk(self, x, y):
        for perk in self.selected_skill().perks():
            if perk.bbox != None:
                if 0 <= x-perk.bbox[0] <= perk.bbox[2] and 0 <= y-perk.bbox[1] <= perk.bbox[3]:
                    return perk
        return None

    def navigate(self, e: int):
        self.selected_index = (self.selected_index+e)%len(self.skills)

    def selected_skill(self):
        return self.skills[self.selected_index]

    def draw(self, window):
        self.selected_skill().draw(window)

    def draw_tooltip(self, window, x, y):
        perk = self.get_perk(x, y)
        if perk != None:
            perk.draw_tooltip(window, x, y)



def empty_skilltree():
    perk1 = Perk("Enforce", "Boost attack by 5%")
    perk2 = Perk("United", "Boost defense by 5%")
    perk3 = Perk("Recover", "Revive 5% of fallen units", 0, 3)
    perk4 = Perk("A", "blabla", 1, 4)
    perk5 = Perk("B", "asd", 2, 2)
    perk6 = Perk("C", "adgf", 2)
    perk7 = Perk("D", "sljkhf", 2)
    skill1 = Skill("Attack", [perk1])
    skill2 = Skill("Defense", [perk2, perk3, perk4, perk5, perk6, perk7])
    skilltree = SkillTree([skill2, skill1])
    return skilltree
