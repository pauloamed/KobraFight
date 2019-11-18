import select
import time
import pickle

class Server():
    def __init__:
        pygame.init()
        self.board = Board()
        self.port = 12345
        self.read_list = []
        self.conn2clientId = dict()


    def manageInput(s):
        readable, writeable, error = select.select(self.read_list,[],[])

        new_players, lost_connections, moves, socks_ok = [], [], [], []

        for sock in readable:
            if sock is s:
                conn, info = sock.accept()
                self.read_list.append(conn)
                print("connection received from ", info)
                ip, port = info
                cons = (ip + ':' + str(port))
                self.conn2clientId[cons] = len(self.conn2clientId)
                new_players.append(self.conn2clientId[cons])

            else:
                data = sock.recv(1048576)

                if data:
                    data = data.decode('ascii').split(';')[0]
                    head, body = data.split('_')
                    id_user = self.conn2clientId[head]

                    if body == 'OUT':
                        lost_connections.append(id_user)
                        sock.close()
                        self.read_list.remove(sock)
                    else:
                        move = body
                        moves.append((id_user, move))
                        socks_ok.append((id_user, sock))

                else:
                    sock.close()
                    self.read_list.remove(sock)

        return new_players, lost_connections, moves, socks_ok

    def manageGameLogic(new_players, lost_connections, moves, checkpoint_500ms):
        for lost_con in lost_connections:
            self.board.killSnake(lost_con)

        for player in new_players:
            self.board.addSnake(player)

        for id_user, move in moves:
            self.board.update({id_user: move})

        if time.time() - checkpoint_500ms >= 0.5:
            self.board.addSnack()
            checkpoint_500ms = time.time()

        return checkpoint_500ms

    def manageOutput(socks_ok):

        for id_user, sock in socks_ok:
            encoded = pickle.dumps((id_user, self.board), protocol=2)
            sock.send(encoded)

    def sendStatsToBalancer(balancerSocket):
        pass

    def run():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setblocking(0)
            s.bind(('', self.read_list))
            s.listen(5)
            self.read_list.append(s)


            while True:
                # pygame.time.delay(50) # pausa em milisegundos
                clock.tick(10) # sincronizacao
                new_players, lost_connections, moves, socks_ok = manageInput(self.read_list, s)
                checkpoint_500ms = manageGameLogic(new_players, lost_connections, moves, checkpoint_500ms)
                manageOutput(socks_ok)

                if len(self.read_list) == 1:
                    break
