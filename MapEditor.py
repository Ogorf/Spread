from SpreadClasses import Cell
from Maps import *
import math


class AdjustRect:
    def __init__(self, screen, rect, cell):
        self.rect = rect
        self.screen = screen
        self.cell = cell
        self.textbox = [
            TextBox("X-Coordinate: ", (rect[0] + rect[3] - 170, rect[1] + 20, 70, 20), cell.center[0], grey,
                    (255, 255, 255)),
            TextBox("Y-Coordinate: ", (rect[0] + rect[3] - 170, rect[1] + 60, 70, 20), cell.center[1], grey,
                    (255, 255, 255)),
            TextBox("Radius: (0 to remove)", (rect[0] + rect[3] - 170, rect[1] + 100, 70, 20), cell.radius, grey,
                    (255, 255, 255)),
            TextBox("Player: ", (rect[0] + rect[3] - 170, rect[1] + 140, 70, 20), cell.player.name, grey,
                    (255, 255, 255)),
            TextBox("Population: ", (rect[0] + rect[3] - 170, rect[1] + 180, 70, 20), cell.population, grey,
                    (255, 255, 255))
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
        self.cells = []
        self.screen = screen
        self.buttons = [
            Button("Menu", (window_width - 60, 0, 60, 30))
        ]
        self.messagebox = []
        self.adjustrect = []

    def blow_cell(self, pos):
        cell_is_near = False

        for cell in self.cells:
            if math.hypot(pos[0] - cell.center[0], pos[1] - cell.center[1]) < cell.radius + 25:
                cell_is_near = True
                if math.hypot(pos[0] - cell.center[0], pos[1] - cell.center[1]) < cell.radius:
                    cell.blow(self.cells)
        if not cell_is_near:
            self.cells.append(Cell((pos[0], pos[1]), 20, p0, 0))

    def adjust_cell(self, cell):
        copy = (cell.center, cell.radius, cell.player, cell.population)
        for box in self.adjustrect[0].textbox:
            if box.text:
                if box.name == "X-Coordinate: " and int(box.text) < window_width:
                    cell.center = (int(box.text), cell.center[1])
                elif box.name == "Y-Coordinate: " and int(box.text) < window_height:
                    cell.center = (cell.center[0], int(box.text))
                elif box.name == "Radius: (0 to remove)":
                    if int(box.text) in range(20, window_width + 1):
                        cell.radius = int(box.text)
                    elif int(box.text) == 0:
                        self.cells.remove(cell)
                elif box.name == "Player: " and int(box.text) in range(0, 5):
                    if int(box.text) == 0:
                        cell.switch_player(p0)
                    elif int(box.text) == 1:
                        cell.switch_player(p1)
                    elif int(box.text) == 2:
                        cell.switch_player(p2)
                    elif int(box.text) == 3:
                        cell.switch_player(p3)
                    elif int(box.text) == 4:
                        cell.switch_player(p4)
                elif box.name == "Population: ":
                    if int(box.text) < math.pow(cell.radius, 2) / 100:
                        cell.population = int(box.text)
                    else:
                        cell.population = int(math.pow(cell.radius, 2) / 100)
        enough_space = True
        for c in filter(lambda x: x != cell, self.cells):
            if math.hypot(cell.center[0] - c.center[0], cell.center[1] - c.center[1]) < c.radius + cell.radius + 4:
                enough_space = False
        if not enough_space:
            cell.center = copy[0]
            cell.radius = copy[1]
            cell.switch_player(copy[2])
            cell.population = copy[3]
            self.messagebox.append(MessageBox(self.screen, "Cell is to close to another cell!", font))

    def draw(self):
        self.screen.fill(dark_blue)
        for cell in self.cells:
            cell.draw(self.screen)
        for obj in self.adjustrect:
            obj.draw()
        for button in self.buttons:
            button.draw(self.screen)
        for box in self.messagebox:
            box.draw(self.screen)
        pygame.display.update()

    def save(self):
        maps = open("Maps.py", "a")
        maps.write("map_name = [\n")
        if self.cells:
            for c in filter(lambda x: x != self.cells[0], self.cells):
                maps.writelines(
                    ["((", str(c.center[0]), ", ", str(c.center[1]), "), ", str(c.radius), ", ",
                     "p" + str(c.player.name), ", ", str(c.population), "),\n"])
            c = self.cells[0]
            maps.writelines(["((", str(c.center[0]), ", ", str(c.center[1]), "), ", str(c.radius), ", ",
                             "p" + str(c.player.name), ", ", str(c.population), ")]\n"])

        self.buttons.clear()
        self.buttons.append(Button("Menu", (window_width - 60, 0, 60, 30)))

    def loop(self):

        while True:
            print(clock)  # delete later

            for event in pygame.event.get():

                # close window
                if event.type == pygame.QUIT:
                    return "Quit"

                # select a cell
                if event.type == pygame.MOUSEBUTTONUP:
                    if not self.adjustrect and not self.messagebox:
                        for cell in self.cells:
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

                    for button in self.buttons:
                        if pygame.Rect(button.rect).collidepoint(event.pos):
                            if button.name == "Menu":
                                self.buttons.clear()
                                self.buttons.append(Button("Close menu", (window_width - 110, 0, 110, 30)))
                                self.buttons.append(Button("Main menu", (window_width - 110, 30, 110, 30)))
                                self.buttons.append(Button("Save", (window_width - 110, 60, 110, 30)))
                            elif button.name == "Close menu":
                                self.buttons.clear()
                                self.buttons.append(Button("Menu", (window_width - 60, 0, 60, 30)))
                            elif button.name == "Main menu":
                                return "MainMenu"
                            elif button.name == "Save":
                                self.save()

                if event.type == pygame.KEYDOWN and self.adjustrect:
                    for box in self.adjustrect[0].textbox:
                        if box.active:
                            box.add_text(event.key)

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                pos = pygame.mouse.get_pos()
                self.blow_cell(pos)

            self.draw()
