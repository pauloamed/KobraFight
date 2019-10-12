#Snake Tutorial Python

import math
import pygame
import tkinter as tk

from Snake import Snake
from Cube import Cube
from globals import *
from Snack import Snack
from Board import Board

import pickle

def main():
    global s, snacks

    win = pygame.display.set_mode((SIZE, SIZE)) # cria o tabuleiro (janela)
    clock = pygame.time.Clock() # clock
    board = Board(SIZE, GRID)

    board.addSnake(0)
    board.addSnack()

    while True:
        pygame.time.delay(50) # pausa em milisegundos
        clock.tick(10) # sincronizacao

        if len(board.snacks) == 0:
            board.addSnack()

        board.update()
        board.draw(win)


    pass

main()
