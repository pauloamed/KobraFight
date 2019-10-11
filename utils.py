from tkinter import messagebox
from globals import *
import tkinter as tk
import pygame

'''
desenha uma caixa de mensagem pro user'''
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

'''
desenha o grid'''
def drawGrid(surface):
    sizeBtwn = SIZE // GRID

    x = 0
    y = 0
    for l in range(GRID):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, WHITE_COLOR, (x,0),(x,SIZE))
        pygame.draw.line(surface, WHITE_COLOR, (0,y),(SIZE,y))
