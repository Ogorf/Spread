from Utils import *

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

    def level_up(self, perk_name):
        for perk in self.perks():
            if perk.name == perk_name:
                perk.level_up()

    def find_perk(self, perk_name):
        for perk in self.perks():
            if perk.name == perk_name:
                return perk
        return None

    def perks(self):
        result = []
        for perk_list in self.tier_perk_dict.values():
            result += perk_list
        return result

    def draw(self, window):
        w, h = pygame.display.get_surface().get_size()
        if Skill._font is None:
            Skill._font = pygame.font.SysFont("comincsans", int(min(w, h) / 10))
        text = Skill._font.render(self.name, 1, (0, 0, 0))
        w2, h2 = text.get_size()
        window.blit(text, ((w - w2) / 2, h * Skill._header_spacing))
        pygame.draw.line(window, (0, 0, 0), (0, h2 + 2 * h * Skill._header_spacing),
                         (w, h2 + 2 * h * Skill._header_spacing), int(min(w, h) * Skill._line_width))

        max_tier = len(self.tier_perk_dict)
        height_per_tier = (h - h2 - 2 * h * Skill._header_spacing) / max_tier
        max_perks_per_tier = 0
        for perk_list in self.tier_perk_dict.values():
            if len(perk_list) > max_perks_per_tier:
                max_perks_per_tier = len(perk_list)
        perk_width = w / max_perks_per_tier
        perk_font = pygame.font.SysFont("comincsans", int(min(perk_width, height_per_tier) / 5))
        # draw perks
        for (perk_tier, perk_list) in self.tier_perk_dict.items():
            y = h2 + 2 * h * Skill._header_spacing + height_per_tier * (max_tier - perk_tier - 0.5)
            x = w / len(perk_list) / 2
            for perk in perk_list:
                perk.draw(window, (x, y), (w / len(perk_list), height_per_tier), perk_font)
                x += w / len(perk_list)

    def attack_modifier(self, info):
        result = 0
        for perk in self.perks():
            result += perk.attack_modifier(info)
        return result

    def defense_modifier(self, info):
        result = 0
        for perk in self.perks():
            result += perk.defense_modifier(info)
        return result



class Perk:
    def __init__(self, name: str, **kwargs):  # tooltip: str, tier: int = 0, levels: int = 1, skilled: int = 0):
        self.name = name
        self.tier = kwargs.get("tier", 0)
        self.values = kwargs.pop("values", [[]])
        l = list(zip(*self.values))
        l = map(lambda x: "/".join(list(map(lambda y: str(y), x))), l)
        l = list(l)
        self.tooltip = kwargs.pop("tooltip", "").format(*l)  # *list(zip(self.values)))
        self.levels = len(self.values)
        self.skilled = kwargs.pop("skilled", 0)
        self.__dict__.update(**kwargs)
        self.bbox = None
        self.rendered_tooltip = None
        self.rendered_text = None

    def condition(self, p):
        return self.skilled > 0

    def draw_tooltip(self, window, x, y):
        if self.rendered_tooltip is None:
            self.rendered_tooltip = SkillTree._tooltip_font.render(self.tooltip, 1, (50, 50, 50))
        w, h = self.rendered_tooltip.get_size()
        window.blit(self.rendered_tooltip, (x - w, y - h))
        pygame.display.update()

    def level_up(self):
        self.skilled = (self.skilled + 1) % (self.levels + 1)
        self.rendered_text = None

    def draw(self, window, center, box_size, font):
        self.bbox = [center[0] - box_size[0] / 2, center[1] - box_size[1] / 2, box_size[0], box_size[1]]
        l = self.skilled / self.levels
        bg_color = (255 - l * (255 - dark_blue[0]), 255 - l * (255 - dark_blue[1]), 255 - l * (255 - dark_blue[2]))
        pygame.draw.rect(window, bg_color, self.bbox)
        if self.rendered_text is None:
            self.rendered_text = font.render(self.name + " (" + str(self.skilled) + "/" + str(self.levels) + ")", 1,
                                             (0, 0, 0))
        a, b = self.rendered_text.get_size()
        window.blit(self.rendered_text, (center[0] - a / 2, center[1] - b / 2))
        pygame.draw.rect(window, (0, 0, 0), self.bbox, 3)

    def attack_modifier(self, info):
        return 0

    def defense_modifier(self, info):
        return 0



import AttackSkill
import InfectionSkill
import DefenseSkill


class SkillTree:
    _tooltip_font = pygame.font.SysFont("comincsans", 20)

    def __init__(self, skills, player=None):
        self.skills = skills
        self.selected_index = 0
        self.player = player
        self.rendered_tooltip = None

    def level_up(self, skill_name, perk_name):
        for skill in self.skills:
            if skill.name == skill_name:
                skill.level_up(perk_name)

    def get_perk(self, x, y):
        for perk in self.selected_skill().perks():
            if perk.bbox is not None:
                if 0 <= x - perk.bbox[0] <= perk.bbox[2] and 0 <= y - perk.bbox[1] <= perk.bbox[3]:
                    return perk
        return None

    def navigate(self, e: int):
        self.selected_index = (self.selected_index + e) % len(self.skills)

    def selected_skill(self):
        return self.skills[self.selected_index]

    def draw(self, window):
        self.selected_skill().draw(window)

    def draw_tooltip(self, window, x, y):
        perk = self.get_perk(x, y)
        if perk is not None:
            perk.draw_tooltip(window, x, y)

    def attack_modifier(self, info):
        result = 0
        for skill in self.skills:
            result += skill.attack_modifier(info)
        return result

    def defense_modifier(self, info):
        result = 0
        for skill in self.skills:
            result += skill.defense_modifier(info)
        return result

    def find_perk(self, skill_name, perk_name):
        for skill in self.skills:
            if skill.name == skill_name:
                return skill.find_perk(perk_name)
        return None


def empty():
    #attack = AttackSkill([Base([(0.1,), (0.2,), (0.3,)]), Rage([(3, 0.2)]), Berserker([(2, 0.05)]), Slavery([(10,)])])
    #infection = InfectionSkill([Base([(50,), (33,), (25,)])])

    # defense1 = Perk("Base", "Increases defense by 10/20/30%", 0, 3)
    # defense2 = Perk("Recover", "For every successful defense, the cell gains +5 pop", 1, 1)
    # defense3 = Perk("Preparation", "For every consecutive second a cell has neither defended nor attacked, it gains +1% defense", 1, 1)
    # defense4 = Perk("Membran", "The first 10 attackers of every attacking enemy bubble die to the membran before doing damage", 2, 1)
    # defense = Skill("Defense", [defense1, defense2, defense3, defense4])
    skilltree = SkillTree([AttackSkill.empty(), DefenseSkill.empty(), InfectionSkill.empty()])
    return skilltree


def skilltree_loop(window):
    skilltree = empty()

    while True:
        # clock.tick(120)

        window.fill(dark_blue)
        skilltree.draw(window)

        events = pygame.event.get()
        if pygame.MOUSEMOTION not in [event.type for event in events]:
            x, y = pygame.mouse.get_pos()
            skilltree.draw_tooltip(window, x, y)

        for event in events:
            # close window
            if event.type == pygame.QUIT:
                return "Quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    skilltree.navigate(-1)
                elif event.key == pygame.K_RIGHT:
                    skilltree.navigate(1)
                elif event.key == pygame.K_ESCAPE:
                    return "MainMenu"
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                perk = skilltree.get_perk(x, y)
                if perk is not None:
                    perk.level_up()

        pygame.display.update()
