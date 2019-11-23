import socket
import pygame
import tkinter as tk

from select import select
from time import time
from pickle import dumps
from kobra_fight import Board

class Server():
    def __init__(self, serverPort):
        pygame.init()
        self.board = Board()
        self.port = serverPort
        self.readList = []

        self.connectedClientsIds = dict()
        self.connectedClients = set()
        self.newClients = set()

        self.socket_do_balanceador = None
        self.ip_do_balaneador = None
        self.balancerMsg = "BAL"
        self.serverSuccessMsg = "OK"


    def manageInput(self, clientsSocket):
        readable, writeable, error = select(self.readList,[],[])

        newPlayers, lostConnections, moves, connectedSockets = [], [], [], []

        for sock in readable:
            if sock is clientsSocket:
                conn, info = sock.accept()
                self.readList.append(conn)
                ip, port = info
                cons = (ip + ':' + str(port))
                self.newClients.add(cons)

            else:
                data = sock.recv(1048576)

                if data:
                    data = data.decode('ascii').split(';')[0]
                    head, body = data.split('_')
                    client = head

                    if body == self.balancerMsg:
                        self.socket_do_balanceador = sock
                        self.ip_do_balaneador = client
                        continue

                    if head == self.ip_do_balaneador:
                        continue

                    if client in self.newClients:
                        sock.send(self.serverSuccessMsg.encode('ascii'))
                        self.newClients.remove(client)
                        self.connectedClientsIds[client] = len(self.connectedClientsIds)
                        self.connectedClients.add(client)
                        newPlayers.append(self.connectedClientsIds[client])
                    else:
                        idUser = self.connectedClientsIds[client]
                        if body == 'OUT':
                            lostConnections.append(idUser)
                            sock.close()
                            self.readList.remove(sock)
                            self.connectedClients.remove(client)
                        else:
                            move = body
                            moves.append((idUser, move))
                            connectedSockets.append((idUser, sock))

                else:
                    sock.close()
                    self.readList.remove(sock)

        return newPlayers, lostConnections, moves, connectedSockets

    def manageGameLogic(self, newPlayers, lostConnections, moves, snackControl):
        for lostCon in lostConnections:
            self.board.killSnake(lostCon)

        for player in newPlayers:
            self.board.addSnake(player)

        for idUser, move in moves:
            self.board.update({idUser: move})

        if time.time() - snackControl >= 0.5:
            self.board.addSnack()
            snackControl = time.time()

        return snackControl

    def manageOutput(self, socks_ok):

        for id_user, sock in socks_ok:
            encoded = pickle.dumps((id_user, self.board), protocol=2)
            sock.send(encoded)

    def sendStatsToBalancer(self):
        # encoded = pickle.dumps(connectedClients)
        self.socket_do_balanceador.send("oi bb".encode('ascii'))

    def run(self):
        snackControl = time.time()
        clock = pygame.time.Clock()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientsSocket:
            clientsSocket.setblocking(0)
            clientsSocket.bind(('', self.port))
            clientsSocket.listen(5)
            self.readList.append(clientsSocket)

            while True:
                # pygame.time.delay(50) # pausa em milisegundos
                clock.tick(10) # sincronizacao
                newPlayers, lostConnections, moves, connectedSockets = self.manageInput(clientsSocket)
                snackControl = self.manageGameLogic(newPlayers, lostConnections, moves, snackControl)
                self.manageOutput(connectedSockets)

                if len(self.readList) == 1:
                    break

                if self.socket_do_balanceador:
                    self.sendStatsToBalancer()
