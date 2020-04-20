import math

class Game:
    def __init__(self, cell_list):
        pl = []
        for cell in cell_list:
            if not cell.player in pl:
                pl += [cell.player]
        self.players = pl
        self.cells = cell_list
        self.bubbles = []


    def draw(self, window):
        for cell in self.cells:
            cell.draw(window)
        for bubble in self.bubbles:
            bubble.draw(window)

    def order_attacks(self, cell_list, cell):
        for c in filter(lambda x: x != cell, cell_list):
            self.bubbles += [c.attack((cell.xcord, cell.ycord))]

    def tick(self, dt, time_since_start):
        # moves bubbles
        for bubble in self.bubbles:
            bubble.move(dt)

        # checks if bubble collides with cell and calls collide function
        for bubble in self.bubbles:
            for cell in filter(lambda x: x != bubble.mother, self.cells):
                if math.hypot(bubble.xcord - cell.xcord, bubble.ycord - cell.ycord) < cell.radius:
                    bubble.collide(cell)
                    self.bubbles.remove(bubble)
        # grow cells
        for cell in self.cells:
            cell.grow(time_since_start)

