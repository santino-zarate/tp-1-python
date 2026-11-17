from datos import estudiantes, guardar_datos
from datetime import datetime
import unicodedata

def _validar_nombre_apellido(nombre, apellido):
    return bool(nombre.strip() and apellido.strip())


def registrar_estudiante(dni, nombre, apellido, fecha_nacimiento, año_ingreso):
    dni = dni.strip()
    nombre = nombre.strip()
    apellido = apellido.strip()
    fecha_nacimiento = fecha_nacimiento.strip()
    año_ingreso = año_ingreso.strip()

    if not dni or not _validar_nombre_apellido(nombre, apellido) or not fecha_nacimiento or not año_ingreso:
        return (False, "Completá todos los campos")

    if not dni.isdigit():
        return (False, "El DNI debe tener solo números")

    if len(dni) != 7 and len(dni) != 8:
        return (False, "El DNI debe tener 7 u 8 números")

    if dni in estudiantes:
        return (False, "Ya hay un estudiante registrado con ese DNI")

    try:
        datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
    except ValueError:
        return (False, "La fecha debe tener el formato DD/MM/AAAA")

    if not año_ingreso.isdigit() or len(año_ingreso) != 4:
        return (False, "El año de ingreso debe tener 4 números")

    estudiantes[dni] = {
        "nombre": nombre,
        "apellido": apellido,
        "fecha_nacimiento": fecha_nacimiento,
        "año_ingreso": año_ingreso,
        "materias": {}
    }
    guardar_datos()
    return (True, "Estudiante registrado")


def eliminar_estudiante(dni):
    dni = dni.strip()
    if dni not in estudiantes:
        return (False, "No existe un estudiante con ese DNI")

    del estudiantes[dni]
    guardar_datos()
    return (True, "Estudiante eliminado")

def editar_estudiante(dni, nombre, apellido):
    dni = dni.strip()
    if dni not in estudiantes:
        return (False, "No existe un estudiante con ese DNI")

    nombre = nombre.strip()
    apellido = apellido.strip()
    if not _validar_nombre_apellido(nombre, apellido):
        return (False, "Complet\u00e1 nombre y apellido")

    estudiantes[dni]["nombre"] = nombre
    estudiantes[dni]["apellido"] = apellido
    guardar_datos()
    return (True, "Estudiante actualizado")

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
