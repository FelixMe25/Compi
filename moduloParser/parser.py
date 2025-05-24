# ================================================================
# Parser Sintáctico del Lenguaje Notch 
# ---------------------------------------------------------------
# Este módulo implementa la clase `Parser`, que se encarga de:
# - Leer los tokens generados por el `Scanner` (analizador léxico)
# - Verificar su validez sintáctica según las reglas del lenguaje
# - Validar identificadores, estructuras y secciones del programa
# - Detectar errores y saltar secciones inválidas si es necesario
# - Procesar instrucciones como declaraciones, bloques y expresiones
# ================================================================

from moduloScanner.scanner import Scanner
from moduloScanner.familias import FAMILIAS_TOKEN
from moduloParser.tabla_simbolos import TablaSimbolos

from moduloParser.comentarios import procesar_comentarios
from moduloParser.constantes import seccion_constante
from moduloParser.entrada_salida import procesar_entrada_estandar, procesar_salida_estandar
from moduloParser.prototipos_rutinas import procesar_funcion_o_procedimiento, seccion_prototipo
from moduloParser.tipos import seccion_tipos

from moduloParser.operaciones import (
    procesar_entity_en_inventory,
    _procesar_incremento_decremento,
    procesar_asignacion_compuesta,
    _procesar_operaciones_enteros,
    procesar_operacion_rune,
    procesar_operacion_torch,
    procesar_operacion_spider,
    procesar_operacion_chest,
    procesar_consulta_chest,
    procesar_operacion_archivo,
    procesar_asignacion_archivo,
    procesar_escritura_archivo,
    _procesar_operaciones_ghast
)

from moduloParser.instrucciones import (
    manejo_bloque,
    procesar_repeater,
    procesar_target,
    procesar_instruccion_switch,
    procesar_spawner,
    procesar_walk,
    procesar_wither,
    procesar_creeper,
    procesar_enderperl,
    procesar_ragequit
)

from moduloParser.variables import (
    seccion_variables,
    procesar_dato_stack,
    procesar_dato_rune,
    procesar_dato_spider,
    procesar_dato_torch,
    procesar_dato_chest,
    procesar_dato_book,
    procesar_dato_ghast,
    procesar_dato_entity,
    procesar_arreglo
)


class Parser:
    def __init__(self, archivo):
        # Inicializa el escáner con el archivo fuente
        self.scanner = Scanner()
        self.scanner.InicializarScanner(archivo)

        self.tokens = []              # Lista de tokens a procesar
        self.token_actual = None      # Token que se está evaluando
        self.current = 0              # Índice actual en la lista de tokens
        self.bandera_bloque = 0      
        self.tipos_personalizados = {}  # Tipos definidos por el usuario

        self.tabla = TablaSimbolos()


        self.cargar_tokens()

    # Extrae todos los tokens del archivo usando el scanner
    def cargar_tokens(self):
        while True:
            token = self.scanner.DemeToken()
            if token is None:
                break
            self.tokens.append(token)
        self.scanner.FinalizarScanner()
        if self.tokens:
            self.token_actual = self.tokens[0]


    # Avanza al siguiente token
    def avanzar(self):
        self.current += 1
        if self.current < len(self.tokens):
            self.token_actual = self.tokens[self.current]
        else:
            self.token_actual = (None, None)  

    # Retrocede al token anterior
    def retroceder(self):
        if self.current > 0:
            self.current -= 1
            self.token_actual = self.tokens[self.current]


    # Retorna tipo y valor del token actual
    def token_actual_tipo_valor(self):
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return (None, None)


    # Modifica el token actual (por ejemplo, para marcar errores)   
    def actualizar_token(self, tipo, valor):
        if 0 <= self.current < len(self.tokens):
            self.tokens[self.current] = (tipo, valor)
            self.token_actual = (tipo, valor)

    # Verifica si una palabra es reservada del lenguaje
    def es_palabra_reservada(self, palabra):
        return palabra in FAMILIAS_TOKEN
    

    # Valida que un token sea un identificador válido
    def validar_identificador(self, tipo, valor):
        if tipo != "IDENTIFICADOR":
            print(f"Error: Se esperaba un identificador, pero se encontró ({tipo}, '{valor}')")
            self.actualizar_token("ERROR", valor)
            return False
        if self.es_palabra_reservada(valor):
            print(f"Error: '{valor}' es una palabra reservada y no puede usarse como identificador.")
            self.actualizar_token("ERROR", valor)
            return False
        tipos_no_validos = {
            "Stack", "Rune", "Spider", "Torch", "Chest", "Book", "Ghast", "Shelf", "Entity"
        }
        if valor in tipos_no_validos:
            print(f"Error: '{valor}' es un tipo de dato y no puede usarse como identificador.")
            self.actualizar_token("ERROR", valor)
            return False
        return True
    

    # Salta tokens hasta que encuentra una palabra clave válida de sección
    def saltar_hasta_seccion_valida(self):
        # Salta tokens hasta que encuentra una palabra clave válida de sección
        secciones_validas = {
            "Bedrock", "ResourcePack", "Inventory", "Recipe", "CraftingTable", "worldSave"
        }
        print("↪ Saltando hasta la siguiente sección válida...\n")
        while not self.fin():
            tipo, valor = self.token_actual_tipo_valor()
            if tipo in ["SECCION_CONSTANTES", "SECCION_VARIABLES", "SECCION_TIPOS", "SECCION_PROTOTIPOS", "SECCION_RUTINAS", "FIN_PROGRAMA"]:
                if valor in secciones_validas:
                    return
            self.avanzar()


    # Valida el identificador o salta hasta el siguiente punto y coma si hay error
    def validar_identificador_o_saltar(self):
        tipo, valor = self.token_actual_tipo_valor()
        if not self.validar_identificador(tipo, valor):
            print("↪ Saltando hasta el final de la declaración por error...")
            while not self.fin():
                tipo_salto, valor_salto = self.token_actual_tipo_valor()
                if tipo_salto == "SIMBOLO" and valor_salto == ";":
                    self.avanzar()
                    break
                self.avanzar()
            return None
        return valor

    # Salta tokens hasta el siguiente punto y coma
    def saltar_hasta_puntoycoma(self):
        while not self.fin():
            tipo, valor = self.token_actual_tipo_valor()
            if tipo == "SIMBOLO" and valor == ";":
                self.avanzar()
                break
            self.avanzar()

    # salta hasta la siguiente instruccion 
    def saltar_hasta_siguiente_instrucion(self):
        tokens_sincronizacion = {
            "IDENTIFICADOR", 
            "PALABRA_RESERVADA",
            "PUNTO_ENTRADA", 
            "FIN_PROGRAMA", 
            "MAS_DE_UNA_INSTRUCCION",
            "TIPO_ENTERO", "TIPO_BOOL", "TIPO_STRING", "TIPO_FLOAT",
            "TIPO_CONJUNTO", "TIPO_ARCHIVO", "TIPO_REGISTROS", "TIPO_ARREGLOS"
        }

        while not self.fin():
            tipo, _ = self.token_actual_tipo_valor()
            if tipo in tokens_sincronizacion:
                return
            self.avanzar()

    # salta hasta coma o punto y coma
    def saltar_hasta_coma_o_puntoycoma(self):
        while not self.fin():
            tipo, val = self.token_actual_tipo_valor()
            if tipo == "SIMBOLO" and val in [",", ";"]:
                self.avanzar()
                break
            self.avanzar()

    # saltta hasta instruccion actual
    def parse_instruccion_actual(self):
        tipo, valor = self.token_actual_tipo_valor()

        if tipo == 'MAS_DE_UNA_INSTRUCCION' and valor == 'PolloCrudo':
            manejo_bloque(self, tipo, valor)
        elif tipo == "OPERADOR_SALIDA" and valor.startswith("dropper"):
            procesar_salida_estandar(self)
        elif tipo == "OPERADOR_INCREMENTO" and valor == "soulsand":
            _procesar_operaciones_enteros(self)
        elif tipo == "OPERADOR_DECREMENTO" and valor == "magma":
            _procesar_operaciones_enteros(self)
        elif tipo == "IDENTIFICADOR":
            tipo_sig1, val_sig1 = self.tokens[self.current + 1] if self.current + 1 < len(self.tokens) else (None, None)
            tipo_sig2, val_sig2 = self.tokens[self.current + 2] if self.current + 2 < len(self.tokens) else (None, None)
            tipo_sig3, val_sig3 = self.tokens[self.current + 3] if self.current + 3 < len(self.tokens) else (None, None)
            tipo_sig4, val_sig4 = self.tokens[self.current + 4] if self.current + 4 < len(self.tokens) else (None, None)

            if tipo_sig1 == "OPERADOR" and val_sig1 == "=" and \
            tipo_sig2 in ["IDENTIFICADOR", "LITERAL_ENTERO"] and \
            tipo_sig3 == "OPERADOR" and val_sig3 in ["+", "-", "*", "//", "%"] and \
            tipo_sig4 in ["IDENTIFICADOR", "LITERAL_ENTERO"]:
                _procesar_operaciones_enteros(self)
            else:
                self.avanzar()
        else:
            self.avanzar()

    # processa instruccion actual 
    def _procesar_instruccion_actual(self, tipo, valor):
        if tipo == "OPERADOR_SALIDA" and valor.startswith("dropper"):
            procesar_salida_estandar(self)
        elif tipo == "OPERADOR_ENTRADA" and valor.startswith("hopper"):
            procesar_entrada_estandar(self)
        elif tipo == "OPERADOR_INCREMENTO":
            self.procesar_operacion_incremento()
        elif tipo == "OPERADOR_DECREMENTO":
            self.procesar_operacion_decremento()
        elif tipo == "OPERACION_WHILE" and valor == "repeater":
            procesar_repeater(self)
        elif tipo == "OPERACION_IF" and valor == "target":
            procesar_target(self)
        elif tipo == "OPERACION_SWITCH" and valor == "jukebox":
            procesar_instruccion_switch(self)
        elif tipo == "OPERACION_BREAK" and valor == "creeper":
            procesar_creeper(self)

        else:
            self.avanzar()

    # Retorna True si ya se procesaron todos los tokens
    def fin(self):
        return self.current >= len(self.tokens)

    # Inicia el análisis sintáctico del archivo
    def parse(self):
        print("Iniciando análisis sintáctico...\n")
        tiene_worldname = False
        tiene_spawnpoint = False
        tiene_worldsave = False

        while not self.fin():
            tipo, valor = self.token_actual_tipo_valor()

            # --- Estructura del programa ---
            if tipo == 'INICIO_PROGRAMA' and valor.startswith('WorldName'):
                tiene_worldname = True
                self.titulo_programa(tipo, valor)
                continue

            elif tipo == 'FIN_PROGRAMA':
                print(f"DEBUG: Fin de programa encontrado con valor: {valor}")
                if valor == 'worldSave':
                    print("-- Reconocido 'worldSave'")
                    tiene_worldsave = True
                self.cierre_programa(tipo, valor)

            elif tipo == 'MAS_DE_UNA_INSTRUCCION' and valor == 'PolloCrudo':
                manejo_bloque(self, tipo, valor)

            elif tipo == "FIN_BLOQUE" and valor == "PolloAsado":
                self.cierre_bloque(tipo, valor)

            elif tipo == 'PUNTO_ENTRADA' and valor == 'SpawnPoint':
                tiene_spawnpoint = True
                self.punto_entrada(tipo, valor)

            elif tipo == 'ENCABEZADO_FUNCIONES' and valor == 'Spell':
                procesar_funcion_o_procedimiento(self)

            elif tipo == 'ENCABEZADO_PROCEDIMIENTOS' and valor == 'Ritual':
                procesar_funcion_o_procedimiento(self)

            elif tipo == 'OPERADOR_ENTRADA' and valor.startswith('hopper'):
                procesar_entrada_estandar(self)

            elif tipo == 'OPERADOR_SALIDA' and valor.startswith('dropper'):
                procesar_salida_estandar(self)

            elif tipo == 'COMENTARIO' and valor == 'Inventory':
                seccion_tipos(self, tipo, valor)

            # --- Secciones del programa ---
            elif tipo == 'SECCION_CONSTANTES' and valor == 'Bedrock':
                seccion_constante(self, tipo, valor)

            elif tipo == 'SECCION_TIPOS' and valor == 'ResourcePack':
                seccion_tipos(self, tipo, valor)

            elif tipo == 'SECCION_VARIABLES' and valor == 'Inventory':
                seccion_variables(self, tipo, valor)

            elif tipo == 'SECCION_PROTOTIPOS' and valor == 'Recipe':
                seccion_prototipo(self, tipo, valor)

            elif tipo == 'SECCION_RUTINAS' and valor == 'Recipe':
                seccion_prototipo(self, tipo, valor)
                procesar_funcion_o_procedimiento(self)

            # --- Tipos de datos (literales y declaraciones) ---
            elif tipo == 'TIPO_ENTERO' and valor == 'Stack':
                procesar_dato_stack(self)
                _procesar_operaciones_enteros(self)

            elif tipo == 'TIPO_CARACTER' and valor == 'Rune':
                procesar_dato_rune(self)

            elif tipo == 'TIPO_STRING' and valor == 'Spider':
                procesar_dato_spider(self)

            elif tipo == 'TIPO_BOOL' and valor == 'Torch':
                procesar_dato_torch(self)

            elif tipo == 'TIPO_CONJUNTO' and valor == 'Chest':
                procesar_dato_chest(self)

            elif tipo == 'TIPO_ARCHIVO' and valor == 'Book':
                procesar_dato_book(self)

            elif tipo == 'TIPO_FLOAT' and valor == 'Ghast':
                procesar_dato_ghast(self)

            elif tipo == 'TIPO_REGISTROS' and valor == 'Entity':
                procesar_dato_entity(self)

            elif tipo == 'TIPO_ARREGLOS' and valor == 'Shelf':
                procesar_arreglo(self)
            
            # Instrucciones
            elif tipo == "INSTRUCCION_REPETIR":
                procesar_repeater(self)
                continue

            elif tipo == "INSTRUCCION_CONDICIONAL":
                procesar_target(self)
                continue

            elif tipo == "OPERACION_WHILE" and valor == "repeater":
                procesar_repeater(self)
                continue

            elif tipo == "OPERACION_SWITCH" and valor == "jukebox":
                procesar_instruccion_switch(self)

            elif tipo == "OPERACION_REPEAT" and valor == "spawner":
                procesar_spawner(self)
                continue

            elif tipo == "OPERACION_WITH":
                procesar_wither(self)

            elif tipo == "OPERACION_BREAK":
                procesar_creeper(self)

            elif tipo == "OPERACION_CONTINUE":
                procesar_enderperl(self)

            elif tipo == "OPERACION_HALT":
                procesar_ragequit(self)
            
            elif tipo== "OPERACION_FOR" and valor == "walk":
                procesar_walk(self)
                continue
            elif tipo == 'ENCABEZADO_FUNCIONES' and valor == 'Spell':
                procesar_funcion_o_procedimiento(self)

            elif tipo == 'ENCABEZADO_PROCEDIMIENTOS' and valor == 'Ritual':
                procesar_funcion_o_procedimiento(self)


            elif tipo == 'PALABRA_RESERVADA' and valor == 'PolloCrudo' and self.bandera_bloque == 0:
                manejo_bloque(self, tipo, valor)

            elif tipo == "IDENTIFICADOR":
                tipo_sig1, val_sig1 = self.tokens[self.current + 1] if self.current + 1 < len(self.tokens) else (None, None)
                tipo_sig2, val_sig2 = self.tokens[self.current + 2] if self.current + 2 < len(self.tokens) else (None, None)
                tipo_sig3, val_sig3 = self.tokens[self.current + 3] if self.current + 3 < len(self.tokens) else (None, None)
                tipo_sig4, val_sig4 = self.tokens[self.current + 4] if self.current + 4 < len(self.tokens) else (None, None)

                if tipo_sig1 == "OPERADOR" and val_sig1 == "=" and \
                tipo_sig2 in ["IDENTIFICADOR", "LITERAL_ENTERO"] and \
                tipo_sig3 == "OPERADOR" and val_sig3 in ["+", "-", "*", "//", "%"] and \
                tipo_sig4 in ["IDENTIFICADOR", "LITERAL_ENTERO"]:
                    _procesar_operaciones_enteros(self)
                    continue
            # Reconocer inicio de la sección CraftingTable
            elif tipo == "SECCION_RUTINAS":
                print(f"---- Sección de rutinas detectada: {valor}")
                self.avanzar()
                while not self.fin():
                    tipo, valor = self.token_actual_tipo_valor()

                    if tipo in ["ENCABEZADO_FUNCIONES", "ENCABEZADO_PROCEDIMIENTOS"]:
                        procesar_funcion_o_procedimiento(self)
                        continue

                    elif tipo == "FIN_PROGRAMA" and valor == "worldSave":
                        break

                    else:
                        self.avanzar()
            else:
                self.avanzar()


    #----------------------------------------------------------------------------
    #                          INICIO DEL PROGRAMA 
    #----------------------------------------------------------------------------
    def titulo_programa(self, token, valor):
        print(f"-----------------------------------------------------------------------")
        print(f"---- Título del programa: {valor}")
        if ':' in valor:
            print("---- Título válido.\n")
        else:
            print("Error: Se esperaba ':' al final del encabezado 'WorldName'.")
            print(f"-----------------------------------------------------------------------")
            self.actualizar_token('ERROR', valor)
        self.avanzar()



    #----------------------------------------------------------------------------
    #                         PUNTO DE ENTRADA (main)
    #----------------------------------------------------------------------------
    # No se permiten manejo de bloques dentro del punto de entrada 
    # Solo debe haber un unico punto de entrada 
    # Debe estar antes del cierre 
    # Toda instrucción debe terminar con punto y  
    # declaraciones o contantes deben ir antes 
    #
    # SpawnPoint
    #   instrucciones;
    # worldSave
    #
    # SpawnPoint detecta:
    # - errores sintácticos (ERROR)
    # - cierre con worldSave
    # - soulsand / magma (incremento/decremento)
    # - operaciones enteras tipo: x = a + b
    # - hopperTipo() → entrada estándar
    # - dropperTipo(valor) → salida estándar

    #----------------------------------------------------------------------------
    def punto_entrada(self, tipo, valor):
        print(f"-----------------------------------------------------------------------")
        print(f"---- Punto de entrada detectado con: {valor}")
        self.avanzar()

        while not self.fin():
            tipo_actual, valor_actual = self.token_actual_tipo_valor()

            if tipo_actual == "ERROR":
                print(f"Error sintáctico detectado: {valor_actual}")
                print(f"-----------------------------------------------------------------------")
                self.avanzar()
                continue

            if tipo_actual == "FIN_PROGRAMA" and valor_actual == "worldSave":
                print(f" Cierre del programa detectado con: {valor_actual}")
                print(f"-----------------------------------------------------------------------")
                self.avanzar()
                return

            # Asignación compuesta tipo: gold += 5;
            tipo_sig1, val_sig1 = self.tokens[self.current + 1] if self.current + 1 < len(self.tokens) else (None, None)
            tipo_sig2, val_sig2 = self.tokens[self.current + 2] if self.current + 2 < len(self.tokens) else (None, None)

            if tipo_actual == "IDENTIFICADOR" and tipo_sig1 == "OPERADOR" and val_sig1 in ["+=", "-=", "*=", "//=", "%="]:
                if tipo_sig2 in ["LITERAL_ENTERO", "IDENTIFICADOR"]:
                    procesar_asignacion_compuesta(self)
                    continue
                else:
                    print(f"Error: Se esperaba un valor válido después de '{val_sig1}' en asignación compuesta.")
                    print(f"-----------------------------------------------------------------------")
                    self.avanzar()
                    continue

            # Operaciones estándar con "="
            tipo_sig3, val_sig3 = self.tokens[self.current + 3] if self.current + 3 < len(self.tokens) else (None, None)
            tipo_sig4, val_sig4 = self.tokens[self.current + 4] if self.current + 4 < len(self.tokens) else (None, None)

            if tipo_sig1 == "OPERADOR" and val_sig1 == "=":

                #------------------- Operaciones tipo de dato entero 
                if tipo_sig2 in ["IDENTIFICADOR", "LITERAL_ENTERO"] and \
                tipo_sig3 == "OPERADOR" and val_sig3 in ["+", "-", "*", "//", "%"] and \
                tipo_sig4 in ["IDENTIFICADOR", "LITERAL_ENTERO"]:
                    _procesar_operaciones_enteros(self)
                    continue

                #------------------- Operaciones tipo de dato caracter 
                elif tipo_sig2 in ["OPERACION_ESLETRA", "OPERACION_ESDIGITO", "MAYUSCULA", "MINUSCULA"] and \
                    tipo_sig3 == "IDENTIFICADOR" and tipo_sig4 == "SIMBOLO" and val_sig4 == ";":
                    procesar_operacion_rune(self)
                    continue

                #--------------------Operaciones tipo de dato conjunto 
                elif tipo_sig3 in ["OPERADOR_AGREGAR", "OPERADOR_ELIMINAR", "OPERADOR_INSERCCION", "OPERADOR_PERTENENCIA"]:
                    procesar_operacion_chest(self)
                    continue

                #--------------------Operaciones tipo de dato flotante 
                elif tipo_sig2 in ["IDENTIFICADOR", "LITERAL_FLOAT"] and \
                    tipo_sig3 == "OPERADOR_FLOAT" and val_sig3 in [":+", ":-", ":*", "://", ":%"] and \
                    tipo_sig4 in ["IDENTIFICADOR", "LITERAL_FLOAT"]:
                    _procesar_operaciones_ghast(self)
                    continue

                #-------------------Operaciones de tipo de dato string 
                elif tipo_sig2 in [
                    "LARGO_STRING", "CONCATENAR_STRING", "CORTAR_STRING",
                    "RECORTAR_STRING", "BUSCAR_STRING", "IDENTIFICADOR", "ACCESO_STRING"
                ]:
                    procesar_operacion_spider(self)
                    continue

                # ----------------- Operaciones tipo de dato archivo 
                elif tipo_actual in ["ABRIR_ARCHIVO", "CERRAR_ARCHIVO", "CREAR_ARCHIVO"]:
                    procesar_operacion_archivo(self)
                    continue
                elif tipo_actual == "IDENTIFICADOR" and val_sig1 == "=" and tipo_sig2 == "LEER_ARCHIVO":
                    procesar_asignacion_archivo(self)
                    continue
                elif tipo_actual == "IDENTIFICADOR" and tipo_sig1 == "ESCRIBIR_ARCHIVO":
                    procesar_escritura_archivo(self)
                    continue

                 #------------------- Operaciones tipo booleano Torch ---------------------
                elif tipo_sig2 in ["IDENTIFICADOR", "LITERAL_BOOL"] and \
                    tipo_sig3 == "OPERADOR_LOGICO" and val_sig3 in ["and", "or", "xor"] and \
                    tipo_sig4 in ["IDENTIFICADOR", "LITERAL_BOOL"]:
                    procesar_operacion_torch(self)
                    continue
                elif tipo_sig2 == "OPERADOR_LOGICO" and val_sig2 == "not":
                    procesar_operacion_torch(self)

            # ------ Otras operaciones 
            if tipo_actual == "OPERACION_WHILE" and valor_actual == "repeater":
                procesar_repeater(self)
                continue
            if tipo_actual == "OPERACION_IF" and valor_actual == "target":
                procesar_target(self)
                continue
            if tipo_actual == "OPERACION_SWITCH" and valor_actual == "jukebox":
                procesar_instruccion_switch(self)
                continue
            if tipo_actual == "OPERACION_REPEAT" and valor_actual == "spawner":
                procesar_spawner(self)
                continue
            if tipo_actual == "OPERACION_FOR" and valor_actual == "walk":
                procesar_walk(self)
                continue

            if tipo_actual == "OPERACION_WITH" and valor_actual == "wither":
                procesar_wither(self)
                continue

            if tipo_actual == "OPERACION_BREAK" and valor_actual == "creeper":
                procesar_creeper(self)
                continue


            if tipo_actual == "OPERADOR_ENTRADA" and valor_actual.startswith("hopper"):
                procesar_entrada_estandar(self)
                continue

            if tipo_actual == "OPERADOR_SALIDA" and valor_actual.startswith("dropper"):
                procesar_salida_estandar(self)
                continue

            if tipo_actual in ["LITERAL_CHAR", "OPERADOR_VACIO"]:
                procesar_consulta_chest(self)
            
                continue
         
            self.tabla.mostrar()
            self.avanzar()

    def cierre_programa(self, token, valor):
        print(f"--- Cierre del programa detectado con: {valor}")
        print(f"-----------------------------------------------------------------------")
        print("--- Programa cerrado correctamente con 'worldSave'.\n")
        print(f"-----------------------------------------------------------------------")
        self.avanzar()
