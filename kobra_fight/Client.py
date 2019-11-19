import pickle
import Board
import pygame

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
        win = pygame.display.set_mode((size + 150, size)) # cria o tabuleiro (janela)
        self.clock = pygame.time.Clock() # clock

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
            s.sendall((conn + "_" + newDir + ";").encode('ascii'))
        else:
            s.sendall((conn + "_NO" + ";").encode('ascii'))

        return True

    def processData(self, s):
        data = s.recv(1048576)

        try:
            id, board = pickle.loads(data)
            board.draw(win, id)
        except:
            return False

        return True

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            ip, port = s.getsockname()
            conn = (ip + ':' + str(port))

            while self.flag:
                pygame.time.delay(50) # pausa em milisegundos
                clock.tick(10) # sincronizacao

                if !self.sendDir(s):
                    break

                if !self.processData(s):
                    print('Failed to process data')

            s.sendall((conn + "_OUT" + ";").encode('ascii'))

    def stop(self):
        self.flag = False
        pygame.quit()
