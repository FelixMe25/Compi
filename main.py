# ================================================================
# Proyecto Etapa 1 - Analizador Léxico (Scanner) 
# Estudiantes: María Félix Méndez Abarca - Mariana Fernández Martínez
# ================================================================

from moduloScanner.scanner import Scanner
from moduloScanner.muro import generar_muro
from moduloParser.parser import Parser 


def main():
    # Pedir el nombre del archivo al usuario
    archivo_fuente = input("Digite la ruta del archivo a analizar (ejemplo: Pruebas/Prueba-3-Sumar-flotantes.ne): ").strip()
    
    parser = Parser(archivo_fuente)
    parser.parse()
    try:
        # Inicialización del scanner
        s = Scanner()
        s.InicializarScanner(archivo_fuente)

        tokens = []  # Lista para almacenar tokens detectados

        # Inicialización de contadores
        contador_comentarios_linea = 0
        contador_comentarios_bloque = 0
        contador_palabras_reservadas = 0
        contador_identificadores = 0
        contador_literales = 0
        contador_errores = 0

        # Bucle principal de análisis
        while True:
            token = s.DemeToken()
            if token is None:
                break  # Fin del archivo
            print(">> TOKEN DETECTADO:", token)  # AGREGA ESTA LÍNEA
            tipo, lexema = token

            # Contabilizar comentarios aparte
            if tipo == "COMENTARIO":
                if lexema.startswith('$$'):
                    contador_comentarios_linea += 1
                elif lexema.startswith('$*'):
                    contador_comentarios_bloque += 1
            else:
                tokens.append(token)

                # Clasificación de tokens para el resumen
                if tipo == "PALABRA_RESERVADA":
                    contador_palabras_reservadas += 1
                elif tipo == "IDENTIFICADOR":
                    contador_identificadores += 1
                elif tipo.startswith("LITERAL_"):
                    contador_literales += 1
                elif tipo.startswith("ERROR"):
                    contador_errores += 1

        s.FinalizarScanner()

        # Resumen de estadísticas
        resumen = {
            "comentarios_linea": contador_comentarios_linea,
            "comentarios_bloque": contador_comentarios_bloque,
            "palabras_reservadas": contador_palabras_reservadas,
            "identificadores": contador_identificadores,
            "literales": contador_literales,
            "errores": contador_errores
        }

        # Generar el muro visual
        generar_muro(tokens, archivo_fuente, resumen)
        print("Muro generado en muro.html")
        print("Resumen:", resumen)

    except Exception as e:
        print("Error al generar el muro:", e)

# Punto de entrada del programa
if __name__ == "__main__":
    main()
