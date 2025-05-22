#----------------------------------------------------------------------------
#                   ENCABEZADO DE FUNCIONES Y PROCEDIMIENTO 
#----------------------------------------------------------------------------
def procesar_funcion_o_procedimiento(parser):
        tipo, valor = parser.token_actual_tipo_valor()

        if tipo not in ["ENCABEZADO_FUNCIONES", "ENCABEZADO_PROCEDIMIENTOS"]:
            return

        tipo_rutina = valor  # Spell o Ritual
        print(f"--- Rutina {tipo_rutina} detectada")
        parser.avanzar()

        # Nombre de la función/procedimiento
        tipo, nombre = parser.token_actual_tipo_valor()
        if tipo != "IDENTIFICADOR":
            print(f"Error: Se esperaba el nombre del {tipo_rutina} después de {tipo_rutina}")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", nombre)
            return
        parser.avanzar()

        # Paréntesis de apertura
        tipo, simbolo = parser.token_actual_tipo_valor()
        if tipo != "SIMBOLO" or simbolo != "(":
            print("Error: Se esperaba '(' para iniciar la lista de parámetros")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", simbolo)
            return
        parser.avanzar()

        print(f"---- Iniciando lectura de parámetros para {nombre}()")
        print(f"-----------------------------------------------------------------------")

        # ✅ Manejar funciones sin parámetros
        tipo, simbolo = parser.token_actual_tipo_valor()
        if tipo == "SIMBOLO" and simbolo == ")":
            parser.avanzar()
        else:
            while not parser.fin():
                tipo, valor = parser.token_actual_tipo_valor()

                if not tipo.startswith("TIPO_"):
                    print(f"Error: Se esperaba un tipo de dato, pero se encontró: {valor}")
                    print(f"-----------------------------------------------------------------------")
                    parser.actualizar_token("ERROR", valor)
                    return
                tipo_dato = valor
                parser.avanzar()

                # Manejo de "ref" y "::"
                tipo, posible_ref = parser.token_actual_tipo_valor()
                por_referencia = False

                if tipo == "PALABRA_RESERVADA" and posible_ref == "ref":
                    por_referencia = True
                    parser.avanzar()
                    tipo, posible_ref = parser.token_actual_tipo_valor()

                if tipo == "SIMBOLO" and posible_ref == "::":
                    parser.avanzar()
                    tipo, valor = parser.token_actual_tipo_valor()
                else:
                    valor = posible_ref

                if tipo != "IDENTIFICADOR":
                    print(f"Error: Se esperaba identificador para el parámetro, se obtuvo: {valor}")
                    print(f"-----------------------------------------------------------------------")
                    parser.actualizar_token("ERROR", valor)
                    return

                print(f"---- Parámetro detectado: {tipo_dato} {'ref ' if por_referencia else ''}{valor}")
                print(f"-----------------------------------------------------------------------")
                parser.avanzar()

                tipo, simbolo = parser.token_actual_tipo_valor()
                if simbolo == ",":
                    parser.avanzar()
                    continue
                elif simbolo == ";":
                    parser.avanzar()
                    continue
                elif simbolo == ")":
                    parser.avanzar()
                    break
                else:
                    print(f" Error: Se esperaba ',', ';' o ')' después del parámetro")
                    print(f"-----------------------------------------------------------------------")
                    parser.actualizar_token("ERROR", simbolo)
                    return

        # Si es una función, verificar retorno
        if tipo_rutina == "Spell":
            tipo, simbolo = parser.token_actual_tipo_valor()
            if tipo != "FLECHA" or simbolo != "->":
                print("Error: Se esperaba '->' después de los parámetros de Spell")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", simbolo)
                return
            parser.avanzar()

            tipo, retorno = parser.token_actual_tipo_valor()
            if not tipo.startswith("TIPO_"):
                print(f"Error: Tipo de retorno inválido: {retorno}")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", retorno)
                return
            print(f"--- Retorno declarado: {retorno}")
            parser.avanzar()

        # Finalización con punto y coma
        tipo, simbolo = parser.token_actual_tipo_valor()
        if tipo == "SIMBOLO" and simbolo == ";":
            print(f"---- Encabezado de {tipo_rutina} '{nombre}' procesado correctamente.")
            print(f"-----------------------------------------------------------------------")
            parser.avanzar()
        else:
            print("Error: Se esperaba ';' al final del encabezado")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", simbolo)
            return

#----------------------------------------------------------------------------
#   SECCIÓN DE PROTOTIPOS (Recipe)
#   SISTEMA DE DECLARACIÓN DE PROTOTIPOS DE FUNCIONES (Spell) Y PROCEDIMIENTOS (Ritual)
#   Ejemplos de sintaxis:
#   - Spell forgeGemstone (Spider :: mineralName);
#   - Ritual calculateValue (Stack :: diamonds) -> cobblestone;
#----------------------------------------------------------------------------
def seccion_prototipo(parser, token, valor):
        print(f"---- Sección de prototipos detectada: {valor}")
        parser.avanzar()

        while not parser.fin():
            tipo, valor = parser.token_actual_tipo_valor()

            if tipo not in ("ENCABEZADO_FUNCIONES", "ENCABEZADO_PROCEDIMIENTOS"):
                break

            tipo_rutina = valor  # Spell o Ritual
            parser.avanzar()

            # Nombre del prototipo
            tipo, nombre_rutina = parser.token_actual_tipo_valor()
            if tipo != "IDENTIFICADOR":
                print(f"Error: Se esperaba el nombre del prototipo después de '{tipo_rutina}'")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", nombre_rutina)
                return
            parser.avanzar()

            # Paréntesis de apertura
            tipo, simbolo = parser.token_actual_tipo_valor()
            if tipo != "SIMBOLO" or simbolo != "(":
                print("Error: Se esperaba '(' antes de los parámetros")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", simbolo)
                return
            parser.avanzar()

            # Tipo del parámetro
            tipo, tipo_param = parser.token_actual_tipo_valor()
            if not tipo.startswith("TIPO_") and tipo not in parser.tipos_personalizados:
                print(f" Error: Tipo de parámetro inválido: {tipo_param}")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", tipo_param)
                return
            parser.avanzar()

            # Separador '::'
            tipo, simbolo = parser.token_actual_tipo_valor()
            if tipo != "SIMBOLO" or simbolo != "::":
                print("Error: Se esperaba '::' entre tipo y nombre del parámetro")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", simbolo)
                return
            parser.avanzar()

            # Nombre del parámetro
            tipo, nombre_param = parser.token_actual_tipo_valor()
            if tipo != "IDENTIFICADOR":
                print("Error: Se esperaba un identificador como nombre del parámetro")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", nombre_param)
                return
            parser.avanzar()

            # Paréntesis de cierre
            tipo, simbolo = parser.token_actual_tipo_valor()
            if tipo != "SIMBOLO" or simbolo != ")":
                print("Error: Se esperaba ')' al final de los parámetros")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", simbolo)
                return
            parser.avanzar()

            # Si es una función (Spell), debe terminar con ;
            if tipo_rutina == "Spell":
                tipo, simbolo = parser.token_actual_tipo_valor()
                if tipo == "SIMBOLO" and simbolo == ";":
                    print(f"---- Prototipo válido: {tipo_rutina} {nombre_rutina} ({tipo_param} :: {nombre_param});\n")
                    parser.avanzar()
                else:
                    print(" Error: Se esperaba ';' al final del prototipo de función")
                    print(f"-----------------------------------------------------------------------")
                    parser.actualizar_token("ERROR", simbolo)
                    return

            # Si es un procedimiento (Ritual), debe tener -> tipo y luego ;
            elif tipo_rutina == "Ritual":
                tipo, simbolo = parser.token_actual_tipo_valor()
                if tipo != "FLECHA" or simbolo != "->":
                    print("Error: Se esperaba '->' después del paréntesis en Ritual")
                    print(f"-----------------------------------------------------------------------")
                    parser.actualizar_token("ERROR", simbolo)
                    return
                parser.avanzar()

                tipo, tipo_retorno = parser.token_actual_tipo_valor()
                if not tipo.startswith("TIPO_") and tipo not in parser.tipos_personalizados:
                    print(f"Error: Tipo de retorno inválido: {tipo_retorno}")
                    print(f"-----------------------------------------------------------------------")
                    parser.actualizar_token("ERROR", tipo_retorno)
                    return
                parser.avanzar()

                tipo, simbolo = parser.token_actual_tipo_valor()
                if tipo == "SIMBOLO" and simbolo == ";":
                    print(f"---- Prototipo válido: {tipo_rutina} {nombre_rutina} ({tipo_param} :: {nombre_param}) -> {tipo_retorno};\n")
                    parser.avanzar()
                else:
                    print("Error: Se esperaba ';' al final del prototipo de procedimiento")
                    print(f"-----------------------------------------------------------------------")
                    parser.actualizar_token("ERROR", simbolo)
                    return
            else:
                print(" Error: Tipo de encabezado desconocido")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", tipo_rutina)
                return
