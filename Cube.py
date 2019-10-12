import pygame
from globals import *

class Cube(object):
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start # tupla com coord x e coord y (x, y)
        self.dirnx = 1
        self.dirny = 0
        self.color = color # cor em rgb do bloco


    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = SIZE // GRID
        i, j = self.pos

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes: # quero desenhar os olhos
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
