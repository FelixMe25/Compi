# ================================================================
# GENERADOR DE MURO VISUAL - Brick Wall
# Conversión de tokens detectados a un muro HTML de ladrillos
# Estudiantes: María Félix Méndez Abarca - Mariana Fernández Martínez
# 
# Descripción:
# A partir de los tokens analizados, este programa crea un archivo 
# HTML que visualiza cada token como un ladrillo de color,
# clasificado por tipo y familia. Además, muestra estadísticas
# resumidas del análisis léxico realizado.
# ================================================================

from modulosScanner.scanner import TIPOS_TOKEN
from modulosScanner.familias import FAMILIAS_TOKEN

def generar_muro(tokens, nombre_archivo="archivo", resumen=None):
    if resumen is None:
        resumen = {}

    # Crear el archivo HTML
    with open("muro.html", "w", encoding="utf-8") as writer:
        # Escribir la estructura básica de HTML y estilos
        writer.write(f"""
        <html>
        <head>
        <title>Brick Wall - {nombre_archivo}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f9f9f9;
                padding: 20px;
            }}
            h1 {{
                text-align: center;
                font-style: italic;
                color: #2c3e50;
                font-size: 26px;
                margin-bottom: 25px;
            }}
            .estadisticas {{
                background: #ffffff;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                margin-bottom: 30px;
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 15px;
            }}
            .estadisticas-item {{
                background: #f0f8ff;
                border: 1px solid #cce7ff;
                border-radius: 8px;
                padding: 15px;
                min-width: 130px;
                text-align: center;
            }}
            .estadisticas-item b {{
                font-size: 14px;
                display: block;
                color: #34495e;
                margin-bottom: 6px;
            }}
            .estadisticas-item span {{
                font-size: 20px;
                color: #2c3e50;
                font-weight: bold;
            }}
            .token {{
                display: inline-flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                margin: 3px;
                padding: 6px;
                border-radius: 6px;
                text-align: center;
                box-shadow: 1px 1px 2px rgba(0,0,0,0.15);
                max-width: 300px;
                min-width: 120px;
                min-height: 50px;
                vertical-align: top;
                white-space: normal;
                overflow-wrap: break-word;
                font-size: 13px;
            }}
            .token small {{
                font-size: 10px;
                margin-top: 2px;
                color: #333;
            }}
            .sin-familia small {{
                color: green !important;
                font-style: italic;
            }}
            .error small {{
                color: red !important;
                font-style: italic;
            }}
        </style>
        </head>
        <body>
        <h1>Brick Wall – {nombre_archivo}</h1>

        <div class="estadisticas">
            <div class="estadisticas-item"><b>Total tokens</b><span>{len(tokens)}</span></div>
            <div class="estadisticas-item"><b>Reserved words</b><span>{resumen.get('palabras_reservadas', 0)}</span></div>
            <div class="estadisticas-item"><b>Identifiers</b><span>{resumen.get('identificadores', 0)}</span></div>
            <div class="estadisticas-item"><b>Literals</b><span>{resumen.get('literales', 0)}</span></div>
            <div class="estadisticas-item"><b>Errors</b><span>{resumen.get('errores', 0)}</span></div>
            <div class="estadisticas-item"><b>Line comments</b><span>{resumen.get('comentarios_linea', 0)}</span></div>
            <div class="estadisticas-item"><b>Block comments</b><span>{resumen.get('comentarios_bloque', 0)}</span></div>
        </div>
        """)

        # Escribir cada token como un ladrillo
        for tipo, lexema in tokens:
            color = TIPOS_TOKEN.get(tipo, "white")
            
            if tipo == "ERROR":
                contenido = f"{lexema}<br><small>Error</small>"
                extra_class = " error"

            elif tipo.startswith("LITERAL_"):
                familia = tipo.replace("LITERAL_", "Literal ").capitalize()
                contenido = f"{lexema}<br><small>{familia}</small>"
                extra_class = ""

            else:
                familia = FAMILIAS_TOKEN.get(lexema)
                if familia:
                    contenido = f"{lexema}<br><small>{familia}</small>"
                    extra_class = ""
                else:
                    contenido = f"{lexema}<br><small>Id</small>"
                    extra_class = " sin-familia"

            writer.write(f"<div class='token{extra_class}' style='background-color:{color};'>")
            writer.write(contenido)
            writer.write("</div>")

        # Cerrar etiquetas HTML
        writer.write("</body></html>")
