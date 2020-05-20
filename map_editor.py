from spread_classes import Cell, Player
from utils import *
from game import Map
import math
import maps
from pathlib import Path


def default_players():
    p0 = Player(0, "0", (dim_grey, grey, light_grey), 0.03)    # id 0 stands for NeutralPlayer
    p1 = Player(1, "1", (olive, yellow_green, yellow), 0.12)
    p2 = Player(2, "2", (maroon, brown, peru), 0.4)
    p3 = Player(3, "3", (indian_red, light_coral, light_salmon), 0.2)
    p4 = Player(4, "4", (dark_magenta, medium_violet_red, magenta), 0.1)
    return [p0, p1, p2, p3, p4]

class AdjustRect:
    def __init__(self, screen, rect, cell):
        self.rect = rect
        self.screen = screen
        self.cell = cell
        self.textbox = [
            TextBox("X-Coordinate: ", (rect[0] + rect[3] - 170, rect[1] + 20, 70, 20), cell.center[0]),
            TextBox("Y-Coordinate: ", (rect[0] + rect[3] - 170, rect[1] + 60, 70, 20), cell.center[1]),
            TextBox("Radius: (0 to remove)", (rect[0] + rect[3] - 170, rect[1] + 100, 70, 20), cell.radius),
            TextBox("Player: ", (rect[0] + rect[3] - 170, rect[1] + 140, 70, 20), cell.player_id),
            TextBox("Population: ", (rect[0] + rect[3] - 170, rect[1] + 180, 70, 20), cell.population)
        ]
        self.button = [
            Button("OK", (self.rect[0] + 150, self.rect[1] + 360, 50, 30))
        ]

    def draw(self):
        pygame.draw.rect(self.screen, dark_golden_rod, self.rect, 5)
        pygame.draw.rect(self.screen, gold, (self.rect[0] + 5, self.rect[1] + 5, self.rect[2] - 10, self.rect[3] - 10))
        for box in self.textbox:
            box.draw(self.screen)
        for button in self.button:
            button.draw(self.screen)


class MapEditor:
    def __init__(self, screen):
        self.players = default_players()
        self.map = Map.new()
        self.map.cells = []
        self.screen = screen
        self.buttons = [
            Button("Menu", (window_width - 60, 0, 60, 30))
        ]
        self.messagebox = []
        self.adjustrect = []
        self.textbox = []
        self.box = []
        self.map_buttons = []

    def load(self, map_name):
        self.map = Map.load(map_name)
        player_list = maps.player_list()
        self.map.init_players(player_list)

    def blow_cell(self, pos):
        cell_is_near = False

        for cell in self.map.cells:
            if math.hypot(pos[0] - cell.center[0], pos[1] - cell.center[1]) < cell.radius + 25:
                cell_is_near = True
                if math.hypot(pos[0] - cell.center[0], pos[1] - cell.center[1]) < cell.radius:
                    cell.blow(self.map.cells)
        if not cell_is_near:
            c = Cell((pos[0], pos[1]), 20, 0, 0)
            self.map.cells.append(c)
            self.map.init_players(self.players)

    def adjust_cell(self, cell):
        copy = (cell.center, cell.radius, cell.population)
        for box in self.adjustrect[0].textbox:
            if box.text:
                if box.name == "X-Coordinate: " and int(box.text) < window_width:
                    cell.center = (int(box.text), cell.center[1])
                elif box.name == "Y-Coordinate: " and int(box.text) < window_height:
                    cell.center = (cell.center[0], int(box.text))
                elif box.name == "Radius: (0 to remove)":
                    if int(box.text) in range(20, window_width + 1):
                        cell.update_radius(int(box.text))
                    elif int(box.text) == 0:
                        self.map.cells.remove(cell)
                elif box.name == "Player: " and int(box.text) in range(0, 5):
                    cell.player_id = int(box.text)
                    self.map.init_players(self.players)
                elif box.name == "Population: ":
                    if int(box.text) < math.pow(cell.radius, 2) / 100:
                        cell.population = int(box.text)
                    else:
                        cell.population = int(math.pow(cell.radius, 2) / 100)
        enough_space = True
        for c in filter(lambda x: x != cell, self.map.cells):
            if math.hypot(cell.center[0] - c.center[0], cell.center[1] - c.center[1]) < c.radius + cell.radius + 4:
                enough_space = False
        if not enough_space:
            cell.center = copy[0]
            cell.population = copy[2]
            cell.update_radius(copy[1])
            self.messagebox.append(MessageBox(self.screen, "Cell is to close to another cell!", font))

    def draw(self):
        self.screen.fill(dark_grey_bt)
        for cell in self.map.cells:
            cell.draw(self.screen)
        for box in self.box:
            box.draw(self.screen)
        for obj in self.adjustrect:
            obj.draw()
        for button in self.buttons:
            button.draw(self.screen)
        for button in self.map_buttons:
            button.draw(self.screen)
        for box in self.textbox:
            box.draw(self.screen)
        for box in self.messagebox:
            box.draw(self.screen)
        pygame.display.update()

    def reset_buttons(self):
        self.box.clear()
        self.textbox.clear()
        self.buttons.clear()
        self.map_buttons.clear()
        self.adjustrect.clear()
        self.buttons.append(Button("Menu", (window_width - 60, 0, 60, 30)))

    def button_effect(self, name):
        if name == "Menu":
            self.box.clear()
            self.textbox.clear()
            self.buttons.clear()
            self.map_buttons.clear()
            self.adjustrect.clear()
            self.buttons.append(Button("Close menu", (window_width - 110, 0, 110, 30)))
            self.buttons.append(Button("Save Map", (window_width - 110, 30, 110, 30)))
            self.buttons.append(Button("Load Map", (window_width - 110, 60, 110, 30)))
            self.buttons.append(Button("Exit", (window_width - 110, 90, 110, 30)))
        elif name == "Close menu":
            self.reset_buttons()
        elif name == "Save Map":
            self.reset_buttons()
            self.buttons.append(Button("save", (window_width/2 - 32, window_height/2 + 30, 64, 30)))
            self.buttons.append(Button("cancel", (window_width / 2 - 32, window_height / 2 + 70, 64, 30)))
            self.textbox.append(TextBox("save as:", (window_width/2 - 50, window_height/2, 210, 20), self.map.name[:-1], True, 100))
            self.box.append(Box((window_width/2 - 180, window_height/2 - 10, 360, 120)))
        elif name == "cancel" or name == "ok":
            self.reset_buttons()
        elif name == "save":
            self.map.save(self.textbox[0].text)
            self.reset_buttons()
        elif name == "Load Map":
            self.reset_buttons()
            height = 0
            entries = Path('maps/')
            for entry in entries.iterdir():
                self.map_buttons.append(Button(entry.name[:-4], (window_width / 2 - 100, window_height / 2 - 90 + height, 200, 30)))
                height += 40
            self.buttons.append(Button("ok", (window_width / 2 - 23, window_height / 2 - 90 + height, 46, 30)))
            self.box.append(Box((window_width / 2 - 110, window_height / 2 - 100, 220, height + 50), dim_grey))

    def loop(self):
        clock = pygame.time.Clock()
        while True:
            print(clock)  # delete later
            clock.tick(fps)

            for event in pygame.event.get():

                # close window
                if event.type == pygame.QUIT:
                    return "Quit"

                # select a cell
                if event.type == pygame.MOUSEBUTTONUP:
                    if not self.adjustrect and not self.messagebox and not self.box:
                        for cell in self.map.cells:
                            if math.hypot(event.pos[0] - cell.center[0], event.pos[1] - cell.center[1]) < cell.radius:
                                self.adjustrect.append(AdjustRect(self.screen, (475, 200, 350, 400), cell))

                    # adjusts cell once AdjustRect is closed
                    if self.adjustrect and pygame.Rect(self.adjustrect[0].button[0].rect).collidepoint(event.pos):
                        self.adjust_cell(self.adjustrect[0].cell)
                        self.adjustrect.clear()

                    if self.adjustrect:
                        for box in self.adjustrect[0].textbox:
                            if pygame.Rect(box.rect).collidepoint(event.pos):
                                box.active = True
                                box.text = ""
                            else:
                                box.active = False
                    if self.messagebox and pygame.Rect(self.messagebox[0].ok).collidepoint(event.pos):
                        self.messagebox.clear()

                    # triggers effect for clicked button
                    for button in self.buttons:
                        if pygame.Rect(button.rect).collidepoint(event.pos):
                            if button.name == "Exit":
                                return "MainMenu"
                            else:
                                self.button_effect(button.name)

                    for button in self.map_buttons:
                        if pygame.Rect(button.rect).collidepoint(event.pos):
                            self.load(button.name)

                    # activates textboxes
                    for box in self.textbox:
                        if pygame.Rect(box.rect).collidepoint(event.pos):
                            box.active = True
                            box.text = ""
                        else:
                            box.active = False

                # writes in active textbox
                if event.type == pygame.KEYDOWN:
                    if self.adjustrect:
                        for box in self.adjustrect[0].textbox:
                            if box.active:
                                box.add_text(event.key)
                    else:
                        for box in self.textbox:
                            if box.active:
                                box.add_text(event.key)

            # activate buttons
            x, y = pygame.mouse.get_pos()
            for button in self.buttons:
                if pygame.Rect(button.rect).collidepoint(x, y):
                    button.active = True
                else:
                    button.active = False

            for button in self.map_buttons:
                if pygame.Rect(button.rect).collidepoint(x, y):
                    button.active = True
                else:
                    button.active = False

            if self.adjustrect:
                if pygame.Rect(self.adjustrect[0].button[0].rect).collidepoint(x, y):
                    self.adjustrect[0].button[0].active = True
                else:
                    self.adjustrect[0].button[0].active = False


            # blows cell
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.blow_cell((x, y))

            self.draw()
