import os

# CONFIGURACIÓN: Solo vamos a mirar dentro de la carpeta 'app' y el 'main.py'
# Esto evitará que lea 'venv', '.env', y archivos basura de git.
INCLUDE_DIRS = ['app']
INCLUDE_FILES = ['main.py']
OUTPUT_FILENAME = 'contexto-formulario-backned.md'

with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as outfile:
    # 1. Escribimos un pequeño encabezado
    outfile.write("CONTENIDO DEL PROYECTO\n\n")

    # 2. Buscamos en las carpetas permitidas
    for target in INCLUDE_DIRS + INCLUDE_FILES:
        if not os.path.exists(target):
            continue
            
        for root, dirs, files in os.walk(target) if os.path.isdir(target) else [(os.path.dirname(target), [], [os.path.basename(target)])]:
            for file in sorted(files):
                if file.endswith(('.py', '.html', '.css', '.js')):
                    path = os.path.join(root, file)
                    print(f"Incluyendo: {path}")
                    outfile.write(f"\n--- FILE: {path} ---\n\n```python\n")
                    try:
                        with open(path, 'r', encoding='utf-8', errors='ignore') as infile:
                            outfile.write(infile.read())
                    except Exception as e:
                        outfile.write(f"Error: {e}")
                    outfile.write("\n```\n")

print(f"\n¡Listo! Revisa el archivo '{OUTPUT_FILENAME}'")