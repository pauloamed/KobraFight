import math
import pygame

from kobra_fight import Client, LoginDialog

import time
import sys
import signal
import subprocess
import atexit


def main():
    param = sys.argv[1:]
    port = int(param[0])
    id = int(param[1])

    host, _ = 'localhost', port
    size, grid = 500, 20



    client = Client(host, port, id, size, grid)

    # signal.signal(signal.SIGINT, client.stop)
    client.run()

main()
