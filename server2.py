# cenario 2

import math
import pygame
import tkinter as tk

from kobra_fight.Board import Board

import socket
import select
import time
import sys

import threading
from server_utils import manageInput, manageGameLogic, manageOutput

fila = []
flag = True

dur = {
    'i_time': 0,
    'o_time': 0,
    'g_time': 0
}



def thread_func(read_list, s, d):
    global flag
    while True:

        t = time.time()
        new_players, lost_connections, moves, socks_ok, d = manageInput(read_list, s, d)
        dur['i_time'] += time.time() - t
        
        fila.append((new_players, lost_connections, moves, socks_ok, d))

        if len(read_list) == 1:
            flag = False
            break


def main():
    global flag
    clock = pygame.time.Clock() # clock

    d = dict()

    board = Board()
    port = 12347

    checkpoint_500ms = time.time()

    read_list = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setblocking(0)
        s.bind(('', port))
        s.listen(5)
        read_list.append(s)

        t = threading.Thread(target=thread_func, args=(read_list, s, d))
        t.start()

        while flag:
            # pygame.time.delay(50) # pausa em milisegundos
            clock.tick(10) # sincronizacao
            while len(fila) != 0:
                new_players, lost_connections, moves, socks_ok, d = fila[0]
                fila.pop(0)

                t = time.time()
                board, checkpoint_500ms = manageGameLogic(board, new_players, lost_connections, moves, checkpoint_500ms)
                dur['g_time'] += time.time() - t

                t = time.time()
                manageOutput(socks_ok, board)
                dur['o_time'] += time.time() - t
        print(dur)


main()
