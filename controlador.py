from modelo import GestorTareas

class Controlador:
    def __init__(self):
        self.gestor = GestorTareas()

    def obtener_tareas(self):
        return self.gestor.obtener_tareas()

    def agregar_tarea(self, tarea):
        if tarea.strip() == "":
            return False
        self.gestor.agregar_tarea(tarea)
        return True

    def eliminar_tarea(self, tarea):
        self.gestor.eliminar_tarea(tarea)