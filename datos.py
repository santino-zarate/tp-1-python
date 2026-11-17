import json
from pathlib import Path
estudiantes = {}
ARCHIVO = Path(__file__).with_name("estudiantes.json")
def cargar_datos():
    if ARCHIVO.exists():
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            estudiantes.clear()
            estudiantes.update(datos)
def guardar_datos():
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(estudiantes, archivo, indent=4, ensure_ascii=False)
cargar_datos()
