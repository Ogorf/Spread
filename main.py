from game import *
from Maps import *

# initialize pygame
pygame.init()

# name window
pygame.display.set_caption("Spread")

# create the game window, size in utils.py
window = pygame.display.set_mode((window_width, window_height))

clock = pygame.time.Clock()
fps = 120


# function in all------------------------------------------------------------------------------------------------------
def button_effect(button):
    if button.name == "Singleplayer":
        MainButton._registry.clear()
        gameloop()
        return False
    elif button.name == "Multiplayer":
        return False
    elif button.name == "Map Editor":
        MainButton._registry.clear()
        mapeditor()
        return False
    elif button.name == "Laboratory":
        return False
    elif button.name == "Quit":
        return False
    elif button.name == "Menu":
        button._registry.remove(button)
        MainButton("Close menu", (window_width - 110, 0, 110, 30))
        MainButton("Main menu", (window_width - 110, 30, 110, 30))
        MainButton("Save", (window_width - 110, 60, 110, 30))
        return True
    elif button.name == "Exit" or button.name == "Main menu":
        MainButton._registry.clear()
        Cell._registry.clear()
        Bubble._registry.clear()
        MessageBox._registry.clear()
        EditorButton._registry.clear()
        TextBox._registry.clear()
        AdjustRect._registry.clear()
        main_menu()
        return False
    elif button.name == "Close menu":
        MainButton._registry.clear()
        MainButton("Menu", (window_width - 60, 0, 60, 30))
        return True
    elif button.name == "Save":      # to-do: check if map is empty
        maps = open("Maps.py", "a")
        maps.write("map_name = [\n")
        for c in filter(lambda x: x != Cell._registry[0], Cell._registry):
            maps.writelines(["Cell((", str(c.xcord), ", ", str(c.ycord), "), ", str(c.radius), ", ", "p" + str(c.player.name), ", ", str(c.population), "),\n"])
        c = Cell._registry[0]
        maps.writelines(["Cell((", str(c.xcord), ", ", str(c.ycord), "), ", str(c.radius), ", ", "p" + str(c.player.name), ", ", str(c.population), ")]\n"])

        MainButton._registry.clear()
        MainButton("Menu", (window_width - 60, 0, 60, 30))
        return True


# functions in main menu ----------------------------------------------------------------------------------------------
def redraw_main_menu_window(screen):
    for button in MainButton._registry:
        button.draw(screen)

    pygame.display.update()


# functions in gameloop -----------------------------------------------------------------------------------------------
def redraw_game_window(screen, game, selected):
    window.fill(dark_blue)

    for obj in selected:
        pygame.draw.circle(screen, (255, 255, 255), (obj.xcord, obj.ycord), obj.radius + 2)

    for button in MainButton._registry:
        button.draw(screen)

    game.draw(window)

    pygame.display.update()


def grow_cell_pop(current_time):
    for obj in Cell._registry:
        obj.grow(current_time)


# funtions for mapeditor --------------------------------------------------------------------------------------------
def blow_cell(pos):
    cell_is_near = False

    for cell in Cell._registry:
        if math.hypot(pos[0] - cell.xcord, pos[1] - cell.ycord) < cell.radius + 25:
            cell_is_near = True
            if math.hypot(pos[0] - cell.xcord, pos[1] - cell.ycord) < cell.radius:
                cell.blow()
    if not cell_is_near:
        Cell((pos[0], pos[1]), 20, p0, 0)


def redraw_editor_window(screen):
    screen.fill(dark_blue)
    for cell in Cell._registry:
        cell.draw(screen)
    for obj in AdjustRect._registry:
        obj.draw(screen)
    for box in TextBox._registry:
        box.draw(screen, font)
    for button in EditorButton._registry:
        button.draw(screen)
    for box in MessageBox._registry:
        box.draw(screen)
    for button in MainButton._registry:
        button.draw(screen)
    pygame.display.update()


def adjust_cell(cell):
    copy = (cell.xcord, cell.ycord, cell.radius, cell.player, cell.population)
    for box in TextBox._registry:
        if box.text:
            if box.name == "X-Coordinate: " and int(box.text) < window_width:
                cell.xcord = int(box.text)
            elif box.name == "Y-Coordinate: " and int(box.text) < window_height:
                cell.ycord = int(box.text)
            elif box.name == "Radius: (0 to remove)":
                if int(box.text) in range(20, window_width + 1):
                    cell.radius = int(box.text)
                elif int(box.text) == 0:
                    Cell._registry.remove(cell)
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
    for c in filter(lambda x: x != cell, Cell._registry):
        if math.hypot(cell.xcord - c.xcord, cell.ycord - c.ycord) < c.radius + cell.radius + 4:
            enough_space = False
    if not enough_space:
        cell.xcord = copy[0]
        cell.ycord = copy[1]
        cell.radius = copy[2]
        cell.switch_player(copy[3])
        cell.population = copy[4]
        MessageBox(window, "Cell is to close to another cell!", font)


# main menu ---------------------------------------------------------------------------------------------------------
def main_menu():
    running_menu = True

    MainButton("Singleplayer", (550, 100, 200, 50))
    MainButton("Multiplayer", (550, 200, 200, 50))
    MainButton("Map Editor", (550, 300, 200, 50))
    MainButton("Laboratory", (550, 400, 200, 50))
    MainButton("Quit", (550, 500, 200, 50))

    while running_menu:
        window.fill(dark_blue)
        print(clock)                                           # delete later

        for event in pygame.event.get():

            # close window
            if event.type == pygame.QUIT:
                running_menu = False

            if event.type == pygame.MOUSEBUTTONUP:
                for button in MainButton._registry:
                    if pygame.Rect(button.rect).collidepoint(event.pos):
                        running_menu = button_effect(button)

        redraw_main_menu_window(window)


# map editor ---------------------------------------------------------------------------------------------------------
def mapeditor():
    running_editor = True
    selected = []

    MainButton("Menu", (window_width - 60, 0, 60, 30))

    while running_editor:
        print(clock)                                     # delete later

        for event in pygame.event.get():

            # close window
            if event.type == pygame.QUIT:
                running_editor = False

            # select a cell
            if event.type == pygame.MOUSEBUTTONUP:
                if not AdjustRect._registry and not MessageBox._registry:
                    for cell in Cell._registry:
                        if math.hypot(event.pos[0] - cell.xcord, event.pos[1] - cell.ycord) < cell.radius:
                            AdjustRect((475, 200, 350, 400), cell)
                            selected.append(cell)

                # adjusts cell once AdjustRect is closed
                if EditorButton._registry and pygame.Rect(EditorButton._registry[0].rect).collidepoint(event.pos):
                    adjust_cell(selected[0])
                    selected.clear()
                    EditorButton._registry[0].effect()

                for box in TextBox._registry:
                    if pygame.Rect(box.rect).collidepoint(event.pos):
                        box.active = True
                        box.text = ""
                    else:
                        box.active = False
                if MessageBox._registry and pygame.Rect(MessageBox._registry[0].ok).collidepoint(event.pos):
                    MessageBox._registry.clear()

                for button in MainButton._registry:
                    if pygame.Rect(button.rect).collidepoint(event.pos):
                        running_editor = button_effect(button)

            if event.type == pygame.KEYDOWN:
                for box in TextBox._registry:
                    if box.active:
                        box.add_text(event.key)

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            pos = pygame.mouse.get_pos()
            blow_cell(pos)

        redraw_editor_window(window)


# game loop-----------------------------------------------------------------------------------------------------------
def gameloop():
    running = True
    selected = []

    cell_list = map_name[:]
    game = Game(cell_list)

    MainButton("Exit", (1240, 0, 60, 30))

    time_before_gameloop = pygame.time.get_ticks()

    while running:
        print(clock)                                    # delete later
        dt = clock.tick(fps)

        for event in pygame.event.get():

            # close window
            if event.type == pygame.QUIT:
                running = False

            # initiating attack/transfer
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for c in Cell._registry:
                    if math.hypot(pos[0] - c.xcord, pos[1] - c.ycord) < c.radius:
                        game.order_attacks(selected, c)
                        break

                for button in MainButton._registry:
                    if pygame.Rect(button.rect).collidepoint(event.pos):
                        running = button_effect(button)

        # selecting Cells
        if pygame.mouse.get_pressed():
            pos = pygame.mouse.get_pos()
            for obj in Cell._registry:
                if math.hypot(obj.xcord - pos[0], obj.ycord - pos[1]) < obj.radius:
                    if obj not in selected:                                          # add (later) and obj.player == p1
                        selected.append(obj)

        if not pygame.mouse.get_pressed()[0]:
            selected.clear()

        game.tick(dt, pygame.time.get_ticks() - time_before_gameloop)

        redraw_game_window(window, game, selected)
# gameloop end -------------------------------------------------------------------------------------------------------


main_menu()
