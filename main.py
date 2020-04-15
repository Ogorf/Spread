from spread_classes import *

# initialize pygame
pygame.init()

# name window
pygame.display.set_caption("Spread")

# create the game window, size in utils.py
window = pygame.display.set_mode((window_width, window_height))

clock = pygame.time.Clock()
fps = 120

neutral = Player("0", dim_grey, grey, light_grey, 0.03, 20)
p1 = Player("1", maroon, brown, peru, 0.12, 30)
p2 = Player("2", olive, yellow_green, yellow, 0.4, 70)
p3 = Player("3", indian_red, light_coral, light_salmon, 0.2, 0)
p4 = Player("4", dark_magenta, medium_violet_red, magenta, 0.1, 10)


# functions in main menu ----------------------------------------------------------------------------------------------
def button_effect(button):
    if button.name == "Singleplayer":
        gameloop()
    if button.name == "Multiplayer":
        pass
    if button.name == "Map Editor":
        mapeditor()
    if button.name == "Laboratory":
        pass
    if button.name == "Quit":
        pass


def redraw_main_menu_window(screen):
    for button in MainButton._registry:
        button.draw(screen)

    pygame.display.update()


# functions in gameloop -----------------------------------------------------------------------------------------------
def redraw_game_window(screen, selected):
    window.fill(dark_blue)

    for obj in selected:
        pygame.draw.circle(screen, (255, 255, 255), (obj.xcord, obj.ycord), obj.radius + 2)

    for obj in Cell._registry:
        obj.draw(screen)

    for obj in Bubble._registry:
        obj.draw(screen)

    pygame.display.update()


def grow_cell_pop(current_time):
    for obj in Cell._registry:
        obj.grow(current_time)


def collide(bubble, cell):
    if bubble.player == cell.player:
        cell.population += bubble.population
    else:
        if cell.population >= bubble.population:
            cell.population -= bubble.population
        else:
            cell.population = bubble.population - cell.population
            cell.switch_player(bubble.player)

    bubble.delete()


# funtions for mapeditor --------------------------------------------------------------------------------------------
def blow_cell(pos):
    cell_is_near = False

    for cell in Cell._registry:
        if math.hypot(pos[0] - cell.xcord, pos[1] - cell.ycord) < cell.radius + 25:
            cell_is_near = True
            if math.hypot(pos[0] - cell.xcord, pos[1] - cell.ycord) < cell.radius:
                cell.blow()
    if not cell_is_near:
        Cell((pos[0], pos[1]), 20, neutral, 0)


def redraw_editor_window(screen):
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
                    cell.switch_player(neutral)
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

    MainButton("Singleplayer", 550, 100, 200, 50)
    MainButton("Multiplayer", 550, 200, 200, 50)
    MainButton("Map Editor", 550, 300, 200, 50)
    MainButton("Laboratory", 550, 400, 200, 50)
    MainButton("Quit", 550, 500, 200, 50)

    while running_menu:
        window.fill(dark_blue)
        print(clock)                                           # delete later

        for event in pygame.event.get():

            # close window
            if event.type == pygame.QUIT:
                running_menu = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for button in MainButton._registry:
                    if button.xcord <= pos[0] <= button.xcord + button.width and button.ycord <= pos[1] <= button.ycord + button.height:
                        button_effect(button)
                        running_menu = False

        redraw_main_menu_window(window)

# map editor ---------------------------------------------------------------------------------------------------------
def mapeditor():
    running_editor = True
    selected = []

    while running_editor:
        window.fill(dark_blue)
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

    # add Cells
    Cell((700, 500), 90, p1, p1.startpop)
    Cell((200, 400), 140, p2, p2.startpop)
    Cell((500, 120), 40, p1, p1.startpop)
    Cell((1100, 500), 80, p2, p2.startpop)
    Cell((1100, 120), 60, neutral, neutral.startpop)
    Cell((900, 550), 100, neutral, neutral.startpop)

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
                        for obj in filter(lambda x: x != c, selected):
                            obj.attack((c.xcord, c.ycord))

        # selecting Cells
        if pygame.mouse.get_pressed():
            pos = pygame.mouse.get_pos()
            for obj in Cell._registry:
                if math.hypot(obj.xcord - pos[0], obj.ycord - pos[1]) < obj.radius:
                    if obj not in selected:                                          # add (later) and obj.player == p1
                        selected.append(obj)

        if not pygame.mouse.get_pressed()[0]:
            selected.clear()

        # moves bubbles
        for bubble in Bubble._registry:
            bubble.move(dt)

        # checks if bubble collides with cell and calls collide function
        for bubble in Bubble._registry:
            for cell in filter(lambda x: x != bubble.mother, Cell._registry):
                if math.hypot(bubble.xcord - cell.xcord, bubble.ycord - cell.ycord) < cell.radius:
                    collide(bubble, cell)

        grow_cell_pop(pygame.time.get_ticks() - time_before_gameloop)

        redraw_game_window(window, selected)
# gameloop end -------------------------------------------------------------------------------------------------------


main_menu()

