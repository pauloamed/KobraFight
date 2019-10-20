from Cube import Cube
import pygame

class Snake(object):
    def __init__(self, color, pos, dir):
        self.color = color # cor da cobrinha
        self.body = [Cube(p, self.color, dir[0], dir[1]) for p in pos]
        self.head = self.body[0]  # cubo indicando a cabeca
        self.dirnx, self.dirny = dir
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

        if (new_dirnx, new_dirny) != (0, 0): # pressionei, mas trtando excecoes
            print(self.dirnx, self.dirny)
            print(new_dirnx, new_dirny)
            if self.dirnx == 0 and new_dirnx != 0:
                self.dirnx, self.dirny = (new_dirnx, new_dirny)
                self.turns[self.head.pos] = [new_dirnx, new_dirny]
            elif self.dirny == 0 and new_dirny != 0:
                self.dirnx, self.dirny = (new_dirnx, new_dirny)
                self.turns[self.head.pos] = [new_dirnx, new_dirny]

        self.moveBody(grid, size)

    def moveBody(self, grid, size):
        for i, c in enumerate(self.body):
            p = c.pos # recupera posicao do cubo
            dirx, diry = None, None

            if p in self.turns: # se a posicao eh uma posicao de trocar de direcao
                turn = self.turns[p] # recupera a 'nova' direcao
                if i == len(self.body) - 1: # se to no rabo
                    self.turns.pop(p) # apago a mudada de direcao
                c.move(turn)
            else:
                c.move()


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
        newPos = (tail.pos[0]-dx, tail.pos[1]-dy)
        self.body.append(Cube(newPos, self.color, dx, dy))


    def draw(self, surface):
        for i, c in enumerate(self.body):
            c.draw(surface, eyes=(i==0))
