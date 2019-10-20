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

def doGameLogic(id_user, move, board):
    board.update({id_user: move})

def manageInput(sock, read_list):
    data = sock.recv(1048576)

    if data:
        move = data.decode('ascii')
        id_user = d[sock.getpeername()]
        return (id_user, move)
    else:
        sock.close()
        read_list.remove(sock)
        return None

def manageOutput(board, socket):
    boardEncoded = pickle.dumps(board)
    sock.send(boardEncoded)


# win = pygame.display.set_mode((500, 500)) # cria o tabuleiro (janela)
clock = pygame.time.Clock() # clock

d = dict()

board = Board(SIZE, GRID)
port = 12346

checkpoint_500ms = time.time()

read_list = []
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setblocking(0)
    s.bind(('', port))
    s.listen(5)
    read_list.append(s)


    while True:
        # pygame.time.delay(50) # pausa em milisegundos
        clock.tick(10) # sincronizacao
        readable, writeable, error = select.select(read_list,[],[])

        # if time.time() -
        if time.time() - checkpoint_500ms >= 0.5:
            board.addSnack()
            checkpoint_500ms = time.time()

        for sock in readable:
            if sock is s:
                conn, info = sock.accept()
                read_list.append(conn)
                print("connection received from ", info)

                d[info] = len(d)

                board.addSnake(d[info])

            else:
                id_user = d[sock.getpeername()]
                data = sock.recv(1048576)
                # print(data)
                # print(board.snakes)
                if data: # se recebi algo valido, imprimo oq recebi e envio de volta
                    board.update({id_user: data.decode('ascii')})
                    # board.draw(win)
                    boardEncoded = pickle.dumps(board)
                    sock.send(boardEncoded)
                else:
                    sock.close()
                    read_list.remove(sock)
                # output = manageInput(socket, read_list)
                #
                # if output is None:
                #     pass
                # id_user, move = output
                #
                # doGameLogic(id_user, move, board)
                # manageOutput(board, socket)
