# Diccionario compartido con todos los estudiantes del sistema.
# La clave es el DNI (string) y el valor es otro diccionario con
# nombre, apellido y materias (cada materia con su lista de notas).
# Ejemplo:
# {"40123456": {"nombre": "Ana", "apellido": "Pérez", "materias": {"Matemática": [8, 7]}}}
# Va en un archivo aparte para que los demás módulos lo importen sin imports circulares.
estudiantes = {}
