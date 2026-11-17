# Traemos el diccionario compartido desde datos.py.
# También traemos guardar_datos para que el alta quede guardada en el archivo JSON.
from datos import estudiantes, guardar_datos


# Registra un estudiante nuevo en el diccionario usando el DNI como clave.
def registrar_estudiante(dni, nombre, apellido):
    # Sacamos los espacios de sobra que pueda tener lo que se escribió.
    dni = dni.strip()
    nombre = nombre.strip()
    apellido = apellido.strip()

    # Ninguno de los tres datos puede quedar vacío.
    if dni == "" or nombre == "" or apellido == "":
        return (False, "Completá el DNI, el nombre y el apellido")

    # El DNI tiene que estar formado solo por números.
    if not dni.isdigit():
        return (False, "El DNI debe tener solo números")

    # El DNI tiene que tener 7 u 8 números.
    if len(dni) != 7 and len(dni) != 8:
        return (False, "El DNI debe tener 7 u 8 números")

    # No se puede registrar dos veces el mismo DNI.
    if dni in estudiantes:
        return (False, "Ya hay un estudiante registrado con ese DNI")

    # Guardamos el estudiante con la misma estructura que usa calificaciones.py:
    # nombre, apellido y un diccionario de materias vacío.
    estudiantes[dni] = {"nombre": nombre, "apellido": apellido, "materias": {}}
    guardar_datos()

    return (True, "Estudiante registrado")


# Busca estudiantes por DNI o por apellido y devuelve los que coincidan.
# (Se completa más adelante.)
def buscar_estudiante(termino):
    pass
