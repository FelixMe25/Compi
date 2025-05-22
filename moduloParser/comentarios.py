#----------------------------------------------------------------------------
#                      COMENTARIO DE BLOQUE Y LINEA 
#----------------------------------------------------------------------------
def procesar_comentarios(self):
    tipo, valor = self.token_actual_tipo_valor()

    if tipo == "COMENTARIO":
        print(f"---- Comentario de línea: {valor}")
        print("-----------------------------------------------------------------------")
        self.avanzar()
    elif tipo == "COMENTARIO_BLOQUE":
        nivel = 1
        comentario_completo = valor
        self.avanzar()
        while not self.fin():
            tipo, val = self.token_actual_tipo_valor()
            comentario_completo += " " + val
            if val == "$*":
                nivel += 1
            elif val == "*$":
                nivel -= 1
                if nivel == 0:
                    break
            self.avanzar()
        if nivel == 0:
            print("---- Comentario de bloque correctamente cerrado.")
            print("-----------------------------------------------------------------------")
            self.avanzar()
        else:
            print("Error: Comentario de bloque no cerrado correctamente.")
            print("-----------------------------------------------------------------------")
            self.actualizar_token("ERROR", valor)