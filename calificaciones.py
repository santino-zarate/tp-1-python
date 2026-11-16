# Traemos el diccionario compartido desde datos.py.
from datos import estudiantes

# Carga una nota en la materia indicada del estudiante.
def cargar_nota(dni, materia, nota):
    if dni not in estudiantes:
        return "Error: no existe un estudiante con ese DNI."

    if not materia or not materia.strip():
        return "Error: debe ingresar una materia."

    materia = materia.strip()
    try:
        nota = float(nota)
    except (ValueError, TypeError):
        return "Error: la nota debe ser un número."

    if nota < 1 or nota > 10:
        return "Error: la nota debe estar entre 1 y 10."

    if "materias" not in estudiantes[dni]:
        estudiantes[dni]["materias"] = {}

    if materia not in estudiantes[dni]["materias"]:
        estudiantes[dni]["materias"][materia] = []

    estudiantes[dni]["materias"][materia].append(nota)
    return "Nota cargada correctamente."

# Calcula el promedio de todas las notas del estudiante.
def calcular_promedio(dni):
    if dni not in estudiantes:
        return {"error": "No existe un estudiante con ese DNI."}

    materias = estudiantes[dni].get("materias", {})
    promedios_materias = {}
    suma_total = 0
    cantidad_total = 0

    for materia, notas in materias.items():
        if len(notas) == 0:
            continue
        suma = sum(notas)
        cantidad = len(notas)
        promedio = suma / cantidad
        promedios_materias[materia] = round(promedio, 2)
        suma_total = suma_total + suma
        cantidad_total = cantidad_total + cantidad
        
    if cantidad_total == 0:
        return {"error": "El estudiante todavía no tiene notas cargadas."}

    promedio_general = suma_total / cantidad_total

    return {
        "promedios_materias": promedios_materias,
        "promedio_general": round(promedio_general, 2)
    }


# Devuelve el historial del estudiante: todas sus materias con sus notas.
def obtener_historial(dni):
    if dni not in estudiantes:
        return {"error": "No existe un estudiante con ese DNI."}
    estudiante = estudiantes[dni]
    materias = estudiante.get("materias", {})
    if not materias:
        return {"error": "El estudiante todavía no tiene materias cargadas."}
    return {
        "nombre": estudiante["nombre"],
        "apellido": estudiante["apellido"],
        "materias": materias
    }
