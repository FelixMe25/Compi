from moduloParser.validaciones_semanticas import (validar_operacion_relacional, 
                                                  validar_condicion_booleana, 
                                                  validar_switch,
                                                  validar_operacion_logica
                                                  )

#----------------------------------------------------------------------------
#                MANEJO DE BLOQUES DE MAS DE UNA INSTRUCCION
#----------------------------------------------------------------------------
def manejo_bloque(parser, tipo, valor):
    print(f"-----------------------------------------------------------------------")
    print(f"---- Bloque de màs de una instrucciòn: {valor}")
    parser.bandera_bloque += 1
    parser.avanzar()
    while not parser.fin():
        tipo_actual, valor_actual = parser.token_actual_tipo_valor()
        if tipo_actual == "FIN_BLOQUE" and valor_actual == "PolloAsado":
            print(f"Fin del bloque detectado con: {valor_actual}")
            print(f"-----------------------------------------------------------------------")
            parser.bandera_bloque -= 1
            parser.avanzar()
            return

        if tipo_actual == "MAS_DE_UNA_INSTRUCCION" and valor_actual == "PolloCrudo":
            print("----- Bloque anidado encontrado dentro de otro bloque (Pollo crudo).")
            manejo_bloque(parser, tipo_actual, valor_actual)
            continue
        # Soporte para instrucción de retorno 'respawn'
        if tipo_actual in ["RETURN_FUNC", "OPERACION_RETURN"]:
            parser.avanzar()
            tipo_valor, valor_retorno = parser.token_actual_tipo_valor()
            # Aquí podrías validar el tipo de retorno según el Spell actual
            print(f"---- Instrucción de retorno detectada: respawn {valor_retorno}")
            parser.avanzar()
            tipo_pyc, pyc = parser.token_actual_tipo_valor()
            if tipo_pyc == "SIMBOLO" and pyc == ";":
                parser.avanzar()
            else:
                print("Error: Se esperaba ';' después de respawn")
                parser.actualizar_token("ERROR", pyc)
                parser.saltar_hasta_puntoycoma()
            continue
        parser.parse_instruccion_actual()

# ------------------------------------------------------------------------------
# OPERACIONES DE REPETAER 
# ------------------------------------------------------------------------------
def procesar_repeater(parser):
    print("--- Instrucción de ciclo REPEATER detectada")
    print(f"-----------------------------------------------------------------------")
    parser.avanzar()

    # ---------------------------
    # Validar condición: a <= 10
    # ---------------------------
    tipo_izq, izq = parser.token_actual_tipo_valor()
    if tipo_izq != "IDENTIFICADOR":
        print("Error: Se esperaba una variable en la condición del repeater")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", izq)
        parser.saltar_hasta_puntoycoma()
        return
    parser.avanzar()

    tipo_op, operador = parser.token_actual_tipo_valor()
    if tipo_op not in ["OPERADOR", "OPERADOR_COMPARACION"] or operador not in [">", "<", ">=", "<=", "==", "!=", "is", "isNot"]:
        print(" Error: Operador de condición inválido en repeater")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", operador)
        parser.saltar_hasta_puntoycoma()
        return
    parser.avanzar()

    tipo_der, der = parser.token_actual_tipo_valor()
    if tipo_der not in ["IDENTIFICADOR", "LITERAL_ENTERO"]:
        print(" Error: Valor inválido en condición del repeater")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", der)
        parser.saltar_hasta_puntoycoma()
        return
    parser.avanzar()

    # Validación Semántica
    if not validar_operacion_relacional(parser.tabla, izq, operador, der):
        parser.actualizar_token("ERROR", operador)
        parser.saltar_hasta_puntoycoma()
        return
    parser.avanzar()

    # ---------------------------
    # Validar palabra clave craft
    # ---------------------------
    tipo_craft, palabra_craft = parser.token_actual_tipo_valor()
    if tipo_craft != "INICIO_BLOQUE" or palabra_craft != "craft":
        print(" Error: Se esperaba 'craft' después de la condición del repeater")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", palabra_craft)
        return
    parser.avanzar()

    # ---------------------------
    # Inicio de bloque PolloCrudo
    # ---------------------------
    tipo_bloque, palabra_bloque = parser.token_actual_tipo_valor()
    if tipo_bloque != "MAS_DE_UNA_INSTRUCCION" or palabra_bloque != "PolloCrudo":
        print("Error: Se esperaba inicio de bloque 'PolloCrudo'")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", palabra_bloque)
        return
    print("---- Bloque de más de una instrucción: PolloCrudo")
    print(f"-----------------------------------------------------------------------")
    parser.avanzar()

    # ---------------------------
    # Instrucciones dentro del repeater
    # ---------------------------
    while not parser.fin():
        tipo, valor = parser.token_actual_tipo_valor()

        if tipo == "FIN_BLOQUE" and valor == "PolloAsado":
            print("---- Fin del bloque detectado con: PolloAsado")
            print(f"-----------------------------------------------------------------------")
            parser.avanzar()
            break

        parser.parse_instruccion_actual()


# ------------------------------------------------------------------------------
# TARGET - IF
# ------------------------------------------------------------------------------
def procesar_target(parser):
    print("---- Instrucción condicional TARGET detectada")
    print(f"-----------------------------------------------------------------------")
    parser.avanzar()

    tipo, izq = parser.token_actual_tipo_valor()
    if tipo != "IDENTIFICADOR":
        print(" Error: Se esperaba una variable en la condición del target")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", izq)
        return
    parser.avanzar()

    tipo, operador = parser.token_actual_tipo_valor()
    if tipo != "OPERADOR_COMPARACION" or operador not in [">", "<", ">=", "<=", "is", "isNot"]:
        print(" Error: Operador inválido en condición del target")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", operador)
        return
    parser.avanzar()

    tipo, der = parser.token_actual_tipo_valor()
    if tipo not in ["IDENTIFICADOR", "LITERAL_ENTERO", "LITERAL_BOOL"]:
        print(" Error: Valor inválido en condición del target")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", der)
        return
    parser.avanzar()

    # ------------- Validación Semántica ---------------------
    # Detectar si hay una operación lógica (e.g., not var, var1 and var2)
    if operador in ["and", "or", "xor"]:
        if not validar_operacion_logica(parser.tabla, izq, operador, der):
            parser.actualizar_token("ERROR", operador)
            return
    elif operador == "not":
        if not validar_operacion_logica(parser.tabla, der, operador):
            parser.actualizar_token("ERROR", operador)
            return
    else:
        # Asumimos que es una comparación relacional
        if not validar_operacion_relacional(parser.tabla, izq, operador, der):
            parser.actualizar_token("ERROR", operador)
            return
    parser.avanzar()

    tipo, palabra = parser.token_actual_tipo_valor()
    if tipo == "PALABRA_CRAFT":
        parser.avanzar()

        while not parser.fin():
            tipo, bloque = parser.token_actual_tipo_valor()
            if tipo == "PALABRA_HIT":
                print("---- Sección 'hit' detectada")
                print(f"-----------------------------------------------------------------------")
                parser.avanzar()
                tipo, inicio = parser.token_actual_tipo_valor()
                if tipo == "MAS_DE_UNA_INSTRUCCION" and inicio == "PolloCrudo":
                    manejo_bloque(parser, tipo, inicio)
                else:
                    print("Error: Se esperaba un bloque PolloCrudo después de 'hit'")
                    print(f"-----------------------------------------------------------------------")
                    return
            elif tipo == "PALABRA_MISS":
                print(" Sección 'miss' detectada")
                print(f"-----------------------------------------------------------------------")
                parser.avanzar()
                tipo, inicio = parser.token_actual_tipo_valor()
                if tipo == "MAS_DE_UNA_INSTRUCCION" and inicio == "PolloCrudo":
                    manejo_bloque(parser, tipo, inicio)
                else:
                    print("Error: Se esperaba un bloque PolloCrudo después de 'miss'")
                    print(f"-----------------------------------------------------------------------")
                    return
            else:
                break


# ------------------------------------------------------------------------------
# SWICH 
# ------------------------------------------------------------------------------
def procesar_instruccion_switch(parser):
    print(f"--- Instrucción switch detectada con jukebox")
    print(f"-----------------------------------------------------------------------")
    parser.avanzar()  # saltar 'jukebox'

    # Condición
    tipo, condicion = parser.token_actual_tipo_valor()
    if tipo != "IDENTIFICADOR":
        print(" Error: Se esperaba una variable como condición para jukebox.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", condicion)
        parser.saltar_hasta_puntoycoma()
        return
    parser.avanzar()

    # Validación Semántica
    if not validar_switch(parser.tabla, condicion):
        print(f"Error semántico: La condición de 'jukebox' debe ser de tipo 'Stack'. Se recibió '{tipo_cond}'.")
        parser.actualizar_token("ERROR", condicion)
        return

    # craft
    tipo, palabra = parser.token_actual_tipo_valor()
    if tipo != "INICIO_BLOQUE" or palabra != "craft":
        print(" Error: Se esperaba 'craft' después de la condición.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", palabra)
        parser.saltar_hasta_puntoycoma()
        return
    parser.avanzar()

    # PolloCrudo
    tipo, palabra = parser.token_actual_tipo_valor()
    if tipo != "MAS_DE_UNA_INSTRUCCION":
        print("Error: Se esperaba 'PolloCrudo' para iniciar el bloque.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", palabra)
        parser.saltar_hasta_puntoycoma()
        return
    parser.avanzar()

    # Procesar casos disc y silence hasta PolloAsado
    while not parser.fin():
        tipo, valor = parser.token_actual_tipo_valor()

        if tipo == "FIN_BLOQUE" and valor == "PolloAsado":
            print("---- Fin de instrucción jukebox con PolloAsado")
            print(f"-----------------------------------------------------------------------")
            parser.avanzar()
            return

        if tipo == "CASO_SWITCH" and valor == "disc":
            parser.avanzar()
            tipo, numero = parser.token_actual_tipo_valor()
            if tipo != "LITERAL_ENTERO":
                print("Error: Se esperaba número después de 'disc'")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", numero)
                parser.saltar_hasta_puntoycoma()
                continue
            print(f"Caso disc {numero}:")
            parser.avanzar()

            tipo, simbolo = parser.token_actual_tipo_valor()
            if simbolo == ":":
                parser.avanzar()

                # Procesar instrucciones del caso
                while not parser.fin():
                    tipo, valor = parser.token_actual_tipo_valor()
                    if tipo in ["CASO_SWITCH", "DEFAULT_SWITCH", "FIN_BLOQUE"]:
                        break
                    parser._procesar_instruccion_actual(tipo, valor)

            elif tipo == "DEFAULT_SWITCH" and valor == "silence":
                print("Caso silence:")
                parser.avanzar()
                while not parser.fin():
                    tipo, valor = parser.token_actual_tipo_valor()
                    if tipo in ["CASO_SWITCH", "DEFAULT_SWITCH", "FIN_BLOQUE"]:
                        break
                    parser._procesar_instruccion_actual(tipo, valor)
            else:
                parser.avanzar()


# ------------------------------------------------------------------------------
# SPAWNER - REPEAT
# ------------------------------------------------------------------------------
def procesar_spawner(parser):
    print("---- Instrucción 'spawner' detectada")
    print(f"-----------------------------------------------------------------------")
    parser.avanzar()

    while not parser.fin():
        tipo, valor = parser.token_actual_tipo_valor()
        if tipo == "PALABRA_RESERVADA" and valor == "exhausted":
            break
        parser.parse()  # procesa instrucciones dentro del spawner

        tipo, palabra = parser.token_actual_tipo_valor()
        if tipo == "PALABRA_RESERVADA" and palabra == "exhausted":
            parser.avanzar()
            tipo, condicion = parser.token_actual_tipo_valor()
            print(f"---- Condición de salida del spawner: {condicion}")
            print(f"-----------------------------------------------------------------------")
            parser.avanzar()
          
            # ----------- Validación Semántica -----------------
            if not validar_condicion_booleana(parser.tabla, condicion):
                parser.actualizar_token("ERROR", condicion)
                return
            
        else:
            print(" Error: Falta 'exhausted' en spawner")
            print(f"-----------------------------------------------------------------------")


# ------------------------------------------------------------------------------
# WALK - FOR
# ------------------------------------------------------------------------------
def procesar_walk(parser):
    print("---- Instrucción 'walk' detectada")
    print(f"-----------------------------------------------------------------------")
    parser.avanzar()

    tipo, variable = parser.token_actual_tipo_valor()
    if tipo != "IDENTIFICADOR":
        print("Error: Se esperaba un identificador en 'walk'")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", variable)
        return
    parser.avanzar()

    palabras_clave = ["set", "to", "step", "craft"]
    valores = []

    for palabra in palabras_clave:
        tipo, valor = parser.token_actual_tipo_valor()
        if palabra == "step" and valor != "step":
            valores.append("1")  # default
            break
        if valor != palabra:

            print(f"Error: Se esperaba '{palabra}'")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", valor)
            return
        parser.avanzar()
            
        tipo, numero = parser.token_actual_tipo_valor()
        if tipo != "LITERAL_ENTERO" and tipo != "IDENTIFICADOR":
            print(f"Error: Se esperaba un número o identificador después de '{palabra}'")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", numero)
            return
        valores.append(numero)
        parser.avanzar()

        tipo, palabra = parser.token_actual_tipo_valor()
        if palabra != "craft":

            print(" Error: Se esperaba 'craft' al final de walk")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", palabra)
            return

        parser.avanzar()
        manejo_bloque(parser, "MAS_DE_UNA_INSTRUCCION", "PolloCrudo")

# ------------------------------------------------------------------------------
# WITHER - WITH
# ------------------------------------------------------------------------------
def procesar_wither(parser):
    print("---- Instrucción 'wither' detectada")
    print(f"-----------------------------------------------------------------------")
    parser.avanzar()

    tipo, registro = parser.token_actual_tipo_valor()
    if tipo != "IDENTIFICADOR":
        print("Error: Se esperaba un identificador de registro para 'wither'")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", registro)
        return
    parser.avanzar()

    tipo, palabra = parser.token_actual_tipo_valor()
    if tipo != "PALABRA_CRAFT":
        print("Error: Se esperaba la palabra 'craft' en 'wither'")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", palabra)
        return
    parser.avanzar()

    tipo, inicio = parser.token_actual_tipo_valor()
    if tipo != "MAS_DE_UNA_INSTRUCCION" or inicio != "PolloCrudo":
        print("Error: Se esperaba bloque PolloCrudo en 'wither'")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", inicio)
        return

    manejo_bloque(parser, tipo, inicio)

# ------------------------------------------------------------------------------
# CREEPER - BREAK
# ------------------------------------------------------------------------------
def procesar_creeper(parser):
    print("---- Instrucción 'creeper' (break) detectada")
    print(f"-----------------------------------------------------------------------")
    parser.avanzar()
    tipo, simbolo = parser.token_actual_tipo_valor()
    if tipo == "SIMBOLO" and simbolo == ";":
        print("---- 'creeper;' detectado correctamente")
        print(f"-----------------------------------------------------------------------")
        parser.avanzar()
    else:
        print(" Error: Se esperaba ';' después de 'creeper'")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", simbolo)
        parser.saltar_hasta_puntoycoma()  # <- Importante para que no se frene

# ------------------------------------------------------------------------------
# ENDERPERL - CONTINUE
# ------------------------------------------------------------------------------
def procesar_enderperl(parser):
    print("---- Instrucción 'enderperl' (continue) detectada")
    parser.avanzar()
    tipo, simbolo = parser.token_actual_tipo_valor()
    if tipo == "SIMBOLO" and simbolo == ";":
        print("----'enderperl;' detectado correctamente")
        print(f"-----------------------------------------------------------------------")
        parser.avanzar()
    else:
        print(" Error: Se esperaba ';' después de 'enderperl'")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", simbolo)

# ------------------------------------------------------------------------------
# RAQUEQUIT - HALT
# ------------------------------------------------------------------------------
def procesar_ragequit(parser):
    print("---- Instrucción 'ragequit' (halt) detectada")
    print(f"-----------------------------------------------------------------------")
    parser.avanzar()
    tipo, simbolo = parser.token_actual_tipo_valor()
    if tipo == "SIMBOLO" and simbolo == ";":
        print("---- 'ragequit;' detectado correctamente")
        parser.avanzar()
    else:
        print("Error: Se esperaba ';' después de 'ragequit'")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", simbolo)