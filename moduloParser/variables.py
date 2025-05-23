from moduloParser.validaciones_semanticas import validar_declaracion_variable

#----------------------------------------------------------------------------
#   SECCION DE VARIABLES (Inventory)
#----------------------------------------------------------------------------
#   Declaración de variables con o sin inicialización, múltiples por línea.
#   AQUI ya se esta validando que los tipos de dato cumplan con la estructura 
#   adentro del Inventory 
#   Inventory
#       Stack vidas;
#       Stack monedas = 100;
#       Stack vidas, monedas, intentos;
#----------------------------------------------------------------------------

def seccion_variables(parser, token, valor):
        print(f"---- Sección de variables detectada: {valor}")
        parser.avanzar()
        tabla_simbolos = parser.tabla
        es_inicializado = False
        valor_inicializacion = None

        while not parser.fin():
            tipo_token, tipo_valor = parser.token_actual_tipo_valor()
            tipos_validos = (
                "TIPO_ENTERO", "TIPO_STRING", "TIPO_CARACTER", "TIPO_FLOAT",
                "TIPO_CONJUNTO", "TIPO_ARCHIVO", "TIPO_ARREGLOS",
                "TIPO_REGISTROS", "TIPO_BOOL"
            )

            if tipo_token not in tipos_validos:
                break  
             # Detectar Shelf y procesar arreglo aparte
            if tipo_token == "TIPO_ARREGLOS" and tipo_valor == "Shelf":
                procesar_arreglo(parser)
                continue
            tipo_dato = tipo_valor
            tipo_base = tipo_token.replace("TIPO_", "")
            parser.avanzar()

            while True:
                tipo, var_name = parser.token_actual_tipo_valor()
                if tipo != "IDENTIFICADOR":
                    print(f"Error: Se esperaba un identificador después del tipo '{tipo_dato}'")
                    parser.actualizar_token("ERROR", var_name)
                    return
                print(f"-----------------------------------------------------------------------")
                print(f"---- Variable detectada: {tipo_dato} {var_name}")
                parser.avanzar()

                # ¿Inicialización?
                tipo, val = parser.token_actual_tipo_valor()
                if tipo == "OPERADOR" and val == "=":
                    parser.avanzar()
                    tipo_literal, literal_val = parser.token_actual_tipo_valor()

                    literales_validos = {
                        "ENTERO": ["LITERAL_ENTERO"],
                        "STRING": ["LITERAL_STRING"],
                        "CARACTER": ["LITERAL_CHAR"],
                        "FLOAT": ["LITERAL_FLOAT"],
                        "CONJUNTO": ["LITERAL_CONJUNTO"],
                        "ARCHIVO": ["LITERAL_ARCHIVO"],
                        "ARREGLOS": ["LITERAL_ARREGLO"],
                        "REGISTROS": ["LITERAL_REGISTRO"],
                        "BOOL": ["LITERAL_BOOL"]
                    }

                    if tipo_literal not in literales_validos.get(tipo_base, []):
                        print(f"Error: El valor '{literal_val}' no es válido para el tipo {tipo_dato}")
                        print(f"-----------------------------------------------------------------------")
                        parser.actualizar_token("ERROR", literal_val)
                        return
                    es_inicializado = True
                    valor_inicializacion = literal_val 
                    print(f"---- Inicialización: {var_name} = {literal_val}")
                    print(f"-----------------------------------------------------------------------")
                    parser.avanzar()
                    tipo, sep = parser.token_actual_tipo_valor()
                else:
                    tipo, sep = parser.token_actual_tipo_valor()
                
                # Validación Semántica
                if not validar_declaracion_variable(tabla_simbolos, var_name, tipo_base, es_inicializado, valor_inicializacion):
                    parser.actualizar_token("ERROR", var_name)
                    return
                
                if tipo == "SIMBOLO" and sep == ",":
                    parser.avanzar()
                    continue
                elif tipo == "SIMBOLO" and sep == ";":
                    print(f"---- Declaración finalizada para tipo {tipo_dato}\n")
                    print(f"-----------------------------------------------------------------------")
                    parser.avanzar()
                    break
                else:
                    print("Error: Se esperaba ',' o ';' después del identificador o literal")
                    print(f"-----------------------------------------------------------------------")
                    parser.actualizar_token("ERROR", sep)
                    return
                
#----------------------------------------------------------------------------
# TIPOS DE DATOS 
#----------------------------------------------------------------------------
#   TIPO DE DATO ENTERO, DECLARACION Y LITERAL (Stack <id> = <integer_literal> )
#
#   TIPO DE DATO CARACTER, DECLARACION Y LITERAL  (Rune <id> = <char_literal>)
# 
#   TIPO DE DATO STRING, DECLARACION Y LITERAL (Spider <id> = <string_literal>)
#
#   TIPO DE DATO BOOL, DECLARACION Y LITERAL  (Torch <id> = <bool_literal> )
# 
#   TIPO DE DATO CONJUNTO, DECLARACION Y LITERAL (Chest <id> = <set_literal> )
#
#   TIPO DE DATO ARCHIVO, DECLARACION Y LITERAL  (Book <id> = <file_literal>;)
# 
#   TIPO DE DATO FLOAT, DECLARACION Y LITERAL (Ghast <id> = <float_literal>; )
#----------------------------------------------------------------------------
# 
#----------------------------------------------------------------------------
# ENTERO - Stack <id> = <int>;
#----------------------------------------------------------------------------
# ACEPTA 
# Stack vidas       SCANNER stack -> tipo entero        vidas -> id           
# Stack monedas = 100;
# Stack vidas, monedas, intentos;
# Stack vidas = 3, monedas = 50, intentos = 2;
# Stack vidas, monedas = 50, intentos;
#
# RECHAZA
# Stack ;                            # Error 1: Falta identificador
# Stack worldSave;                   # Error 2: Identificador es palabra reservada
# Stack vidas = "cinco";             # Error 3: Literal incorrecto (string)
# Stack vidas = 3, monedas = 50;     # Error 4: Coma como separador decimal
# Stack vidas = 5                    # Error 5: Falta punto y coma
# Stack vidas := 5;                  # Error 6: Operador mal escrito
# Stack a = 5 b = 6;                 # Error 7: Múltiples literales mal separados
# Stack vidas = 5a;                  # Error 8: Literal con letra
# Stack vidas = 5.;                  # Error 9: Float mal formado
# Stack vidas = ;                    # Error 10: Asignación sin valor
# Stack vidas,;                      # Error 11: Coma sin siguiente identificador
# Stack (vidas) = 5;                 # Error 12: Paréntesis inesperado
#----------------------------------------------------------------------------

def procesar_dato_stack(parser):
    _procesar_tipo_dato(parser, "Stack", "ENTERO")
  
"""
----------------------------------------------------------------------------
 CARÁCTER - Rune <id> = <char_literal>;
----------------------------------------------------------------------------
ACEPTA 
Rune letra = 'A';     
Rune simbolo = '%';
Rune numero = '7';
-------------------------------------------------------------------------------
Rune 'a';                     # Error: Se esperaba un identificador
Rune letra = 97;              # Error: El valor '97' no es válido para el tipo Rune
Rune letra = "a";             # Error: El valor '"a"' no es válido para el tipo Rune
Rune letra = 'x' 'y';         # Error: Se esperaba ',' o ';' después del literal
Rune Rune = 'r';              # Error: 'Rune' es un tipo de dato y no puede usarse como identificador
----------------------------------------------------------------------------
"""

def procesar_dato_rune(parser):
    _procesar_tipo_dato(parser, "Rune", "CARACTER")

#----------------------------------------------------------------------------
# STRING - Spider <id> = <string_literal>;
#----------------------------------------------------------------------------
# ACEPTA 
# Spider nombre = "Steve"        Stack -> tipo entero   nombree _>id    = ->simbolo     steve->literal de string  ;->terminador 
# Spider saludo = "Hola mundo"; 
# Spider texto = "";   

# Spider "Minecraft";              # Error: Se esperaba un identificador
# Spider nombre = 'H';             # Error: El valor 'H' no es válido para el tipo Spider
# Spider nombre = 42;              # Error: El valor '42' no es válido para el tipo Spider
# Spider nombre = "a" "b";         # Error: Se esperaba ',' o ';' después del literal
# Spider Spider = "x";             # Error: 'Spider' es un tipo de dato y no puede usarse como identificador
#----------------------------------------------------------------------------
def procesar_dato_spider(parser):
    _procesar_tipo_dato(parser, "Spider", "STRING")


#----------------------------------------------------------------------------
# BOOLEANO - Torch <id> = On/Off;
#----------------------------------------------------------------------------
# ACEPTA 
# Torch encendido = On;
# Torch apagado = Off;

# Torch On;                          # Error: Se esperaba un identificador
# Torch luz = 'O';                   # Error: El valor ''O'' no es válido para el tipo Torch
# Torch luz = "On";                  # Error: El valor '"On"' no es válido para el tipo Torch
# Torch luz = Verdadero;             # Error: El valor 'Verdadero' no es válido para el tipo Torch
# Torch Torch = Off;                 # Error: 'Torch' es un tipo de dato y no puede usarse como identificador
# Torch encendido = On Off;          # Error: Se esperaba ',' o ';' después del literal
#----------------------------------------------------------------------------
def procesar_dato_torch(parser):
    _procesar_tipo_dato(parser, "Torch", "BOOL")


#----------------------------------------------------------------------------
# CONJUNTO - Chest <id> = {: ... :};
#----------------------------------------------------------------------------
# ACEPTA 
# Chest inventario = {: 'A' :};
# Chest loot = {: 'x' 'y' 'z' :};
# Chest loot = {: "x" 'y' 5 :};
# Chest vacio = {: :};

# Chest {: 'a' :};                    # Error: Se esperaba un identificador
# Chest cosas = { 'a', 'b' };         # Error: El valor '{ 'a', 'b' }' no es válido para el tipo Chest
# Chest elementos = [: 'a' :];        # Error: El valor '[: 'a' :]' no es válido para el tipo Chest
# Chest chest = {: 'a' 'b' :} 'c';    # Error: Se esperaba ',' o ';' después del literal
# Chest Chest = {: 'a' :};            # Error: 'Chest' es un tipo de dato y no puede usarse como identificador
#----------------------------------------------------------------------------
def procesar_dato_chest(parser):
    _procesar_tipo_dato(parser, "Chest", "CONJUNTO")

"""
----------------------------------------------------------------------------
 ARCHIVO - Book <id> = {/ ... /};
----------------------------------------------------------------------------
 ACEPTA
Book bitacora = {/ "bitacora.txt", 'L' /};
Book registro = {/ "registro.txt", 'C' /};
Book archivo = {/ "archivo.txt", 'X' /};
Book conf = {/ "config.sys", 'R' /};
----------------------------------------------------------------------------
RECHAZA 
Book = {/ "archivo.txt", 'L' /};                  # Error: Falta el identificador
Book archivo = { "archivo.txt", 'L' /};           # Error: Falta la barra inicial '/'
Book archivo = {/ "archivo.txt", 'L' };           # Error: Falta la barra final '/'
Book archivo = {/ archivo.txt, 'L' /};            # Error: Nombre del archivo sin comillas dobles
Book archivo = {/ "archivo.txt", L /};            # Error: Modo sin comillas simples
Book archivo = {/ "archivo.txt" /};               # Error: Falta el modo
Book archivo = {/ "archivo.txt", 'L', 'X' /};     # Error: Demasiados argumentos
Book archivo = "archivo.txt";                     # Error: Literal de string fuera de estructura de archivo
Book Book = {/ "archivo.txt", 'L' /};             # Error: 'Book' es un tipo, no se permite como identificador
----------------------------------------------------------------------------
"""
def procesar_dato_book(parser):
    _procesar_tipo_dato(parser, "Book", "ARCHIVO")


#----------------------------------------------------------------------------
# FLOAT - Ghast <id> = <float_literal>;
#----------------------------------------------------------------------------
# ACEPTA 
# Ghast temperatura = 36.6;
# Ghast decimal = 0.75;
# Ghast entero = 5.0;        

# RECHAZA
# Ghast = 3.14;                   # Error: Falta identificador
# Ghast masa = "3.14";            # Error: Literal tipo string
# Ghast masa = 3,14;              # Error: Coma en lugar de punto decimal
# Ghast masa = 5.;                # Error: Punto decimal sin decimales
# Ghast masa = .5;                # Error: Punto decimal sin parte entera
# Ghast masa = 2.3.4;             # Error: Más de un punto decimal
# Ghast Ghast = 4.0;              # Error: 'Ghast' es un tipo, no se puede usar como identificador
#----------------------------------------------------------------------------
def procesar_dato_ghast(parser):
    _procesar_tipo_dato(parser, "Ghast", "FLOAT")



#----------------------------------------------------------------------------
# REGISTRO - Entity <id> = { ... };
#----------------------------------------------------------------------------
# ACEPTA 
# Entity jugador = { 'J', "Steve", 100 };
# Entity enemigo = { 'E', "Zombie", 75 };
# Entity jefe = { 'B', "Boss", 250 };

# RECHAZA 
# Entity = { 'E', "Zombie", 75 };              # Error: Falta identificador
# Entity jugador = { "Steve", 'J', 100 };      # Error: Orden incorrecto (tipo literal inválido)
# Entity jefe = { 'B', "Boss" };               # Error: Falta un valor
# Entity enemigo = { 'E', "Zombie", 75 };;     # Error: Punto y coma duplicado
# Entity jugador = { 'B', Boss, 100 };         # Error: String sin comillas
# Entity jugador = { 'B', "Boss", setenta };   # Error: Literal numérico inválido
# Entity Entity = { 'X', "Data", 1 };          # Error: 'Entity' es un tipo, no puede ser nombre
#----------------------------------------------------------------------------
def procesar_dato_entity(parser):
    _procesar_tipo_dato(parser, "Entity", "REGISTROS")

#----------------------------------------------------------------------------
# TIPO DE DATO ARREGLO, DECLARACION Y LITERAL  (Shelf <type> <id> = <array_literal> )    FALTA 
#----------------------------------------------------------------------------
# ACEPTA
# Shelf Stack valores = [1, 2, 3];
# Shelf Rune letras = ['A', 'B', 'C'];
# Shelf Spider palabras = ["hola", "mundo"];
# Shelf Chest cofres = [{: 'a' :}, {: "x" 'y' :}];
# Shelf Book archivos = [{/ "log.txt", 'L' /}, {/ "reg.txt", 'C' /}];
# Shelf Entity enemigos = [{ 'E', "Zombie", 100 }, { 'B', "Boss", 250 }];

# RECHAZA 
# Shelf Stack = [1, 2, 3];                     # Falta identificador
# Shelf Stack conteo = 1, 2, 3;                # Falta corchetes []
# Shelf Rune letras = [A, B, C];               # Caracteres sin comillas simples
# Shelf Spider palabras = ['hola', mundo];     # String sin comillas dobles
# Shelf Torch luces = [On, Maybe, Off];        # Valor booleano inválido "Maybe"
# Shelf Ghast nums = [5.];                     # Float con punto sin decimales
# Shelf Chest inventario = [{: :}];            # Conjunto con coma final sin valor
# Shelf Book datos = [{/ log.txt, 'L' /}];     # Archivo sin comillas en el nombre
# Shelf Entity e = [{ 'B', Boss, 100 }];       # String sin comillas ("Boss")
# Shelf Shelf items = [...]                    # 'Shelf' es tipo, no identificador válido
#----------------------------------------------------------------------------

def procesar_arreglo(parser):
        print(f"-----------------------------------------------------------------------")
        print("---- Procesando declaración de arreglo Shelf")
        parser.avanzar()  # saltar 'Shelf'

        # Validar tipo base
        tipo, tipo_base = parser.token_actual_tipo_valor()
        if not tipo.startswith("TIPO_"):
            print(f"Error: Se esperaba un tipo base después de 'Shelf', pero se encontró: {tipo_base}")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", tipo_base)
            return
        parser.avanzar()

        # Validar identificador
        tipo, var_name = parser.token_actual_tipo_valor()
        if tipo != "IDENTIFICADOR":
            print(f"Error: Se esperaba un identificador para el arreglo después del tipo '{tipo_base}'")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", var_name)
            return
        print(f"Arreglo detectado: Shelf {tipo_base} {var_name}")
        parser.avanzar()

        # Validar '='
        tipo, simbolo = parser.token_actual_tipo_valor()
        if tipo != "OPERADOR" or simbolo != "=":
            print("Error: Se esperaba '=' después del identificador del arreglo")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", simbolo)
            return
        parser.avanzar()

        # Validar literal de arreglo
        tipo, arreglo_val = parser.token_actual_tipo_valor()
        if tipo != "LITERAL_ARREGLO":
            print(f"Error: Se esperaba un literal de arreglo, pero se encontró: ({tipo}, '{arreglo_val}')")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", arreglo_val)
            return
        print(f"---- Inicialización válida: {var_name} = {arreglo_val}")
        print(f"-----------------------------------------------------------------------")
        parser.avanzar()

        # Validar cierre con ;
        tipo, simbolo = parser.token_actual_tipo_valor()
        if tipo == "SIMBOLO" and simbolo == ";":
            print(f"---- Declaración finalizada: Shelf {tipo_base} {var_name} = {arreglo_val}\n")
            print(f"-----------------------------------------------------------------------")
            parser.avanzar()
        else:
            print("Error: Se esperaba ';' al final de la declaración del arreglo")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", simbolo)
            return

#----------------------------------------------------------------------------
#   FUNCION BASE QUE VALIDA ESTRUCTURA Y LITERALES POR TIPO
#----------------------------------------------------------------------------
def _procesar_tipo_dato(parser, tipo_dato_base, tipo_base):
        print(f"---- Procesando declaración de tipo: {tipo_dato_base}")
        print(f"-----------------------------------------------------------------------")
        parser.avanzar()
        while not parser.fin():
            tipo, valor = parser.token_actual_tipo_valor()

            # ERROR 1 y 2: No es identificador, o es palabra reservada o tipo no válido
            if not parser.validar_identificador(tipo, valor):
                # Error ya mostrado por la función
                return
            
            nombre = valor
            print(f"-----------------------------------------------------------------------")
            print(f"---- Tipo de dato detectado: {tipo_dato_base} {nombre}")
            parser.avanzar()

            valor_literal = None

            # Posible asignación con '='
            tipo, simbolo = parser.token_actual_tipo_valor()
            if tipo == "OPERADOR" and simbolo == "=":
                parser.avanzar()
                tipo_lit, valor_lit = parser.token_actual_tipo_valor()

                # ERROR 3: Literal incompatible con el tipo
                literales_validos = {
                    "ENTERO": ["LITERAL_ENTERO"],
                    "FLOAT": ["LITERAL_FLOAT"],
                    "STRING": ["LITERAL_STRING"],
                    "CARACTER": ["LITERAL_CHAR"],
                    "BOOL": ["LITERAL_BOOL"],
                    "CONJUNTO": ["LITERAL_CONJUNTO"],
                    "ARCHIVO": ["LITERAL_ARCHIVO"],
                    "ARREGLOS": ["LITERAL_ARREGLO"],
                    "REGISTROS": ["LITERAL_REGISTRO"]
                }

                if tipo_lit not in literales_validos.get(tipo_base, []):
                    print(f"Error: El valor '{valor_lit}' no es válido para el tipo {tipo_dato_base}")
                    print(f"-----------------------------------------------------------------------")
                    parser.actualizar_token("ERROR", valor_lit)
                    parser.saltar_hasta_coma_o_puntoycoma()
                    continue  # O sigue procesando el siguiente identificador
                valor_literal = valor_lit
                print(f"---- Inicialización válida: {nombre} = {valor_literal}")
                parser.avanzar()

            # Cierre con ; o , o error
            tipo, simbolo = parser.token_actual_tipo_valor()
            if tipo == "SIMBOLO" and simbolo == ",":
                print(f"↪ Otra variable del mismo tipo {tipo_dato_base} continúa...")
                print(f"-----------------------------------------------------------------------")
                parser.avanzar()
                continue
            elif tipo == "SIMBOLO" and simbolo == ";":
                print(f"---- Declaración finalizada: {tipo_dato_base} {nombre}" + (f" = {valor_literal}" if valor_literal else ""))
                print(f"-----------------------------------------------------------------------")
                parser.avanzar()
                break
            else:
                # ERROR 4: Se esperaba ',' o ';'
                print(f"Error: Se esperaba ',' o ';' después de la variable '{nombre}'")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", simbolo)
                return