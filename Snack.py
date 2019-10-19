from globals import *
from Cube import Cube

class Snack(object):
    def __init__(self, pos):
        self.c = Cube(pos, GREEN_COLOR, 0, 0)

    def draw(self, surface):
        self.c.draw(surface)
