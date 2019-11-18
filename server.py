import math
import pygame
import tkinter as tk

from kobra_fight.Board import Board

import socket
import time
import sys

from server_utils import manageInput, manageGameLogic, manageOutput

def main():
    pygame.init()

    clock = pygame.time.Clock() # clock
    d = dict()

    board = Board()
    #port = 12345

    # --------------- Número da porta passado pelo popen ---------------
    param = sys.argv[1:]
    print(param)

    port = int(param[0])
    # --------------- --------------- --------------- ---------------

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
            new_players, lost_connections, moves, socks_ok, d = manageInput(read_list, s, d)
            board, checkpoint_500ms = manageGameLogic(board, new_players, lost_connections, moves, checkpoint_500ms)
            manageOutput(socks_ok, board)

            if len(read_list) == 1:
                break

main()
