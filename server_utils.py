import select
import time
import pickle

def manageInput(read_list, s, d):
    readable, writeable, error = select.select(read_list,[],[])

    new_players, lost_connections, moves, socks_ok = [], [], [], []

    print("read_list:" + str(read_list))
    print("s: " + str(s))
    print("readable: " + str(readable))
    for sock in readable:
        if sock is s:
            conn, info = sock.accept()
            read_list.append(conn)
            print("connection received from ", info)
            ip, port = info
            cons = (ip + ':' + str(port))
            d[cons] = len(d)
            new_players.append(d[cons])

        else:
            data = sock.recv(1048576)

            if data:
                data = data.decode('ascii').split(';')[0]
                head, body = data.split('_')
                id_user = d[head]

                if body == 'OUT':
                    lost_connections.append(id_user)
                    sock.close()
                    read_list.remove(sock)
                else:
                    move = body
                    moves.append((id_user, move))
                    socks_ok.append((id_user, sock))

            else:
                sock.close()
                read_list.remove(sock)

    return new_players, lost_connections, moves, socks_ok, d

def manageGameLogic(board, new_players, lost_connections, moves, checkpoint_500ms):
    for lost_con in lost_connections:
        board.killSnake(lost_con)

    for player in new_players:
        board.addSnake(player)

    for id_user, move in moves:
        board.update({id_user: move})

    if time.time() - checkpoint_500ms >= 0.5:
        board.addSnack()
        checkpoint_500ms = time.time()

    return board, checkpoint_500ms

def manageOutput(socks_ok, board):
    # boardEncoded = pickle.dumps(board, protocol=2)

    for id_user, sock in socks_ok:
        encoded = pickle.dumps((id_user, board), protocol=2)
        sock.send(encoded)
