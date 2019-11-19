import pickle
from . import Board
import pygame
import socket
import select

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

        self.balancerHost = None
        self.balancerPort = None

        self.outMsg = "OUT"
        self.delimiterMsg = ";"
        self.balancerSuccessMsg = "OK"
        self.serverSuccessMsg = "OK"
        self.balancerFailureMsg = "NOT OK"
        self.requestServerMsg = "PING"

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

    def sendDir(self, s, conn):
        try:
            newDir = self.getNewDir()
        except:
            return False

        if newDir:
            s.sendall((conn + "_" + newDir + ";").encode('ascii'))
        else:
            s.sendall((conn + "_NO" + ";").encode('ascii'))

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
        serverSocket.connect((self.host, self.port))

        serverSocket.sendall(self.requestServerMsg.encode('ascii'))

        serverFeedback = s.recv(1048576)

        if serverFeedback ==

        return True

    def connectToServerFromBalancer(self, serverSocket):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as balancerSocket:
            balancerSocket.connect((self.balancerHost, self.balancerPort))

            serverSpecs = balancerSocket.recv(1048576)

            if self.initServerConnection(serverSocket, serverSpecs):
                balancerSocket.sendall(self.balancerSuccessMsg.encode("ascii"))
                return True, serverSpecs
            else:
                balancerSocket.sendall(self.balancerFailureMsg.encode("ascii"))
                return False, None

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:

            success, serverSpecs =  self.connectToServerFromBalancer(serverSocket):

            if not success:
                return

            ip, port = serverSocket.getsockname()
            conn = (ip + ':' + str(port))

            while self.flag:
                pygame.time.delay(50) # pausa em milisegundos
                self.clock.tick(10) # sincronizacao

                if not self.sendDir(serverSocket, conn):
                    break

                if not self.processData(serverSocket):
                    print('Failed to process data')

            s.sendall((conn + "_" + self.outMsg + self.delimiterMsg).encode('ascii'))

    def stop(self, sig_num, arg):
        self.flag = False
        pygame.quit()
