import tkinter as tk
from tkinter import messagebox

class App:
    def __init__(self, root, controlador):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("400x450")
        self.root.config(bg="#1e1e2f")
        
        self.controlador = controlador
        
        self.titulo = tk.Label(
            root, text="Lista de Tareas",
            font=("Arial", 16, "bold"),
            bg="#1e1e2f", fg="white"
        )
        self.titulo.pack(pady=10)
        
        frame_input = tk.Frame(root, bg="#1e1e2f")
        frame_input.pack(pady=10)
        
        self.entry = tk.Entry(frame_input, width=25, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, padx=5)
        
        self.boton_agregar = tk.Button(
            frame_input, text="Agregar",
            bg="#4CAF50", fg="white",
            font=("Arial", 10, "bold"),
            command=self.agregar
        )
        self.boton_agregar.pack(side=tk.LEFT)
        
        self.listbox = tk.Listbox(
            root, width=40, height=12,
            font=("Arial", 11),
            bg="#2c2c3e", fg="white",
            selectbackground="#6a5acd"
        )
        self.listbox.pack(pady=15)
        
        self.boton_eliminar = tk.Button(
            root, text="✔ Completar tarea",
            bg="#e74c3c", fg="white",
            font=("Arial", 11, "bold"),
            command=self.eliminar
        )
        self.boton_eliminar.pack(pady=10)
        
        self.cargar_tareas()
        
    def cargar_tareas(self):
        self.listbox.delete(0, tk.END)
        tareas = self.controlador.obtener_tareas()
        for tarea in tareas:
            self.listbox.insert(tk.END, tarea)
    
    def agregar(self):
        tarea = self.entry.get()
        if not self.controlador.agregar_tarea(tarea):
            messagebox.showwarning("Error", "La tarea no puede estar vacía.")
            return
        
        self.entry.delete(0, tk.END)
        self.cargar_tareas()
    
    def eliminar(self):
        seleccion = self.listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Error", "Seleccione una tarea.")
            return
        
        tarea = self.listbox.get(seleccion[0])
        self.controlador.eliminar_tarea(tarea)
        self.cargar_tareas()