import math
import pygame
import tkinter as tk
from tkinter import simpledialog

from kobra_fight import Board, LoginDialog

import socket
import select
import time
import sys
import signal

import pickle

allowedKeys = [
    (pygame.K_LEFT, "left"),
    (pygame.K_RIGHT, "right"),
    (pygame.K_UP, "up"),
    (pygame.K_DOWN, "down")
]

flag = True

def INT_handler(sig_num, arg):
    flag = False
    pygame.quit()

signal.signal(signal.SIGINT, INT_handler)

def selectIP():
    root = tk.Tk()
    root.withdraw()
    d = LoginDialog(root, "Login")
    return (d.r1, int(d.r2))

def getNewDir():
    for event in pygame.event.get():
        # event: qualquer evento que acontece (mouse, qlqr tecla, etc)
        if event.type == pygame.QUIT: # se o evento for pra quitar, quita
            flag = False
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

    ip, port = s.getsockname()
    conn = (ip + ':' + str(port))

    while flag:
        pygame.time.delay(50) # pausa em milisegundos
        clock.tick(10) # sincronizacao

        try:
            newDir = getNewDir()
        except:
            break

        if newDir:
            s.sendall((conn + "_" + newDir + ";").encode('ascii'))
        else:
            s.sendall((conn + "_NO" + ";").encode('ascii'))

        data = s.recv(1048576)


        try:
            board = pickle.loads(data)
            board.draw(win)
        except:
            print("Failed to load")

    s.sendall((conn + "_OUT" + ";").encode('ascii'))

# print('Received', repr(data))
