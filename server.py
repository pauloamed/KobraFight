import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from kobra_fight import Server
import sys

# print("oi")

def main():
    # --------------- Número da porta passado pelo popen ---------------
    param = sys.argv[1:]

    port = int(param[0])
    # --------------- --------------- --------------- ---------------

    s = Server(port)
    s.run()

main()
