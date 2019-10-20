# cenario 2

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

fila = []
flag = True

dur = {
    'i_time': 0,
    'o_time': 0,
    'g_time': 0
}

def manageInput(read_list, s, d):
    readable, writeable, error = select.select(read_list,[],[])

    new_players = []
    lost_connections = []
    moves = []
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
                data = data.decode('ascii').split(';')[0]
                head, body = data.split('_')
                id_user = d[head]

                if body == 'OUT':
                    lost_connections.append(id_user)
                    sock.close()
                    read_list.remove(sock)
                else:
                    move = body
                    moves.append((id_user, move))
                    socks_ok.append(sock)

            else:
                sock.close()
                read_list.remove(sock)

    return new_players, lost_connections, moves, socks_ok, d

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

def manageOutput(socks_ok, board):
    boardEncoded = pickle.dumps(board, protocol=2)

    for sock in socks_ok:
        sock.send(boardEncoded)


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
