class GestorTareas:
    def __init__(self, archivo="tareas.txt"):
        self.archivo = archivo
        
    def obtener_tareas(self):
        try:
            with open(self.archivo, "r") as f:
                tareas = [linea.strip() for linea in f.readlines()]
            return tareas
        except FileNotFoundError:
            return []
    
    def agregar_tarea(self, tarea):
        with open(self.archivo, "a") as f:
            f.write(tarea + "\n")
    
    def eliminar_tarea(self, tarea):
        tareas = self.obtener_tareas()
        if tarea in tareas:
            tareas.remove(tarea)
            with open(self.archivo, "w") as f:
                for t in tareas:
                    f.write(t + "\n")