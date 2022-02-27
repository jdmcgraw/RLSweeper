from graphics import *
import numpy as np
import random
import itertools
import re


code_colors = {0: (255, 255, 255),
               1: (40, 0, 245),
               2: (128, 0, 28),
               3: (255, 0, 28),
               4: (15, 0, 123),
               5: (137, 0, 19),
               6: (0, 128, 127),
               7: (0, 0, 0),
               8: (128, 128, 128)}


class Minesweeper(object):

    def __init__(self, height, width, mines):
        print("[INIT] Game Init")
        self.field = None  # This is the hidden game state
        self.display_field = None  # This is the public game state
        self.game_over = False
        self.mines = mines
        self.width, self.height = height, width
        random.seed = 0
        self.win = GraphWin("Minesweeper", 32 * width, 32 * height, autoflush=False)
        self.tiles = {}  # (0, 0) : (graphicsObject, textObject)
        self.draw_field()

        x, y = 0, 0
        while not (0 < x < width) or not (0 < y < height):
            first_move = input("What is your first move? ")
            x, y = [int(k) for k in re.findall(r'\b\d+\b', first_move)]

        self.generate_field(x-1, y-1)
        self.play_square(x, y)

        # click = self.win.getMouse()
        # click_x, click_y = click.x, click.y

        # self.generate_field(*self.clickPos(click_x-1, click_y-1))
        # self.play_square(*self.clickPos(click_x, click_y))

        while True:
            self.draw_field()
            move = input(f"Make a move: ")
            if 'f' not in move.lower():
               self.play_square(*[int(k) for k in re.findall(r'\b\d+\b', move)])
            else:
               self.flag_square(*[int(k) for k in re.findall(r'\b\d+\b', move)])

            # click = self.win.getMouse()
            # click_x, click_y = click.x, click.y
            # self.play_square(*self.clickPos(click_x, click_y))

            if self.check_for_win():
                self.game_over = True

    def clickPos(self, x, y):
        return int((x // 32)+1), int((y // 32)+1)

    def get_neighboring_mines(self, x, y):
        neighbors = self.field[:, max(0, x - 1): min(self.width, x + 2)][max(0, y - 1): min(self.height, y + 2), :]
        return np.sum(neighbors)

    def play_square(self, x=0, y=0, expand=True):
        if x == 0 or y == 0:
            return
        if self.game_over:
            return
        if (x < 1 or x > self.width) or (y < 1 or y > self.height):
            return
        if self.display_field[y - 1][x - 1] == 1:
            return
        self.display_field[y - 1][x - 1] = 1

        neighbors = self.get_neighboring_mines(x-1, y-1)
        if expand and neighbors == 0:
            go_to = []
            for (x_delta, y_delta) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                x_new = x + x_delta
                y_new = y + y_delta
                if 0 <= x_new <= self.width and 0 <= y_new <= self.width:
                    neighbors = self.get_neighboring_mines(x_new-1, y_new-1)
                    if self.field[y_new-1][x_new-1] == 0:
                        if neighbors > 0:
                            self.play_square(x_new, y_new, expand=False)
                        else:
                            go_to.append((x_new, y_new))

            for (x_new, y_new) in go_to:
                self.play_square(x_new, y_new)

    def flag_square(self, x=0, y=0):
        if x == 0 or y == 0:
            return
        if self.game_over:
            return
        if (x < 1 or x > self.width) or (y < 1 or y > self.height):
            return
        if self.display_field[y - 1][x - 1] == 1:
            return
        if self.display_field[y - 1][x - 1] == 2:
            self.display_field[y - 1][x - 1] = 0
        else:
            self.display_field[y - 1][x - 1] = 2

    def check_for_win(self):
        for i, row in enumerate(self.field):
            for k, item in enumerate(row):
                if self.display_field[i][k] == 0:
                    return False
                if self.field[i][k] == 1 and self.display_field[i][k] != 2:
                    return False
        print("\nYOU WIN!\n")
        return True

    def generate_field(self, first_x, first_y, show=False):
        print("[INFO] Generating Minefield")
        self.field = np.zeros(shape=(self.height, self.width))
        self.mines = min(self.mines, self.height * self.width)

        mine_counter = 0
        while mine_counter < self.mines:
            proposed_x = random.randrange(0, self.width)
            proposed_y = random.randrange(0, self.height)
            if (proposed_x, proposed_y) != (first_x, first_y):
                if self.field[proposed_y][proposed_x] == 0:
                    self.field[proposed_y][proposed_x] = 1
                    mine_counter += 1

        self.display_field = np.zeros_like(self.field)  # This is the public game state
        if show:
            print(self.field)

    def draw_field(self):
        for x, y in itertools.product(range(0, self.width), range(0, self.height)):
            r = Rectangle(Point((x*32), (y*32)), Point((x*32) + 32, (y*32) + 32))
            r.setFill(color_rgb(220, 220, 220))
            t = Text(Point((x * 32) + 16, (y * 32) + 16), "")

            if self.field is not None:
                if self.display_field[y][x] == 1:
                    r.setFill(color_rgb(180, 180, 180))

                if self.display_field[y][x] > 0:
                    if self.display_field[y][x] == 2:
                        t.setText("🚩")
                        r.setFill(color_rgb(254, 242, 78))
                    elif (self.field[y][x] == 1) and (self.display_field[y][x] != 2):
                        t.setText("💣")
                        r.setFill(color_rgb(236, 48, 56))
                        self.game_over = True
                    else:
                        neighbors = self.get_neighboring_mines(x, y)
                        if neighbors > 0:
                            t.setText(int(neighbors))
                            t.setTextColor(color_rgb(*code_colors[int(neighbors)]))

            r.draw(self.win)
            t.draw(self.win)
            t.setStyle('bold')
            self.tiles[(x, y)] = (r, t)
            self.win.update()


if __name__ == "__main__":
    Minesweeper(10, 10, 10)
