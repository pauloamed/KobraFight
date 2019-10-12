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

board = Board(500, 20)
# win = pygame.display.set_mode((20, 20)) # cria o tabuleiro (janela)
# clock = pygame.time.Clock() # clock
board.addSnack()

port = 65431

read_list = []
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setblocking(0)
    s.bind(('', port))
    s.listen(5)
    read_list.append(s)


    while True :
        time.sleep(2)
        readable, writeable, error = select.select(read_list,[],[])
        if len(readable) == 2:
            print(readable)
        for sock in readable:
            if sock is s:
                conn, info = sock.accept()
                read_list.append(conn)
                print("connection received from ", info)
            else:
                data = sock.recv(1024)
                print(data)
                if data: # se recebi algo valido, imprimo oq recebi e envio de volta
                    boardEncoded = pickle.dumps(board)
                    sock.send(boardEncoded)
                    board.addSnack()
                else:
                    sock.close()
                    read_list.remove(sock)