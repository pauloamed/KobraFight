from globals import *
from Cube import Cube
import random
import pygame


class Snack(object):
    def __init__(self, c=None, fromSnake=False):
        self.fromSnake = fromSnake
        self.c = c
        if self.c == None:
            self.c = Cube(self.gen([]), 0, 0, GREEN_COLOR)

    def draw(self, surface):
        self.c.draw(surface)

    def reset(self, snakes):
        self.c.pos = self.gen(snakes)

    '''
    Gera um snack em uma posicao valida (sem ser numa cobra) aleatoria'''
    def gen(self, snakes):

        positions = {c.pos for snake in snakes for c in snake.body} # recupera o corpo da cobra (lista de posicoes)

        while True:
            x = random.randrange(GRID) # gera inteiro aleatorio pra posicao x
            y = random.randrange(GRID) # gera inteiro aleatorio pra posicao y

            # se a posicao aleatoria ta na cobra, gera novamente
            if (x, y) in positions: continue
            else: break

        return (x,y) # retorna posicao gerada
