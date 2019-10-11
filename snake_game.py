#Snake Tutorial Python

import math
import pygame
import tkinter as tk

from Snake import Snake
from Cube import Cube
from utils import message_box, drawGrid
from globals import *
from Snack import Snack



def redrawWindow(surface):
    global s, snacks
    surface.fill((0,0,0))
    s.draw(surface)
    for snack in snacks:
        snack.draw(surface)
    drawGrid(surface)
    pygame.display.update()

def main():
    global s, snacks

    win = pygame.display.set_mode((SIZE, SIZE)) # cria o tabuleiro (janela)
    s = Snake(RED_COLOR, INITAL_POS_SNAKE) # onde a snake comeca
    snacks = [Snack()] # onde o snack comeca
    clock = pygame.time.Clock() # clock

    while True:
        pygame.time.delay(50) # pausa em milisegundos
        clock.tick(10) # sincronizacao
        s.move() # mexa a cobra

        for i in range(len(snacks)):
            if s.body[0].pos == snacks[i].c.pos:
                s.addCube()
                snacks[i] = Cube(snacks[i].reset([s]), color=GREEN_COLOR) # gera um novo snack
                break

        for x in range(len(s.body)): # para cada bloquinho da cobra
            blockPos = s.body[x].pos # posicao do bloco
            # se houve colisao (TODO ver essa logica)
            if blockPos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', len(s.body)) # imprime o score
                message_box('You Lost!', 'Play again...') # mensagem pro user
                snacks += [s.body]
                s.reset(INITAL_POS_SNAKE) # reseta a cobrinha
                break # sai do for

        redrawWindow(win) # sempre redesenha a janela

    pass

main()
