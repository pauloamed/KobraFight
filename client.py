import math
import pygame
import tkinter as tk
from tkinter import simpledialog

from kobra_fight import Client, LoginDialog

import time
import sys
import signal
import subprocess
import atexit


def selectIP():
    root = tk.Tk()
    root.withdraw()
    d = LoginDialog(root, "Login")
    return (d.r1, int(d.r2))

def killServer():
    serverProcess.terminate()

def main():
    # host, port = selectIP()
    host, port = 'localhost', 11112
    size, grid = 500, 20

    client = Client(host, port, size, grid)

    signal.signal(signal.SIGINT, client.stop)
    client.run()



    # Para criar o servidor
    portNumber = 1234
    serverProcess = subprocess.Popen([sys.executable, "server.py", str(portNumber)])
    time.sleep(2)

main()

# Matar o servidor quando o cliente fechar (acho que não está funcionando)
atexit.register(killServer)
