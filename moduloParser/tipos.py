#----------------------------------------------------------------------------
#   SECCION DE TIPOS (ResourcePack)
#   SISTEMA DE ASIGNACION DE TIPOS (Anvil <id> -> <dataType>)
#----------------------------------------------------------------------------
#   WorldName TypesSectionExample: 
#   ResourcePack 
#       Anvil Gemstone -> Spider; 
#   worldSave 
#----------------------------------------------------------------------------
    
def seccion_tipos(self, token, valor):
        print(f"➡ Sección de tipos detectada: {valor}")
        self.avanzar()

        tipos_base_validos = (
            "TIPO_ENTERO", "TIPO_STRING", "TIPO_CARACTER",
            "TIPO_FLOAT", "TIPO_CONJUNTO", "TIPO_ARCHIVO",
            "TIPO_ARREGLOS", "TIPO_REGISTROS"
        )

        while not self.fin():
            tipo, valor = self.token_actual_tipo_valor()

            if tipo == "ASIGNACION_TIPOS" and valor == "Anvil":
                print(f"-----------------------------------------------------------------------")
                print("---- Asignación de tipos Anvil encontrada")
                self.avanzar()

                # Error 1 y 2: identificador inválido
                # Anvil Rune -> Spider;
                nombre = self.validar_identificador_o_saltar()
                if nombre is None:
                    continue  
                self.avanzar()  

                # Error 3: falta de flecha ->
                # Anvil hola Spider; 
                tipo, simbolo = self.token_actual_tipo_valor()
                if tipo != "FLECHA" or simbolo != "->":
                    print(f"Error: Se esperaba '->' después de '{nombre}', pero se encontró ({tipo}, '{simbolo}')")
                    print(f"---------------------------------------------------------------")
                    self.actualizar_token("ERROR", simbolo)
                    self.saltar_hasta_puntoycoma()
                    continue

                self.avanzar()

                # Error 4: tipo base no válido
                # Anvil recurso -> Papaya;
                tipo, tipo_asignado = self.token_actual_tipo_valor()
                if tipo not in tipos_base_validos:
                    print(f"Error: '{tipo_asignado}' no es un tipo válido para asignar a '{nombre}'.")
                    print(f"---------------------------------------------------------------")
                    self.actualizar_token("ERROR", tipo_asignado)
                    self.saltar_hasta_puntoycoma()
                    continue

                self.avanzar()

                # Error 5: falta de ;
                # Anvil recurso -> Stack 
                tipo, fin = self.token_actual_tipo_valor()
                if tipo == "SIMBOLO" and fin == ";":
                    tipo_base = tipo.replace("TIPO_", "")
                    self.tipos_personalizados[nombre] = tipo_base
                    print(f"---- Asignación válida: {nombre} es de tipo {tipo_base}")
                    print(f"---------------------------------------------------------------")
                    self.avanzar()
                else:
                    print("Error: Se esperaba ';' al final de la asignación.")
                    print(f"---------------------------------------------------------------")
                    self.actualizar_token("ERROR", fin)
                    self.avanzar()
                    continue
            else:
                break  