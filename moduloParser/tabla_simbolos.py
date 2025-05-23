class TablaSimbolos:
    def __init__(self, ambito="global"):  # Añadido: ámbito
        self.simbolos = {}
        self.ambito = ambito  # "global" o el nombre de la función/bloque
        self.padre = None  # Para tablas anidadas (ámbitos internos)

    def definir_ambito_padre(self, tabla_padre):
        self.padre = tabla_padre

    def agregar(self, nombre, tipo, clase="variable", inicializado=False, info=None):
        if nombre in self.simbolos:
            return False  # Ya declarado en este ámbito
        self.simbolos[nombre] = {
            "tipo": tipo,
            "clase": clase,
            "inicializado": inicializado,
            "info": info  # Para información adicional (parámetros, etc.)
        }
        return True

    def existe(self, nombre, buscar_en_padre=False):
        if nombre in self.simbolos:
            return True
        if buscar_en_padre and self.padre:
            return self.padre.existe(nombre, buscar_en_padre)  # Búsqueda recursiva
        return False

    def obtener(self, nombre, buscar_en_padre=False):
        if nombre in self.simbolos:
            return self.simbolos[nombre]
        if buscar_en_padre and self.padre:
            return self.padre.obtener(nombre, buscar_en_padre)
        return None

    def marcar_inicializado(self, nombre):
        if self.existe(nombre, buscar_en_padre=True):  # Buscar en ámbitos superiores
            simbolo = self.obtener(nombre, buscar_en_padre=True)
            simbolo["inicializado"] = True

    def mostrar(self):
        print(f"--- Tabla de Símbolos ({self.ambito}) ---")
        for nombre, datos in self.simbolos.items():
            print(f"   {nombre} -> {datos}")
        if self.padre:
            print("--- Ámbito Padre ---")
            self.padre.mostrar()

    # --- Nuevas Funcionalidades ---

    def agregar_parametro(self, nombre_funcion, nombre_parametro, tipo_parametro):
        if nombre_funcion not in self.simbolos:
            return False  # Función no existe
        if self.simbolos[nombre_funcion]["clase"] != "funcion":
            return False  # No es una función
        if "parametros" not in self.simbolos[nombre_funcion]["info"]:
            self.simbolos[nombre_funcion]["info"]["parametros"] = []
        self.simbolos[nombre_funcion]["info"]["parametros"].append({
            "nombre": nombre_parametro,
            "tipo": tipo_parametro
        })
        return True

    def obtener_parametros(self, nombre_funcion):
        if self.existe(nombre_funcion, buscar_en_padre=True):
            simbolo = self.obtener(nombre_funcion, buscar_en_padre=True)
            if simbolo and simbolo["clase"] == "funcion" and "parametros" in simbolo["info"]:
                return simbolo["info"]["parametros"]
        return []

    def agregar_tipo_retorno(self, nombre_funcion, tipo_retorno):
        if nombre_funcion not in self.simbolos:
            return False
        if self.simbolos[nombre_funcion]["clase"] != "funcion":
            return False
        self.simbolos[nombre_funcion]["info"]["tipo_retorno"] = tipo_retorno
        return True

    def obtener_tipo_retorno(self, nombre_funcion):
        if self.existe(nombre_funcion, buscar_en_padre=True):
            simbolo = self.obtener(nombre_funcion, buscar_en_padre=True)
            if simbolo and simbolo["clase"] == "funcion" and "tipo_retorno" in simbolo["info"]:
                return simbolo["info"]["tipo_retorno"]
        return None
