from globals import *

import math
import pygame
import tkinter as tk
import random

from Snake import Snake
from Cube import Cube
from globals import *
from Snack import Snack

class Board():

    def __init__(self, size, grid):
        self.grid = grid
        self.size = size
        self.snakes = {}
        self.snacks = {}

    def addSnake(self, idUser):
        self.snakes[idUser] = Snake(GREEN_COLOR, self.getValidPos())

    def getValidPos(self):
        positions = {c.pos for snake in self.snakes.values() for c in snake.body} # recupera o corpo da cobra (lista de posicoes)
        positions.union({pos for pos in self.snacks})

        while True:
            x = random.randrange(self.grid) # gera inteiro aleatorio pra posicao x
            y = random.randrange(self.grid) # gera inteiro aleatorio pra posicao y

            # se a posicao aleatoria ta na cobra, gera novamente
            if (x, y) in positions: continue
            else: break

        return (x,y) # retorna posicao gerada

    def addSnack(self, pos=None):
        if pos is None:
            pos = self.getValidPos()
        self.snacks[pos] = Snack(pos)

    def update(self):

        for snake in self.snakes.values():
            snake.move()

            self.eatSnacks()
            self.checkCollisions()

    def eatSnacks(self):
        for snake in self.snakes.values():
            print(snake.body[0].pos, self.snacks)
            if snake.body[0].pos in self.snacks:
                snake.addCube()
                del self.snacks[snake.body[0].pos]

    def checkCollisions(self):
        badBlocks = {}
        for snake in self.snakes.values():
            for c in snake.body:
                if c.pos in badBlocks:
                    badBlocks[c.pos] += 1
                else:
                    badBlocks[c.pos] = 1

        for snake in self.snakes.values():
            if badBlocks[snake.body[0].pos] > 1:
                snake.alive = False
                snake.reset(self.getValidPos())

        del badBlocks


    '''
    desenha uma caixa de mensagem pro user'''
    def message_box(self, subject, content):
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        messagebox.showinfo(subject, content)
        try:
            root.destroy()
        except:
            pass

    '''
    desenha o grid'''
    def drawGrid(self, surface):
        sizeBtwn = self.size // self.grid

        x = 0
        y = 0
        for l in range(self.grid):
            x = x + sizeBtwn
            y = y + sizeBtwn

            pygame.draw.line(surface, WHITE_COLOR, (x, 0),(x, self.size))
            pygame.draw.line(surface, WHITE_COLOR, (0, y),(self.size, y))

    def draw(self, surface):
        surface.fill((0,0,0))

        for snake in self.snakes.values():
            snake.draw(surface)

        for snack in self.snacks.values():
            snack.draw(surface)

        self.drawGrid(surface)
        pygame.display.update()
