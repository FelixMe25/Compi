#----------------------------------------------------------------------------
#   SECCION DE TIPOS (ResourcePack)
#   SISTEMA DE ASIGNACION DE TIPOS (Anvil <id> -> <dataType>)
#----------------------------------------------------------------------------
#   WorldName TypesSectionExample: 
#   ResourcePack 
#       Anvil Gemstone -> Spider; 
#   worldSave 
#----------------------------------------------------------------------------
    
def seccion_tipos(parser, token, valor):
        print(f"Sección de tipos detectada: {valor}")
        parser.avanzar()

        tipos_base_validos = (
            "TIPO_ENTERO", "TIPO_STRING", "TIPO_CARACTER",
            "TIPO_FLOAT", "TIPO_CONJUNTO", "TIPO_ARCHIVO",
            "TIPO_ARREGLOS", "TIPO_REGISTROS"
        )

        while not parser.fin():
            tipo, valor = parser.token_actual_tipo_valor()

            if tipo == "ASIGNACION_TIPOS" and valor == "Anvil":
                print(f"-----------------------------------------------------------------------")
                print("---- Asignación de tipos Anvil encontrada")
                parser.avanzar()

                # Error 1 y 2: identificador inválido
                # Anvil Rune -> Spider;
                nombre = parser.validar_identificador_o_saltar()
                if nombre is None:
                    continue  
                parser.avanzar()  

                # Error 3: falta de flecha ->
                # Anvil hola Spider; 
                tipo, simbolo = parser.token_actual_tipo_valor()
                if tipo != "FLECHA" or simbolo != "->":
                    print(f"Error: Se esperaba '->' después de '{nombre}', pero se encontró ({tipo}, '{simbolo}')")
                    print(f"---------------------------------------------------------------")
                    parser.actualizar_token("ERROR", simbolo)
                    parser.saltar_hasta_puntoycoma()
                    continue

                parser.avanzar()

                # Error 4: tipo base no válido
                # Anvil recurso -> Papaya;
                tipo, tipo_asignado = parser.token_actual_tipo_valor()
                if tipo not in tipos_base_validos:
                    print(f"Error: '{tipo_asignado}' no es un tipo válido para asignar a '{nombre}'.")
                    print(f"---------------------------------------------------------------")
                    parser.actualizar_token("ERROR", tipo_asignado)
                    parser.saltar_hasta_puntoycoma()
                    continue

                parser.avanzar()

                # Error 5: falta de ;
                # Anvil recurso -> Stack 
                tipo, fin = parser.token_actual_tipo_valor()
                if tipo == "SIMBOLO" and fin == ";":
                    tipo_base = tipo.replace("TIPO_", "")
                    parser.tipos_personalizados[nombre] = tipo_base
                    print(f"---- Asignación válida: {nombre} es de tipo {tipo_base}")
                    print(f"---------------------------------------------------------------")
                    parser.avanzar()
                else:
                    print("Error: Se esperaba ';' al final de la asignación.")
                    print(f"---------------------------------------------------------------")
                    parser.actualizar_token("ERROR", fin)
                    parser.avanzar()
                    continue
            else:
                break  