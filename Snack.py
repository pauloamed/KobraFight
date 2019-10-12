from globals import *
from Cube import Cube

class Snack(object):
    def __init__(self, pos):
        self.c = Cube(pos, 0, 0, GREEN_COLOR)

    def draw(self, surface):
        self.c.draw(surface)