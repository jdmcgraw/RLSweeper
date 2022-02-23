import numpy as np
import random

num_to_emoji = {0: "0️⃣",
                1: "1️⃣",
                2: "2️⃣",
                3: "3️⃣",
                4: "4️⃣",
                5: "5️⃣",
                6: "6️⃣",
                7: "7️⃣",
                8: "8️⃣",
                9: "9️⃣"}


class Minesweeper(object):
    def __init__(self, height, width, mines):
        print("[INIT] Game Init")
        self.field = None  # This is the hidden game state
        self.display_field = None  # This is the public game state
        self.game_over = False
        self.mines = mines
        self.width, self.height = height, width
        random.seed = 0
        self.generate_field()

    def get_neighboring_mines(self, x, y):
        neighbors = self.field[:, max(0, x - 1): min(self.width, x + 2)][max(0, y - 1): min(self.height, y + 2), :]
        return np.sum(neighbors)

    def play_square(self, x, y):
        if self.game_over:
            self.draw_field()
            return
        if (x < 1 or x > self.width) or (y < 1 or y > self.height):
            self.draw_field()
            print("[ERROR] Invalid Position!")
            return
        if (self.display_field[y - 1][x - 1] == 1):
            self.draw_field()
            print("[ERROR] This position has already been sweeped!")
            return
        self.display_field[y - 1][x - 1] = 1
        self.draw_field()

    def flag_square(self, x, y):
        if self.game_over:
            self.draw_field()
            return
        if (x < 1 or x > self.width) or (y < 1 or y > self.height):
            self.draw_field()
            print("[ERROR] Invalid Position!")
            return
        if (self.display_field[y - 1][x - 1] == 1):
            self.draw_field()
            print("[ERROR] This position has already been sweeped!")
            return
        self.display_field[y - 1][x - 1] = 2
        self.draw_field()

    def draw_field(self):
        print()
        for y, row in enumerate(self.display_field):
            for x, item in enumerate(self.display_field[y]):
                if self.display_field[y][x] == 0:
                    print("🟦", end="\t")
                if self.display_field[y][x] == 1:
                    if self.field[y][x] == 0:
                        print(num_to_emoji[int(self.get_neighboring_mines(x, y))]
                              , end="\t")
                    else:
                        print("💣", end="\t")
                        self.game_over = True
                if self.display_field[y][x] == 2:
                    print("🚩", end="\t")
            print("\n")
        if self.game_over:
            print("\nGAME OVER!\n")

    def check_for_win(self):
        for i, row in enumerate(self.field):
            for k, item in enumerate(row):
                if self.display_field[i][k] == 0:
                    return False
                if self.field[i][k] == 1 and self.display_field[i][k] != 2:
                    return False
        print("\nYOU WIN!\n")
        return True

    def generate_field(self, show=False):
        print("[INFO] Generating Minefield")
        self.field = np.zeros(shape=(self.height, self.width))
        self.mines = min(self.mines, self.height * self.width)

        mine_counter = 0
        while mine_counter < self.mines:
            proposed_x = random.randrange(0, self.width)
            proposed_y = random.randrange(0, self.height)
            if self.field[proposed_y][proposed_x] == 0:
                self.field[proposed_y][proposed_x] = 1
                mine_counter += 1

        self.display_field = np.zeros_like(self.field)  # This is the public game state
        if show:
            print(self.field)
