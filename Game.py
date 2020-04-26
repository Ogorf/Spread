import math
import SpreadClasses

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
            self.bubbles += [c.attack(cell.center)]

    def tick(self, dt, current_time):
        # grow cells
        for cell in self.cells:
            cell.grow(dt, current_time)
        # moves bubbles
        for bubble in self.bubbles:
            bubble.move(dt)
        # check bubble-bubble-collision
        new_bubbles = []
        while self.bubbles != []:
            bubble = self.bubbles.pop()
            fought = False
            for b in new_bubbles:
                if SpreadClasses.collides(bubble.center, b.center, bubble.radius, b.radius):
                    winner_bubble = b.collide_with_bubble(bubble)
                    if winner_bubble == bubble:
                        new_bubbles.remove(b)
                        new_bubbles += [winner_bubble]
                    elif winner_bubble is None:
                        continue
                    fought = True
                    break
            if not fought:
                new_bubbles += [bubble]
        self.bubbles = new_bubbles

        # checks if bubble collides with cell and calls collide function
        for bubble in self.bubbles:
            for cell in filter(lambda x: x != bubble.mother, self.cells):
                if SpreadClasses.collides(bubble.center, cell.center, bubble.radius, cell.radius):
                    bubble.collide_with_cell(cell)
                    self.bubbles.remove(bubble)

