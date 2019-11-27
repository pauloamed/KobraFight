import socket
import pygame

import sys

from select import select
from time import time
from pickle import dumps
from kobra_fight import Board

class Server():
    def __init__(self, serverPort):
        self.board = Board()
        self.port = serverPort
        self.readList = []

        self.connectedClientsIds = dict()
        self.connectedClients = set()
        self.newClients = set()
        self.idFromip = {}

        self.balancerSocket = None
        self.balancerIp = None
        self.balancerMsg = "BAL"
        self.serverSuccessMsg = "OK"
        self.delimiterBody = "_"
        self.delimiterId = "#"


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
                    head, body = data.split(self.delimiterBody)
                    clientIp, clientId = head.split(self.delimiterId)

                    if clientIp == self.balancerIp:
                        continue

                    if body == self.balancerMsg:
                        sock.send(self.serverSuccessMsg.encode('ascii'))
                        self.balancerSocket = sock
                        self.balancerIp = clientIp
                        continue

                    if clientIp in self.newClients:
                        sock.send(self.serverSuccessMsg.encode('ascii'))
                        self.newClients.remove(clientIp)
                        self.connectedClientsIds[clientIp] = len(self.connectedClientsIds)
                        self.connectedClients.add(clientId)
                        newPlayers.append(self.connectedClientsIds[clientIp])
                    else:
                        idUser = self.connectedClientsIds[clientIp]
                        if body == 'OUT':
                            lostConnections.append(idUser)
                            sock.close()
                            self.readList.remove(sock)
                            self.connectedClients.remove(clientId)
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

        if time() - snackControl >= 0.5:
            self.board.addSnack()
            snackControl = time()

        return snackControl

    def manageOutput(self, socks_ok):

        for id_user, sock in socks_ok:
            encoded = dumps((id_user, self.board), protocol=2)
            sock.send(encoded)

    def sendStatsToBalancer(self):
        encoded = dumps(self.connectedClients)
        # sys.stderr.write(str(self.port) + " " + str(self.connectedClients) + "\n")
        self.balancerSocket.send(encoded)

    def run(self):
        snackControl = time()
        clock = pygame.time.Clock()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientsSocket:
            clientsSocket.setblocking(0)
            clientsSocket.bind(('', self.port))
            clientsSocket.listen(5)
            self.readList.append(clientsSocket)

            sys.stdout.write("OK\n")
            sys.stdout.flush()
            pygame.init()

            while True:
                # pygame.time.delay(50) # pausa em milisegundos
                clock.tick(10) # sincronizacao
                newPlayers, lostConnections, moves, connectedSockets = self.manageInput(clientsSocket)
                snackControl = self.manageGameLogic(newPlayers, lostConnections, moves, snackControl)
                self.manageOutput(connectedSockets)

                if len(self.readList) == 1:
                    break

                if self.balancerSocket:
                    self.sendStatsToBalancer()
