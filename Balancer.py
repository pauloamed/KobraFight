from threading import thread

class Balancer():
    def __init__():
        self.quantos_clientes_enviados_pro_server = dict()
        self.quantos_cleintes_conectados_no_server = dict()
        self.max = 1
        self.id_do_server2ip_e_porta = dict()

        self.clientsReadList = []

        self.client2server = dict()
        self.clientConns2State = dict()


    def initServer(self):
        # como criar? processo?
        # usar multiprocessing

        # retorna (id ou ip+port)
        self.quantos_clientes_enviados_pro_server[assignedServer] = 0
        self.quantos_cleintes_conectados_no_server[assignedServer] = 0
        self.trhreaddoserver() # inicar thread q observa o server
        pass

    def delServer(self):
        # chamada de SO pra dar kill. multiprocessing consegue fz isso?
        pass

    def caso1(sock):
        conn, info = sock.accept()
        read_list.append(conn)
        ip, port = info
        cons = (ip + ':' + str(port))
        self.clientConns2State[cons] = 'UNASGND'

    def caso2():
        if body == 'OK':
            # designa um server pra ele
            assignedServer = findServer()
            self.client2server[head] = assignedServer
            self.quantos_clientes_enviados_pro_server[assignedServer] += 1
            sock.send(assignedServer.encode())
            self.clientConns2State[head] = 'ASGND'
        else:
            sock.close()
            read_list.remove(sock)
            del self.clientConns2State[head]

    def caso3():
        assignedServer = self.client2server[head]
        if body == 'SUCCESSFUL':
            self.quantos_cleintes_conectados_no_server[assignedServer] += 1
        elif body == 'UNSUCCESSFUL':
            self.quantos_cleintes_enviados_no_server[assignedServer] -= 1
        sock.close()
        read_list.remove(sock)
        del self.clientConns2State[head]

    def processClientsConns(self, s):
        readable, _, _ = select.select(read_list,[],[])

        for sock in readable:
            if sock is s:
                caso1(sock)
            else:
                data = sock.recv(1048576)

                if data:
                    data = data.decode('ascii').split(';')[0]
                    head, body = data.split('_')
                    # head tem o ip e porta do cliente
                    # body tem a mensagem

                    if self.clientConns2State[head] == 'UNASGND':
                        caso2()
                    elif self.clientConns2State[head] == 'ASGND':
                        caso3()
                    else:
                        print("FUDEU KKKKKK")
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
        serverachado = -1

        for server, qntd in self.quantos_clientes_enviados_pro_server.items():
            if qntd < limite:
                serverachado = server
                break

        if(serverachado == -1):
            serverachado = self.initServer()
        return serverachado

    def trhreaddoserver(self, servertoconnect):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            while True:
                # pergunta quantos tem
                # responde quantos tem
                # atualiza o quantos_cleintes_conectados_no_server
