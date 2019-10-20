from Cube import Cube
import pygame

class Snake(object):
    def __init__(self, color, pos):
        # pos: posicao inicial
        self.body = []
        self.color = color # cor da cobrinha
        self.head = Cube(pos, color) # cubo indicando a cabeca
        self.body.append(self.head) # body (lista com blocos) sempre tem a head
        self.dirnx = 0 # comeco nao me movendo na vertical
        self.dirny = 1 # comeco me movendo pra direita
        self.alive = True
        self.turns = {} # dicionario guardando onde o mudou de direcao e pra onde

    def move(self, grid, size, dir=None):
        new_dirnx, new_dirny = (0, 0)

        if dir == "up":
            new_dirnx, new_dirny = (0, -1)
        elif dir == "down":
            new_dirnx, new_dirny = (0, 1)
        elif dir == "left":
            new_dirnx, new_dirny = (-1, 0)
        elif dir == "right":
            new_dirnx, new_dirny = (1, 0)

        if (new_dirnx, new_dirny) != (0, 0): # se nao pressionei nenhuma tecla, movo como moveria
            if not (len(self.body) > 2 and (self.dirnx == 0 and new_dirny == -(self.dirny) or new_dirnx == -(self.dirnx))):
                self.dirnx, self.dirny = (new_dirnx, new_dirny)
                self.turns[self.head.pos] = [new_dirnx, new_dirny]

        for i, c in enumerate(self.body):
            p = c.pos # recupera posicao do cubo
            dirx, diry = None, None

            if p in self.turns: # se a posicao eh uma posicao de trocar de direcao
                turn = self.turns[p] # recupera a 'nova' direcao
                if i == len(self.body) - 1: # se to no rabo
                    self.turns.pop(p) # apago a mudada de direcao
                dirx, diry = turn
            else:
                dirx = c.dirnx
                diry = c.dirny

            c.move(dirx, diry)

            if c.pos[0] < 0:
                c.pos = (grid-1, c.pos[1])
            if c.pos[1] < 0:
                c.pos = (c.pos[0], grid-1)
            if c.pos[0] >= grid:
                c.pos = (0 , c.pos[1])
            if c.pos[1] >= grid:
                c.pos = (c.pos[0], 0)

    def reset(self, pos):
        self.head = Cube(pos, self.color)
        self.body = [self.head]
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def die(self):
        self.head = None
        self.alive = False
        self.body = []
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    # def initSnake(self, board):

    def addCube(self):
        tail = self.body[-1] # reucpernado o ultimo cubo
        dx, dy = tail.dirnx, tail.dirny # direcoes do ulimo cubo
        self.body.append(Cube((tail.pos[0]-dx, tail.pos[1]-dy), self.color))
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy


    def draw(self, surface):
        for i, c in enumerate(self.body):
            c.draw(surface, eyes=(i==0))
