# cenario 1
import math
import pygame
import tkinter as tk

from kobra_fight.Board import Board

import socket
import select
import time
import sys

import pickle

import threading


def manageInput(read_list, s, d):
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
            ip, port = info
            cons = (ip + ':' + str(port))
            d[cons] = len(d)
            new_players.append(d[cons])

        else:
            data = sock.recv(1048576)

            if data:
                data = data.decode('ascii')
                head, body = data.split('_')
                id_user = d[head]

                if body == 'OUT':
                    lost_connections.append(id_user)
                    socks_lc.append(sock)
                else:
                    move = body
                    moves.append((id_user, move))
                    socks_ok.append(sock)

            else:
                socks_lc.append(sock)

    return new_players, lost_connections, moves, socks_lc, socks_ok


def manageGameLogic(board, new_players, lost_connections, moves, checkpoint_500ms):
    for lost_con in lost_connections:
        board.killSnake(lost_con)

    for player in new_players:
        board.addSnake(player)

    for id_user, move in moves:
        board.update({id_user: move})

    if time.time() - checkpoint_500ms >= 0.5:
        board.addSnack()
        checkpoint_500ms = time.time()

    return board, checkpoint_500ms

def manageOutput(socks_lc, socks_ok, board, read_list):
    boardEncoded = pickle.dumps(board, protocol=2)

    for sock in socks_lc:
        sock.close()
        read_list.remove(sock)

    for sock in socks_ok:
        sock.send(boardEncoded)


def thread_func(port):
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
            print(read_list)
            new_players, lost_connections, moves, socks_lc, socks_ok = manageInput(read_list, s, d)
            board, checkpoint_500ms = manageGameLogic(board, new_players, lost_connections, moves, checkpoint_500ms)
            manageOutput(socks_lc, socks_ok, board, read_list)


def main():
    port = 12347


    t = threading.Thread(target=thread_func, args=(port,))
    t.start()


main()
