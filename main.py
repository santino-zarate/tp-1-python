import tkinter as tk
import estudiantes
import calificaciones

# Abre una ventana secundaria con el título de la sección y el aviso "En construcción".
def abrir_ventana(titulo):
    ventana = tk.Toplevel()
    ventana.title(titulo)
    tk.Label(ventana, text="En construcción").pack(padx=40, pady=30)

# Sección 1: acá después se va a llamar a estudiantes.registrar_estudiante().
def abrir_registro():
    abrir_ventana("Registrar estudiante")

# Sección 2: acá después se va a llamar a estudiantes.buscar_estudiante().
def abrir_busqueda():
    abrir_ventana("Buscar estudiante")

def abrir_calificaciones():
    ventana = tk.Toplevel()
    ventana.title("Cargar materias y calificaciones")
    ventana.geometry("400x350")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Cargar calificación",
             font=("Arial", 14, "bold")).pack(pady=15)

    tk.Label(ventana, text="DNI del estudiante:").pack()
    entrada_dni = tk.Entry(ventana)
    entrada_dni.pack(pady=5)

    tk.Label(ventana, text="Materia:").pack()
    entrada_materia = tk.Entry(ventana)
    entrada_materia.pack(pady=5)

    tk.Label(ventana, text="Nota (1 a 10):").pack()
    entrada_nota = tk.Entry(ventana)
    entrada_nota.pack(pady=5)

    resultado = tk.Label(ventana, text="")
    resultado.pack(pady=10)

    def guardar_nota():
        dni = entrada_dni.get()
        materia = entrada_materia.get()
        nota = entrada_nota.get()

        mensaje = calificaciones.cargar_nota(dni, materia, nota)
        resultado.config(text=mensaje)

    tk.Button(ventana, text="Guardar nota",
              command=guardar_nota).pack(pady=10)

def abrir_promedios():
    ventana = tk.Toplevel()
    ventana.title("Calcular promedios")
    tk.Label(ventana, text="DNI del estudiante:").pack()
    entrada_dni = tk.Entry(ventana)
    entrada_dni.pack()
    resultado = tk.Label(ventana, text="")
    resultado.pack(pady=10)
    def mostrar_promedios():
        dni = entrada_dni.get()
        datos = calificaciones.calcular_promedio(dni)
        if "error" in datos:
            resultado.config(text=datos["error"])
        else:
            texto = "Promedios por materia:\n"

            for materia, promedio in datos["promedios_materias"].items():
                texto += materia + ": " + str(promedio) + "\n"

            texto += "Promedio general: " + str(datos["promedio_general"])
            resultado.config(text=texto)
    tk.Button(ventana, text="Calcular", command=mostrar_promedios).pack()

# Sección 5: acá después se va a llamar a calificaciones.obtener_historial().
def abrir_historial():
    abrir_ventana("Consultar historial académico")

# El programa arranca solo si ejecutamos este archivo directamente.
if __name__ == "__main__":
    # Creamos la ventana principal con su título.
    ventana = tk.Tk()
    ventana.title("Sistema de Gestión Académica")

    # Tamaño fijo: no se puede agrandar ni achicar.
    ventana.geometry("400x380")
    ventana.resizable(False, False)

    # Título que aparece arriba de los botones.
    tk.Label(ventana, text="Sistema de Gestión Académica", font=("Arial", 14, "bold")).pack(pady=20)

    # Los 5 botones del menú, uno debajo del otro. Cada uno llama a su función.
    tk.Button(ventana, text="Registrar estudiante", width=32, command=abrir_registro).pack(pady=5)
    tk.Button(ventana, text="Buscar estudiante", width=32, command=abrir_busqueda).pack(pady=5)
    tk.Button(ventana, text="Cargar materias y calificaciones", width=32, command=abrir_calificaciones).pack(pady=5)
    tk.Button(ventana, text="Calcular promedios", width=32, command=abrir_promedios).pack(pady=5)
    tk.Button(ventana, text="Consultar historial académico", width=32, command=abrir_historial).pack(pady=5)

    # Botón para cerrar la aplicación.
    tk.Button(ventana, text="Salir", width=32, command=ventana.destroy).pack(pady=20)

    # Mantiene la ventana abierta esperando los clics del usuario.
    ventana.mainloop()
