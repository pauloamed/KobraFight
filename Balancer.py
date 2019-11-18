from threading import thread
import subprocess
import atexit

class Balancer():
    def __init__():

        # key: ip+port, value: id
        self.serversId = dict()

        # key: ip+port, value: id
        self.serverFromClient = dict()

        # key: id, value: set of clients in ip+port
        self.connectedClients = dict()
        self.pendingClients = dict()

        # key: ip+port, values: UNASGND or ASGND
        self.clientConns2State = dict()

        self.clientsReadList = []

        self.maxPerServer = 1
        self.serverCount = 0


    def genServerPort(self):
        return 0

    def initServer(self):
        serverCount += 1
        # como criar? processo?
        portNumber = self.genServerPort()
        serverProcess = subprocess.Popen([sys.executable, "server.py", str(portNumber)])

        # retorna (id ou ip+port)
        self.serverId[portNumber] = serverCount
        self.pendingClients[serverCount] = set()
        self.connectedClients[serverCount] = set()
        self.startServerThread(portNumber) # inicar thread q observa o server

        return serverCount

    def delServer(self):
        # chamada de SO pra dar kill. multiprocessing consegue fz isso?
        pass

    def newClientCase(self, sock):
        conn, info = sock.accept()
        read_list.append(conn)
        ip, port = info
        client = (ip + ':' + str(port))
        self.clientConns2State[client] = 'UNASGND'

    def unassignedCase(self, client):
        if body == 'OK':
            # designa um server pra ele
            assignedServer = findServer()
            self.serverFromClient[client] = assignedServer
            self.pendingClients[assignedServer].insert(client)
            self.clientConns2State[client] = 'ASGND'

            sock.send(assignedServer.encode())
        else:
            sock.close()
            read_list.remove(sock)
            del self.clientConns2State[head]

    def assignedClientCase(self, client):
        assignedServer = self.serverFromClient[client]

        if client not in self.pendingClients[assignedServer]:
            throw 'Cliente nao conectado ao server passado'

        # remove client from self.pendingClients[assignedServer]

        if body == 'SUCCESSFUL':
            self.connectedClients[assignedServer].insert(client)
        elif body == 'UNSUCCESSFUL':
            pass

        sock.close()
        read_list.remove(sock)

        del self.clientConns2State[client]

    def processClientsConns(self, s):
        readable, _, _ = select.select(read_list,[],[])

        for sock in readable:
            if sock is s:
                self.newClientCase(sock)
            else:
                data = sock.recv(1048576)

                if data:
                    data = data.decode('ascii').split(';')[0]
                    head, body = data.split('_')
                    # head tem o ip e porta do cliente
                    # body tem a mensagem

                    client = head

                    if self.clientConns2State[client] == 'UNASGND':
                        self.unassignedClientCase(client)
                    elif self.clientConns2State[client] == 'ASGND':
                        self.assignedClientCase(client)
                    else:
                        throw 'Erro'
                        exit()
                else:
                    sock.close()
                    read_list.remove(sock)

    def run(self):
        # tem que ter o socket dos clientes
        # tem q um socket para cada servidor
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setblocking(0)
            s.bind(('', port))
            s.listen(5)
            read_list.append(s)

            while True:
                self.processClientsConns(s)


    def findServer(self):
        foundServer = -1

        for serverId in serversId.values():
            if len(self.connectedClients[serverId]) + len(self.pendingClients[serverId]) < maxPerServer:
                foundServer = serverId

        if(foundServer == -1):
            foundServer = self.initServer()
        return foundServer

    def startServerThread(self, serverPort):
        host = 'localhost'
        serverId = self.serverId[serverPort]
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, serverPort))

            while True:
                data = s.recv(1048576)
                connectedClients = set(data)

                # fazer diferenca entre self.connectedClients[serverId] e connectedClients
                # atualizar connectedClients
