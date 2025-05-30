class TablaSimbolos:
    contador_codigo = 0  # contador global para asignar códigos únicos

    def __init__(self, ambito=0):  # 0 = global, 1 = local
        self.simbolos = []
        self.ambito = ambito
        self.padre = None

    def definir_ambito_padre(self, tabla_padre):
        self.padre = tabla_padre

    def _generar_codigo(self):
        codigo = TablaSimbolos.contador_codigo
        TablaSimbolos.contador_codigo += 1
        return codigo

    def agregar(self, nombre, tipo, clase="variable", inicializado=False, info=None):
        if any(sim["Nombre"] == nombre for sim in self.simbolos):
            return False

        nuevo = {
            "Código": self._generar_codigo(),
            "Nombre": nombre,
            "Categoría": clase,
            "Tipo": tipo,
            "NumParam": -1,
            "ListaDeParam": "null",
            "Dirección": -1,
            "Ámbito": self.ambito,
            "Inicializado": inicializado,
            "Info": info or {}
        }

        if clase == "funcion":
            parametros = info.get("parametros", []) if info else []
            nuevo["NumParam"] = len(parametros)
            nuevo["ListaDeParam"] = [p["tipo"] for p in parametros] if parametros else []

        self.simbolos.append(nuevo)
        return True

    def existe(self, nombre, buscar_en_padre=False):
        if any(sim["Nombre"] == nombre for sim in self.simbolos):
            return True
        if buscar_en_padre and self.padre:
            return self.padre.existe(nombre, buscar_en_padre)
        return False

    def obtener(self, nombre, buscar_en_padre=False):
        for sim in self.simbolos:
            if sim["Nombre"] == nombre:
                return sim
        if buscar_en_padre and self.padre:
            return self.padre.obtener(nombre, buscar_en_padre)
        return None

    def mostrar(self):
        print(f"\n TABLA DE SÍMBOLOS - Ámbito {'Global' if self.ambito == 0 else 'Local'}")
        print("=" * 130)
        encabezado = ["Código", "Nombre", "Categoría", "Tipo", "NumParam", "ListaDeParam", "Dirección", "Ámbito", "Inicializado", "Info"]
        print(" | ".join(f"{h:<14}" for h in encabezado))
        print("-" * 130)
        for sim in self.simbolos:
            fila = [sim.get("Código"),
                    sim.get("Nombre"),
                    sim.get("Categoría"),
                    sim.get("Tipo"),
                    sim.get("NumParam"),
                    sim.get("ListaDeParam"),
                    sim.get("Dirección"),
                    sim.get("Ámbito"),
                    sim.get("Inicializado"),
                    self._formatear_info(sim.get("Info"))]
            print(" | ".join(f"{str(val):<14}" for val in fila))
        print("=" * 130)
        if self.padre:
            print("↪ Ámbito Padre:")
            self.padre.mostrar()

    def _formatear_info(self, info):
        if not info:
            return "null"
        return ", ".join(f"{k}={v}" for k, v in info.items())

    def agregar_parametro(self, nombre_funcion, nombre_parametro, tipo_parametro):
        funcion = self.obtener(nombre_funcion)
        if not funcion or funcion["Categoría"] != "funcion":
            return False
        if funcion["ListaDeParam"] == "null":
            funcion["ListaDeParam"] = []
        funcion["ListaDeParam"].append(tipo_parametro)
        funcion["NumParam"] = len(funcion["ListaDeParam"])
        return True

    def obtener_parametros(self, nombre_funcion):
        simbolo = self.obtener(nombre_funcion, buscar_en_padre=True)
        if simbolo and simbolo["Categoría"] == "funcion":
            return simbolo.get("ListaDeParam", [])
        return []

    def agregar_tipo_retorno(self, nombre_funcion, tipo_retorno):
        simbolo = self.obtener(nombre_funcion)
        if simbolo and simbolo["Categoría"] == "funcion":
            simbolo["Tipo"] = tipo_retorno
            return True
        return False

    def obtener_tipo_retorno(self, nombre_funcion):
        simbolo = self.obtener(nombre_funcion, buscar_en_padre=True)
        if simbolo and simbolo["Categoría"] == "funcion":
            return simbolo["Tipo"]
        return None
