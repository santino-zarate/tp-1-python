# Traemos el diccionario compartido desde datos.py.
# También traemos guardar_datos para que el alta quede guardada en el archivo JSON.
from datos import estudiantes, guardar_datos

# Traemos unicodedata, que nos sirve para sacar los acentos al buscar.
import unicodedata


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


# Saca los acentos de un texto y lo pasa a minúsculas, para poder comparar
# sin distinguir mayúsculas ni tildes (así "Pérez" y "perez" quedan iguales).
def normalizar(texto):
    # "NFD" separa cada letra de su acento, y después borramos los acentos.
    texto_separado = unicodedata.normalize("NFD", texto)
    letras = ""
    for letra in texto_separado:
        if unicodedata.category(letra) != "Mn":
            letras += letra
    return letras.lower()


# Busca estudiantes por DNI exacto o por apellido (coincidencia parcial,
# sin importar mayúsculas ni acentos).
def buscar_estudiante(termino):
    # Sacamos los espacios de sobra del texto que se escribió.
    termino = termino.strip()

    # Si no escribieron nada, avisamos que falta el dato.
    if termino == "":
        return (False, "Ingresá un DNI o un apellido")

    # Preparamos el texto una sola vez, sin acentos y en minúsculas.
    buscado = normalizar(termino)
    resultados = []

    # Recorremos todos los estudiantes y nos quedamos con los que coinciden.
    for dni, datos in estudiantes.items():
        if termino.isdigit():
            # Si escribieron números, buscamos ese DNI exacto.
            coincide = (dni == termino)
        else:
            # Si escribieron letras, buscamos que el apellido contenga el texto.
            coincide = (buscado in normalizar(datos["apellido"]))

        # Si coincide, lo agregamos a la lista con los datos que se muestran.
        if coincide:
            resultados.append({
                "dni": dni,
                "nombre": datos["nombre"],
                "apellido": datos["apellido"]
            })

    # La lista puede volver vacía: eso no es un error, es que no hubo coincidencias.
    return (True, resultados)
