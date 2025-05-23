"""
Valida la declaración de una variable.

Args:
    tabla_simbolos (TablaSimbolos): La tabla de símbolos actual.
    nombre_variable (str): El nombre de la variable que se está declarando.
    tipo_variable (str): El tipo de la variable.
    inicializado (bool, optional): Indica si la variable se inicializa en la declaración.
                                    Defaults to False.
    valor_inicializacion (any, optional): El valor con el que se inicializa la variable (si aplica).
                                          Defaults to None.

Returns:
bool: True si la declaración es válida, False si hay un error.
"""
def validar_declaracion_variable(tabla_simbolos, nombre_variable, tipo_variable, inicializado=False, valor_inicializacion=None):
    if tabla_simbolos.existe(nombre_variable):
        print(f"Error semántico: La variable '{nombre_variable}' ya ha sido declarada.")
        return False
    else:
        # Usar la nueva función 'agregar' de la Tabla de Símbolos
        tabla_simbolos.agregar(nombre_variable, tipo_variable, clase="variable", inicializado=inicializado, info={"valor_inicializacion": valor_inicializacion})

        print(f"---- Variable '{nombre_variable}' de tipo '{tipo_variable}' declarada correctamente.")
        return True

def validar_tipo_dato_entero(tipo_dato):
    if tipo_dato != "Stack":
        return False
    print(f"---- Tipo '{tipo_dato}' declarado correctamente.")
    return True
