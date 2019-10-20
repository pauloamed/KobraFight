import math
import pygame
import tkinter as tk
from tkinter import simpledialog

from Snake import Snake
from Cube import Cube
from globals import *
from Snack import Snack
from Board import Board
from dialogs import LoginDialog

import socket
import select
import time
import sys

import pickle
import struct

allowedKeys = [
    (pygame.K_LEFT, "left"),
    (pygame.K_RIGHT, "right"),
    (pygame.K_UP, "up"),
    (pygame.K_DOWN, "down")
]

def selectIP():
    root = tk.Tk()
    root.withdraw()
    d = LoginDialog(root, "Login")
    return (d.r1, int(d.r2))

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

HOST, PORT = selectIP()

win = pygame.display.set_mode((500, 500)) # cria o tabuleiro (janela)
clock = pygame.time.Clock() # clock



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        pygame.time.delay(50) # pausa em milisegundos
        clock.tick(10) # sincronizacao
        newDir = getNewDir()
        if newDir:
            s.sendall(newDir.encode('ascii'))
        else:
            s.sendall("no".encode('ascii'))

        data = s.recv(1048576)
        # data = s.recv( struct.calcsize("!I") )
        # print(data)
        # print(int.from_bytes(data, "big"))
        # print(struct.calcsize("!I"))
        # body_size = struct.unpack("!I", data)[0]
        # body = s.recv( body_size )
        # board = pickle.loads(body)

        try:
            board = pickle.loads(data)
        except:
            print("Failed to load")
            # print(board.snakes)
            # print(board.snacks)
        board.draw(win)



# print('Received', repr(data))
