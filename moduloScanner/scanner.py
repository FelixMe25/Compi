# ================================================================
# Proyecto Etapa 1 - Analizador Léxico (Scanner) 
# Estudiantes: María Félix Méndez Abarca - Mariana Fernández Martínez

# Este archivo reconoce:
# - Palabras reservadas
# - Identificadores
# - Números enteros y flotantes
# - Strings, caracteres, booleanos
# - Archivos, arreglos, registros
# - Símbolos y operadores
# - Comentarios de línea y bloque
# ================================================================

import re

# Tamaño del buffer de lectura
BUFFER_SIZE = 128


# Tipos de token y su color asociado para el muro visual
TIPOS_TOKEN = {
    "PALABRA_RESERVADA": "deepskyblue",
    "IDENTIFICADOR": "mediumspringgreen",

    # Estrustura del programa
    "INICIO_PROGRAMA": "mediumpurple",      
    "PUNTO_ENTRADA": "mistyrose",   
    "FIN_PROGRAMA": "coral",    
    "MAS_DE_UNA_INSTRUCCION": "lightgoldenrodyellow",
    "FIN_BLOQUE":"lightgoldenrodyellow",
    "ENCABEZADO_FUNCIONES": "lightgoldenrodyellow",
    "ENCABEZADO_PROCEDIMIENTOS": "linen",
    "ENTRADA_ESTANDAR": "lightgoldenrodyellow",
    "SALIDA_ESTANDAR": "linen",


    # secciones
    "SECCION_CONSTANTES": "cadetblue",
    "SECCION_TIPOS": "darkorange",
    "SECCION_VARIABLES": "olivedrab",
    "SECCION_PROTOTIPOS": "darkgoldenrod",
    "SECCION_RUTINAS": "sienna",

    "ASIGNACION_CONSTANTE": "slateblue",
    "ASIGNACION_TIPO": "darkorchid",

    # Tipos de datos
    "TIPO_ENTERO": "lightyellow",
    "TIPO_CARACTER": "wheat",
    "TIPO_STRING": "moccasin",
    "TIPO_CONJUNTO": "lemonchiffon",
    "TIPO_ARCHIVO": "beige",
    "TIPO_FLOAT": "lightsalmon",
    "TIPO_ARREGLOS": "papayawhip",
    "TIPO_REGISTROS": "oldlace",
    "TIPO_BOOL": "oldlace",

    # Literales
    "LITERAL_ENTERO": "palegoldenrod",
    "LITERAL_CONJUNTO": "palegoldenrod",
    "LITERAL_STRING": "lightcyan",
    "LITERAL_CHAR": "lightpink",
    "LITERAL_BOOL": "palegreen",
    "LITERAL_ARCHIVO": "salmon",
    "LITERAL_ARREGLO": "khaki",
    "LITERAL_REGISTRO": "plum",
    "LITERAL_FLOAT": "plum",

    "SIMBOLO": "lightcoral",
    "OPERADOR": "lightgray",

    # Incremento y Decremento
    "OPERADOR_INCREMENTO": "gold",
    "OPERADOR_DECREMENTO": "tomato",

    # Operaciones básicas sobre caracteres
    "OPERADOR_ESLETRA": "mediumaquamarine",
    "OPERADOR_ESDIGITO": "mediumturquoise",
    "MAYUSCULA": "aquamarine",
    "MINUSCULA": "turquoise",

    # Operaciones lógicas solicitadas
    "OPERADOR_LOGICO": "mediumslateblue",

    # Operaciones de Strings solicitadas
    "CONCATENAR_STRING": "lightsteelblue",   # bind
    "CORTAR_STRING": "paleturquoise",        # from
    "RECORTAR_STRING": "lightcyan",          # except
    "BUSCAR_STRING": "lightblue",            # seek
    "LARGO_STRING": "skyblue",               # #
    "SEPARADOR_STRING_TERNARIO": "lightskyblue", # ##,

    # Operaciones de conjuntos solicitadas
    "OPERADOR_AGREGAR": "orchid",
    "OPERADOR_ELIMINAR": "lightseagreen",
    "OPERADOR_INSERCCION": "lightsalmon",
    "OPERADOR_PERTENENCIA": "mediumseagreen",
    "OPERADOR_BIOM": "springgreen",
    "OPERADOR_VACIO": "ivory",
    "OPERADOR_COMPARACION": "ivory",


    # Operaciones de archivos solicitadas
    "ABRI_ARCHIVO": "lightsteelblue",
    "CERRAR_ARCHIVO": "skyblue",
    "CREAR_ARCHIVO": "lightblue",
    "LEER_ARCHIVO": "paleturquoise",
    "ESCRIBIR_ARCHIVO": "cornflowerblue",

    # Operaciones de números flotantes
    "OPERADOR_FLOAT": "peachpuff",

    # Operaciones de comparación solicitadas
    "OPERADOR_COMPARACION": "navajowhite",

    # Manejo de Bloques de más de una instrucción
    "MAS_DE_UNA_INSTRUCCION": "honeydew",
    "FIN_BLOQUE": "honeydew",

    # WHILE 
    "OPERACION_WHILE": "lavender",

    # IF-THEN-ELSE
    "OPERACION_IF": "azure",

    # SWITCH
    "OPERACION_SWITCH": "seashell",

    # REPEAT
    "OPERACION_REPEAT": "mintcream",
    
    # FOR
    "OPERACION_FOR": "antiquewhite",

    # WITH
    "OPERACION_WITH": "ghostwhite",

    # BREAK
    "OPERACION_BREAK": "whitesmoke",

    # CONTINUE
    "OPERACION_CONTINUE": "floralwhite",

    # HALT
    "OPERACION_HALT": "gainsboro",


    # return
    "OPERACION_RETURN": "lightgreen",

    # Size of 
    "OPERACION_SIZE_OF": "cornsilk",

    "BLOQUE_CONTROL": "lightcyan",

    "COMENTARIO": "mediumgray",
    "ERROR": "lightgray",
    "ERROR_FATAL": "black"
}


class Scanner:
    def __init__(self):
        self.buffer = ""
        self.buffer_pos = 0
        self.file = None
        self.linea = 1
        self.columna = 1
        self.modo_esperando_funcion = False
        self.modo_esperando_titulo = False
        self.esperando_flecha_spell = False
        self.modo_spell = False
        self.modo_encabezado_ritual = False
        self.variables_spider = set()



    def InicializarScanner(self, filename):
        self.file = open(filename, 'r', encoding='utf-8')
        self.buffer = ""
        self.buffer_pos = 0
        self.refillBuffer()

    def FinalizarScanner(self):
        if self.file:
            self.file.close()

    def refillBuffer(self):
        new_data = self.file.read(BUFFER_SIZE)
        self.buffer = new_data
        self.buffer_pos = 0

    def demeCaracter(self):
        if self.buffer_pos >= len(self.buffer):
            self.refillBuffer()
            if not self.buffer:
                return None
        c = self.buffer[self.buffer_pos]
        self.buffer_pos += 1

        if c == '\n':
            self.linea += 1
            self.columna = 1
        else:
            self.columna += 1

        return c

    def peekCaracter(self):
        if self.buffer_pos >= len(self.buffer):
            return None
        return self.buffer[self.buffer_pos]

    def tomeCaracter(self):
        self.buffer_pos = max(0, self.buffer_pos - 1)
        self.columna = max(1, self.columna - 1)

    def DemeToken(self):
        lexema = ""
        c = self.demeCaracter()

        while c is not None and c.isspace():
            c = self.demeCaracter()

        if c is None:
            return None
        
        # ---------------------------------------------------------------------------------------------
        #                60. MANEJO DE ENTRADA Y SALIDA ESTÁNDAR - dropper TipoBásico(dato) y Hopper
        # ---------------------------------------------------------------------------------------------
        if c == 'd' or c == 'h':
            posible_inicio = c
            temp_pos = self.buffer_pos
            c = self.demeCaracter()
            while c is not None and c.isalpha():
                posible_inicio += c
                c = self.demeCaracter()

            operadores_validos = [
                "dropperStack", "dropperRune", "dropperSpider", "dropperTorch", "dropperBook", "dropperDNA",
                "hopperStack", "hopperRune", "hopperSpider", "hopperTorch", "hopperBook", "hopperDNA"
            ]

            if posible_inicio in operadores_validos:
                self.tomeCaracter()  # devolver el carácter que sigue, usualmente '('
                tipo_token = "OPERADOR_SALIDA" if posible_inicio.startswith("dropper") else "OPERADOR_ENTRADA"
                return (tipo_token, posible_inicio)
            elif posible_inicio.startswith("dropper") or posible_inicio.startswith("hopper"):
                # ⚠️ Tiene la forma de un operador, pero no es válido
                return ("ERROR", f"{posible_inicio} no es un operador válido. Tipo no reconocido.")
            else:
                # No se parece a nada especial, tratar como identificador
                self.buffer_pos = temp_pos
                c = posible_inicio[0]
            if lexema == 'Spider':
                # Guardar la variable tipo Spider
                temp = ""
                c = self.demeCaracter()
                while c is not None and c.isspace():
                    c = self.demeCaracter()
                while c is not None and (c.isalnum() or c == "_"):
                    temp += c
                    c = self.demeCaracter()
                if temp:
                    self.variables_spider.add(temp)
                    self.tomeCaracter()
                return ("TIPO_STRING", lexema)
            if c == ':':
                peek = self.peekCaracter()
                if peek == ':':
                    self.demeCaracter()
                    return ("SIMBOLO", "::")
                else:
                    return ("ERROR", ": (uso incorrecto)")





        if c == '-':
            peek = self.peekCaracter()
            if peek == '>':
                self.demeCaracter()
                return ("FLECHA", '->')
            else:
                lexema = '-'
                siguiente = self.peekCaracter()
                if siguiente == '=':
                    self.demeCaracter()
                    return ("OPERADOR", '-=')
                elif siguiente is not None and not siguiente.isspace() and not siguiente.isalnum():
                    return ("ERROR", '-' + siguiente + " (uso incorrecto del operador aritmético)")
                return ("OPERADOR", '-')
                

        if c.isalpha():
            lexema += c
            c = self.demeCaracter()
            while c is not None and (c.isalnum() or c == "_"):
                lexema += c
                c = self.demeCaracter()
            if c is not None:
                
                self.tomeCaracter()

            if lexema == "WorldName":
                 # Verificamos si viene un identificador y luego ":"
                nombre_mundo = ""
                c = self.demeCaracter()
                while c is not None and c.isspace():
                    c = self.demeCaracter()

                # Leer identificador del nombre del mundo
                while c is not None and (c.isalnum() or c == "_"):
                    nombre_mundo += c
                    c = self.demeCaracter()

                while c is not None and c.isspace():
                    c = self.demeCaracter()

                if c == ":" and nombre_mundo != "":
                    return ("INICIO_PROGRAMA", f"{lexema} {nombre_mundo}:")
                else:
                    # Devolvemos solo WorldName si no hay formato completo
                    self.tomeCaracter()
                    return ("INICIO_PROGRAMA", lexema)
            

            elif lexema == 'PolloCrudo':
                return ("MAS_DE_UNA_INSTRUCCION", lexema)

            elif lexema == 'PolloAsado':
                return ("FIN_BLOQUE", lexema)
            
            elif lexema == 'SpawnPoint':
                return ("PUNTO_ENTRADA", lexema)




            
            elif lexema == 'worldSave':
                return ("FIN_PROGRAMA", lexema)
            
            elif lexema == 'Torch':
                return ("TIPO_BOOL", lexema)
            
            elif lexema in ("On", "Off"):
                return ("LITERAL_BOOL", lexema)
        
            elif lexema == 'Bedrock':
                return ("SECCION_CONSTANTES", lexema)
            
            elif lexema == 'ResourcePack':
                return ("SECCION_TIPOS", lexema)

            elif lexema == 'Inventory':
                return ("SECCION_VARIABLES", lexema)

            elif lexema == 'Recipe':
                return ("SECCION_PROTOTIPOS", lexema)

            elif lexema == 'CraftingTable':
                return ("SECCION_RUTINAS", lexema)
            
            elif lexema == 'Obsidian':
                return ("ASIGNACION_CONSTANTE", lexema)
              
            elif lexema == 'Anvil':
                return ("ASIGNACION_TIPOS", lexema)

            elif lexema == 'Stack':
                return ("TIPO_ENTERO", lexema)
            
            elif lexema == 'Rune':
                return ("TIPO_CARACTER", lexema)
            
            elif lexema == 'Spider':
                return ("TIPO_STRING", lexema)
            
            elif lexema == 'Spider':
                # Leer el nombre de la variable
                nombre_variable = ""
                c = self.demeCaracter()
                while c is not None and c.isspace():
                    c = self.demeCaracter()

                while c is not None and (c.isalnum() or c == "_"):
                    nombre_variable += c
                    c = self.demeCaracter()

                if nombre_variable:
                    self.variables_spider.add(nombre_variable)

                if c is not None:
                    self.tomeCaracter()

                return ("TIPO_STRING", "Spider")

            
            elif lexema == 'Chest':
                return ("TIPO_CONJUNTO", lexema)
            
            elif lexema == 'Book':
                return ("TIPO_ARCHIVO", lexema)
            
            elif lexema == 'Ghast':
                return ("TIPO_FLOAT", lexema)
            
            elif lexema == 'Shelf':
                return ("TIPO_ARREGLOS", lexema)
            
            elif lexema == 'Entity':
                return ("TIPO_REGISTROS", lexema)
            
            elif lexema == 'soulsand':
                return ("OPERADOR_INCREMENTO", lexema) 
            
            elif lexema == 'magma':
                return ("OPERADOR_DECREMENTO", lexema)  
            
            #----------------- Operaciones básicas sobre caracteres ------------------------------
            elif lexema == 'isEngraved':
                return ("OPERACION_ESLETRA", lexema)
            
            elif lexema == 'isInscribed':
                return ("OPERACION_ESDIGITO", lexema)
            
            elif lexema == 'etchUp':
                return ("MAYUSCULA", lexema)
            
            elif lexema == 'etchDown':
                return ("MINUSCULA", lexema)
            
            
            #----------------- Operaciones lógicas solicitadas ------------------------------
            # Operadores lógicos para Torch
            elif lexema in ['and', 'or', 'xor', 'not']:
                return ("OPERADOR_LOGICO", lexema)


            #----------------- Operaciones de Strings solicitadas ------------------------------
            elif lexema == "bind":
                return ("CONCATENAR_STRING", lexema)

            elif lexema == "from":
                return ("CORTAR_STRING", lexema)

            elif lexema == "except":
                return ("RECORTAR_STRING", lexema)

            elif lexema == "seek":
                return ("BUSCAR_STRING", lexema)


            #----------------- Operaciones de conjuntos solicitadas ------------------------------
            elif lexema == 'add':
                return ("OPERADOR_AGREGAR", lexema)
            
            elif lexema == 'drop':
                return ("OPERADOR_ELIMINAR", lexema)  
            
            elif lexema == 'feed':
                return ("OPERADOR_INSERCCION", lexema)  
            
            elif lexema == 'map':
                return ("OPERADOR_PERTENENCIA", lexema)  

            elif lexema == 'biom':
                return ("OPERADOR_BIOM", lexema)  
            
            elif lexema == 'void':
                return ("OPERADOR_VACIO", lexema)  


         #----------------- Operaciones de strings solicitadas ------------------------------
            elif lexema == 'unlock':
                return ("ABRIR_ARCHIVO", lexema)
            
            elif lexema == 'lock':
                return ("CERRAR_ARCHIVO", lexema)  
            
            elif lexema == 'make':
                return ("CREAR_ARCHIVO", lexema)  
            
            elif lexema == 'gather':
                return ("LEER_ARCHIVO", lexema)  

            elif lexema == 'forge':
                return ("ESCRIBIR_ARCHIVO", lexema)  
            
        #----------------- 	Operaciones de números flotantes ------------------------------
        #OPERADOR_FLOAT


    

        #----------------- Operaciones de comparación solicitadas ------------------------
        #OPERADOR_COMPARACION




        #----------------- Operaciones de comparación solicitadas ------------------------
        #MAS_DE_UNA_INSTRUCCION
            
            elif lexema == 'PolloCrudo':
                return ("MAS_DE_UNA_INSTRUCCION", lexema)

            elif lexema == 'PolloAsado':
                return ("FIN_BLOQUE", lexema)

        
        # INSTRUCCIONES DE FLUJO

            elif lexema == 'repeater':
                return ("OPERACION_WHILE", lexema)

            elif lexema == 'target':
                return ("OPERACION_IF", lexema)

            elif lexema == 'hit':
                return ("BLOQUE_HIT", lexema)

            elif lexema == 'miss':
                return ("BLOQUE_MISS", lexema)

            elif lexema == 'jukebox':
                return ("OPERACION_SWITCH", lexema)

            elif lexema == 'disc':
                return ("CASO_SWITCH", lexema)

            elif lexema == 'silence':
                return ("DEFAULT_SWITCH", lexema)

            elif lexema == 'creeper':
                return ("INSTRUCCION_BREAK", lexema)

            elif lexema == 'spawner':
                return ("OPERACION_REPEAT", lexema)

            elif lexema == 'exhausted':
                return ("CONDICION_REPEAT", lexema)

            elif lexema == 'walk':
                return ("OPERACION_FOR", lexema)

            elif lexema == 'set':
                return ("SET_FOR", lexema)

            elif lexema == 'to':
                return ("TO_FOR", lexema)

            elif lexema == 'step':
                return ("STEP_FOR", lexema)

            elif lexema == 'craft':
                return ("INICIO_BLOQUE", lexema)

            elif lexema == 'wither':
                return ("OPERACION_WITH", lexema)  
        #BREAK

            elif lexema == 'creeper':
                return ("OPERACION_BREAK", lexema)  
        #CONTINUE

            elif lexema == 'enderperl':
                return ("OPERACION_CONTINUE", lexema)  
        #HALT

            elif lexema == 'ragequit':
                return ("OPERACION_HALT", lexema)  
       
        #Encabezado de funciones SPELL

            elif lexema == 'Spell':
                return ("ENCABEZADO_FUNCIONES", lexema)  
            
        #Encabezado de procedimientos

            elif lexema == 'Ritual':
                return ("ENCABEZADO_PROCEDIMIENTOS", lexema)  

        #return

            elif lexema == 'respawn ':
                return ("OPERACION_RETURN", lexema)  
        #Size of

            elif lexema == 'chunk':
                return ("OPERACION_SIZE_OF", lexema)  
            elif c == '[':
                return ("SIMBOLO", '[')

            elif c == ']':
                return ("SIMBOLO", ']')



            return ("IDENTIFICADOR", lexema)
    












        # ---------------------------------------------------------------------------------------------
        #                        9. SISTEMA DE ASIGNACION DE TIPOS (Anvil)
        # Declara una variable y le asigna un tipo..
        # Anvil vida -> Stack
        # ---------------------------------------------------------------------------------------------
        elif lexema == 'Anvil':
            identificador = self.leerPalabra()
            flecha = self.leerPalabra()
            tipo = self.leerPalabra()
            if flecha == '->':
                return ("ASIGNACION_TIPO", f"{lexema} {identificador} -> {tipo}")
            else:
                return ("ERROR", f"{lexema} {identificador} {flecha} {tipo} (esperado '->')")


        # ---------------------------------------------------------------------------------------------
        #                                 11. TIPO DE DATO ENTERO
        #                                 17. TIPO DE ENTRADA FLOTANTE
        # ---------------------------------------------------------------------------------------------
        #ACEPTA
        # ENTEROS:123, -456
        # FLOTANTES: 1.5, -0.01

        #RECHAZA

        #-.5, .5, 5. (punto sin número antes o después)
        #12,345 (coma)
        #123a (letra dentro del número)

        # ---------------------------------------------------------------------------------------------
            
        elif c.isdigit() or (c == '-' and self.peekCaracter() and self.peekCaracter().isdigit()):
            if c == '-':
                lexema += c
                c = self.demeCaracter()
                if c is None or not c.isdigit():
                    return ("ERROR", lexema + (c or ''))  # Caso: '-' solo o '-x'

            lexema += c
            c = self.demeCaracter()
            is_float = False

            while c is not None and (c.isdigit() or c == '.' or c.isalpha()):
                if c == '.':
                    if is_float:
                        return ("ERROR", lexema + "." + " (contiene más de un punto decimal)")
                    is_float = True
                elif c.isalpha():
                    return ("ERROR", lexema + c + " (contiene una letra)")
                
                lexema += c
                c = self.demeCaracter()

            # Si encontramos una coma u otro símbolo separador, lo devolvemos al flujo
            if c in {',', ';', ')', '(', ' '}:
                self.tomeCaracter()

            # Validar flotantes mal formados (como '.5', '5.')
            if is_float:
                check = lexema[1:] if lexema.startswith('-') else lexema
                if check.startswith('.') or check.endswith('.'):
                    return ("ERROR", lexema + " (formato flotante incorrecto)")
                return ("LITERAL_FLOAT", lexema) 
            else:
                return ("LITERAL_ENTERO", lexema)


        
        # ---------------------------------------------------------------------------------------------
        #                                         13. STRINGS
        # ---------------------------------------------------------------------------------------------
        #ACEPTA
        #"Hola"	
        # "123"	
        #"Hola123"	
        #" "	
        #""	

        #RECHAZA
        #"Hola	
        #Hola"	
        #---------------------------------------------------------------------------------------------

        elif c == '"':
            lexema = '"'
            c = self.demeCaracter()
            while c is not None:
                if c == '"':
                    lexema += '"'
                    return ("LITERAL_STRING", lexema)
                elif c == '\n':
                    return ("ERROR", lexema + " (Sin alguna comilla)")
                else:
                    lexema += c
                c = self.demeCaracter()

            return ("ERROR", lexema + " (Sin alguna comilla)")


        # ---------------------------------------------------------------------------------------------
        #                                         12.  CARACTERES
        # ---------------------------------------------------------------------------------------------
        #ACEPTA
        
        #'a'	
        #' '	

        #RECHAZA
        #''	
        #'ab	
        #'A
        #A'
        #---------------------------------------------------------------------------------------------

        elif c == "'":
            lexema = "'"
            char1 = self.demeCaracter()
            if char1 is None:
                return ("ERROR", lexema + " (carácter vacío)")

            # Verificamos si hay una comilla de cierre después del char1
            char2 = self.peekCaracter()

            if char2 == "'":
                self.demeCaracter()  # consumir comilla final
                lexema += char1 + "'"
                return ("LITERAL_CHAR", lexema)

            # Si no hay cierre correcto, devolvemos lo leído para evitar residuos
            self.tomeCaracter()  # devuelve char1
            return ("ERROR", lexema + char1 + " (carácter mal formado)")

        # ---------------------------------------------------------------------------------------------
        #                                        18.  ARREGLOS
        # ---------------------------------------------------------------------------------------------
        # ACEPTA
        # []
        # [1, 2, 3]
        # ["a", "b", "c"]

        # RECHAZA
        # [1; 2; 3]
        # [1, "dos, 'a'] 
         # ---------------------------------------------------------------------------------------------
        elif c == '[':
            lexema = '['
            c = self.demeCaracter()
            esperando_valor = True

            if c == ']':
                lexema += ']'
                return ("LITERAL_ARREGLO", lexema)  # Arreglo vacío

            while c is not None:
                if c == ']':
                    lexema += ']'
                    if esperando_valor:
                        return ("ERROR", lexema + " (coma final sin valor en arreglo)")
                    return ("LITERAL_ARREGLO", lexema)

                if c == ',':
                    if esperando_valor:
                        return ("ERROR", lexema + " (coma sin valor previo en arreglo)")
                    esperando_valor = True
                    lexema += c

                elif not c.isspace():
                    esperando_valor = False

                    # Validar string
                    if c == '"':
                        lexema += c
                        c = self.demeCaracter()
                        while c is not None and c != '"':
                            if c == '\n':
                                return ("ERROR", lexema + " (string no cerrado en arreglo)")
                            lexema += c
                            c = self.demeCaracter()
                        if c != '"':
                            return ("ERROR", lexema + " (falta comilla final en string en arreglo)")
                        lexema += '"'

                    # Validar char
                    elif c == "'":
                        lexema += c
                        char1 = self.demeCaracter()
                        char2 = self.demeCaracter()
                        if char2 != "'":
                            lexema += (char1 or '') + (char2 or '')
                            return ("ERROR", lexema + " (carácter mal formado en arreglo)")
                        lexema += char1 + "'"

                    # Validar número
                    elif c.isdigit() or (c == '-' and self.peekCaracter() and self.peekCaracter().isdigit()):
                        lexema += c
                        c = self.demeCaracter()
                        is_float = False
                        while c is not None and (c.isdigit() or c == '.'):
                            if c == '.':
                                if is_float:
                                    return ("ERROR", lexema + c + " (demasiados puntos decimales en número)")
                                is_float = True
                            lexema += c
                            c = self.demeCaracter()
                        if c is not None:
                            self.tomeCaracter()

                    # Validar booleanos (On / Off)
                    elif c.isalpha():
                        palabra = c
                        c = self.demeCaracter()
                        while c is not None and c.isalpha():
                            palabra += c
                            c = self.demeCaracter()
                        if palabra not in ["On", "Off"]:
                            return ("ERROR", lexema + palabra + " (elemento inválido en arreglo)")
                        lexema += palabra
                        if c is not None:
                            self.tomeCaracter()

                    # Elemento inválido general
                    else:
                        lexema += c
                        while c is not None and c != ']':
                            c = self.demeCaracter()
                            if c is not None:
                                lexema += c
                        return ("ERROR", lexema + " (elemento inválido en arreglo)")

                else:
                    lexema += c

                c = self.demeCaracter()

            return ("ERROR", lexema + " (arreglo sin cierre)")
                            

        # ---------------------------------------------------------------------------------------------
        #                                 15. TIPO DE DATO  CONJUNTO
        #                                 19. TIPO DE DATO  REGISTRO 
        #                                 16. TIPO DE DATO ARCHIVO DE TEXTO
        # ---------------------------------------------------------------------------------------------
        elif c == '{':
                lexema = '{'
                c = self.demeCaracter()

                # ------------------------------------------------------------------------
                #                                     16. ARCHIVOS 
                # ------------------------------------------------------------------------
                # ACEPTA
                # {/ "bitacora.txt", 'L' /};
                # {/ "registro.txt", 'C' /};
                # {/ "archivo.txt", 'X' /};

                # RECHAZA
                # - Mas de un caracter → {/ "archivo.txt", 'LL' /};    
                # - Sin comillas en carácter → {/ "archivo.txt", L /};       
                # - Sin comillas en el nombre → {/ archivo.txt, 'L' /};       
                # - Sin coma → {/ "archivo.txt" 'L' /};   
                # - Sin cierre → {/ "archivo.txt", 'L' };      

                # ------------------------------------------------------------------------
                if c == '/':
                        lexema += '/'

                        # Saltar espacios antes del nombre
                        c = self.demeCaracter()
                        while c is not None and c.isspace():
                            lexema += c
                            c = self.demeCaracter()

                        if c != '"':
                            return ("ERROR", lexema + (c or '') + " (archivo sin comilla inicial)")
                        lexema += '"'

                        # Leer nombre de archivo
                        c = self.demeCaracter()
                        while c is not None and c != '"':
                            if c == '\n':
                                return ("ERROR", lexema + " (salto de línea en nombre de archivo)")
                            lexema += c
                            c = self.demeCaracter()

                        if c != '"':
                            return ("ERROR", lexema + " (archivo sin comilla final)")
                        lexema += '"'

                        # Saltar espacios antes de coma
                        c = self.demeCaracter()
                        while c is not None and c.isspace():
                            c = self.demeCaracter()
                        if c != ',':
                            return ("ERROR", lexema + (c or '') + " (falta coma en archivo)")
                        lexema += ','

                        # Saltar espacios antes del carácter
                        c = self.demeCaracter()
                        while c is not None and c.isspace():
                            c = self.demeCaracter()
                        if c != "'":
                            return ("ERROR", lexema + (c or '') + " (carácter sin comilla inicial)")
                        lexema += "'"

                        char1 = self.demeCaracter()
                        char2 = self.demeCaracter()
                        if char2 != "'":
                            lexema += (char1 or '') + (char2 or '')
                            return ("ERROR", lexema + " (carácter mal formado)")
                        lexema += char1 + "'"

                        # Saltar espacios antes del cierre
                        c = self.demeCaracter()
                        while c is not None and c.isspace():
                            c = self.demeCaracter()
                        if c != '/':
                            return ("ERROR", lexema + (c or '') + " (archivo sin '/' de cierre)")
                        c2 = self.demeCaracter()
                        if c2 != '}':
                            return ("ERROR", lexema + c + (c2 or '') + " (archivo sin '}' final)")
                        lexema += '/' + c2

                        return ("LITERAL_ARCHIVO", lexema)

                # ------------------------------------------------------------------------
                #                            15.  CONJUNTOS
                # ------------------------------------------------------------------------
                # ACEPTA
                # {: 1, 2, "texto", 'a', 3.14 :} 
                # {: 1, 2, 3 :}

                # RECHAZA
                # - Coma sin valor previo → {: , 2 :}
                # - Elementos mal formados → {: "hola :}, {: 'ab' :}
                # - Cierre incorrecto → {: 1, 2, 3 };
                # ------------------------------------------------------------------------

                elif c == ':':
                    lexema += ':'                           # Guardamos el ':' inicial después de '{'
                    c = self.demeCaracter()                 # Avanzamos al siguiente carácter
                    esperando_valor = True                  # Para controlar si se esperaba un valor después de una coma

                    while c is not None:

                        # Cierre válido del conjunto ----------
                        # Si encontramos ":}", cerramos el conjunto correctamente
                        if c == ':' and self.peekCaracter() == '}':
                            lexema += ':'                   # Agregamos el segundo ':'
                            c = self.demeCaracter()         # Consumimos '}'
                            lexema += c                     # Agregamos '}'
                            if esperando_valor and lexema not in ('{::}', '{: :}'): 
                                return ("ERROR", lexema + " (coma final sin valor)")
                            return ("LITERAL_CONJUNTO", lexema)

                        #  Validación de coma sin valor ----------
                        if c == ',':
                            if esperando_valor:
                                return ("ERROR", lexema + " (coma sin valor previo)")
                            esperando_valor = True          # Esperamos un nuevo valor después de la coma

                        elif not c.isspace():
                            esperando_valor = False         # Ya hay un valor después de la coma

                            # STRING ----------
                            # Evita errores como {: "hola :}
                            if c == '"':
                                lexema += c
                                c = self.demeCaracter()
                                while c is not None and c != '"':
                                    if c == '\n':
                                        return ("ERROR", lexema + " (string no cerrado)")
                                    lexema += c
                                    c = self.demeCaracter()
                                if c != '"':
                                    return ("ERROR", lexema + " (falta comilla final en string)")
                                lexema += '"'

                            # CHAR ----------
                            # Evita errores como {: 'ab' :} o {: 'a :}
                            elif c == "'":
                                lexema += c
                                char1 = self.demeCaracter()
                                char2 = self.demeCaracter()
                                if char2 != "'":
                                    lexema += (char1 or '') + (char2 or '')
                                    return ("ERROR", lexema + " (carácter mal formado)")
                                lexema += char1 + "'"

                            # ENTEROS y FLOAT ----------
                            # Acepta: 5, -4, 3.14
                            # Rechaza: 5. (mal formado), 1.2.3 (dos puntos), .5 (punto inicial)
                            elif c.isdigit() or (c == '-' and self.peekCaracter() and self.peekCaracter().isdigit()):
                                lexema += c
                                c = self.demeCaracter()
                                is_float = False

                                while c is not None and (c.isdigit() or c == '.'):
                                    if c == '.':
                                        if is_float:
                                            return ("ERROR", lexema + " (float con múltiples puntos)")
                                        is_float = True
                                    lexema += c
                                    c = self.demeCaracter()

                                if is_float:
                                    partes = lexema.lstrip('-').split('.')
                                    if len(partes) != 2 or not partes[0] or not partes[1]:
                                        return ("ERROR", lexema + " (formato flotante inválido)")

                                if c is not None:
                                    self.tomeCaracter()  # Preparar para el siguiente token

                            # ELEMENTO INVÁLIDO ----------
                            else:
                                return ("ERROR", lexema + c + " (elemento inválido en conjunto)")

                        else:
                            lexema += c  # Añadir espacios en blanco si son válidos

                        c = self.demeCaracter()

                    return ("ERROR", lexema + " (conjunto sin cierre)")  # Si nunca encontramos ":}"


                # ------------------------------------------------------------------------
                #                           19.  REGISTRO
                # ------------------------------------------------------------------------
                # ACEPTA
                # {nombre: "Steve", vida: 20};
                # {tipo: "granjero", activo: On};
                # {clave: "valor", extra: 99, activo: Off};
                # {a: 'x', b: 3.14, c: -5};

                #RECHAZA
                # {nombre: "Alex"
                # {};
                # {nombre: };
                # {: "Steve"};
                # {nombre "Steve"};
                # {nombre: ~Steve~};
                # ------------------------------------------------------------------------

                else:
                    self.tomeCaracter()  # devolver el carácter que no era / ni :
                    lexema = '{'
                    c = self.demeCaracter()
                    contiene_dos_puntos = False
                    tiene_llave = False
                    tiene_valor = False

                    while c is not None and c != '}':
                        lexema += c

                        # Detectar clave
                        if c.isalpha():
                            tiene_llave = True

                        if c == ':':
                            contiene_dos_puntos = True
                            c = self.demeCaracter()
                            while c is not None and c.isspace():
                                lexema += c
                                c = self.demeCaracter()
                            if c is not None:
                                tiene_valor = True
                                lexema += c

                        c = self.demeCaracter()

                    if c == '}':
                        lexema += '}'
                        if not contiene_dos_puntos:
                            return ("ERROR", lexema + " (registro sin clave:valor)")
                        if not tiene_llave:
                            return ("ERROR", lexema + " (registro sin clave)")
                        if not tiene_valor:
                            return ("ERROR", lexema + " (registro sin valor)")
                        return ("LITERAL_REGISTRO", lexema)
                    else:
                        return ("ERROR", lexema + " (registro sin cierre)")



        # ---------------------------------------------------------------------------------------------
        #                        29. SISTEMA DE ACCESO A ARREGLOS
        # ---------------------------------------------------------------------------------------------
        # ACEPTA:
        # vector[0]              → ACCESO_ARREGLO   (Número entero válido)
        # matriz[2][3]           → ACCESO_ARREGLO   (Acceso encadenado correcto)
        # numeros[i]             → ACCESO_ARREGLO   (Índice como identificador válido)
        # datos[counter][index]  → ACCESO_ARREGLO   (Índices tipo variable, encadenados)

        # ERRORES:
        # vector[]               → ERROR (Falta índice entre corchetes)
        # vector[12              → ERROR (Falta cierre ']')
        # vector[1,2]            → ERROR (No debe haber coma dentro del acceso simple)
        # vector[;]              → ERROR (Carácter inválido en índice)
        # vector[3a]             → ERROR (Índice inválido: debe ser entero o identificador simple)

        # ---------------------------------------------------------------------------------------------
        #                        30. SISTEMA DE ACCESO A STRINGS
        # ---------------------------------------------------------------------------------------------
        # ACEPTA:
        # string[1]              → ACCESO_STRING    (Índice correcto)
        # Spider_nombre[5]       → ACCESO_STRING    (Variable tipo Spider con índice correcto)
        # Spider_contenido[i]    → ACCESO_STRING    (Índice como variable permitido)
        # string_variable[0][2]  → ACCESO_STRING    (Acceso múltiple en string permitido)

        # ERRORES:
        # Spider_nombre[]        → ERROR (Falta índice)
        # string[abc]            → ERROR (Índice inválido, no puede ser palabra compuesta)
        # Spider_[5]             → ERROR (Spider_ no es un tipo Spider completo sin nombre)
        # string[1,2]            → ERROR (Coma dentro del índice no permitida)
        #----------------------------------------------------------------------------------------------

        elif c.isalpha() or c == '_':
            lexema = c
            c = self.demeCaracter()
            while c is not None and (c.isalnum() or c == "_"):
                lexema += c
                c = self.demeCaracter()

            # Se guarda el identificador base
            base_identificador = lexema

            # Ahora verificar si sigue un acceso a [ ]
            acceso = ""
            while c == '[':
                acceso += c
                c = self.demeCaracter()

                # Leer índice (puede ser número o identificador como 'i')
                if c is None or not (c.isalnum() or c == '_'):
                    return ("ERROR", acceso + (c or '') + " (índice inválido en acceso)")

                while c is not None and (c.isalnum() or c == "_"):
                    acceso += c
                    c = self.demeCaracter()

                if c != ']':
                    return ("ERROR", acceso + (c or '') + " (falta cierre de corchete)")
                acceso += ']'
                c = self.demeCaracter()

            if c is not None:
                self.tomeCaracter()

            if acceso:
                # Ahora decidir: ¿es acceso a STRING o ARREGLO?
                if base_identificador in self.variables_spider:
                    return ("ACCESO_STRING", base_identificador + acceso)
                else:
                    return ("ACCESO_ARREGLO", base_identificador + acceso)

            else:
                # No había acceso
                return ("IDENTIFICADOR", base_identificador)

        # ---------------------------------------------------------------------------------------------
        #                          31.  SISTEMA DE ACCESO A REGISTROS           
        # ---------------------------------------------------------------------------------------------
        # ACEPTA

        # RECHAZA
 
         # -------------------------------------------------------------------------------------------
        elif c == '@':  # Acceso a registros tipo objeto@campo
            lexema = '@'
            c = self.demeCaracter()
            if c is None or not c.isalpha():
                return ("ERROR_202", lexema + (c or '') + " (acceso a registro mal formado)")
            while c is not None and (c.isalnum() or c == "_"):
                lexema += c
                c = self.demeCaracter()
            if c is not None:
                self.tomeCaracter()
            return ("ACCESO_REGISTRO", lexema)

        # ---------------------------------------------------------------------------------------------
        #                  32. OPERADORES DE ASIGNACIÓN Y FAMILIA (=, +=, -=, *=, /=, %=)
        #                  33. OPERACIONS ARITMETICAS BASICAS DE ENTEROS
        # ---------------------------------------------------------------------------------------------
        # ACEPTA
        # Stack a = 5;
        # Stack b += 1;
        # Stack c -= 3;
        # Stack d *= 2;
        # Stack e /= 4;
        # Stack f %= 2;
        # Stack suma = 4 + 3;
        # Stack resta = 10 - 2;
        # Stack producto = 2 * 5;
        # Stack division = 9 // 2;
        # Stack modulo = 7 % 3;
        # Stack avanzar += 2;
        # Stack retroceder -= 1;

        # RECHAZA
        # Stack h =;              → falta valor a asignar
        # Stack mal1 = 3 ++ 2;    → Signo doble
        # Stack mal2 = 4 ** 5;    → Signo doble
        # Stack mal3 = 9 %% 3;    → Signo doble
        # Stack mal4 = 8 /& 2;    → Signo doble
         # ---------------------------------------------------------------------------------------------
        elif c == '=':
            lexema = '='
            c = self.peekCaracter()
            if c == '=':
                self.demeCaracter()
                return ("OPERADOR", lexema + '=')
            elif c is not None and not c.isspace() and not c.isalnum():
                return ("ERROR", lexema + c + " (uso incorrecto del operador de asignación)")
            return ("OPERADOR", lexema)

        elif c in ['+', '-', '*', '/', '%']:
            lexema = c
            siguiente = self.peekCaracter()

            if siguiente == '=':
                self.demeCaracter()
                return ("OPERADOR", lexema + '=')
            elif c == '/' and siguiente == '/':
                self.demeCaracter()
                return ("OPERADOR", '//')
            elif siguiente is not None and not siguiente.isspace() and not siguiente.isalnum():
                return ("ERROR", lexema + siguiente + " (uso incorrecto del operador aritmético)")
            return ("OPERADOR", lexema)
        
        # ---------------------------------------------------------------------------------------------
        #                      34.  INCREMENTO Y DECREMENTO (soulsand, magma)
        # ---------------------------------------------------------------------------------------------
        # ACEPTA
        # bloques soulsand;
        # picos magma;

        # RECHAZA
        # bloques soulsandd;   → No se reconoce como operador, se interpreta como identificador
        # picos magmaa;        → No se reconoce como operador, se interpreta como identificador
        # ---------------------------------------------------------------------------------------------

        elif c.isalpha():
            lexema = c
            c = self.demeCaracter()
            while c is not None and c.isalpha():
                lexema += c
                c = self.demeCaracter()

            if lexema == 'soulsand':
                return ("OPERADOR_INCREMENTO", lexema)  # Tipo específico para color personalizado
            elif lexema == 'magma':
                return ("OPERADOR_DECREMENTO", lexema)  # Tipo específico para color personalizado
            elif lexema.startswith('soulsand') or lexema.startswith('magma'):
                return ("ERROR", lexema + " (uso incorrecto de operador de incremento/decremento)")
            else:
                return ("IDENTIFICADOR", lexema)


        # ---------------------------------------------------------------------------------------------
        #  35. OPERACIONES SOBRE CARACETRES  isEngraved('A'), isInscribed('7'), etchUp('c'), etchDown('D')
        # ---------------------------------------------------------------------------------------------
        
        # ACEPTA
        # isEngraved('A')
        # isInscribed('7')
        # VetchUp('c')
        # etchDown('D')

        # RECHAZA
        # isEngravedA')         →  (falta paréntesis)
        # isInscribed("7")      →  (comillas incorrectas)
        # etchUp('')            →  (carácter vacío)
        # etchDown('ab')        → (más de un carácter)
        # etchUp('c")           → (falta comilla de cierre)
        # etchDown('d'          → (falta paréntesis de cierre)
        # ---------------------------------------------------------------------------------------------
        elif c.isalpha():
            lexema = c
            c = self.demeCaracter()
            while c is not None and c.isalpha():
                lexema += c
                c = self.demeCaracter()

            if lexema in ['isEngraved', 'isInscribed', 'etchUp', 'etchDown']:
                if c != '(':
                    return ("ERROR", lexema + (c or '') + " (falta paréntesis de apertura)")
                lexema += c
                c = self.demeCaracter()

                if c != "'":
                    return ("ERROR", lexema + (c or '') + " (falta comilla simple de apertura para el carácter)")
                lexema += c

                char = self.demeCaracter()
                if char is None or not char.isalnum():
                    return ("ERROR", lexema + (char or '') + " (carácter inválido)")
                lexema += char

                cierre_comilla = self.demeCaracter()
                if cierre_comilla != "'":
                    return ("ERROR", lexema + (cierre_comilla or '') + " (falta comilla simple de cierre)")
                lexema += cierre_comilla

                cierre_par = self.demeCaracter()
                if cierre_par != ')':
                    return ("ERROR", lexema + (cierre_par or '') + " (falta paréntesis de cierre)")
                lexema += cierre_par

                return ("OPERADOR_CARACTER", lexema)

            else:
                return ("IDENTIFICADOR", lexema)


        # ---------------------------------------------------------------------------------------------
        #                            36. OPERACIONES LOGICAS
        # ---------------------------------------------------------------------------------------------
        # ACEPTA
        #Torch combinacion1 = On and Off;
        #Torch combinacion2 = On or Off;
        #Torch negacion = not Off;
        #Torch exclusivo = On xor On;

        
        #RECHAZA
        #Torch combinacion = On nand Off;       
        #Torch negacion = onn not Off;         
        #Torch exclusivo = xor On On;           
        #Torch fallo = On andor Off;            
        # ---------------------------------------------------------------------------------------------

        elif c.isalpha():
            lexema = c
            c = self.demeCaracter()
            while c is not None and c.isalpha():
                lexema += c
                c = self.demeCaracter()

            # Validación de operadores lógicos
            if lexema in ['and', 'or', 'not', 'xor']:
                return ("OPERADOR_LOGICO", lexema)

            # Validación de errores comunes al usar estos operadores
            elif any(invalid in lexema for invalid in ['nand', 'andor', 'orxor']):
                return ("ERROR", lexema + " (operador lógico mal formado)")

            else:
                return ("IDENTIFICADOR", lexema)



        # ---------------------------------------------------------------------------------------------
        #                           37. OPERACIONES STRING SOLICITADOS
        # ---------------------------------------------------------------------------------------------
        #ACEPTA
        # Spider nombre = bind("Steve", "Smith") ;             
        # Stack longitud = #nombre ;                           
        # Spider parcial = nombre from ## 5 ;                 
        # Spider recorte = nombre except ## 5 ;                
        # Torch encontrado = seek("e", nombre) ;  

        # RECHAZA
        # Spider mal1 = nombre from # 5 ;                     
        # Spider mal2 = nombre except# ;                       
        # Spider mal3 = seeke("e", nombre) ;                  
        # ---------------------------------------------------------------------------------------------
        
        elif c == "#":
            siguiente = self.demeCaracter()
            if siguiente == "#":
                return ("SEPARADOR_STRING_TERNARIO", "##")
            else:
                self.tomeCaracter()
                return ("LARGO_STRING", "#")

        elif c.isalpha():
            lexema = c
            c = self.demeCaracter()
            while c is not None and (c.isalnum() or c == "_"):
                lexema += c
                c = self.demeCaracter()

            if c is not None:
                self.tomeCaracter()

            # Reconocimiento de operadores de string
            if lexema == "bind":
                return ("CONCATENAR_STRING", lexema)
            elif lexema == "from":
                return ("CORTAR_STRING", lexema)
            elif lexema == "except":
                return ("RECORTAR_STRING", lexema)
            elif lexema == "seek":
                return ("BUSCAR_STRING", lexema)

            # Errores comunes de mal escritura
            elif any(lexema.startswith(op) for op in ["bind", "from", "except", "seek"]) and lexema not in ["bind", "from", "except", "seek"]:
                return ("ERROR", f"{lexema} (uso incorrecto de operador de string)")

            # Otros identificadores
            return ("IDENTIFICADOR", lexema)    
        











        # ---------------------------------------------------------------------------------------------
        #                            38. OPERACIONES CONJUNTOS
        # ---------------------------------------------------------------------------------------------
        # ACEPTA
        # vocales add 'u';                             → agregar un elemento
        # vocales drop 'a';                            → eliminar un elemento
        # Chest comunes = feed(a, b);                  → intersección de conjuntos
        # Torch pertenece = map('e', vocales);         → verificar pertenencia
        # Chest vacio = void;                          → conjunto vacío
        # Torch estaVacio = (vacio is void);           → verificación de vacío
        # kill herramientas;                           → eliminar todo

        #RECHAZA
        #vocales add u;                                → falta comillas simples
        #vocales dropp 'a';                            → palabra mal escrita
        #Chest comunes = feed a, b;                    → falta paréntesis
        #Torch pertenece = map 'e', vocales;           → falta paréntesis
        #Chest vacio = voiid;                          → palabra mal escrita
        #kill;                                         → falta el identificador del conjunto
        #add vocales, 'u';                             → orden incorrecto
        #void herramientas;                            → mal uso de void
        # ---------------------------------------------------------------------------------------------

        elif c.isalpha():
            lexema = c
            c = self.demeCaracter()
            while c is not None and c.isalpha():
                lexema += c
                c = self.demeCaracter()

            if lexema in ['add', 'drop', 'kill', 'void']:
                return ("OPERADOR_CONJUNTO", lexema)

            elif lexema == 'map':
                # Validar formato map('a', conjunto)
                c = self.demeCaracter()
                if c != '(':
                    return ("ERROR", "map debe ir seguido de paréntesis de apertura")
                lexema += c

                # Leer carácter
                c = self.demeCaracter()
                if c != "'":
                    return ("ERROR", "map debe comenzar con un carácter entre comillas simples")
                lexema += c
                char = self.demeCaracter()
                lexema += char
                c = self.demeCaracter()
                if c != "'":
                    return ("ERROR", "carácter en map debe cerrar con comilla simple")
                lexema += c

                # Leer coma
                c = self.demeCaracter()
                while c is not None and c.isspace():
                    c = self.demeCaracter()
                if c != ',':
                    return ("ERROR", "falta coma después del carácter en map")
                lexema += c

                # Leer conjunto
                c = self.demeCaracter()
                while c is not None and c.isspace():
                    c = self.demeCaracter()
                if c is None or not c.isalpha():
                    return ("ERROR", "conjunto inválido en map")
                while c is not None and (c.isalnum() or c == "_"):
                    lexema += c
                    c = self.demeCaracter()

                # Cierre de paréntesis
                while c is not None and c.isspace():
                    c = self.demeCaracter()
                if c != ')':
                    return ("ERROR", "map debe cerrar con paréntesis")
                lexema += ')'
                return ("OPERADOR_CONJUNTO", "map(" + lexema.split('(', 1)[1])  # Mostrar map(...)

            elif lexema == 'feed':
                # Validar formato feed(conjuntoA, conjuntoB)
                c = self.demeCaracter()
                if c != '(':
                    return ("ERROR", "feed debe tener paréntesis de apertura")
                lexema += c

                # Leer primer identificador
                c = self.demeCaracter()
                while c is not None and c.isspace():
                    c = self.demeCaracter()
                if not c.isalpha():
                    return ("ERROR", "primer conjunto inválido en feed")
                while c is not None and (c.isalnum() or c == "_"):
                    lexema += c
                    c = self.demeCaracter()

                # Coma
                while c is not None and c.isspace():
                    c = self.demeCaracter()
                if c != ',':
                    return ("ERROR", "falta coma entre conjuntos en feed")
                lexema += c

                # Segundo identificador
                c = self.demeCaracter()
                while c is not None and c.isspace():
                    c = self.demeCaracter()
                if not c.isalpha():
                    return ("ERROR", "segundo conjunto inválido en feed")
                while c is not None and (c.isalnum() or c == "_"):
                    lexema += c
                    c = self.demeCaracter()

                # Cierre
                while c is not None and c.isspace():
                    c = self.demeCaracter()
                if c != ')':
                    return ("ERROR", "feed debe cerrar con paréntesis")
                lexema += ')'
                return ("OPERADOR_CONJUNTO", "feed(" + lexema.split('(', 1)[1])  # Mostrar feed(...)

            # --------------------------
            # Error: Mal uso de operadores
            # --------------------------
            elif any(lexema.startswith(op) for op in ['add', 'drop', 'feed', 'map', 'void', 'kill']) and lexema not in ['add', 'drop', 'feed', 'map', 'void', 'kill']:
                return ("ERROR", lexema + " (uso incorrecto de operador de conjunto)")

            else:
                return ("IDENTIFICADOR", lexema)

        # ---------------------------------------------------------------------------------------------
        #                           39. OPERACIONES SOBRE ARCHIVOS
        # ---------------------------------------------------------------------------------------------
        #ACEPTAR
        # unlock libro;
        # lock libro;
        # craft archivoNuevo;
        # gather libro into contenido;
        # forge libro with "Bienvenido al mundo Minecraft";
        # expand archivo1, archivo2 into archivoTotal;

        # RECHAZA
        # unlockk libro;                        → operador mal escrito
        # lock "libro";                         → libro con comillas
        # gather libro contenido;               → falta 'into'
        # forge libro "mensaje";                → falta 'with'
        # expand archivo1 archivo2 archivo3;    → falta 'into'
        # ---------------------------------------------------------------------------------------------

        if lexema in ['unlock', 'lock', 'craft', 'gather', 'forge', 'expand']:
            return ("OPERADOR_ARCHIVO", lexema)

        elif any(lexema.startswith(op) for op in ['unlock', 'lock', 'craft', 'gather', 'forge', 'expand']) and lexema not in ['unlock', 'lock', 'craft', 'gather', 'forge', 'expand']:
            return ("ERROR", lexema + " (uso incorrecto de operador de archivo)")



        # ---------------------------------------------------------------------------------------------
        #                           40.  OPERACIONES SOBRE FLOTANTES
        # ---------------------------------------------------------------------------------------------
        # ACEPTAR
        # Ghast total = 3.5 :+ 2.0;         → suma flotante
        # Ghast resta = 5.0 :- 1.5;         → resta flotante
        # Ghast producto = 2.0 :* 4.0;      → multiplicación flotante
        # Ghast modulo = 7.5 :% 2.0;        → módulo flotante
        # Ghast division = 9.0 :// 3.0;     → división flotante

        # RECHAZA 
        # Ghast suma = 3.5 + 2.0;           → operador flotante debe usar ":+" no "+"
        # Ghast resta = 5.0 :- ;            →  falta un operando
        # Ghast multi = :* 4.0;             →  falta operando izquierdo
        # Ghast div = 9.0 :// ;             →  falta operando derecho
        # Ghast modulo = 7.5 :%% 2.0;       →  operador inválido ":%%"
        # Ghast mal = 2.5 :+3.5;            → falta espacio entre operador y segundo operando
        # ---------------------------------------------------------------------------------------------
        elif c == ':':
            siguiente = self.demeCaracter()

            if siguiente == ':':
                return ("SIMBOLO", '::')
            elif siguiente in ['+', '-', '*', '%']:
                return ("OPERADOR_FLOAT", ':' + siguiente)
            elif siguiente == '/':
                if self.peekCaracter() == '/':
                    self.demeCaracter()
                    return ("OPERADOR_FLOAT", '://')
                else:
                    return ("ERROR", ":/ (operador flotante mal formado)")
            else:
                return ("SIMBOLO", ':')


            # ---------------------- OPERADORES FLOTANTES ----------------------
            lexema = ':'
            if siguiente in ['+', '-', '*', '%']:
                lexema += siguiente
                return ("OPERADOR_FLOAT", lexema)
            elif siguiente == '/':
                peek = self.peekCaracter()
                if peek == '/':
                    self.demeCaracter()
                    return ("OPERADOR_FLOAT", '://')
                else:
                    return ("ERROR", lexema + '/' + " (operador de división flotante mal formado)")
            elif siguiente == ':':
                return ("ERROR", ':: (mal ubicado: fuera de Spell/Ritual)')
            else:
                return ("ERROR", lexema + (siguiente or '') + " (operador flotante inválido)")




        # ---------------------------------------------------------------------------------------------
        #                        41.  OPERACIONES DE COMPARACION SOLICITADAS
        # ---------------------------------------------------------------------------------------------
        # Torch menor = 3 < 5;
        # Torch mayor = 8 > 2;
        # Torch menorIgual = 6 <= 6;
        # Torch mayorIgual = 7 >= 3;

        # Torch igual = nombre is "SteveSmith";
        # Torch distinto = nombre isNot "Alex";

        # Torch menor = 3 << 5;               
        # Torch comparador = nombre isNotAlex;      → falta espacio entre isNot y valor
        # Torch comparador2 = nombre is Not;        → Not no es válido
        # Torch comparador3 = nombre isNott "Alex"; → mal escrito
        # ---------------------------------------------------------------------------------------------

        elif c in ['<', '>']:
            lexema = c
            siguiente = self.peekCaracter()

            if c == '>' and siguiente == '>':
                self.demeCaracter()
                return ("OPERADOR_COHERSION", ">>")

            if siguiente == '=':
                self.demeCaracter()
                return ("OPERADOR_COMPARACION", lexema + '=')

            return ("OPERADOR_COMPARACION", lexema)

        elif c == 'i':  # Para is y isNot
            lexema = c
            c = self.demeCaracter()
            while c is not None and c.isalpha():
                lexema += c
                c = self.demeCaracter()

            if lexema == "is":
                return ("OPERADOR_COMPARACION", lexema)
            elif lexema == "isNot":
                return ("OPERADOR_COMPARACION", lexema)
            elif lexema.startswith("is") or lexema.startswith("isNot"):
                return ("ERROR", lexema + " (uso incorrecto de operador de comparación)")
            else:
                return ("IDENTIFICADOR", lexema)



        # ---------------------------------------------------------------------------------------------
        #                          52.  ENCABEZADO DE FUNCIONES Spell <id>(<params>) -> <return_type>
        # ---------------------------------------------------------------------------------------------
        elif lexema == 'Spell':
            self.modo_spell = True
            lexema += ' '
            c = self.demeCaracter()
            while c is not None and c.isspace():
                c = self.demeCaracter()
            if c is None or not c.isalpha():
                self.modo_spell = False
                return ("ERROR", lexema + (c or '') + " (falta identificador en Spell)")
            while c is not None and (c.isalnum() or c == "_"):
                lexema += c
                c = self.demeCaracter()
            if c != '(':
                self.modo_spell = False
                return ("ERROR", lexema + (c or '') + " (faltan paréntesis de apertura en parámetros)")
            lexema += c
            c = self.demeCaracter()
            while c is not None and c != ')':
                lexema += c
                c = self.demeCaracter()
            if c != ')':
                self.modo_spell = False
                return ("ERROR", lexema + " (falta cierre de paréntesis)")
            lexema += c
            c = self.demeCaracter()
            while c is not None and c.isspace():
                c = self.demeCaracter()
            if c != '-':
                self.modo_spell = False
                return ("ERROR", lexema + (c or '') + " (se esperaba '->')")
            siguiente = self.demeCaracter()
            if siguiente != '>':
                self.modo_spell = False
                return ("ERROR", lexema + '-' + (siguiente or '') + " (se esperaba '->')")
            lexema += '->'
            c = self.demeCaracter()
            while c is not None and c.isspace():
                c = self.demeCaracter()
            if c is None or not c.isalpha():
                self.modo_spell = False
                return ("ERROR", lexema + (c or '') + " (tipo de retorno inválido)")
            while c is not None and (c.isalnum() or c == "_"):
                lexema += c
                c = self.demeCaracter()
            if c is not None:
                self.tomeCaracter()
            self.modo_spell = False
            return ("ENCABEZADO_FUNCION", lexema)



        # ---------------------------------------------------------------------------------------------
        #                           53. Ritual <id>(<params>);
        # ---------------------------------------------------------------------------------------------
        elif lexema == 'Ritual':
            lexema += ' '
            c = self.demeCaracter()
            while c is not None and c.isspace():
                c = self.demeCaracter()
            if c is None or not c.isalpha():
                return ("ERROR", lexema + (c or '') + " (falta identificador en Ritual)")
            while c is not None and (c.isalnum() or c == "_"):
                lexema += c
                c = self.demeCaracter()
            if c != '(':
                return ("ERROR", lexema + (c or '') + " (faltan paréntesis de apertura en parámetros)")
            lexema += c
            c = self.demeCaracter()
            while c is not None and c != ')':
                lexema += c
                c = self.demeCaracter()
            if c != ')':
                return ("ERROR", lexema + " (falta cierre de paréntesis)")
            lexema += c
            c = self.demeCaracter()
            if c == ';':
                lexema += c
            else:
                self.tomeCaracter()
            return ("ENCABEZADO_PROCEDIMIENTO", lexema)


        # ---------------------------------------------------------------------------------------------
        #                                   56. RETURN
        # ---------------------------------------------------------------------------------------------
        elif lexema == 'respawn':
            return ("RETURN_FUNC", lexema)

        # ---------------------------------------------------------------------------------------------
        #                                   57. SIZE OFF
        # ---------------------------------------------------------------------------------------------
        elif lexema == 'chunk':
            # Verifica si hay un espacio y luego un tipo válido (identificador)
            c = self.demeCaracter()
            while c is not None and c.isspace():
                c = self.demeCaracter()

            if c is None:
                return ("ERROR", "chunk (falta operando para operación de tamaño)")

            operando = ""
            while c is not None and (c.isalnum() or c == "_"):
                operando += c
                c = self.demeCaracter()

            if not operando:
                return ("ERROR", "chunk (operando inválido para operación de tamaño)")

            if c is not None:
                self.tomeCaracter()  # Devolver último caracter si se pasó

            return ("OPERADOR_CHUNK", f"chunk {operando}")




        # ---------------------------------------------------------------------------------------------
        #                           63. COEMNTARIO DE BLOQUE
        #                           64. COMENTARIO DE LINEA
        # ---------------------------------------------------------------------------------------------
        elif c == '$':
            c2 = self.demeCaracter()
            if c2 == '$':
                lexema = "$$"
                while True:
                    c = self.demeCaracter()
                    if c is None or c == '\n':
                        break
                    lexema += c
                return ("COMENTARIO", lexema)
            elif c2 == '*':
                lexema = "$*"
                while True:
                    c = self.demeCaracter()
                    if c is None:
                        return ("ERROR", lexema)
                    lexema += c
                    if lexema.endswith("*$"):
                        return ("COMENTARIO", lexema)
            else:
                return ("ERROR", "$" + (c2 or ""))

        # --------------------------- Símbolos y operadores ---------------------------
        elif c in "=;{}(),:+-*/%<>":
            return ("SIMBOLO", c)

        # --------------------------- Error general ---------------------------
        else:
            return ("ERROR", c)

    def TomeToken(self):
        return self.DemeToken()
