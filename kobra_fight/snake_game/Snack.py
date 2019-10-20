from .Cube import Cube
from .globals import GREEN_COLOR

class Snack(object):
    def __init__(self, pos):
        self.c = Cube(pos, GREEN_COLOR, 0, 0)

    def draw(self, surface, size, grid):
        self.c.draw(surface, size, grid)
