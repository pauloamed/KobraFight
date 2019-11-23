from threading import Thread
from subprocess import Popen
import atexit
import socket
from select import select
from sys import executable
from time import sleep

debug = True

class Balancer():
    def __init__(self, port):

        self.port = port
        self.host = 'localhost'

        self.servers = set()

        # key: ip+port, value: port
        self.serverFromClient = dict()

        # key: port, value: set of clients in port
        self.connectedClients = dict()
        self.pendingClients = dict()

        # key: port, values: UNASGND or ASGND
        self.clientConns2State = dict()

        self.clientsReadList = []

        self.maxPerServer = 3
        self.serverCount = 0

        self.createdThreads = []

        self.flag = True

        self.delimiterMsg = ";"

        if debug:
            print('>>> Balancer instanciado')

    def genServerPort(self):
        if len(self.servers) == 0:
            return 12349
        else:
            return 12350

    def initServer(self):
        if debug:
            print(">>> Tentando inicializar um novo server")

        # como criar? processo?
        portNumber = self.genServerPort()
        serverProcess = Popen([executable, "server.py", str(portNumber)])
        sleep(5)

        # retorna (id ou ip+port)
        self.servers.add(portNumber)
        self.pendingClients[portNumber] = set()
        self.connectedClients[portNumber] = set()

        thread = Thread(target = self.watchServerThread, args = (portNumber, ))
        thread.start()

        self.createdThreads.append(thread)

        return portNumber

    def delServer(self):
        # chamada de SO pra dar kill. multiprocessing consegue fz isso?
        pass

    def newClientCase(self, sock):
        conn, info = sock.accept()
        self.clientsReadList.append(conn)
        ip, port = info
        client = (ip + ':' + str(port))
        self.clientConns2State[client] = 'UNASGND'

        if debug:
            print(">>> Caso de novo client: {}".format(client))


    def unassignedClientCase(self, client, body, sock):
        if debug:
            print(">>> Caso de cliente unssigned: {}".format(client))

        if body == 'OK':
            # designa um server pra ele
            assignedServer = self.findServer()
            self.serverFromClient[client] = assignedServer
            self.pendingClients[assignedServer].add(client)
            self.clientConns2State[client] = 'ASGND'


            serverSpecs = "{}_{}".format(self.host, assignedServer)
            sock.send(serverSpecs.encode('ascii'))
        else:
            sock.close()
            self.clientsReadList.remove(sock)
            del self.clientConns2State[client]

    def assignedClientCase(self, client, body, sock):
        if debug:
            print(">>> Caso de cliente assigned: {}".format(client))

        assignedServer = self.serverFromClient[client]

        if client not in self.pendingClients[assignedServer]:
            raise Exception('Cliente nao conectado ao server passado')

        # remove client from self.pendingClients[assignedServer]

        if body == 'SUCCESSFUL':
            self.connectedClients[assignedServer].add(client)
        elif body == 'UNSUCCESSFUL':
            pass

        sock.close()
        self.clientsReadList.remove(sock)

        del self.clientConns2State[client]

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
                    head, body = data.split('_')
                    # head tem o ip e porta do cliente
                    # body tem a mensagem

                    client = head

                    if self.clientConns2State[client] == 'UNASGND':
                        self.unassignedClientCase(client, body, sock)
                    elif self.clientConns2State[client] == 'ASGND':
                        self.assignedClientCase(client, body, sock)
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

        for serverPort in self.servers:
            if len(self.connectedClients[serverPort]) + len(self.pendingClients[serverPort]) < self.maxPerServer:
                foundServer = serverPort

        if(foundServer == -1):
            foundServer = self.initServer()
        return foundServer

    def prepareMsg(self, msg, conn):
        return (conn + "_" + msg + self.delimiterMsg).encode('ascii')

    def watchServerThread(self, serverPort):
        host = 'localhost'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as watchedServerSocket:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" + host + " " + str(serverPort))
            watchedServerSocket.connect((host, serverPort))

            ip, port = watchedServerSocket.getsockname()
            conn = (ip + ':' + str(port))

            while True:
                data = watchedServerSocket.recv(1048576)
                print(data.decode())
                watchedServerSocket.send(self.prepareMsg("oi bb", conn))
                # connectedClients = set(data)
                # fazer diferenca entre self.connectedClients[serverPort] e connectedClients
                # atualizar connectedClients

    def stop(self, sig_num, arg):
        self.flag = False
