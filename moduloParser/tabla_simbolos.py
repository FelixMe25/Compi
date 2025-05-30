# ------------------------------------------------------------------------------
# Clase TablaSimbolos: Implementa una tabla de símbolos para el análisis semántico
# de North Engine .Permite almacenar información sobre variables, identificadores
# funciones, constantes
# ------------------------------------------------------------------------------

class TablaSimbolos:
    contador_codigo = 0  # contador global para asignar códigos únicos

    def __init__(self, ambito=0):  # 0 = global, 1 = local
        # Inicializa la tabla de símbolos con un ámbito (0=global, 1=local)
        self.simbolos = []
        self.ambito = ambito
        self.padre = None  # Referencia a la tabla de símbolos padre (para ámbitos anidados)

    def definir_ambito_padre(self, tabla_padre):
        # Define la tabla de símbolos padre para permitir búsqueda jerárquica
        self.padre = tabla_padre

    def _generar_codigo(self):
        # Genera un código único para cada símbolo
        codigo = TablaSimbolos.contador_codigo
        TablaSimbolos.contador_codigo += 1
        return codigo

    def agregar(self, nombre, tipo, clase="variable", inicializado=False, info=None):
        # Agrega un nuevo símbolo a la tabla si no existe ya con ese nombre en el mismo ámbito
        if any(sim["Nombre"] == nombre for sim in self.simbolos):
            return False

        nuevo = {
            "Código": self._generar_codigo(),  # Código único
            "Nombre": nombre,                  # Nombre del símbolo
            "Categoría": clase,                # variable, funcion, constante, etc.
            "Tipo": tipo,                      # Tipo de dato
            "NumParam": -1,                    # Número de parámetros (si es función)
            "ListaDeParam": "null",           # Lista de tipos de parámetros (si es función)
            "Dirección": -1,                   # Dirección de memoria (no usado aquí)
            "Ámbito": self.ambito,             # Ámbito (0=global, 1=local)
            "Inicializado": inicializado,      # Si la variable está inicializada
            "Info": info or {}                 # Información adicional (diccionario)
        }

        # Si es una función, guarda información de parámetros
        if clase == "funcion":
            parametros = info.get("parametros", []) if info else []
            nuevo["NumParam"] = len(parametros)
            nuevo["ListaDeParam"] = [p["tipo"] for p in parametros] if parametros else []

        self.simbolos.append(nuevo)
        return True

    def existe(self, nombre, buscar_en_padre=False):
        # Verifica si un símbolo existe en la tabla (y opcionalmente en las tablas padre)
        if any(sim["Nombre"] == nombre for sim in self.simbolos):
            return True
        if buscar_en_padre and self.padre:
            return self.padre.existe(nombre, buscar_en_padre)
        return False

    def obtener(self, nombre, buscar_en_padre=False):
        # Obtiene el símbolo por nombre (opcionalmente busca en las tablas padre)
        for sim in self.simbolos:
            if sim["Nombre"] == nombre:
                return sim
        if buscar_en_padre and self.padre:
            return self.padre.obtener(nombre, buscar_en_padre)
        return None

    def mostrar(self):
        # Imprime la tabla de símbolos en formato tabular
        encabezado = ["Código", "Nombre", "Categoría", "Tipo", "NumParam", "ListaDeParam", "Dirección", "Ámbito", "Inicializado", "Info"]
        ancho_col = [8, 15, 12, 12, 9, 18, 10, 6, 12, 25]

        def linea():
            print("+" + "+".join("-" * (w + 2) for w in ancho_col) + "+")

        def imprimir_fila(valores):
            fila = ""
            for i, val in enumerate(valores):
                val_str = str(val)
                if len(val_str) > ancho_col[i]:
                    val_str = val_str[:ancho_col[i]-3] + "..."
                fila += f" {val_str:<{ancho_col[i]}} |"
            print("|" + fila)

        print(f"\n TABLA DE SÍMBOLOS - Ámbito {'Global' if self.ambito == 0 else 'Local'}")
        linea()
        imprimir_fila(encabezado)
        linea()
        for sim in self.simbolos:
            fila = [
                sim.get("Código"),
                sim.get("Nombre"),
                sim.get("Categoría"),
                sim.get("Tipo"),
                sim.get("NumParam"),
                sim.get("ListaDeParam"),
                sim.get("Dirección"),
                sim.get("Ámbito"),
                sim.get("Inicializado"),
                self._formatear_info(sim.get("Info"))
            ]
            imprimir_fila(fila)
        linea()
        if self.padre:
            print("↪ Ámbito Padre:")
            self.padre.mostrar()

    def _formatear_info(self, info):
        # Formatea el campo Info para mostrarlo en la tabla
        if not info:
            return "null"
        texto = ", ".join(f"{k}={v}" for k, v in info.items())
        if len(texto) > 25:
            return texto[:22] + "..."
        return texto

    # Métodos para parámetros y tipos de retorno (idénticos a tu versión)
    def agregar_parametro(self, nombre_funcion, nombre_parametro, tipo_parametro):
        # Agrega un tipo de parámetro a una función existente
        funcion = self.obtener(nombre_funcion)
        if not funcion or funcion["Categoría"] != "funcion":
            return False
        if funcion["ListaDeParam"] == "null":
            funcion["ListaDeParam"] = []
        funcion["ListaDeParam"].append(tipo_parametro)
        funcion["NumParam"] = len(funcion["ListaDeParam"])
        return True

    def obtener_parametros(self, nombre_funcion):
        # Devuelve la lista de tipos de parámetros de una función
        simbolo = self.obtener(nombre_funcion, buscar_en_padre=True)
        if simbolo and simbolo["Categoría"] == "funcion":
            return simbolo.get("ListaDeParam", [])
        return []

    def agregar_tipo_retorno(self, nombre_funcion, tipo_retorno):
        # Asigna el tipo de retorno a una función
        simbolo = self.obtener(nombre_funcion)
        if simbolo and simbolo["Categoría"] == "funcion":
            simbolo["Tipo"] = tipo_retorno
            return True
        return False

    def obtener_tipo_retorno(self, nombre_funcion):
        # Devuelve el tipo de retorno de una función si existe
        simbolo = self.obtener(nombre_funcion, buscar_en_padre=True)
        if simbolo and simbolo["Categoría"] == "funcion":
            return simbolo["Tipo"]
        return None
