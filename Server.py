import select
import time
import pickle

class Server():
    def __init__(serverPort):
        pygame.init()
        self.board = Board()
        self.port = serverPort
        self.readList = []
        self.connectedClientsIds = dict()

        self.connectedClients = set()


    def manageInput(s):
        readable, writeable, error = select.select(self.readList,[],[])

        newPlayers, lostConnections, moves, connectedSockets = [], [], [], []

        for sock in readable:
            if sock is s:
                conn, info = sock.accept()
                self.readList.append(conn)
                ip, port = info
                cons = (ip + ':' + str(port))

                self.connectedClientsIds[cons] = len(self.connectedClientsIds)
                self.connectedClients.insert(cons)

                newPlayers.append(self.connectedClientsIds[cons])

            else:
                data = sock.recv(1048576)

                if data:
                    data = data.decode('ascii').split(';')[0]
                    head, body = data.split('_')
                    client = head
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

    def manageGameLogic(newPlayers, lostConnections, moves, snackControl):
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

    def manageOutput(socks_ok):

        for id_user, sock in socks_ok:
            encoded = pickle.dumps((id_user, self.board), protocol=2)
            sock.send(encoded)

    def sendStatsToBalancer(self, balancerSocket):
        encoded = pickle.dumps(connectedClients)
        balancerSocket.send(encoded)

    def run():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientsSocker:
            s.setblocking(0)
            s.bind(('', self.read_list))
            s.listen(5)
            self.readList.append(s)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as balancerSocket:
                # s.setblocking(0)
                # s.bind(('', self.read_list))
                # s.listen(5)
                # self.read_list.append(s)


                while True:
                    # pygame.time.delay(50) # pausa em milisegundos
                    clock.tick(10) # sincronizacao
                    newPlayers, lostConnections, moves, connectedSockets = manageInput(clientsSocker)
                    snackControl = manageGameLogic(newPlayers, lostConnections, moves, snackControl)
                    manageOutput(connectedSockets)

                    if len(self.readList) == 1:
                        break

                    self.sendStatsToBalancer(balancerSocket)
