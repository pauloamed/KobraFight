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
port = 12347

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

        new_players = []
        lost_connections = []
        moves = []

        socks_lc = []
        socks_ok = []

        for sock in readable:
            if sock is s:
                conn, info = sock.accept()
                read_list.append(conn)
                print("connection received from ", info)

                d[info] = len(d)
                new_players.append(d[info])

            else:
                data = sock.recv(1048576)
                id_user = d[sock.getpeername()]

                if data:
                    move = data.decode('ascii')
                    moves.append((id_user, move))
                    socks_ok.append(sock)
                else:
                    lost_connections.append(id_user)
                    socks_lc.append(sock)


        for lost_con in lost_connections:
            # board.getSnake(lost_con).die()
            pass

        for player in new_players:
            board.addSnake(player)

        for id_user, move in moves:
            board.update({id_user: move})

        if time.time() - checkpoint_500ms >= 0.5:
            board.addSnack()
            checkpoint_500ms = time.time()

        boardEncoded = pickle.dumps(board)

        for sock in socks_lc:
            sock.close()
            read_list.remove(sock)

        for sock in socks_ok:
            sock.send(boardEncoded)
