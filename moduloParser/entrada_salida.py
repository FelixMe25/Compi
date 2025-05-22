#----------------------------------------------------------------------------
#                          MANEJO DE ENTRADA ESTANDAR 
#----------------------------------------------------------------------------

def procesar_entrada_estandar(parser):
        # Obtener el tipo y valor del token actual
        tipo, valor = parser.token_actual_tipo_valor()

        # Verificar si es un operador de entrada estándar tipo hopper<Tipo>()
        if tipo != "OPERADOR_ENTRADA" or not valor.startswith("hopper"):
            return

        # Extraer el tipo de dato de la operación hopper<Tipo>()
        tipo_dato = valor.replace("hopper", "")
        print("-----------------------------------------------------------------------")
        print(f"---- Entrada estándar detectada con: {valor}")
        parser.avanzar()

        # Verificar apertura de paréntesis
        tipo, simbolo = parser.token_actual_tipo_valor()
        if tipo == "SIMBOLO" and simbolo == "(":
            parser.avanzar()
            tipo, simbolo = parser.token_actual_tipo_valor()

            # Verificar cierre de paréntesis
            if tipo == "SIMBOLO" and simbolo == ")":
                parser.avanzar()
                tipo, fin = parser.token_actual_tipo_valor()

                # Verificar punto y coma final
                if tipo == "SIMBOLO" and fin == ";":
                    print(f"---- Entrada estándar completada: {valor}();")
                    print("-----------------------------------------------------------------------")
                    parser.avanzar()
                else:
                    print("Error: Falta ';' al final de hopper.")
                    print("-----------------------------------------------------------------------")
                    parser.actualizar_token("ERROR", fin)
            else:
                print("Error: hopper<Tipo>() no debe tener argumento.")
                print("-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", simbolo)
        else:
            print("Error: Se esperaba '(' después de hopper<Tipo>.")
            print("-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", simbolo)


#----------------------------------------------------------------------------
#                          MANEJO DE SALIDA ESTANDAR 
#----------------------------------------------------------------------------
def procesar_salida_estandar(parser):
        tipo, valor = parser.token_actual_tipo_valor()
        if tipo != "OPERADOR_SALIDA" or not valor.startswith("dropper"):
            return

        tipo_dato = valor.replace("dropper", "")
        print("-----------------------------------------------------------------------")
        print(f"---- Salida estándar detectada: {valor}()")
        parser.avanzar()

        tipo, simbolo = parser.token_actual_tipo_valor()
        if tipo == "SIMBOLO" and simbolo == "(":
            parser.avanzar()
            tipo, argumento = parser.token_actual_tipo_valor()

            # Tipos esperados según dropper<Tipo>
            tipos_esperados = {
                "Stack": "LITERAL_ENTERO",
                "Rune": "LITERAL_CHAR",
                "Spider": "LITERAL_STRING",
                "Torch": "LITERAL_BOOL",
                "Book": "LITERAL_STRING",
                "DNA": "LITERAL_STRING",
            }

            tipo_esperado = tipos_esperados.get(tipo_dato)

            # -------------------------------------------------------------------
            # Soporte para chunk: chunk <identificador o tipo>
            # -------------------------------------------------------------------
            if tipo == "OPERACION_SIZE_OF" and argumento == "chunk":
                parser.avanzar()
                tipo_chunk, valor_chunk = parser.token_actual_tipo_valor()
                if tipo_chunk in ["IDENTIFICADOR", "TIPO_ENTERO", "TIPO_STRING", "TIPO_BOOL", "TIPO_CARACTER",
                                "TIPO_ARCHIVO", "TIPO_CONJUNTO", "TIPO_FLOAT", "TIPO_REGISTROS", "TIPO_ARREGLOS"]:
                    print(f"---- Argumento válido: chunk {valor_chunk}")
                    parser.avanzar()
                    tipo, cierre = parser.token_actual_tipo_valor()
                    if tipo == "SIMBOLO" and cierre == ")":
                        parser.avanzar()
                        tipo, fin = parser.token_actual_tipo_valor()
                        if tipo == "SIMBOLO" and fin == ";":
                            print(f"---- dropper{tipo_dato}(chunk {valor_chunk}); completado correctamente.")
                            print("-----------------------------------------------------------------------")
                            parser.avanzar()
                            return
                        else:
                            print("Error: Falta ';' al final de la salida estándar con chunk.")
                            print("-----------------------------------------------------------------------")
                            parser.actualizar_token("ERROR", fin)
                    else:
                        print("Error: Falta ')' después de chunk <valor>.")
                        print("-----------------------------------------------------------------------")
                        parser.actualizar_token("ERROR", cierre)
                else:
                    print(f"Error: Argumento inválido después de chunk: {valor_chunk}")
                    print("-----------------------------------------------------------------------")
                    parser.actualizar_token("ERROR", valor_chunk)
                return

            # -------------------------------------------------------------------
            # Argumento normal (literal o identificador)
            # -------------------------------------------------------------------
            if tipo == tipo_esperado or tipo == "IDENTIFICADOR":
                print(f"---- Argumento válido para salida {tipo_dato}: {argumento}")
                print("-----------------------------------------------------------------------")
                parser.avanzar()
                tipo, cierre = parser.token_actual_tipo_valor()
                if tipo == "SIMBOLO" and cierre == ")":
                    parser.avanzar()
                    tipo, fin = parser.token_actual_tipo_valor()
                    if tipo == "SIMBOLO" and fin == ";":
                        print(f"---- dropper{tipo_dato}({argumento}); completado correctamente.")
                        print("-----------------------------------------------------------------------")
                        parser.avanzar()
                    else:
                        print("Error: Falta ';' al final de la salida estándar.")
                        print("-----------------------------------------------------------------------")
                        parser.actualizar_token("ERROR", fin)
                else:
                    print("Error: Falta ')' después del argumento.")
                    print("-----------------------------------------------------------------------")
                    parser.actualizar_token("ERROR", cierre)
            else:
                print(f"Error: Se esperaba un argumento de tipo {tipo_esperado} o una variable, pero se recibió {tipo}.")
                print("-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", argumento)

        else:
            print("Error: Se esperaba '(' después de dropper<Tipo>.")
            print("-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", simbolo)