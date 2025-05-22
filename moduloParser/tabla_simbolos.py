class TablaSimbolos:
    def __init__(self):
        self.simbolos = {}

    def agregar(self, nombre, tipo, clase="variable", inicializado=False):
        if nombre in self.simbolos:
            return False  # Ya declarado
        self.simbolos[nombre] = {
            "tipo": tipo,
            "clase": clase,
            "inicializado": inicializado
        }
        return True

    def existe(self, nombre):
        return nombre in self.simbolos

    def obtener(self, nombre):
        return self.simbolos.get(nombre, None)

    def marcar_inicializado(self, nombre):
        if nombre in self.simbolos:
            self.simbolos[nombre]["inicializado"] = True

    def mostrar(self):
        for nombre, datos in self.simbolos.items():
            print(f"{nombre} -> {datos}")
