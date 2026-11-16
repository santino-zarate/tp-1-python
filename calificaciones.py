# Traemos el diccionario compartido desde datos.py.
from datos import estudiantes


# Carga una nota en la materia indicada del estudiante.
def cargar_nota(dni, materia, nota):

    # Verificamos que el estudiante exista.
    if dni not in estudiantes:
        return "Error: no existe un estudiante con ese DNI."

    # Verificamos que se haya ingresado una materia.
    if not materia or not materia.strip():
        return "Error: debe ingresar una materia."

    materia = materia.strip()

    # Intentamos convertir la nota a un número.
    try:
        nota = float(nota)
    except (ValueError, TypeError):
        return "Error: la nota debe ser un número."

    # Verificamos que la nota esté entre 1 y 10.
    if nota < 1 or nota > 10:
        return "Error: la nota debe estar entre 1 y 10."

    # Si el estudiante todavía no tiene materias, creamos el diccionario.
    if "materias" not in estudiantes[dni]:
        estudiantes[dni]["materias"] = {}

    # Si la materia todavía no existe, creamos una lista vacía.
    if materia not in estudiantes[dni]["materias"]:
        estudiantes[dni]["materias"][materia] = []

    # Agregamos la nota a la lista de esa materia.
    estudiantes[dni]["materias"][materia].append(nota)

    return "Nota cargada correctamente."



# Calcula el promedio de todas las notas del estudiante.
# (Se completa más adelante.)
def calcular_promedio(dni):
    pass


# Devuelve el historial del estudiante: todas sus materias con sus notas.
# (Se completa más adelante.)
def obtener_historial(dni):
    pass
