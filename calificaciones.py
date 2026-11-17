from datos import estudiantes, guardar_datos
def _obtener_estudiante(dni):
    return estudiantes.get(dni)

def cargar_nota(dni, materia, nota):
    estudiante = _obtener_estudiante(dni)
    if estudiante is None:
        return {"error": "Error: no existe un estudiante con ese DNI."}
    if not materia or not materia.strip():
        return {"error": "Error: debe ingresar una materia."}
    materia = materia.strip()
    try:
        nota = float(nota)
    except (ValueError, TypeError):
        return {"error": "Error: la nota debe ser un número."}
    if nota < 1 or nota > 10:
        return {"error": "Error: la nota debe estar entre 1 y 10."}
    materias = estudiante.setdefault("materias", {})
    if materia not in materias:
        materias[materia] = []
    materias[materia].append(nota)
    guardar_datos()
    return {"message": "Nota cargada correctamente."}

def calcular_promedio(dni):
    estudiante = _obtener_estudiante(dni)
    if estudiante is None:
        return {"error": "Error: no existe un estudiante con ese DNI."}
    materias = estudiante.get("materias", {})
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
        suma_total += suma
        cantidad_total += cantidad
    if cantidad_total == 0:
        return {"error": "El estudiante todavía no tiene notas cargadas."}
    promedio_general = suma_total / cantidad_total
    return {
        "promedios_materias": promedios_materias,
        "promedio_general": round(promedio_general, 2)
    }

def obtener_historial(dni):
    estudiante = _obtener_estudiante(dni)
    if estudiante is None:
        return {"error": "Error: no existe un estudiante con ese DNI."}
    materias = estudiante.get("materias", {})
    if not materias:
        return {"error": "El estudiante todavía no tiene materias cargadas."}
    return {
        "nombre": estudiante["nombre"],
        "apellido": estudiante["apellido"],
        "materias": materias
    }
