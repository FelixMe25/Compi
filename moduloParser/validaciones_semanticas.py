# ------------------------------------------------------------
# Utilidades Generales
# ------------------------------------------------------------
def normalizar_tipo(tipo_raw):
    equivalencias = {
        "STRING": "Spider",
        "ENTERO": "Stack",
        "CARACTER": "Rune",
        "FLOAT": "Ghast",
        "BOOL": "Wither",
        "FLOTANTE": "Ghast",
        "STACK": "Stack",
        "RUNE": "Rune",
        "SPIDER": "Spider",
        "GHAST": "Ghast"
    }
    if not tipo_raw:
        return None
    return equivalencias.get(tipo_raw.upper(), tipo_raw)


def verificar_tipo_operando(tabla_simbolos, operando):
    if isinstance(operando, int):
        return "Stack"
    elif isinstance(operando, float):
        return "Ghast"
    elif isinstance(operando, str) and (
        (operando.startswith('"') and operando.endswith('"')) or 
        (operando.startswith("'") and operando.endswith("'"))
    ):
        return "Spider"
    elif isinstance(operando, str):  # Identificador
        simbolo = tabla_simbolos.obtener(operando, buscar_en_padre=True)
        if not simbolo:
            print(f"Error semántico: Variable '{operando}' no declarada.")
            return None
        tipo_raw = simbolo.get("Tipo")
        if not tipo_raw:
            print(f"Error semántico: El símbolo '{operando}' no tiene campo 'Tipo'.")
            return None
        return normalizar_tipo(tipo_raw)
    return None

#  ------------------------------- DECLARACIONES ----------------------------------------------------------------------

#------------------------------------
# SECCION DE CONSTANTES
#-----------------------------------
def validar_declaracion_constante(tabla_simbolos, nombre, tipo, inicializado=False, valor=None):
    if tabla_simbolos.existe(nombre):
        print(f"Error semántico: La constante '{nombre}' ya ha sido declarada.")
        return False
    tabla_simbolos.agregar(nombre, tipo, 
                           clase="constante", 
                           inicializado=inicializado, 
                           info={"valor_inicializacion": valor})
    print(f"---- Constante '{nombre}' declarada correctamente.")
    return True

#------------------------------------
# SECCION DE VARIABLES
#-----------------------------------
def validar_declaracion_variable(tabla_simbolos, nombre_variable, tipo_variable, inicializado=False, valor_inicializacion=None):
    if tabla_simbolos.existe(nombre_variable):
        print(f"Error semántico: La variable '{nombre_variable}' ya ha sido declarada.")
        return False
    tabla_simbolos.agregar(nombre_variable, 
                           tipo_variable, clase="variable", 
                           inicializado=inicializado, 
                           info={"valor_inicializacion": valor_inicializacion})
    print(f"---- Variable '{nombre_variable}' de tipo '{tipo_variable}' declarada correctamente.")
    return True

def validar_variable_inicializada(tabla_simbolos, nombre):
    simbolo = tabla_simbolos.obtener(nombre, buscar_en_padre=True)
    if not simbolo:
        print(f"Error semántico: Variable '{nombre}' no declarada.")
        return False
    if not simbolo["inicializado"]:
        print(f"Error semántico: Variable '{nombre}' usada antes de ser inicializada.")
        return False
    return True

def validar_variable_shelf(tabla_simbolos, nombre, tipo_base, valor):
    if tabla_simbolos.existe(nombre):
        print(f"Error semántico: El arreglo Shelf '{nombre}' ya ha sido declarado.")
        return False
    tabla_simbolos.agregar(nombre, "TIPO_ARREGLOS", 
                           clase="variable", 
                           inicializado=True, 
                           info={"tipo_base_shelf": tipo_base, "valor_inicializacion": valor, "es_arreglo_shelf": True})
    print(f"---- Arreglo Shelf '{nombre}' de tipo '{tipo_base}' declarado correctamente.")
    return True

def validar_declaracion_entity(tabla_simbolos, nombre_variable, inicializado=False, valor_inicializacion=None):
    if tabla_simbolos.existe(nombre_variable):
        print(f"Error semántico: La variable Entity '{nombre_variable}' ya ha sido declarada.")
        return False
    tabla_simbolos.agregar(nombre_variable,
                           "Entity",
                           clase="variable",
                           inicializado=inicializado,
                           info={"valor_inicializacion": valor_inicializacion})
    print(f"---- Entity '{nombre_variable}' declarada correctamente.")
    return True


#------------------------------------
# SECCION DE TIPOS
#-----------------------------------
def validar_declaracion_tipos(tabla_simbolos, nombre, tipo, inicializado=False, valor=None):
    if tabla_simbolos.existe(nombre):
        print(f"Error semántico: El tipo '{nombre}' ya ha sido declarado.")
        return False
    tabla_simbolos.agregar(nombre, tipo, 
                           clase="tipo", 
                           inicializado=inicializado, 
                           info={"valor_inicializacion": valor})
    print(f"---- Tipo '{nombre}' declarado correctamente.")
    return True

#------------------------------------
# SECCION DE PROTOTIPOS - RUTINAS 
#-----------------------------------
def validar_parametros_unicos(parametros):
    nombres = set()
    for param in parametros:
        if param["nombre"] in nombres:
            print(f"Error semántico: El parámetro '{param['nombre']}' está repetido.")
            return False
        nombres.add(param["nombre"])
    return True

def validar_nombre_unico_global(tabla_simbolos, nombre):
    simbolo = tabla_simbolos.obtener(nombre)
    if simbolo:
        print(f"Error semántico: El identificador '{nombre}' ya fue declarado como '{simbolo['clase']}'.")
        return False
    return True

#--------------------- FUNCIONES Y PROCEDIMIENTOS -------------------------------------------------------------------

#-----------------------------
# VALIDACION ASIGNACION
#------------------------------
def validar_asignacion(tabla, nombre, valor):
    simbolo = tabla.obtener(nombre, buscar_en_padre=True)
    if not simbolo:
        print(f"Error: Variable '{nombre}' no declarada.")
        return False
    tipo_valor = verificar_tipo_operando(tabla, valor)
    # Permitir asignación de literal de registro a Entity
    if simbolo["tipo"] in ["Entity", "REGISTROS"]:
        if isinstance(valor, str) and (valor.startswith("{") or valor.startswith("{/")):
            simbolo["inicializado"] = True
            simbolo["info"]["valor_inicializacion"] = valor
            print(f"---- Entity '{nombre}' inicializada correctamente.")
            # Desglosar y asignar a los campos individuales si existen
            # Quitar llaves y espacios, luego separar por comas
            campos = valor.strip("{} ").split(",")
            nombres_campos = ["name", "material", "durability", "isEnchanted"]
            for i, campo in enumerate(campos):
                if i >= len(nombres_campos):
                    break
                nombre_campo = nombres_campos[i].strip()
                valor_campo = campo.strip().strip('"')
                if tabla.existe(nombre_campo):
                    simbolo_campo = tabla.obtener(nombre_campo)
                    simbolo_campo["inicializado"] = True
                    simbolo_campo["info"]["valor_inicializacion"] = valor_campo
            return True
        else:
            print(f"Error: Asignación inválida para Entity '{nombre}'.")
            return False
    if tipo_valor != simbolo["tipo"]:
        print(f"Error: Tipo de valor '{tipo_valor}' no coincide con '{simbolo['tipo']}'.")
        return False
    simbolo["inicializado"] = True
    simbolo["info"]["valor_inicializacion"] = valor
    print(f"---- Variable '{nombre}' inicializada correctamente.")
    return True

#-----------------------------------
# VALIDACION LLAMADA A FUNCION (RITUAL - SPELL)
# --------------------------------
def validar_llamada_funcion(tabla, nombre, args):
    simbolo = tabla.obtener(nombre, buscar_en_padre=True)
    if not simbolo or simbolo["clase"] != "funcion":
        print(f"Error: '{nombre}' no es función.")
        return False
    parametros = simbolo["info"].get("parametros", [])
    if len(args) != len(parametros):
        print(f"Error: La función '{nombre}' espera {len(parametros)} argumentos, pero se pasaron {len(args)}.")
        return False
    for i, (arg, param) in enumerate(zip(args, parametros)):
        tipo_arg = verificar_tipo_operando(tabla, arg)
        if tipo_arg != param["tipo"]:
            print(f"Error: Arg {i+1} debe ser '{param['tipo']}', se recibió '{tipo_arg}'.")
            return False
    return True

#-----------------------------------
# VALIDACION SPELL - TIPO DE RETORNO
# --------------------------------
def validar_retorno_funcion(tabla, nombre, valor):
    simbolo = tabla.obtener(nombre, buscar_en_padre=True)
    if not simbolo or simbolo["clase"] != "funcion":
        print(f"Error: '{nombre}' no es una función.")
        return False
    tipo_esperado = simbolo["info"].get("tipo_retorno")
    tipo_valor = verificar_tipo_operando(tabla, valor)
    if tipo_esperado != tipo_valor:
        print(f"Error: Retorno debe ser '{tipo_esperado}', se retornó '{tipo_valor}'.")
        return False
    return True

#-----------------------------------
# VALIDACION SPELL CON RETURN
# --------------------------------
def validar_funcion_tiene_retorno(nombre_funcion, tuvo_retorno):
    if not tuvo_retorno:
        print(f"Error: La función '{nombre_funcion}' debe retornar un valor.")
        return False
    return True


# -------------------------------- OPERACIONES -----------------------------------------------------------------------------------------

#-----------------------------------
# VALIDACION DE CONVERSION DE TIPOS
# --------------------------------
def validar_conversion_de_tipos(origen, destino):
    conversiones = {("Stack", "Ghast"), ("Ghast", "Stack"), 
                    ("Rune", "Stack"), ("Stack", "Rune"), 
                    ("Rune", "Ghast"), ("Ghast", "Rune")}
    if (origen, destino) not in conversiones:
        print(f"Error: Conversión inválida de '{origen}' a '{destino}'.")
        return False
    
    # [REVISAR CONVERSIONES PERMITIDAS]
    return True

#-----------------------------------
# VALIDACION INCREMENTO - DECREMENTO
# --------------------------------
def validar_operacion_incremento_decremento(tabla, nombre, tipo_esperado):
    simbolo = tabla.obtener(nombre, buscar_en_padre=True)
    if not simbolo:
        print(f"Error semántico: Variable '{nombre}' no declarada.")
        return False
    if tipo_esperado != "Stack" or tipo_esperado != "Ghast":
        print(f"Error semántico: '{nombre}' solo es válido para 'Stack' or 'Ghast'.")
        return False

    print(f"Operación de Incremento - Decremento válida sobre variable '{nombre}'.")
    return True

# -----------------------------------
# VALIDACION DE OPERACIONES ENTEROS
# -------------------------------------
def validar_operacion_entera(tabla, destino, op, izq, der):
    simbolo = tabla.obtener(destino, buscar_en_padre=True)
    if not simbolo:
        print(f"Error: Variable '{destino}' no ha sido declarada previamente.")
        return False

    if simbolo["Tipo"] != "Stack":
        print(f"Error: Variable de destino '{destino}' debe ser 'Stack'.")
        return False

    tipo_izq = verificar_tipo_operando(tabla, izq)
    tipo_der = verificar_tipo_operando(tabla, der)

    if tipo_izq != "Stack" or tipo_der != "Stack":
        print(f"Error: Operandos de '{op}' deben ser 'Stack'.")
        return False

    return True


# -----------------------------------
# VALIDACION DE OPERACIONES FLOTANTES
# -------------------------------------
def validar_operacion_flotante(tabla, destino, op, izq, der):
    simbolo = tabla.obtener(destino, buscar_en_padre=True)
    if not simbolo or normalizar_tipo(simbolo.get("Tipo")) != "Ghast":
        print(f"Error: Variable de destino '{destino}' debe ser 'Ghast'.")
        return False
    tipo_izq = verificar_tipo_operando(tabla, izq)
    tipo_der = verificar_tipo_operando(tabla, der)
    if tipo_izq != "Ghast" or tipo_der != "Ghast":
        print(f"Error: Operandos de '{op}' deben ser 'Ghast'.")
        return False
    return True

# ------------------------------------
# VALIDACION DE OPERACIONES CARACTERES
# -------------------------------------
def validar_operacion_caracter(tabla, destino, operador, operando):
    simbolo_dest = tabla.obtener(destino, buscar_en_padre=True)
    simbolo_op = tabla.obtener(operando, buscar_en_padre=True)
    
    if not simbolo_dest or simbolo_dest["tipo"] != "Rune":
        print(f"Error: Destino '{destino}' debe ser 'Rune'.")
        return False
    
    if not simbolo_op or simbolo_op["tipo"] != "Rune":
        print(f"Error: Operando '{operando}' debe ser 'Rune'.")
        return False
    # [REVISAR SI EL PARAMETRO 'OPERADOR' ES NECESARIO]
    return True

# -----------------------------------
# VALIDACION DE OPERACIONES STRING
# -------------------------------------

# -----------------------------------
# ACCESO A STRING
# -------------------------------------
def validar_acceso_spider(tabla_simbolos, spider_nombre, indice, destino):
    spider = tabla_simbolos.obtener(spider_nombre, buscar_en_padre=True)
    if not spider or normalizar_tipo(spider.get("Tipo"))  != "Spider":
        print(f"Error semántico: '{spider_nombre}' debe ser de tipo 'Spider'.")
        return False

    tipo_indice = verificar_tipo_operando(tabla_simbolos, indice)
    if tipo_indice != "Stack":
        print(f"Error semántico: El índice debe ser de tipo 'Stack', no '{tipo_indice}'.")
        return False

    simbolo_destino = tabla_simbolos.obtener(destino, buscar_en_padre=True)
    if not simbolo_destino or  normalizar_tipo(simbolo_destino.get("Tipo")) != "Rune":
        print(f"Error semántico: El resultado del acceso debe asignarse a una variable de tipo 'Rune'.")
        return False

    print(f"✔ Acceso Spider válido: {spider_nombre}[{indice}] → {destino}")
    return True

#-----------------
# CONCATENAR
# ------------------
def validar_concatenacion_spider(tabla_simbolos, destino, spider1, spider2):
    for spider in [spider1, spider2]:
        tipo = verificar_tipo_operando(tabla_simbolos, spider)
        if tipo != "Spider":
            print(f"Error semántico: '{spider}' debe ser de tipo 'Spider'.")
            return False

    simbolo_destino = tabla_simbolos.obtener(destino, buscar_en_padre=True)
    if not simbolo_destino or normalizar_tipo(simbolo_destino.get("Tipo")) != "Spider":
        print(f"Error semántico: El resultado de 'bind' debe asignarse a una variable 'Spider'.")
        return False

    print(f"✔ Concatenación Spider válida: {spider1} bind {spider2} → {destino}")
    return True

#-----------------
# LENGTH
# ------------------
def validar_longitud_spider(tabla_simbolos, spider, destino):
    simbolo_spider = tabla_simbolos.obtener(spider, buscar_en_padre=True)
    if not simbolo_spider or normalizar_tipo(simbolo_spider.get("Tipo")) != "Spider":
        print(f"Error semántico: '{spider}' debe ser de tipo 'Spider'.")
        return False

    simbolo_destino = tabla_simbolos.obtener(destino, buscar_en_padre=True)
    if not simbolo_destino or normalizar_tipo(simbolo_destino.get("Tipo")) != "Stack":
        print(f"Error semántico: El resultado de '#' debe almacenarse en una variable 'Stack'.")
        return False

    print(f"✔ Longitud Spider válida: # {spider} → {destino}")
    return True

#-----------------
# CORTAR
# ------------------
def validar_corte_spider(tabla_simbolos, destino, spider, inicio, cantidad):
    if verificar_tipo_operando(tabla_simbolos, spider) != "Spider":
        print(f"Error semántico: '{spider}' debe ser tipo 'Spider'.")
        return False
    if verificar_tipo_operando(tabla_simbolos, inicio) != "Stack" or verificar_tipo_operando(tabla_simbolos, cantidad) != "Stack":
        print(f"Error semántico: Los índices 'from' y '##' deben ser de tipo 'Stack'.")
        return False
    if verificar_tipo_operando(tabla_simbolos, destino) != "Spider":
        print(f"Error semántico: El resultado del 'from ##' debe asignarse a una variable 'Spider'.")
        return False

    print(f"✔ Corte Spider válido: {spider} from {inicio} ## {cantidad} → {destino}")
    return True

#-----------------
# RECORTAR 
# ------------------
def validar_recorte_spider(tabla_simbolos, destino, spider, inicio, cantidad):
    if verificar_tipo_operando(tabla_simbolos, spider) != "Spider":
        print(f"Error semántico: '{spider}' debe ser tipo 'Spider'.")
        return False
    if verificar_tipo_operando(tabla_simbolos, inicio) != "Stack" or verificar_tipo_operando(tabla_simbolos, cantidad) != "Stack":
        print(f"Error semántico: Los índices 'except ##' deben ser de tipo 'Stack'.")
        return False
    if verificar_tipo_operando(tabla_simbolos, destino) != "Spider":
        print(f"Error semántico: El resultado del 'except ##' debe asignarse a una variable 'Spider'.")
        return False

    print(f"✔ Recorte Spider válido: {spider} except {inicio} ## {cantidad} → {destino}")
    return True

#-----------------
# BUSCAR
# ------------------
def validar_seek_spider(tabla_simbolos, destino, spider_base, spider_sub):
    if verificar_tipo_operando(tabla_simbolos, spider_base) != "Spider":
        print(f"Error semántico: '{spider_base}' debe ser tipo 'Spider'.")
        return False
    if verificar_tipo_operando(tabla_simbolos, spider_sub) != "Spider":
        print(f"Error semántico: El valor buscado '{spider_sub}' debe ser tipo 'Spider'.")
        return False
    if verificar_tipo_operando(tabla_simbolos, destino) != "Stack":
        print(f"Error semántico: El resultado de 'seek' debe asignarse a una variable 'Stack'.")
        return False

    print(f"✔ Búsqueda Spider válida: {spider_base} seek {spider_sub} → {destino}")
    return True

# -----------------------------------
# VALIDACION DE OPERACIONES LOGICAS
# -------------------------------------
def validar_operacion_logica(tabla_simbolos, izq, op, der):
    tipo_izq = verificar_tipo_operando(tabla_simbolos, izq)
    tipo_der = verificar_tipo_operando(tabla_simbolos, der)

    if tipo_izq != "Wither" or tipo_der != "Wither":
        print(f"Error: Operación lógica '{op}' requiere 'Wither'.")
        return False
    # [FALTA OPERACIONES LOGICAS/NECESITA MEJORAS]
    return True

# -----------------------------------------------
# VALIDACION DE COMPATIBILIDAD ENTRE DOS DATOS
# ----------------------------------------------
def validar_operacion_relacional(tabla_simbolos, izq, op, der):
    tipo_izq = verificar_tipo_operando(tabla_simbolos, izq)
    tipo_der = verificar_tipo_operando(tabla_simbolos, der)

    if tipo_izq != tipo_der or tipo_izq not in {"Stack", "Ghast", "Rune"}:
        print(f"Error: Relacional entre tipos incompatibles '{tipo_izq}' y '{tipo_der}'.")
        return False
    # [REVISAR DONDE SE IMPLEMENTARÍA Y SI EL PARAMETRO 'OP' ES NECESARIO]
    return True

# -----------------------------------
# VALIDACION DE CONDICIONALES
# -------------------------------------
def validar_condicion_booleana(tabla, condicion):
    tipo = verificar_tipo_operando(tabla, condicion)
    if tipo != "Wither":
        print(f"Error: Condición debe ser tipo 'Wither', se recibió '{tipo}'.")
        return False
    # [FALTA VALIDACIONES, REVISAR SI SE COMBINA CON LAS OPERACIONES LOGICAS Y RELACIONAL]
    return True

# -----------------------------------
# VALIDACION DE ACCESO A SHELF
# -------------------------------------
def validar_acceso_shelf_por_indice(tabla_simbolos, nombre, indice):
    simbolo = tabla_simbolos.obtener(nombre, buscar_en_padre=True)
    if not simbolo or not simbolo["info"].get("es_arreglo_shelf", False):
        print(f"Error: '{nombre}' no es Shelf.")
        return False
    if not isinstance(indice, int):
        print(f"Error: Índice debe ser entero.")
        return False
    return True

