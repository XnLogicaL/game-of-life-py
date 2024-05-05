# https://github.com/XnLogicaL/game-of-life-python
# MIT License

import pygame
import threading

from libs.screensize import ScreenSize

dead_color = "black"
alive_color = "white"


class Game:
    def __init__(self):
        pygame.init()

        # Create a screensize class for utility purposes
        screen_size = ScreenSize(800, 800)

        self.screen_size = screen_size
        self.window = pygame.display.set_mode(screen_size.to_tuple())
        self.clock = pygame.time.Clock()
        self.running = True
        self.generation = 0
        # This is the grid size, defines the amount of cells in a column or row
        # For example:
        #
        # self.screen_size = ScreenSize(400, 400)
        # self.rect_size = 40
        #
        # [cells/column] = self.screen_size.Y / self.rect_size (10)
        # [cells/row] = self.screen_size.X / self.rect_size (10)
        self.rect_size = 20

        self.create_map()

        # Create and start the runner thread
        # Should be optional
        runner_thread = threading.Thread(target=self.start, daemon=True)
        runner_thread.run()

        self.runner_thread = runner_thread

    def start(self):
        while self.running:
            self.render()
        pygame.quit()

    def handle_event(self, event):
        if event == pygame.QUIT:
            self.running = False

    def draw_cell(self, x, y, color):
        cell_object = pygame.draw.rect(
            self.window,
            color,
            pygame.rect.Rect(
                x,
                y,
                self.rect_size,
                self.rect_size
            ),
            self.rect_size
        ),

        return cell_object

    def kill_cell(self, x, y):
        self.cells[x][y] = {
            "alive": False,
            "object": self.draw_cell(x, y, dead_color)
        }

    def rev_cell(self, x, y):
        self.cells[x][y] = {
            "alive": True,
            "object": self.draw_cell(x, y, alive_color)
        }

    def create_map(self):
        # For the sake of organization and keeping the constructor clean
        # I prefer to put this here instead
        self.cells = {}

        for x in range(int(self.screen_size.X / self.rect_size)):
            self.cells[x * self.rect_size] = {}

            for y in range(int(self.screen_size.Y / self.rect_size)):
                self.kill_cell(x * self.rect_size, y * self.rect_size)

    def get_neighbor(self, x, y):
        if x >= self.screen_size.X or x < 0:
            return None

        if y >= self.screen_size.Y or y < 0:
            return None

        return self.cells[x][y]

    def get_neighbours(self, x, y):
        i = self.rect_size
        neighbours = [
            self.get_neighbor(x + self.rect_size, y),
            self.get_neighbor(x - self.rect_size, y),
            self.get_neighbor(x, y + self.rect_size),
            self.get_neighbor(x, y - self.rect_size),

            self.get_neighbor(x + self.rect_size, y + self.rect_size),
            self.get_neighbor(x - self.rect_size, y - self.rect_size),
            self.get_neighbor(x + self.rect_size, y - self.rect_size),
            self.get_neighbor(x - self.rect_size, y + self.rect_size)
        ]
        filtered = []

        # Clear null neighbours that occur if the cell is adjacent to the edges
        for neighbour in neighbours:
            if neighbour is None:
                continue
            filtered.append(neighbour)

        return filtered

    def update_cell(self, x, y):
        cell = self.cells[x][y]
        neighbours = self.get_neighbours(x, y)

        alive_neighbours = 0
        dead_neighbours = 0

        for neighbour in neighbours:
            if neighbour["alive"]:
                alive_neighbours += 1
            elif not neighbour["alive"]:
                dead_neighbours += 1

        if cell["alive"]:
            if alive_neighbours < 2 or alive_neighbours > 3:
                print("killing cell:[%s, %s]" % (str(x), str(y)))
                cell["alive"] = False
                cell["object"] = self.draw_cell(x, y, dead_color)

        else:
            if alive_neighbours == 3:
                print("reviving cell:[%s, %s]" % (str(x), str(y)))
                cell["alive"] = True
                cell["object"] = self.draw_cell(x, y, alive_color)

    def render(self):
        for event in pygame.event.get():
            self.handle_event(event.type)

        for x in range(int(self.screen_size.X / self.rect_size)):
            for y in range(int(self.screen_size.Y / self.rect_size)):
                self.update_cell(x * self.rect_size, y * self.rect_size)

        pygame.display.flip()

        self.clock.tick(3)
        self.generation += 1


if __name__ == "__main__":
    Game()
