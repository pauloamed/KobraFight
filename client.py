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


from deef import port


def selectIP():
    root = tk.Tk()
    root.withdraw()
    d = LoginDialog(root, "Login")
    return (d.r1, int(d.r2))

def main():
    # host, port = selectIP()
    host, _ = 'localhost', port
    size, grid = 500, 20

    client = Client(host, port, size, grid)

    # signal.signal(signal.SIGINT, client.stop)
    client.run()

main()
