import numpy as np
import random


class Minesweeper(object):
    def __init__(self):
        print("[INIT] Game Init")
        self.field = None  # This is the hidden game state
        self.display_field = None  # This is the public game state
        self.game_over = False
        self.mines = 10
        random.seed = 0

    def get_neighboring_mines(self, x, y):
        neighbors = self.field[:, x-1:x+2][y-1:y+2, :]
        return np.sum(neighbors)

    def play_square(self, x, y):
        if self.game_over:
            return
        # This is not zero-indexed, because it's on the side of the player's request
        self.display_field[y-1][x-1] = 1
        self.draw_field()

    def flag_square(self, x, y):
        if self.game_over:
            return
        # This is not zero-indexed, because it's on the side of the player's request
        self.display_field[y-1][x-1] = 2
        self.draw_field()

    def draw_field(self):
        print()
        for y, row in enumerate(self.display_field):
            for x, item in enumerate(self.display_field[y]):
                if self.display_field[y][x] == 0:
                    print("⬜", end="\t")
                if self.display_field[y][x] == 1:
                    if self.field[y][x] == 0:
                        print(int(self.get_neighboring_mines(x, y)), end="\t")
                    else:
                        print("💣", end="\t")
                        self.game_over = True
                if self.display_field[y][x] == 2:
                    print("🚩", end="\t")
            print("\n")

    def generate_field(self, height, width, show=False):
        print("[INFO] Generating Minefield")
        self.field = np.zeros(shape=(height, width))
        self.mines = min(self.mines, height*width)

        mine_counter = 0
        while mine_counter < self.mines:
            proposed_x = random.randrange(0, width)
            proposed_y = random.randrange(0, height)
            if self.field[proposed_y][proposed_x] == 0:
                self.field[proposed_y][proposed_x] = 1
                mine_counter += 1

        self.display_field = np.zeros_like(self.field)  # This is the public game state
        if show:
            print(self.field)


if __name__ == "__main__":

    ms = Minesweeper()
    ms.generate_field(10, 10)
    ms.play_square(3, 3)
    ms.flag_square(3, 4)
