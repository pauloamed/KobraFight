from kobra_fight import Server
import sys
import os

print("oi")

def main():
    # --------------- Número da porta passado pelo popen ---------------
    param = sys.argv[1:]

    port = int(param[0])
    # --------------- --------------- --------------- ---------------

    s = Server(port)
    s.run()

main()
