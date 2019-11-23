from threading import Thread
from subprocess import Popen, TimeoutExpired, PIPE, STDOUT
import atexit
import socket
from select import select
from sys import executable
from time import sleep
from pickle import loads
import random

debug = True

class Balancer():
    def __init__(self, port):

        self.port = port
        self.host = 'localhost'

        self.servers = []

        self.popenFromServer = {}

        # key: ip+port, value: port
        self.serverFromClient = {}

        # key: port, value: set of clients in port
        self.connectedClients = {}
        self.pendingClients = {}

        # key: port, values: UNASGND or ASGND
        self.clientConns2State = {}

        self.clientsReadList = []

        self.maxPerServer = 2
        self.serverCount = 0

        self.createdThreads = []

        self.flag = True

        self.delimiterMsg = ";"
        self.delimiterId = "#"
        self.delimiterBody = "_"

        if debug:
            print('>>> Balancer instanciado')

    def genServerPort(self):
        return random.randint(1000, 64000)

    def initServer(self):
        if debug:
            print(">>> Tentando inicializar um novo server")

        portNumber = None
        while True:
            portNumber = self.genServerPort()
            serverProcess = Popen([executable, "server.py", str(portNumber)], stdout=PIPE)
            output = None
            while True:
                output = serverProcess.stdout.readline()
                if output:
                    break
            if output.decode().strip() == "OK":
                break

        self.servers.append(portNumber)
        self.pendingClients[portNumber] = set()
        self.connectedClients[portNumber] = set()
        self.popenFromServer[portNumber] = serverProcess

        # print(serverProcess)
        thread = Thread(target = self.watchServerThread, args = (portNumber, ))
        thread.start()

        self.createdThreads.append(thread)

        return portNumber

    def isServerFull(self, serverPos):
        serverPort = self.servers[serverPos]
        return len(self.connectedClients[serverPort]) + len(self.pendingClients[serverPort]) >= self.maxPerServer

    def delServer(self):
        for subp in self.popenFromServer.values():
            subp.kill()

    def newClientCase(self, sock):
        conn, info = sock.accept()
        self.clientsReadList.append(conn)
        ip, port = info
        clientIp = (ip + ':' + str(port))
        self.clientConns2State[clientIp] = 'UNASGND'

        if debug:
            print(">>> Caso de novo client: {}".format(clientIp))


    def unassignedClientCase(self, clientIp, clientId, body, sock):
        if debug:
            print(">>> Caso de cliente unssigned: {}".format(clientIp))

        if body == 'OK':
            # designa um server pra ele
            assignedServer = self.findServer()
            self.serverFromClient[clientIp] = assignedServer
            self.pendingClients[assignedServer].add(clientId)
            self.clientConns2State[clientIp] = 'ASGND'


            serverSpecs = "{}_{}".format(self.host, assignedServer)
            sock.send(serverSpecs.encode('ascii'))
        else:
            sock.close()
            self.clientsReadList.remove(sock)
            del self.clientConns2State[clientIp]

    def assignedClientCase(self, clientIp, clientId, body, sock):
        if debug:
            print(">>> Caso de cliente assigned: {}".format(clientIp))

        assignedServer = self.serverFromClient[clientIp]

        if clientId not in self.pendingClients[assignedServer]:
            raise Exception('Cliente nao conectado ao server passado')

        # remove client from self.pendingClients[assignedServer]
        self.pendingClients[assignedServer].remove(clientId)

        if body == 'SUCCESSFUL':
            self.connectedClients[assignedServer].add(clientId)
        elif body == 'UNSUCCESSFUL':
            pass

        sock.close()
        self.clientsReadList.remove(sock)

        del self.clientConns2State[clientIp]

    def processClientsConns(self, clientsSocket):

        readable, _, _ = select(self.clientsReadList,[],[])

        for sock in readable:
            if debug:
                print('>>> Processando socket {}'.format(sock))

            if sock is clientsSocket:
                self.newClientCase(sock)
            else:
                data = sock.recv(1048576)
                print(data)

                if data:
                    data = data.decode('ascii').split(';')[0]
                    head, body = data.split(self.delimiterBody)
                    clientIp, clientId = head.split(self.delimiterId)
                    # head tem o ip e porta do cliente
                    # body tem a mensagem

                    if self.clientConns2State[clientIp] == 'UNASGND':
                        self.unassignedClientCase(clientIp, clientId, body, sock)
                    elif self.clientConns2State[clientIp] == 'ASGND':
                        self.assignedClientCase(clientIp, clientId, body, sock)
                    else:
                        raise Exception('Erro')
                        exit()
                else:
                    sock.close()
                    self.clientsReadList.remove(sock)

    def run(self):
        # tem que ter o socket dos clientes
        # tem q um socket para cada servidor
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientsSocket:
            clientsSocket.setblocking(0)
            clientsSocket.bind(('', self.port))
            clientsSocket.listen(5)
            self.clientsReadList.append(clientsSocket)

            if debug:
                print('>>> Socket para clientes inicializado. Porta: {}'.format(self.port))

            while self.flag:
                # if debug:
                    # print('>>> Processando conexoes de clientes')
                self.processClientsConns(clientsSocket)

        for thread in createdThreads:
            thread.join()

    def findServer(self):
        if debug:
            print(">>> Tentando achar server")
        foundServer = -1

        for i in range(len(self.servers)):
            if not self.isServerFull(i):
                foundServer = self.servers[i]

        if(foundServer == -1):
            foundServer = self.initServer()
        return foundServer

    def prepareMsg(self, msg, conn):
        return (conn + self.delimiterId + "-1" + self.delimiterBody + msg + self.delimiterMsg).encode('ascii')

    def watchServerThread(self, serverPort):
        host = 'localhost'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as watchedServerSocket:
            # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" + host + " " + str(serverPort))
            watchedServerSocket.connect((host, serverPort))

            ip, port = watchedServerSocket.getsockname()
            conn = (ip + ':' + str(port))

            while True:
                watchedServerSocket.send(self.prepareMsg("BAL", conn))
                data = watchedServerSocket.recv(1048576)

                if data[:2] == "OK".encode('ascii'):
                    print(">>> Balancer conectado ao server de porta {}".format(serverPort))
                else:
                    self.connectedClients[serverPort] = loads(data)

    def stop(self, sig_num, arg):
        self.flag = False
