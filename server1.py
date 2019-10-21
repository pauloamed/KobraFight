# cenario 1
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

def thread_func(port, dur):
    read_list = []
    clock = pygame.time.Clock() # clock
    checkpoint_500ms = time.time()
    d = dict()
    board = Board()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setblocking(0)
        s.bind(('', port))
        s.listen(5)
        read_list.append(s)
        while True:
            # pygame.time.delay(50) # pausa em milisegundos
            clock.tick(10) # sincronizacao

            t = time.time()
            new_players, lost_connections, moves, socks_ok, d = manageInput(read_list, s, d)
            dur['io_time'] += time.time() - t

            t = time.time()
            board, checkpoint_500ms = manageGameLogic(board, new_players, lost_connections, moves, checkpoint_500ms)
            dur['game_logic_time'] += time.time() - t

            t = time.time()
            manageOutput(socks_ok, board)
            dur['io_time'] += time.time() - t

            if(len(read_list) == 1):
                break

def main():
    port = 12347

    dur = {
        'io_time': 0,
        'game_logic_time': 0
    }

    t = threading.Thread(target=thread_func, args=(port, dur))
    t.start()
    t.join()

    print(dur)


main()
