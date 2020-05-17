from utils import *
from pathlib import Path

pygame.init()


def empty():
    skilltree = SkillTree([offense_skill.empty(), defense_skill.empty(), infection_skill.empty(), population_skill.empty()])
    return skilltree


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

    def growth_modifier(self, info):
        result = 0
        for perk in self.perks():
            result += perk.growth_modifier(info)
        return result

    def code(self):
        result = ""
        l = [self.name]
        for tier in self.tier_perk_dict:
            for i in self.tier_perk_dict[tier]:
                l += [i.code()]
        for i in l:
            result += str(i) + ", "
        return result

    @classmethod
    def decode(cls, s):
        perks = []
        l = s.split(", ")[:-1]
        name = l[0]
        for i in l[1:]:
            i = i.split(": ")
            perk = empty().find_perk(name, i[0])
            perk.skilled = int(i[1])
            perks += [perk]
        return cls(name, perks)


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

    def growth_modifier(self, info):
        return 0

    def code(self):
        return self.name + ": " + str(self.skilled)

    @classmethod  # not used
    def decode(cls, s):
        l = s.split(": ")
        return cls(l[0], skilled=int(l[1]))


class SkillTree:
    _tooltip_font = pygame.font.SysFont("comincsans", 20)
    phage_dir = "profiles/phages/"
    phage_ending = ".phg"

    def __init__(self, skills, name="unnamed", player=None):
        self.name = name
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
        window.fill(dark_blue)
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

    def growth_modifier(self, info):
        result = 0
        for skill in self.skills:
            result += skill.growth_modifier(info)
        return result

    def find_perk(self, skill_name, perk_name):
        for skill in self.skills:
            if skill.name == skill_name:
                return skill.find_perk(perk_name)
        return None

    def save(self, name="unnamed"):
        self.name = name
        with open(SkillTree.phage_dir + self.name + SkillTree.phage_ending, 'w') as f:
            f.write(self.name + "\n")
            for skill in self.skills:
                f.write(skill.code() + "\n")

    @classmethod
    def load(cls, phage_name):
        with open(SkillTree.phage_dir + phage_name + SkillTree.phage_ending, "r") as f:
            lines = f.readlines()
            name = lines[0]
            skills = []
            for s in lines[1:]:
                skills += [Skill.decode(s)]
            return cls(skills, name)


import offense_skill
import infection_skill
import defense_skill
import population_skill


class SkilltreeMenu:
    def __init__(self, screen):
        self.screen = screen
        self.skilltree = empty()
        self.buttons = [
            Button("Menu", (window_width - 60, 0, 60, 30))
        ]
        self.virus_buttons = []
        self.textbox = []
        self.box = []

    def draw(self):
        self.skilltree.draw(self.screen)
        for box in self.box:
            box.draw(self.screen)
        for button in self.buttons:
            button.draw(self.screen)
        for box in self.textbox:
            box.draw(self.screen)
        pygame.display.update()

    def reset_buttons(self):
        self.box.clear()
        self.textbox.clear()
        self.buttons.clear()
        self.virus_buttons.clear()
        self.buttons.append(Button("Menu", (window_width - 60, 0, 60, 30)))

    def button_effect(self, name):
        if name == "Menu":
            self.box.clear()
            self.textbox.clear()
            self.buttons.clear()
            self.virus_buttons.clear()
            self.buttons.append(Button("Close menu", (window_width - 110, 0, 110, 30)))
            self.buttons.append(Button("Save phage", (window_width - 110, 30, 110, 30)))
            self.buttons.append(Button("Load phage", (window_width - 110, 60, 110, 30)))
            self.buttons.append(Button("Exit", (window_width - 110, 90, 110, 30)))
        elif name == "Close menu":
            self.reset_buttons()
        elif name == "Save phage":
            self.reset_buttons()
            self.buttons.append(Button("save", (window_width / 2 - 32, window_height / 2 + 30, 64, 30)))
            self.buttons.append(Button("cancel", (window_width / 2 - 32, window_height / 2 + 70, 64, 30)))
            self.textbox.append(
                TextBox("save as:", (window_width / 2 - 50, window_height / 2, 210, 20), "new", True, 100))
            self.box.append(Box((window_width / 2 - 180, window_height / 2 - 10, 360, 120)))
        elif name == "cancel" or name == "ok":
            self.reset_buttons()
        elif name == "save":
            self.skilltree.save(self.textbox[0].text)
            self.reset_buttons()
        elif name == "Load phage":
            self.reset_buttons()
            height = 0
            entries = Path('profiles/phages/')
            for entry in entries.iterdir():
                self.virus_buttons.append(
                    Button(entry.name[:-4], (window_width / 2 - 100, window_height / 2 - 90 + height, 200, 30)))
                height += 40
            self.buttons.append(Button("ok", (window_width / 2 - 23, window_height / 2 - 90 + height, 46, 30)))
            self.box.append(Box((window_width / 2 - 110, window_height / 2 - 100, 220, height + 50), dim_grey))

    def skilltree_loop(self):
        while True:
            # clock.tick(120)

            events = pygame.event.get()
            if pygame.MOUSEMOTION not in [event.type for event in events]:
                x, y = pygame.mouse.get_pos()
                self.skilltree.draw_tooltip(self.screen, x, y)

            for event in events:
                # close window
                if event.type == pygame.QUIT:
                    return "Quit"

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.skilltree.navigate(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.skilltree.navigate(1)
                    elif event.key == pygame.K_ESCAPE:
                        return "MainMenu"

                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos
                    perk = self.skilltree.get_perk(x, y)
                    if perk is not None and self.box == []:
                        perk.level_up()

                    for button in self.buttons:
                        if pygame.Rect(button.rect).collidepoint(x, y):
                            if button.name == "Exit":
                                return "MainMenu"
                            else:
                                self.button_effect(button.name)

                    for box in self.textbox:
                        if pygame.Rect(box.rect).collidepoint(x, y):
                            box.active = True
                            box.text = ""
                        else:
                            box.active = False

                # writes in active textbox
                if event.type == pygame.KEYDOWN:
                    for box in self.textbox:
                        if box.active:
                            box.add_text(event.key)

            self.draw()
