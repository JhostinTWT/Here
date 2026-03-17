import tkinter as tk
from controlador import Controlador
from vista import App

root = tk.Tk()

controlador = Controlador()
app = App(root, controlador)

root.mainloop()