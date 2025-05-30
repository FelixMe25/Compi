from moduloParser.validaciones_semanticas import (validar_operacion_entera, 
                                                  validar_operacion_incremento_decremento,
                                                  validar_longitud_spider,
                                                  validar_acceso_spider,
                                                  validar_concatenacion_spider,
                                                  validar_seek_spider,
                                                  validar_corte_spider,
                                                  validar_recorte_spider, 
                                                  validar_operacion_caracter,
                                                  validar_operacion_logica,
                                                  validar_operacion_chest,
                                                  validar_operacion_archivo
                                                  )

# ------------------------------------------------------------------------------
# ASIGANACION COMPUESTA 
# ------------------------------------------------------------------------------
def procesar_asignacion_compuesta(parser):
        variable = parser.token_actual[1]
        parser.avanzar()  # Identificador

        operador = parser.token_actual[1]
        parser.avanzar()  # Operador compuesto

        valor = parser.token_actual[1]
        parser.avanzar()  # Valor literal o identificador

        if parser.token_actual[1] != ';':
            print(" Error: Se esperaba ';' al final de la asignación compuesta.")
            print(f"-----------------------------------------------------------------------")
            parser.saltar_hasta_puntoycoma()
            return

        parser.avanzar()  # ;
        print(f"---- Asignación compuesta detectada: {variable} {operador} {valor}")

# ------------------------------------------------------------------------------
# OPERACIONES DE ENTEROS
# ------------------------------------------------------------------------------
def _procesar_operaciones_enteros(parser):
        tipo, valor = parser.token_actual_tipo_valor()
        
        # Operación aritmética binaria: resultado = op1 + op2;
        if tipo == "IDENTIFICADOR":
            var_res = valor
            parser.avanzar()
            tipo_op1, op1 = parser.token_actual_tipo_valor()
            if tipo_op1 != "OPERADOR" or op1 != "=":
                print(f"Error: Se esperaba '=' después de '{var_res}'")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", op1)
                return
            parser.avanzar()

            tipo_izq, izq = parser.token_actual_tipo_valor()
            if tipo_izq not in ["IDENTIFICADOR", "LITERAL_ENTERO"]:
                print(f"Error: Se esperaba identificador o literal después de '='")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", izq)
                return
            parser.avanzar()

            tipo_operador, operador = parser.token_actual_tipo_valor()
            if tipo_operador != "OPERADOR" or operador not in ["+", "-", "*", "//", "%"]:
                print(f"Error: Operador '{operador}' inválido. Se esperaba +, -, *, // o %")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", operador)
                return
            parser.avanzar()

            tipo_der, der = parser.token_actual_tipo_valor()
            if tipo_der not in ["IDENTIFICADOR", "LITERAL_ENTERO"]:
                print(f"Error: Se esperaba identificador o literal después del operador")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", der)
                return
            parser.avanzar()

            # Validación semántica
    
            tabla_simbolos = parser.tabla
            if not validar_operacion_entera(tabla_simbolos, var_res, operador, izq, der):
                parser.actualizar_token("ERROR", var_res)
                parser.saltar_hasta_siguiente_instrucion()
                return

            tipo_fin, simb = parser.token_actual_tipo_valor()
            if tipo_fin == "SIMBOLO" and simb == ";":
                print(f"---- Operación válida: {var_res} = {izq} {operador} {der};")
                print(f"-----------------------------------------------------------------------")
                parser.avanzar()
            else:
                print(f"Error: Falta ';' al final de la operación")
                print("↪ Recuperación: saltando a la siguiente instrucción válida...")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", simb)
                parser.saltar_hasta_siguiente_instrucion() 
            return

## ------------------------------------------------------------------------------
# DECREMENTO Y INCREMENTO
# ------------------------------------------------------------------------------

def _procesar_incremento_decremento(parser, operador, tipo_dato_esperado):
    print(f"-----------------------------------------------------------------------")
    print(f"---- Operación unaria detectada: {operador}")
    parser.avanzar()

    tipo, identificador = parser.token_actual_tipo_valor()
    if tipo != "IDENTIFICADOR":
        print(f"Error: Se esperaba un identificador después de '{operador}' pero se encontró: {tipo}")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", identificador)
        parser.saltar_hasta_puntoycoma()
        return

    # Validación semántica
    tabla_simbolo = parser.tabla
    if not validar_operacion_incremento_decremento(tabla_simbolo, identificador, tipo_dato_esperado):
        parser.actualizar_token("ERROR", identificador)
        parser.saltar_hasta_puntoycoma()
        

    # simbolo = parser.tabla.obtener(identificador, buscar_en_padre=True)
    """
    if not simbolo:
        print(f"Error semántico: Variable '{identificador}' no ha sido declarada.")
        parser.actualizar_token("ERROR", identificador)
        parser.saltar_hasta_puntoycoma()
        return
    if simbolo["Tipo"] != tipo_dato_esperado:
        print(f"Error semántico: '{operador}' solo es válido para variables tipo '{tipo_dato_esperado}', no '{simbolo['Tipo']}'")
        parser.actualizar_token("ERROR", identificador)
        parser.saltar_hasta_puntoycoma()
        return
    """

    print(f"---- {operador} aplicado a: {identificador}")
    parser.avanzar()

    tipo, simbolo = parser.token_actual_tipo_valor()
    if tipo == "SIMBOLO" and simbolo == ";":
        print(f"----- Instrucción {operador} {identificador}; finalizada correctamente.")
    else:
        print(f"Error: Se esperaba ';' después de la instrucción {operador} {identificador}")
        parser.actualizar_token("ERROR", simbolo)

    parser.avanzar()
    print(f"-----------------------------------------------------------------------")

def procesar_operacion_incremento(parser):
    tipo, valor = parser.token_actual_tipo_valor()

    if tipo == "PALABRA_RESERVADA" and valor == "soulsand":
        parser.avanzar()
        tipo_var, var_name = parser.token_actual_tipo_valor()
        if tipo_var != "IDENTIFICADOR":
            print(f"Error: Se esperaba identificador después de 'soulsand'")
            parser.actualizar_token("ERROR", var_name)
            return
        parser.avanzar()
        tipo_simb, simb = parser.token_actual_tipo_valor()
        if tipo_simb != "SIMBOLO" or simb != ";":
            print(f"Error: Falta ';' luego de soulsand {var_name}")
            parser.actualizar_token("ERROR", simb)
        else:
            parser.avanzar()
        _procesar_incremento_decremento(parser, valor, "Stack")
        return

    if tipo == "PALABRA_RESERVADA" and valor == "soulsandf":
        parser.avanzar()
        tipo_var, var_name = parser.token_actual_tipo_valor()
        if tipo_var != "IDENTIFICADOR":
            print(f"Error: Se esperaba identificador después de 'soulsandf'")
            parser.actualizar_token("ERROR", var_name)
            return
        parser.avanzar()
        tipo_simb, simb = parser.token_actual_tipo_valor()
        if tipo_simb != "SIMBOLO" or simb != ";":
            print(f"Error: Falta ';' luego de soulsandf {var_name}")
            parser.actualizar_token("ERROR", simb)
        else:
            parser.avanzar()
        _procesar_incremento_decremento(parser, valor, "Ghast")
        return

def procesar_operacion_decremento(parser):
    tipo, valor = parser.token_actual_tipo_valor()

    if tipo == "PALABRA_RESERVADA" and valor == "magma":
        parser.avanzar()
        tipo_var, var_name = parser.token_actual_tipo_valor()
        if tipo_var != "IDENTIFICADOR":
            print(f"Error: Se esperaba identificador después de 'magma'")
            parser.actualizar_token("ERROR", var_name)
            return
        parser.avanzar()
        tipo_simb, simb = parser.token_actual_tipo_valor()
        if tipo_simb != "SIMBOLO" or simb != ";":
            print(f"Error: Falta ';' luego de magma {var_name}")
            parser.actualizar_token("ERROR", simb)
        else:
            parser.avanzar()
        _procesar_incremento_decremento(parser, valor, "Stack")
        return

    if tipo == "PALABRA_RESERVADA" and valor == "magmaf":
        parser.avanzar()
        tipo_var, var_name = parser.token_actual_tipo_valor()
        if tipo_var != "IDENTIFICADOR":
            print(f"Error: Se esperaba identificador después de 'magmaf'")
            parser.actualizar_token("ERROR", var_name)
            return
        parser.avanzar()
        tipo_simb, simb = parser.token_actual_tipo_valor()
        if tipo_simb != "SIMBOLO" or simb != ";":
            print(f"Error: Falta ';' luego de magmaf {var_name}")
            parser.actualizar_token("ERROR", simb)
        else:
            parser.avanzar()
        _procesar_incremento_decremento(parser, valor, "Ghast")
        return



# ------------------------------------------------------------------------------
#  OPERACIONES DE TIPO CARACTER 
# ------------------------------------------------------------------------------
def procesar_operacion_rune(parser):
        tipo, destino = parser.token_actual_tipo_valor()
        if tipo != "IDENTIFICADOR":
            print(f"Error: Se esperaba un identificador como destino.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", destino)
            parser.saltar_hasta_puntoycoma()
            return

        parser.avanzar()

        tipo, operador_igual = parser.token_actual_tipo_valor()
        if tipo != "OPERADOR" or operador_igual != "=":
            print(f"Error: Se esperaba '=' después del destino.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", operador_igual)
            parser.saltar_hasta_puntoycoma()
            return

        parser.avanzar()

        tipo, operacion = parser.token_actual_tipo_valor()
        if tipo not in ["OPERACION_ESDIGITO", "OPERACION_ESLETRA", "MAYUSCULA", "MINUSCULA"]:
            print(f"Error: '{operacion}' no es una operación válida de Rune.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", operacion)
            parser.saltar_hasta_puntoycoma()
            return

        parser.avanzar()

        tipo, argumento = parser.token_actual_tipo_valor()
        if tipo != "IDENTIFICADOR":
            print(f"Error: Se esperaba una variable Rune como argumento.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", argumento)
            parser.saltar_hasta_puntoycoma()
            return

        parser.avanzar()

        tipo, simbolo = parser.token_actual_tipo_valor()
        if tipo != "SIMBOLO" or simbolo != ";":
            print(f"Error: Se esperaba ';' al final de la operación Rune.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", simbolo)
            parser.saltar_hasta_puntoycoma()
            return
        
        # Validación semántica
        if not validar_operacion_caracter(parser.tabla, destino, operacion, argumento):
            parser.actualizar_token("ERROR", argumento)
            parser.saltar_hasta_puntoycoma()
            return

        parser.avanzar()
        print(f"---- Operación Rune detectada: {destino} = {operacion} {argumento};")

# ------------------------------------------------------------------------------
# OPERACIONES DE TIPO BOOL 
# ------------------------------------------------------------------------------
def procesar_operacion_torch(parser):
        tipo, destino = parser.token_actual_tipo_valor()
        if tipo != "IDENTIFICADOR":
            print(" Error: Se esperaba un identificador como destino de la operación Torch.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", destino)
            parser.saltar_hasta_puntoycoma()
            return
        parser.avanzar()

        tipo, igual = parser.token_actual_tipo_valor()
        if tipo != "OPERADOR" or igual != "=":
            print("Error: Se esperaba '=' en la asignación Torch.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", igual)
            parser.saltar_hasta_puntoycoma()
            return
        parser.avanzar()

        tipo, token = parser.token_actual_tipo_valor()

        # Caso NOT
        if tipo == "OPERADOR_LOGICO" and token == "not":
            parser.avanzar()
            tipo, abre = parser.token_actual_tipo_valor()
            if tipo != "SIMBOLO" or abre != "(":
                print(" Error: Se esperaba '(' después de 'not'.")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", abre)
                parser.saltar_hasta_puntoycoma()
                return
            parser.avanzar()

            _validar_operacion_booleana(interno=True)
            tipo, cierra = parser.token_actual_tipo_valor()
            if tipo != "SIMBOLO" or cierra != ")":
                print(" Error: Se esperaba ')' para cerrar la operación not().")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", cierra)
                parser.saltar_hasta_puntoycoma()
                return
            parser.avanzar()
            
        # Caso directo: A and B, A or B, A xor B
        else:
            _validar_operacion_booleana(interno=False)

        # Validar cierre con punto y coma
        tipo, final = parser.token_actual_tipo_valor()
        if tipo != "SIMBOLO" or final != ";":
            print("Error: Se esperaba ';' al final de la operación Torch.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", final)
            parser.saltar_hasta_puntoycoma()
            return

        print(f"--- Operación booleana Torch válida asignada a '{destino}'.")
        print(f"-----------------------------------------------------------------------")
        parser.avanzar()

# ------------------------------------------------------------------------------
# OPERACIONES DE TIPO STRING 
# ------------------------------------------------------------------------------
def procesar_operacion_spider(parser):
    tipo, destino = parser.token_actual_tipo_valor()
    if tipo != "IDENTIFICADOR":
        print("Error: Se esperaba un identificador como destino de la operación Spider.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", destino)
        parser.saltar_hasta_puntoycoma()
        return
    parser.avanzar()

    tipo, igual = parser.token_actual_tipo_valor()
    if tipo != "OPERADOR" or igual != "=":
        print("Error: Se esperaba '=' en la asignación Spider.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", igual)
        parser.saltar_hasta_puntoycoma()
        return
    parser.avanzar()

    # Validar si viene un '#' (LARGO_STRING) para operación largo = #saludo;
    tipo, token = parser.token_actual_tipo_valor()
    if tipo == "LARGO_STRING":
        parser.avanzar()
        tipo, spider = parser.token_actual_tipo_valor()
        if tipo != "IDENTIFICADOR":
            print("Error: Se esperaba un identificador después de '#' en operación Spider.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", spider)
            parser.saltar_hasta_puntoycoma()
            return
        parser.avanzar()
        tipo, fin = parser.token_actual_tipo_valor()
        if tipo != "SIMBOLO" or fin != ";":
            print("Error: Falta ';' en operación Spider con '#'.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", fin)
            parser.saltar_hasta_puntoycoma()
            return
        parser.avanzar()

        # Validación semántica 
        if not validar_longitud_spider(parser.tabla, spider, destino):
            parser.actualizar_token("ERROR", spider)
            return
        
        print(f"---- Operación Spider: {destino} = #{spider};")
        return

    # Caso normal: saludo bind, saludo seek, saludo from, etc.
    if tipo != "IDENTIFICADOR":
        print("Error: Se esperaba una Spider como origen de la operación.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", token)
        parser.saltar_hasta_puntoycoma()
        return

    spider = token
    parser.avanzar()
    tipo, operador = parser.token_actual_tipo_valor()

    if tipo not in [ "CONCATENAR_STRING", "BUSCAR_STRING", "CORTAR_STRING", "RECORTAR_STRING",
            "LITERAL_ARREGLO" ]:
        print(f"Error: Operador Spider inválido después de '{spider}': '{operador}'")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", operador)
        parser.saltar_hasta_puntoycoma()
        return

    if tipo == "LITERAL_ARREGLO":
        index = operador
        parser.avanzar()
        tipo, fin = parser.token_actual_tipo_valor()
        if tipo != "SIMBOLO" or fin != ";":
            print("Error: Se esperaba ';' después del acceso Spider.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", fin)
            parser.saltar_hasta_puntoycoma()
            return
        parser.avanzar()

        # Validación semántica
        if not validar_acceso_spider(parser.tabla, spider, index, destino):
            parser.actualizar_token("ERROR", index)
            return

        print(f"---- Operación Spider: {destino} = {spider}{index};")
        return

    if tipo in ["CONCATENAR_STRING", "BUSCAR_STRING"]:
        op = operador
        parser.avanzar()
        tipo, argumento = parser.token_actual_tipo_valor()
        if tipo not in ["IDENTIFICADOR", "LITERAL_STRING"]:
                print(f"Error: Se esperaba argumento válido para operación {op}.")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", argumento)
                parser.saltar_hasta_puntoycoma()
                return
        parser.avanzar()
        tipo, fin = parser.token_actual_tipo_valor()
        if tipo != "SIMBOLO" or fin != ";":
            print("Error: Falta ';' en operación Spider.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", fin)
            parser.saltar_hasta_puntoycoma()
            return
        parser.avanzar()

        # Validación semántica
        if op == "bind":
            if not validar_concatenacion_spider(parser.tabla, destino, spider, argumento):
                parser.actualizar_token("ERROR", argumento)
                return
        elif op == "seek":
            if not validar_seek_spider(parser.tabla, destino, spider, argumento):
                parser.actualizar_token("ERROR", argumento)
                return

        print(f"---- Operación Spider: {destino} = {spider} {op} {argumento};")
        return

    if tipo in ["CORTAR_STRING", "RECORTAR_STRING"]:
        op = operador
        parser.avanzar()
        tipo, inicio = parser.token_actual_tipo_valor()
        if tipo not in ["LITERAL_ENTERO", "IDENTIFICADOR"]:
            print(f"Error: Se esperaba un valor numérico válido como inicio después de '{op}', pero se encontró '{inicio}' ({tipo}).")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", inicio)
            parser.saltar_hasta_puntoycoma()
            return
        parser.avanzar()
        tipo, separador = parser.token_actual_tipo_valor()
        if tipo != "SEPARADOR_STRING_TERNARIO":
                print("Error: Se esperaba separador '##' en operación ternaria.")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", separador)
                parser.saltar_hasta_puntoycoma()
                return
        parser.avanzar()
        tipo, cantidad = parser.token_actual_tipo_valor()
        if tipo not in ["LITERAL_ENTERO", "IDENTIFICADOR"]:
                print(f"Error: Se esperaba una cantidad válida después de '##', pero se encontró '{cantidad}' ({tipo}).")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", cantidad)
                parser.saltar_hasta_puntoycoma()
                return
        parser.avanzar()
        tipo, fin = parser.token_actual_tipo_valor()
        if tipo != "SIMBOLO" or fin != ";":
                print("Error: Falta ';' al final de la operación Spider.")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", fin)
                parser.saltar_hasta_puntoycoma()
                return
        parser.avanzar()

        # Validación semántica
        if op == "from":
            if not validar_corte_spider(parser.tabla, destino, spider, inicio, cantidad):
                parser.actualizar_token("ERROR", cantidad)
                return
        elif op == "except":
            if not validar_recorte_spider(parser.tabla, destino, spider, inicio, cantidad):
                parser.actualizar_token("ERROR", cantidad)
                return
            
        print(f"---- Operación Spider: {destino} = {spider} {op} {inicio} ## {cantidad};")
        return

    print("Error: Estructura no reconocida como operación Spider.")
    print(f"-----------------------------------------------------------------------")
    parser.saltar_hasta_puntoycoma()

#--------------------------------------------------------
# VALIDACIÓN DE OPERACION BOLEANA
#----------------------------------------------------------

def _validar_operacion_booleana(parser, interno=False):
        # primer operando: literal o variable
        tipo, val = parser.token_actual_tipo_valor()
        if tipo not in ["IDENTIFICADOR", "LITERAL_BOOL"]:
            print(f" Error: Se esperaba literal booleano o identificador, pero se obtuvo '{val}'.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", val)
            parser.saltar_hasta_puntoycoma()
            return
        parser.avanzar()

        # operador lógico
        tipo, op = parser.token_actual_tipo_valor()
        if tipo != "OPERADOR_LOGICO" or op not in ["and", "or", "xor"]:
            print(f" Error: Se esperaba operador lógico válido (and/or/xor), pero se obtuvo '{op}'.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", op)
            parser.saltar_hasta_puntoycoma()
            return
        parser.avanzar()

        # segundo operando
        tipo, val2 = parser.token_actual_tipo_valor()
        if tipo not in ["IDENTIFICADOR", "LITERAL_BOOL"]:
            print(f" Error: Se esperaba literal booleano o identificador, pero se obtuvo '{val2}'.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", val2)
            parser.saltar_hasta_puntoycoma()
            return
        parser.avanzar()
        
        # ---- Validaciones Semánticas -------

        # ---- NOT -----------
        if not validar_operacion_logica(parser.tabla, val, "not"):
            parser.actualizar_token("ERROR", val)
            parser.saltar_hasta_puntoycoma()
            return
        parser.avanzar()

        # ---- OPERACIONES AND, OR, XOR -----------------
        if not validar_operacion_logica(parser.tabla, val, op, val2):
            parser.actualizar_token("ERROR", op)
            parser.saltar_hasta_puntoycoma()
            return
        parser.avanzar()


# ------------------------------------------------------------------------------
# OPERACIONES DE TIPO CONJUNTO
# ------------------------------------------------------------------------------
def procesar_operacion_chest(parser):
    tipo, destino = parser.token_actual_tipo_valor()
    if tipo != "IDENTIFICADOR":
        print("Error: Se esperaba un identificador como destino de la operación Chest.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", destino)
        parser.saltar_hasta_puntoycoma()
        return
    parser.avanzar()

    tipo, igual = parser.token_actual_tipo_valor()
    if tipo != "OPERADOR" or igual != "=":
        print("Error: Se esperaba '=' en la asignación Chest.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", igual)
        parser.saltar_hasta_puntoycoma()
        return
    parser.avanzar()

    tipo, origen = parser.token_actual_tipo_valor()
    if tipo != "IDENTIFICADOR":
        print("Error: Se esperaba identificador del conjunto origen.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", origen)
        parser.saltar_hasta_puntoycoma()
        return
    parser.avanzar()

    tipo, operador = parser.token_actual_tipo_valor()
    if tipo not in ["OPERADOR_AGREGAR", "OPERADOR_ELIMINAR", "OPERADOR_INSERCCION", "OPERADOR_PERTENENCIA"]:
        print(f"Error: Operador inválido para operación Chest: '{operador}'")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", operador)
        parser.saltar_hasta_puntoycoma()
        return
    parser.avanzar()

    tipo_argumento, argumento = parser.token_actual_tipo_valor()

    if tipo in ["OPERADOR_AGREGAR", "OPERADOR_ELIMINAR"]:
        if tipo_argumento != "LITERAL_CHAR":
            print(f"Error: Se esperaba un carácter en operación '{operador}'.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", argumento)
            parser.saltar_hasta_puntoycoma()
            return

    elif tipo in ["OPERADOR_INSERCCION", "OPERADOR_PERTENENCIA"]:
        if tipo_argumento != "IDENTIFICADOR":
            print(f"Error: Se esperaba un identificador de conjunto en operación '{operador}'.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", argumento)
            parser.saltar_hasta_puntoycoma()
            return
        parser.avanzar()

        tipo, fin = parser.token_actual_tipo_valor()
        if tipo != "SIMBOLO" or fin != ";":
            print("Error: Se esperaba ';' al final de la operación Chest.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", fin)
            parser.saltar_hasta_puntoycoma()
            return

    # Validación Semántica
    if not validar_operacion_chest(parser.tabla, operador, origen, argumento):
        parser.actualizar_token("ERROR", operador)
        return
    parser.avanzar()

    print(f"---- Operación Chest: {destino} = {origen} {operador} {argumento};")
    print(f"-----------------------------------------------------------------------")

# ------------------------------------------------------------------------------
# OPERACIONES DE PROCESAR CONSULTA CHEST
# ------------------------------------------------------------------------------
def procesar_consulta_chest(parser):
    tipo, valor = parser.token_actual_tipo_valor()
    # 'char' biom conjunto;
    if tipo == "LITERAL_CHAR":
        parser.avanzar()
        tipo, operador = parser.token_actual_tipo_valor()
        
        if tipo != "OPERADOR_BIOM":
            print("Error: Se esperaba 'biom' después del carácter.")
            print(f"-----------------------------------------------------------------------")
                
            parser.actualizar_token("ERROR", operador)
            parser.saltar_hasta_puntoycoma()
            return
        parser.avanzar()
            
        tipo, conjunto = parser.token_actual_tipo_valor()
        if tipo != "IDENTIFICADOR":
            print("Error: Se esperaba identificador de conjunto después de 'biom'.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", conjunto)
            parser.saltar_hasta_puntoycoma()
            return
        parser.avanzar()
        
        tipo, fin = parser.token_actual_tipo_valor()
        if tipo != "SIMBOLO" or fin != ";":
            print(" Error: Falta ';' en consulta biom.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", fin)
            parser.saltar_hasta_puntoycoma()
            return
        
        # Validación Semántica
        if not validar_operacion_chest(parser.tabla, operador, valor, conjunto):
            parser.actualizar_token("ERROR", operador)
            return
        
        parser.avanzar()
        print(f"---- Consulta Chest: {valor} biom {conjunto};")
        print(f"-----------------------------------------------------------------------")
        return

    # void conjunto;
    elif tipo == "OPERADOR_VACIO":
        parser.avanzar()
        tipo, conjunto = parser.token_actual_tipo_valor()
        if tipo != "IDENTIFICADOR":
            print("Error: Se esperaba identificador de conjunto después de 'void'.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", conjunto)
            parser.saltar_hasta_puntoycoma()
            return
        parser.avanzar()
        tipo, fin = parser.token_actual_tipo_valor()
        if tipo != "SIMBOLO" or fin != ";":
            print("Error: Falta ';' al final de consulta void.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", fin)
            parser.saltar_hasta_puntoycoma()
            return
        
        # Validación Semántica
        if not validar_operacion_chest(parser.tabla, "void", conjunto, None):
            parser.actualizar_token("ERROR", "void")
            return
        
        parser.avanzar()
        print(f"✔ Consulta Chest: void {conjunto};")
        return
    
# ----------------------------------------------------------------------------
# OPERACIONES SOBRE TIPO DE DATO ARCHIVO
# ------------------------------------------------------------------------------
def procesar_operacion_archivo(parser):
    tipo, operacion = parser.token_actual_tipo_valor()
    if tipo not in ["ABRIR_ARCHIVO", "CERRAR_ARCHIVO", "CREAR_ARCHIVO"]:
        print(f"Error: Operación de archivo inválida: '{operacion}'")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", operacion)
        parser.saltar_hasta_puntoycoma()
        return

    parser.avanzar()
    tipo, archivo = parser.token_actual_tipo_valor()
    if tipo != "IDENTIFICADOR":
        print(f"Error: Se esperaba el nombre del archivo para '{operacion}'.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", archivo)
        parser.saltar_hasta_puntoycoma()
        return

    parser.avanzar()
    tipo, simbolo = parser.token_actual_tipo_valor()
    if tipo != "SIMBOLO" or simbolo != ";":
        print(f"Error: Se esperaba ';' al final de la operación {operacion}.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", simbolo)
        parser.saltar_hasta_puntoycoma()
        return
    
    # ---------- Validación Semántica -------------------
    print("--------- VALIDACION SEMANTICA ----------------- ")
    if not validar_operacion_archivo(parser.tabla, operacion, archivo):
        parser.actualizar_token("ERROR", archivo)
        return

    parser.avanzar()
    print(f"---- Operación archivo: {operacion} {archivo};")
    print(f"-----------------------------------------------------------------------")

# ------------------------------------------------------------------------------
# LECTURA DE ARCHIVOS
# ------------------------------------------------------------------------------
def procesar_asignacion_archivo(parser):
    tipo, destino = parser.token_actual_tipo_valor()
    if tipo != "IDENTIFICADOR":
        print("Error: Se esperaba un identificador como destino.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", destino)
        parser.saltar_hasta_puntoycoma()
        return

    parser.avanzar()
    
    tipo, igual = parser.token_actual_tipo_valor()
    if tipo != "OPERADOR" or igual != "=":
        print("Error: Se esperaba '=' en la asignación de lectura de archivo.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", igual)
        parser.saltar_hasta_puntoycoma()
        return

    parser.avanzar()
    tipo, op = parser.token_actual_tipo_valor()
    if tipo != "LEER_ARCHIVO":
        print("Error: Se esperaba la operación 'gather'.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", op)
        parser.saltar_hasta_puntoycoma()
        return

    parser.avanzar()
    tipo, archivo = parser.token_actual_tipo_valor()
    if tipo != "IDENTIFICADOR":
        print("Error: Se esperaba identificador del archivo para gather.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", archivo)
        parser.saltar_hasta_puntoycoma()
        return

    parser.avanzar()
        
    tipo, fin = parser.token_actual_tipo_valor()
    if tipo != "SIMBOLO" or fin != ";":
        print("Error: Falta ';' al final de gather.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", fin)
        parser.saltar_hasta_puntoycoma()
        return
    
    # ---------- Validación Semántica -------------------
    if not validar_operacion_archivo(parser.tabla, op, destino, archivo):
        parser.actualizar_token("ERROR", archivo)
        return

    parser.avanzar()
    print(f"---- Lectura desde archivo: {destino} = gather {archivo};")
    print(f"-----------------------------------------------------------------------")

# ------------------------------------------------------------------------------
# ESCRITURA DE ARCHIVOS
# ------------------------------------------------------------------------------
def procesar_escritura_archivo(parser):
    tipo, archivo = parser.token_actual_tipo_valor()
    if tipo != "IDENTIFICADOR":
        print("Error: Se esperaba nombre de archivo para forge.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", archivo)
        parser.saltar_hasta_puntoycoma()
        return

    parser.avanzar()

    tipo, operacion = parser.token_actual_tipo_valor()
    if tipo != "ESCRIBIR_ARCHIVO":
        print("Error: Se esperaba operador 'forge'.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", operacion)
        parser.saltar_hasta_puntoycoma()
        return

    parser.avanzar()
        
    tipo, contenido = parser.token_actual_tipo_valor()
    if tipo not in ["IDENTIFICADOR", "LITERAL_STRING"]:
        print("Error: Se esperaba contenido válido para forge.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", contenido)
        parser.saltar_hasta_puntoycoma()
        return

    parser.avanzar()
        
    tipo, fin = parser.token_actual_tipo_valor()
    if tipo != "SIMBOLO" or fin != ";":
        print("Error: Falta ';' al final de forge.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", fin)
        parser.saltar_hasta_puntoycoma()
        return
    
    # ---------- Validación Semántica -------------------
    print("--------- VALIDACION SEMANTICA ----------------- ")
    if not validar_operacion_archivo(parser.tabla, operacion, archivo, contenido):
        parser.actualizar_token("ERROR", archivo)
        parser.saltar_hasta_puntoycoma()
        return

    parser.avanzar()
    print(f"---- Escritura en archivo: {archivo} forge {contenido};")
    print(f"-----------------------------------------------------------------------")

# ------------------------------------------------------------------------------
# OPERACIONES DE FLOTANTES
# ------------------------------------------------------------------------------
def _procesar_operaciones_ghast(parser):
    tipo, destino = parser.token_actual_tipo_valor()
    parser.avanzar()

    tipo, igual = parser.token_actual_tipo_valor()
    if tipo != "OPERADOR" or igual != "=":
        print("Error: Se esperaba '=' en la operación Ghast.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", igual)
        parser.saltar_hasta_puntoycoma()
        return
    parser.avanzar()

    tipo_izq, izq = parser.token_actual_tipo_valor()
    if tipo_izq not in ["IDENTIFICADOR", "LITERAL_FLOAT"]:
        print(f"Error: Se esperaba identificador o literal float a la izquierda.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", izq)
        parser.saltar_hasta_puntoycoma()
        return
    parser.avanzar()

    tipo_op, op = parser.token_actual_tipo_valor()
    if tipo_op != "OPERADOR_FLOAT" or op not in [":+", ":-", ":*", "://", ":%"]:
        print(f" Error: Operador flotante inválido: {op}")
        parser.actualizar_token("ERROR", op)
        print(f"-----------------------------------------------------------------------")
        parser.saltar_hasta_puntoycoma()
        return
    parser.avanzar()

    tipo_der, der = parser.token_actual_tipo_valor()
    if tipo_der not in ["IDENTIFICADOR", "LITERAL_FLOAT"]:
        print(f"Error: Se esperaba identificador o literal float a la derecha.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", der)
        parser.saltar_hasta_puntoycoma()
        return
    parser.avanzar()

    tipo_fin, simbolo = parser.token_actual_tipo_valor()
    if tipo_fin != "SIMBOLO" or simbolo != ";":
        print("Error: Se esperaba ';' al final de la operación Ghast.")
        print(f"-----------------------------------------------------------------------")
        parser.actualizar_token("ERROR", simbolo)
        parser.saltar_hasta_puntoycoma()
        return

    parser.avanzar()
    print(f"---- Operación Ghast válida: {destino} = {izq} {op} {der};")
    print(f"-----------------------------------------------------------------------")

# ------------------------------------------------------------------------------
# OPERACIONES DE REGISTROS
# ------------------------------------------------------------------------------
def procesar_entity_en_inventory(parser):
    print("➡ Iniciando definición de Entity dentro del Inventory")
    parser.avanzar()
    campos = []
    while not parser.fin():
        tipo, tipo_dato = parser.token_actual_tipo_valor()

        if tipo == "PALABRA_RESERVADA" and tipo_dato == "kill":
            break  # se detecta final de Entity con 'kill'

        if not tipo.startswith("TIPO_"):
            print(f"Error: Se esperaba un tipo de campo dentro de Entity, se encontró: {tipo_dato}")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", tipo_dato)
            parser.saltar_hasta_puntoycoma()
            continue

        parser.avanzar()
            
        tipo_id, nombre_campo = parser.token_actual_tipo_valor()
        if tipo_id != "IDENTIFICADOR":
            print(f"Error: Se esperaba identificador para campo de Entity.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", nombre_campo)
            parser.saltar_hasta_puntoycoma()
            continue

        parser.avanzar()
            
        tipo_fin, simbolo = parser.token_actual_tipo_valor()
        if tipo_fin != "SIMBOLO" or simbolo != ";":
            print(f"Error: Se esperaba ';' después del campo de Entity.")
            print(f"-----------------------------------------------------------------------")
            parser.actualizar_token("ERROR", simbolo)
            parser.saltar_hasta_puntoycoma()
            continue

        print(f"---- Campo de Entity: {tipo_dato} {nombre_campo};")
        print(f"-----------------------------------------------------------------------")
        campos.append((tipo_dato, nombre_campo))
        parser.avanzar()

        # Detectar el cierre con `kill <nombre>;`
        tipo, palabra = parser.token_actual_tipo_valor()
        if tipo == "PALABRA_RESERVADA" and palabra == "kill":
            parser.avanzar()
            tipo, nombre_entity = parser.token_actual_tipo_valor()
            if tipo != "IDENTIFICADOR":
                print("Error: Se esperaba el nombre del Entity luego de 'kill'")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", nombre_entity)
                return

            parser.avanzar()
            tipo, simb = parser.token_actual_tipo_valor()
            if tipo == "SIMBOLO" and simb == ";":
                print(f"✔ Entity definido correctamente: {nombre_entity} con campos: {len(campos)}\n")
                print(f"-----------------------------------------------------------------------")
                parser.avanzar()
            else:
                print("Error: Falta ';' luego de kill <nombre>")
                print(f"-----------------------------------------------------------------------")
                parser.actualizar_token("ERROR", simb)