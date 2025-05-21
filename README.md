# Notch Engine - Analizador Léxico

> Este proyecto implementa un scanner (analizador léxico) y parser para el lenguaje Notch Engine, inspirado en Minecraft.
El analizador procesa un archivo de texto y genera un "muro visual" con los tokens detectados en el código fuente..

---

## ¿Cómo usarlo?

### 1. Prepara tu archivo de prueba
- Crea o edita un archivo de texto, por ejemplo: `prueba.txt`.
- Escribe el contenido en el lenguaje **Notch Engine** que deseas analizar.

### 2. Ejecuta el analizador
Abre una terminal o CMD, navega a la carpeta del proyecto y ejecuta:
```
python main.py
```

Luego, el programa te pedirá la ruta del archivo a analizar:

```
Digite la ruta del archivo a analizar:
```

Ejemplo de ruta simple:

```
Pruebas/Prueba-3-Sumar-flotantes.txt
```

### 3. Visualiza los resultados
- Se generará automáticamente un archivo llamado `muro.html`.
- Ábrelo en tu navegador favorito para ver los tokens **clasificados y coloreados**.


## Estructura del proyecto

| Archivo         | Descripción                                                             |
|-----------------|-------------------------------------------------------------------------|
| `scanner.py`    | Implementa el analizador léxico.                                        |
| `parser.py`     | Implementa el parser                                                    |
| `muro.py`       | Crea el muro visual (`muro.html`) con los resultados del análisis.      |
| `prueba.txt`    | Archivo de entrada con el código fuente a analizar.                     |
| `main.py`       | Ejecuta el scanner y genera el muro visual.                             |
| `muro.html`     | Archivo de salida: muro visual con los tokens analizados.               |
| `Ejemplos.txt`  | Contiene ejemplos básicos de código para practicar el análisis léxico.  |

---

##  Notas importantes

- No necesitas instalar librerías adicionales.
- Solo requieres **Python 3.8 o superior**.
- Compatible con Windows, Linux y Mac.
- Fácil de ejecutar desde terminal o CMD.

---

