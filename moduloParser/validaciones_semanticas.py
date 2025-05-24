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
        tabla_simbolos.agregar(nombre_variable, 
                               tipo_variable, clase="variable", 
                               inicializado=inicializado, 
                               info={"valor_inicializacion": valor_inicializacion})

        print("-------- VALIDACIÓN SEMÁNTICA -------------------------")
        print(f"---- Variable '{nombre_variable}' de tipo '{tipo_variable}' declarada correctamente.")
        return True


def validar_declaracion_constante(tabla_simbolos, nombre_variable, tipo_variable, inicializado=False, valor_inicializacion=None):
    if tabla_simbolos.existe(nombre_variable):
        print(f"Error semántico: La constante '{nombre_variable}' ya ha sido declarada.")
        return False
    else:
        # Usar la nueva función 'agregar' de la Tabla de Símbolos
        tabla_simbolos.agregar(nombre_variable, 
                               tipo_variable, clase="variable", 
                               inicializado=inicializado, 
                               info={"valor_inicializacion": valor_inicializacion})
        
        print("-------- VALIDACIÓN SEMÁNTICA -------------------------")
        print(f"---- Variable '{nombre_variable}' de tipo '{tipo_variable}' declarada correctamente.")
        return True

"""
Valida la declaración de una variable de tipo Shelf.

Args:
    tabla_simbolos (TablaSimbolos): La tabla de símbolos actual.
    nombre_variable (str): El nombre de la variable Shelf que se está declarando.
    tipo_base_shelf (str): El tipo base de los elementos del Shelf (e.g., "ENTERO", "STRING").
    valor_inicializacion (any): El valor con el que se inicializa el Shelf (debe ser un literal de arreglo).

Returns:
    bool: True si la declaración es válida, False si hay un error.
"""
def validar_variable_shelf(tabla_simbolos, nombre_variable, tipo_base_shelf, valor_inicializacion):
  if tabla_simbolos.existe(nombre_variable):
     print(f"Error semántico: El arreglo Shelf '{nombre_variable}' ya ha sido declarado.")
     return False
  else:
     tabla_simbolos.agregar(
       nombre_variable,
       "TIPO_ARREGLOS", # Tipo genérico para Shelf
       clase="variable",
       inicializado=True, # Shelf siempre se inicializa
       info={
         "tipo_base_shelf": tipo_base_shelf,
         "valor_inicializacion": valor_inicializacion,
         "es_arreglo_shelf": True  # Marcador para Shelf
       }
     )
     print("-------- VALIDACIÓN SEMÁNTICA -------------------------")
     print(f"---- Arreglo Shelf '{nombre_variable}' de tipo '{tipo_base_shelf}' declarado e inicializado correctamente.")
     return True




def validar_tipo_dato_entero(tipo_dato):
    if tipo_dato != "Stack":
        return False
    print(f"---- Tipo '{tipo_dato}' declarado correctamente.")
    return True
