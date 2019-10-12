from globals import SIZE, GRID
from Cube import Cube
import pygame

class Snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        # pos: posicao inicial
        self.color = color # cor da cobrinha
        self.head = Cube(pos) # cubo indicando a cabeca
        self.body.append(self.head) # body (lista com blocos) sempre tem a head
        self.dirnx = 0 # comeco nao me movendo na vertical
        self.dirny = 1 # comeco me movendo pra direita
        self.alive = True
        self.turns = {} # dicionario guardando onde o mudou de direcao e pra onde

    def move(self):
        for event in pygame.event.get():
            # event: qualquer evento que acontece (mouse, qlqr tecla, etc)
            if event.type == pygame.QUIT: # se o evento for pra quitar, quita
                pygame.quit()

        keys = pygame.key.get_pressed() # recuperando mapa de teclas

        new_dirnx, new_dirny = (0, 0)
        for key, move in self.allowedKeys: # para cada uma das teclas de interesse
            if keys[key]: # se a tecla foi pressionada, faco os movs dela
                new_dirnx, new_dirny = move
                break

        if (new_dirnx, new_dirny) != (0, 0): # se nao pressionei nenhuma tecla, movo como moveria
            if not (len(self.body) > 2 and (self.dirnx == 0 and new_dirny == -(self.dirny) or new_dirnx == -(self.dirnx))):
                self.dirnx, self.dirny = (new_dirnx, new_dirny)
                self.turns[self.head.pos] = [new_dirnx, new_dirny]

        for i, c in enumerate(self.body):
            p = c.pos # recupera posicao do cubo
            if p in self.turns: # se a posicao eh uma posicao de trocar de direcao
                turn = self.turns[p] # recupera a 'nova' direcao
                if i == len(self.body) - 1: # se to no rabo
                    self.turns.pop(p) # apago a mudada de direcao
                c.move(turn[0],turn[1]) # mova o cubo pra sua direcao
            else: # se nao to numa posicao de trocar de direcao
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (GRID-1, c.pos[1]) # se tenho q ir pra esq e
                elif c.dirnx == 1 and c.pos[0] >= GRID-1:
                    c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= GRID-1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0],GRID-1)
                else: c.move(c.dirnx,c.dirny)
                # if c.pos[0] < 0: c.pos = (GRID-1, c.pos[1])
                # if c.pos[0] == GRID: c.pos = (0, c.pos[1])
                # if c.pos[1] < 0: c.pos = (c.pos[0], GRID-1)
                # if c.pos[1] == GRID: c.pos = (c.pos[0], 0)



    def reset(self, pos):
        self.head = Cube(pos)
        self.body = [self.head]
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1


    def addCube(self):
        tail = self.body[-1] # reucpernado o ultimo cubo
        dx, dy = tail.dirnx, tail.dirny # direcoes do ulimo cubo
        self.body.append(Cube((tail.pos[0]-dx, tail.pos[1]-dy))) # TODO
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy


    def draw(self, surface):
        for i, c in enumerate(self.body):
            c.draw(surface, eyes=(i==0))
