import math
import pygame
import tkinter as tk

from Snake import Snake
from Cube import Cube
from globals import *
from Snack import Snack
from Board import Board

import socket
import select
import time
import sys

import pickle

allowedKeys = [
    (pygame.K_LEFT, "left"),
    (pygame.K_RIGHT, "right"),
    (pygame.K_UP, "up"),
    (pygame.K_DOWN, "down")
]

def getNewDir():
    for event in pygame.event.get():
        # event: qualquer evento que acontece (mouse, qlqr tecla, etc)
        if event.type == pygame.QUIT: # se o evento for pra quitar, quita
            pygame.quit()

    keys = pygame.key.get_pressed() # recuperando mapa de teclas

    new_dirnx, new_dirny = (0, 0)
    for key, move in allowedKeys: # para cada uma das teclas de interesse
        if keys[key]: # se a tecla foi pressionada, faco os movs dela
            return move

    return None

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432     # The port used by the server

win = pygame.display.set_mode((50, 500)) # cria o tabuleiro (janela)
clock = pygame.time.Clock() # clock

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        pygame.time.delay(40) # pausa em milisegundos
        clock.tick(10) # sincronizacao
        newDir = getNewDir()
        if newDir:
            s.sendall(newDir.encode('ascii'))
        else:
            s.sendall("no".encode('ascii'))
        data = s.recv(1024)
        # print(data)
        board = pickle.loads(data)
        # print(board.snakes)
        # print(board.snacks)
        # board.draw(win)


# print('Received', repr(data))
