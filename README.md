# Notch Engine - Scanner, Parser y Analizador Semántico

> Implementa un **scanner** (analizador léxico), un **parser** (analizador sintáctico) y un **analizador semántico** para el lenguaje Notch Engine, inspirado en Minecraft.
> El sistema procesa archivos fuente, genera tokens, construye y muestra la tabla de símbolos, y valida operaciones y tipos. Además, produce un “muro visual” (`muro.html`) con los tokens clasificados y coloreados.

---

## Tabla de Contenidos

- [Requisitos](#requisitos)
- [¿Cómo usarlo?](#cómo-usarlo)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Notas importantes](#notas-importantes)
- [Créditos](#créditos)

---

## Requisitos

- **Python 3.8 o superior**
- No necesitas instalar librerías adicionales.
- Compatible con Windows, Linux y Mac.

---

## ¿Cómo usarlo?

1. **Prepara tu archivo de prueba**
   - Crea o edita un archivo de texto, por ejemplo: `prueba.ne`.
   - Escribe el código en el lenguaje **Notch Engine** que deseas analizar.

2. **Ejecuta el analizador**
   - Abre una terminal o CMD, navega a la carpeta del proyecto y ejecuta:
     ```
     python main.py
     ```
   - El programa te pedirá la ruta del archivo a analizar:
     ```
     Digite la ruta del archivo a analizar:
     ```
   - Ejemplo de ruta:
     ```
     Pruebas/Prueba-3-Sumar-flotantes.txt
     ```

3. **Visualiza los resultados**
   - Se generará automáticamente un archivo llamado `muro.html`.
   - Ábrelo en tu navegador favorito para ver los tokens **clasificados y coloreados**.
   - El programa también mostrará la **tabla de símbolos** después de cada instrucción y validará operaciones, tipos y estructuras del lenguaje.

---

## Estructura del proyecto

| Archivo/Carpeta         | Descripción                                                        |
|-------------------------|--------------------------------------------------------------------|
| `main.py`               | Ejecuta el scanner, parser y analizador semántico.                 |
| `moduloScanner/`        | Contiene el scanner (analizador léxico) y utilidades de tokens.    |
| `moduloParser/`         | Contiene el parser, validaciones semánticas y manejo de símbolos.  |
| `muro.html`             | Archivo de salida: muro visual con los tokens analizados.          |
| `prueba.txt`            | Archivo de entrada con el código fuente a analizar.                |
| `Ejemplos.txt`          | Ejemplos de código para practicar el análisis léxico y sintáctico.  |

---

## Notas importantes

- El **scanner** detecta y clasifica los tokens del código fuente.
- El **parser** analiza la estructura sintáctica y construye la tabla de símbolos.
- El **analizador semántico** valida tipos, operaciones y el uso correcto de variables, arreglos, registros, etc.
- El “muro visual” (`muro.html`) muestra los tokens detectados, su tipo y color para facilitar el análisis.
- El sistema imprime la **tabla de símbolos** después de cada instrucción en el punto de entrada (`SpawnPoint`).
- El proyecto es educativo y puede ampliarse para soportar más características del lenguaje.

