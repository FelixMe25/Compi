
# ===============================================================
#FAMILIAS_TOKEN - Clasificación semántica de tokens
# ===============================================================

FAMILIAS_TOKEN = {
    # --------------------------------------------------------------
    # Estructura general del programa
    # --------------------------------------------------------------
    "WorldName": "Main",  # Define nombre del mundo
    "SpawnPoint": "Punto de entrada",       # Inicio de ejecución
    "worldSave": "Fin de programa",   # Marca el cierre del programa

    # --------------------------------------------------------------
    # Secciones de declaración
    # --------------------------------------------------------------
    "Bedrock": "Sección de Constante",
    "ResourcePack": "Sección de tipos",
    "Inventory": "Sección de variables",
    "Recipe": "Sección de prototipos",
    "CraftingTable": "Sección de rutinas",
    "Obsidian": "Sección de asignación de constantes",
    "Anvil": "Sección de asignación de tipos",
    
    # --------------------------------------------------------------
    # Tipos de datos
    # --------------------------------------------------------------
    "Stack": "Tipo entero",
    "Rune": "Tipo carácter",
    "Spider": "Tipo string",
    "Torch": "Tipo booleano",
    "Chest": "Tipo conjunto",
    "Book": "Tipo archivo",
    "Ghast": "Tipo flotante",
    "Shelf": "Tipo arreglo",
    "Entity": "Tipo registro",

    # --------------------------------------------------------------
    # Literales
    # --------------------------------------------------------------
    "On": "Literal booleana",
    "Off": "Literal booleana",
    "{::}": "Literal conjunto",
    "{/ }": "Literal archivo",
    "-3.14": "Literal flotante",
    "5": "Literal entero",
    "-5": "Literal entero",
    "'K'": "Literal carácter",
    "\"string\"": "Literal string",
    "[1,2,3]": "Literal arreglo",
    "{id:value}": "Literal registro",

    # --------------------------------------------------------------
    # Accesos
    # --------------------------------------------------------------
    "[2][3][4]": "Acceso arreglo",
    "string[1]": "Acceso string",
    "registro@campo": "Acceso registro",

    # --------------------------------------------------------------
    # Asignaciones
    # --------------------------------------------------------------
    "=": "Asignación",
    "+=": "Asignación compuesta",
    "-=": "Asignación compuesta",
    "*=": "Asignación compuesta",
    "/=": "Asignación compuesta",
    "%=": "Asignación compuesta",

    # --------------------------------------------------------------
    # Operaciones aritméticas (enteros)
    # --------------------------------------------------------------
    "+": "Suma int",
    "-": "Resta int",
    "*": "Producto int",
    "//": "División int",
    "%": "Módulo int",

    # --------------------------------------------------------------
    # Operaciones sobre caracteres
    # --------------------------------------------------------------
    "soulsand": "Incremento",
    "magma": "Decremento",
    "isEngraved": "isAlpha",
    "isInscribed": "isDigit",
    "etchUp": "Mayúscula",
    "etchDown": "Minúscula",

    # --------------------------------------------------------------
    # Operadores lógicos
    # --------------------------------------------------------------
    "and": "Operador AND",
    "or": "Operador OR",
    "not": "Operador NOT",
    "xor": "Operador XOR",

    # --------------------------------------------------------------
    # Operaciones con strings
    # --------------------------------------------------------------
    "bind": "Concatenar",
    "#": "Largo de string",
    "from ##": "Corte desde posición",
    "except ##": "Corte hasta posición",
    "seek": "Búsqueda en string",

    # --------------------------------------------------------------
    # Operaciones con conjuntos
    # --------------------------------------------------------------
    "add": "Agregar a conjunto",
    "drop": "Eliminar del conjunto",
    "feed": "Intersección entre conjuntos",
    "map": "Pertenencia a conjunto",
    "void": "Conjunto vacío",
    "kill": "Eliminar todo el conjunto",

    # --------------------------------------------------------------
    # Operaciones con archivos
    # --------------------------------------------------------------
    "unlock": "Abrir archivo",
    "lock": "Cerrar archivo",
    "craft": "Crear archivo",
    "gather": "Leer archivo",
    "forge": "Escribir archivo",
    "expand": "Juntar contenido de archivos",

    # --------------------------------------------------------------
    # Operaciones con flotantes
    # --------------------------------------------------------------
    ":+": "Suma flotantes",
    ":-": "Resta flotantes",
    ":*": "Multiplicación flotantes",
    ":%": "Módulo flotantes",
    "://": "División flotantes",

    # --------------------------------------------------------------
    # Comparación
    # --------------------------------------------------------------
    "<": "Menor que",
    ">": "Mayor que",
    "<=": "Menor o igual",
    ">=": "Mayor o igual",
    "is": "Igualdad",
    "isNot": "Desigualdad",

    # --------------------------------------------------------------
    # Control de flujo y estructuras
    # --------------------------------------------------------------
    "PolloCrudo": "Bloque de instrucciones (inicio)",
    "PolloAsado": "Bloque de instrucciones (fin)",
    "repeater": "While",
    "target": "If",
    "craft hit": "Then",
    "miss": "Else",
    "jukebox": "Switch",
    "spawner": "Repeat-Until",
    "walk": "For",
    "wither": "With",
    "creeper": "Break",
    "enderperl": "Continue",
    "ragequit": "Halt",
    "respawn": "Return",

    # --------------------------------------------------------------
    # Declaración de funciones y procedimientos
    # --------------------------------------------------------------
    "Spell": "Encabezado función",
    "Ritual": "Encabezado procedimiento",

    # --------------------------------------------------------------
    # RETURN y size of 
    # --------------------------------------------------------------
    "respawn": "Return",
    "chunk": "Size of ",

    # --------------------------------------------------------------
    # Entrada / Salida estándar
    # --------------------------------------------------------------
    "hopper": "Entrada estándar",
    "dropper": "Salida estándar",

    # --------------------------------------------------------------
    # Sintaxis general
    # --------------------------------------------------------------
    ";": "Terminador",
    # --------------------------------------------------------------
    # Comentarios
    # --------------------------------------------------------------
    "$*": "Comentario bloque",
    "$$": "Comentario línea"
}
