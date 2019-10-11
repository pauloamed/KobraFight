#Snake Tutorial Python

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
from snake import snake
from cube import cube
from utils import messagebox
from globals import SIZE, GRID



def drawGrid(w, grid, surface):
    sizeBtwn = w // grid

    x = 0
    y = 0
    for l in range(grid):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))


def redrawWindow(surface):
    global grid, size, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(size,grid, surface)
    pygame.display.update()


'''
Gera um snack em uma posicao valida (sem ser numa cobra) aleatoria'''
def randomSnack(grid, snake):

    positions = snake.body # recupera o corpo da cobra (lista de posicoes)

    while True:
        x = random.randrange(grid) # gera inteiro aleatorio pra posicao x
        y = random.randrange(grid) # gera inteiro aleatorio pra posicao y

        # se a posicao aleatoria ta na cobra, gera novamente
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break

    return (x,y) # retorna posicao gerada


def main():
    global s, snack

    win = pygame.display.set_mode((SIZE, SIZE)) # cria o tabuleiro (janela)
    s = snake(RED_COLOR, INITAL_POS_SNAKE) # onde a snake comeca
    snack = cube(randomSnack(GRID, s), color=GREEN_COLOR) # onde o snack comeca
    clock = pygame.time.Clock() # clock

    while True:
        pygame.time.delay(50) # pausa em milisegundos
        clock.tick(10) # sincronizacao
        s.move() # mexa a cobra

        if s.body[0].pos == snack.pos: # se a cobra chegou no snack
            s.addCube() # bota um rabinho na cobra
            snack = cube(randomSnack(grid, s), color=(0,255,0)) # gera um novo snack

        for x in range(len(s.body)): # para cada bloquinho da cobra
            blockPos = s.body[x].pos # posicao do bloco
            # se houve colisao (TODO ver essa logica)
            if blockPos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', len(s.body)) # imprime o score
                message_box('You Lost!', 'Play again...') # mensagem pro user
                s.reset((10,10)) # reseta a cobrinha
                break # sai do for

        redrawWindow(win) # sempre redesenha a janela

    pass

main()
