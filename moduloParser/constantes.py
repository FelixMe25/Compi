from moduloParser.validaciones_semanticas import validar_declaracion_constante
#----------------------------------------------------------------------------
#   SECCION DE CONSTANTES (Bedrock)
#   SISTEMA DE ASIGNACIONDE CONSTANTES (Obsidian <type> <id> <value>)
#----------------------------------------------------------------------------
#   Bedrock 
#       Obsidian Stack maxDiamonds 5; 
#       Obsidian Torch hasEnchantedGoldenApple On; 
#       Obsidian Chest lootContents {: 's', 'a' :}
#----------------------------------------------------------------------------

def seccion_constante(parser, token, valor):
    print(f"➡ Sección de constantes iniciada con: {valor}")
    parser.avanzar()
    while not parser.fin():
        tipo, valor = parser.token_actual_tipo_valor()
        if tipo == "ASIGNACION_CONSTANTE" and valor == "Obsidian":
            print(f"-----------------------------------------------------------------------")
            print(f"---- Asignación de constantes Obsidian encontrada")
            parser.avanzar()

            # Error 1: No hay tipo de dato después de 'Obsidian' o tipo inválido
            # Obsidian Papaya contador 5;
            tipo_token, tipo_valor = parser.token_actual_tipo_valor()
            tipos_validos = (
                    "TIPO_ENTERO", "TIPO_STRING", "TIPO_CARACTER", "TIPO_FLOAT",
                    "TIPO_CONJUNTO", "TIPO_ARCHIVO", "TIPO_ARREGLOS",
                    "TIPO_REGISTROS", "TIPO_BOOL"
                )
            if tipo_token not in tipos_validos:
                print(f"Error: Se esperaba un tipo válido después de Obsidian, pero se encontró ({tipo_token}, '{tipo_valor}')")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", tipo_valor)
                return

            tipo_dato = tipo_valor
            tipo_base = tipo_token.replace("TIPO_", "")  
            parser.avanzar()

            # Error 2: No hay identificador después del tipo, o es inválido (palabra reservada o tipo)
            # Obsidian Stack 5; 
            # Obsidian Stack worldSave 5;
            # Obsidian Stack Stack 5; 
            nombre = parser.validar_identificador_o_saltar()
            if nombre is None:
                continue  
            parser.avanzar()

            # Error 3: No hay literal de valor o tipo de literal incorrecto para el tipo dado
            # Obsidian Stack contador "cinco";
            # Obsidian Torch encendido Maybe;
            tipo, valor = parser.token_actual_tipo_valor()
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

            if tipo not in literales_validos.get(tipo_base, []):
                print(f"Error: El valor '{valor}' no es válido para el tipo {tipo_dato}")
                print(f"---------------------------------------------------------------")
                parser.actualizar_token("ERROR", valor)
                return

            valor_literal = valor
            parser.avanzar()

            # Error 4: Falta el símbolo ';' al final de la asignación
            # Obsidian Stack monedas 100
            tipo, valor = parser.token_actual_tipo_valor()
            if tipo == "SIMBOLO" and valor == ";":
                print(f"---- Declaración válida: Obsidian {tipo_dato} {nombre} {valor_literal}")
                print(f"-----------------------------------------------------------------------")

                # Validación Semántica
                tabla_simbolos = parser.tabla
                if not validar_declaracion_constante(tabla_simbolos, nombre, tipo_dato, True, valor_literal):
                    parser.actualizar_token("ERROR", nombre)
                    return
                
                parser.avanzar()
                continue

            else:
                print("Error: Se esperaba ';' al final de la declaración.")
                print(f"-------------------------------------------------")
                parser.actualizar_token("ERROR", valor)
                return
        else:
            break