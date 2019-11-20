import pickle
from . import Board
import pygame
import socket
import select

debug = True


class Client():
    def __init__(self, host, port, size, grid):
        self.allowedKeys = [
            (pygame.K_LEFT, "left"),
            (pygame.K_RIGHT, "right"),
            (pygame.K_UP, "up"),
            (pygame.K_DOWN, "down")
        ]

        self.host = host
        self.port = port
        self.flag = True

        pygame.init()
        self.win = pygame.display.set_mode((size + 150, size)) # cria o tabuleiro (janela)
        self.clock = pygame.time.Clock() # clock

        self.balancerHost = host
        self.balancerPort = port

        self.outMsg = "OUT"
        self.delimiterMsg = ";"
        self.balancerSuccessMsg = "OK"
        self.serverSuccessMsg = "OK"
        self.balancerFailureMsg = "NOT OK"
        self.requestServerMsg = "PING"
        self.unassignedMsg = "OK"

        self.connServer = None
        self.connBalancer = None

    def prepareMsg(self, msg, dest):
        if dest == 'server':
            return (self.connServer + "_" + msg + self.delimiterMsg).encode('ascii')
        else:
            return (self.connBalancer + "_" + msg + self.delimiterMsg).encode('ascii')

    def getNewDir(self):
        for event in pygame.event.get():
            # event: qualquer evento que acontece (mouse, qlqr tecla, etc)
            if event.type == pygame.QUIT: # se o evento for pra quitar, quita
                flag = False
                pygame.quit()

        keys = pygame.key.get_pressed() # recuperando mapa de teclas

        new_dirnx, new_dirny = (0, 0)
        for key, move in self.allowedKeys: # para cada uma das teclas de interesse
            if keys[key]: # se a tecla foi pressionada, faco os movs dela
                return move

        return None

    def sendDir(self, s):
        try:
            newDir = self.getNewDir()
        except:
            return False

        if newDir:
            s.sendall(self.prepareMsg(newDir, 'server'))
        else:
            s.sendall(self.prepareMsg('NO', 'server'))

        return True

    def processData(self, s):
        data = s.recv(1048576)

        try:
            id, board = pickle.loads(data)
            board.draw(self.win, id)
        except:
            return False

        return True

    def initServerConnection(self, serverSocket, serverSpecs):
        print(serverSpecs)
        serverSocket.connect((serverSpecs[0], int(serverSpecs[1])))
        ip, port = serverSocket.getsockname()
        self.connServer = (ip + ':' + str(port))

        serverSocket.sendall(self.prepareMsg(self.requestServerMsg, 'server'))

        serverFeedback = serverSocket.recv(1048576)
        serverFeedback = serverFeedback.decode()

        if serverFeedback == self.serverSuccessMsg:
            return True
        else:
            return False

    def connectToServerFromBalancer(self, serverSocket):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as balancerSocket:
            balancerSocket.connect((self.balancerHost, self.balancerPort))

            ip, port = balancerSocket.getsockname()
            self.connBalancer = (ip + ':' + str(port))

            balancerSocket.sendall(self.prepareMsg(self.unassignedMsg, 'balancer'))

            serverSpecs = balancerSocket.recv(1048576)
            serverSpecs = serverSpecs.decode()
            serverSpecs = serverSpecs.split('_')

            if self.initServerConnection(serverSocket, serverSpecs):
                balancerSocket.sendall(self.prepareMsg(self.balancerSuccessMsg, 'balancer'))
                return True, serverSpecs
            else:
                balancerSocket.sendall(self.prepareMsg(self.balancerFailureMsg, 'balancer'))
                return False, None

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:

            success, serverSpecs =  self.connectToServerFromBalancer(serverSocket)

            if not success:
                return

            while self.flag:
                pygame.time.delay(50) # pausa em milisegundos
                self.clock.tick(10) # sincronizacao

                if not self.sendDir(serverSocket):
                    break


                if not self.processData(serverSocket):
                    print('Failed to process data')

            serverSocket.sendall(self.prepareMsg(self.outMsg, 'server'))

    def stop(self, sig_num, arg):
        self.flag = False
        pygame.quit()
