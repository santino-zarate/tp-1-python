# Importamos Tkinter (la librería de ventanas) con el nombre corto "tk".
import tkinter as tk

# Importamos los módulos del equipo para conectarlos más adelante.
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


# Sección 3: acá después se va a llamar a calificaciones.cargar_nota().
def abrir_calificaciones():
    abrir_ventana("Cargar materias y calificaciones")


# Sección 4: acá después se va a llamar a calificaciones.calcular_promedio().
def abrir_promedios():
    abrir_ventana("Calcular promedios")


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
