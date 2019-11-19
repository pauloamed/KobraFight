from snake_game import Server

def main():
    # --------------- Número da porta passado pelo popen ---------------
    param = sys.argv[1:]
    print(param)

    port = int(param[0])
    # --------------- --------------- --------------- ---------------

    s = Server(port)
    s.run()

main()
