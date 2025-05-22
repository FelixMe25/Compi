#----------------------------------------------------------------------------
#                      COMENTARIO DE BLOQUE Y LINEA 
#----------------------------------------------------------------------------
def procesar_comentarios(parser):
    tipo, valor = parser.token_actual_tipo_valor()

    if tipo == "COMENTARIO":
        print(f"---- Comentario de línea: {valor}")
        print("-----------------------------------------------------------------------")
        parser.avanzar()
    elif tipo == "COMENTARIO_BLOQUE":
        nivel = 1
        comentario_completo = valor
        parser.avanzar()
        while not parser.fin():
            tipo, val = parser.token_actual_tipo_valor()
            comentario_completo += " " + val
            if val == "$*":
                nivel += 1
            elif val == "*$":
                nivel -= 1
                if nivel == 0:
                    break
            parser.avanzar()
        if nivel == 0:
            print("---- Comentario de bloque correctamente cerrado.")
            print("-----------------------------------------------------------------------")
            parser.avanzar()
        else:
            print("Error: Comentario de bloque no cerrado correctamente.")
            print("-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", valor)