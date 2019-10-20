import tkinter as tk
from tkinter import simpledialog

class LoginDialog(simpledialog.Dialog):
    def body(self, master):
        self.l1 = tk.Label(master, text="IP do server:", font=(None, 15))
        self.e1 = tk.Entry(master)
        self.e1.grid(row=0, column=1)

        self.l2 = tk.Label(master, text="Porta do server:", font=(None, 15))
        self.e2 = tk.Entry(master)
        self.e2.grid(row=1, column=1)

        # self.l1.config(width=200)
        self.l1.grid(row=0)

        # self.l2.config(width=200)
        self.l2.grid(row=1)

        self.r1 = None
        self.r2 = None

        return self.e1

    def getresult(self):
        self.r1 = self.e1.get()
        self.r2 = self.e2.get()
        self.destroy()
        return (self.r1, self.r2)

    def buttonbox(self):
        b = tk.Button(self, text ="Conectar", command=self.getresult)
        b.pack()

    def apply(self):
        first = self.e1.get()
        self.result = first
        first = self.e2.get()
        self.result = first
