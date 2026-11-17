import tkinter as tk
from tkinter import messagebox
import estudiantes
import calificaciones

COLOR_FONDO = "#F1F5F9"
COLOR_PRINCIPAL = "#203B59"
COLOR_TEXTO = "#243447"
COLOR_BLANCO = "#FFFFFF"
def crear_etiqueta(ventana, texto):
    tk.Label(ventana, text=texto, bg=COLOR_FONDO,
             fg=COLOR_TEXTO).pack()

def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho - ancho) // 2
    y = (pantalla_alto - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    
# Abre una ventana secundaria con el título de la sección y el aviso "En construcción".
def abrir_ventana(titulo):
    ventana = tk.Toplevel()
    ventana.title(titulo)
    tk.Label(ventana, text="En construcción").pack(padx=40, pady=30)

# Sección 1: ventana para cargar un estudiante nuevo.
def abrir_registro():
    ventana = tk.Toplevel()
    ventana.title("Registrar estudiante")
    centrar_ventana(ventana, 400, 350)
    ventana.configure(bg=COLOR_FONDO)
    tk.Label(ventana, text="Registrar estudiante",
             font=("Arial", 16, "bold"),
             bg=COLOR_FONDO, fg=COLOR_PRINCIPAL).pack(pady=15)

    # Los tres campos del formulario.
    crear_etiqueta(ventana, "DNI")
    entrada_dni = tk.Entry(ventana, width=30)
    entrada_dni.pack(pady=5)
    crear_etiqueta(ventana, "Nombre")
    entrada_nombre = tk.Entry(ventana, width=30)
    entrada_nombre.pack(pady=5)
    crear_etiqueta(ventana, "Apellido")
    entrada_apellido = tk.Entry(ventana, width=30)
    entrada_apellido.pack(pady=5)

    # Toma lo escrito, llama a la función y muestra si salió bien o mal.
    def registrar():
        ok, mensaje = estudiantes.registrar_estudiante(
            entrada_dni.get(),
            entrada_nombre.get(),
            entrada_apellido.get()
        )
        if ok:
            messagebox.showinfo("Registrar estudiante", mensaje)
            # Vaciamos los campos para poder cargar otro estudiante.
            entrada_dni.delete(0, tk.END)
            entrada_nombre.delete(0, tk.END)
            entrada_apellido.delete(0, tk.END)
        else:
            messagebox.showerror("Registrar estudiante", mensaje)

    tk.Button(ventana, text="Registrar",
              command=registrar,
              bg=COLOR_PRINCIPAL, fg=COLOR_BLANCO).pack(pady=10)
    tk.Button(ventana, text="Cerrar",
              command=ventana.destroy).pack(pady=5)

# Sección 2: acá después se va a llamar a estudiantes.buscar_estudiante().
def abrir_busqueda():
    abrir_ventana("Buscar estudiante")

def abrir_calificaciones():
    ventana = tk.Toplevel()
    ventana.title("Cargar calificaciones")
    centrar_ventana(ventana, 400, 350)
    ventana.configure(bg=COLOR_FONDO)
    tk.Label(ventana, text="Cargar calificación",
             font=("Arial", 16, "bold"),
             bg=COLOR_FONDO, fg=COLOR_PRINCIPAL).pack(pady=15)
    crear_etiqueta(ventana, "DNI del estudiante")
    entrada_dni = tk.Entry(ventana, width=30)
    entrada_dni.pack(pady=5)
    crear_etiqueta(ventana, "Materia")
    entrada_materia = tk.Entry(ventana, width=30)
    entrada_materia.pack(pady=5)
    crear_etiqueta(ventana, "Nota (1 a 10)")
    entrada_nota = tk.Entry(ventana, width=30)
    entrada_nota.pack(pady=5)
    resultado = tk.Label(ventana, bg=COLOR_FONDO)
    resultado.pack(pady=10)
    def guardar_nota():
        mensaje = calificaciones.cargar_nota(
            entrada_dni.get(),
            entrada_materia.get(),
            entrada_nota.get()
        )
        resultado.config(text=mensaje)
    tk.Button(ventana, text="Guardar calificación",
              command=guardar_nota,
              bg=COLOR_PRINCIPAL, fg=COLOR_BLANCO).pack(pady=10)

def abrir_promedios():
    ventana = tk.Toplevel()
    ventana.title("Calcular promedios")
    centrar_ventana(ventana, 400, 350)
    ventana.configure(bg=COLOR_FONDO)
    tk.Label(ventana, text="Promedios académicos",
             font=("Arial", 16, "bold"),
             bg=COLOR_FONDO, fg=COLOR_PRINCIPAL).pack(pady=15)
    crear_etiqueta(ventana, "DNI del estudiante")
    entrada_dni = tk.Entry(ventana, width=30)
    entrada_dni.pack(pady=5)
    resultado = tk.Label(ventana, bg=COLOR_FONDO, fg=COLOR_TEXTO)
    resultado.pack(pady=15)
    def mostrar_promedios():
        datos = calificaciones.calcular_promedio(entrada_dni.get())
        if "error" in datos:
            resultado.config(text=datos["error"])
        else:
            texto = "Promedios por materia:\n"
            for materia, promedio in datos["promedios_materias"].items():
                texto += materia + ": " + str(promedio) + "\n"
            texto += "\nPromedio general: " + str(datos["promedio_general"])
            resultado.config(text=texto)
    tk.Button(ventana, text="Calcular promedios",
              command=mostrar_promedios,
              bg=COLOR_PRINCIPAL, fg=COLOR_BLANCO).pack(pady=10)

def abrir_historial():
    ventana = tk.Toplevel()
    ventana.title("Historial académico")
    centrar_ventana(ventana, 400, 350)
    ventana.configure(bg=COLOR_FONDO)
    tk.Label(ventana, text="Historial académico",
             font=("Arial", 16, "bold"),
             bg=COLOR_FONDO, fg=COLOR_PRINCIPAL).pack(pady=15)
    crear_etiqueta(ventana, "DNI del estudiante")
    entrada_dni = tk.Entry(ventana, width=30)
    entrada_dni.pack(pady=5)
    resultado = tk.Label(ventana, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                         justify="left")
    resultado.pack(pady=15)
    def mostrar_historial():
        datos = calificaciones.obtener_historial(entrada_dni.get())
        if "error" in datos:
            resultado.config(text=datos["error"])
        else:
            texto = "Estudiante: " + datos["nombre"] + " " + datos["apellido"] + "\n"
            for materia, notas in datos["materias"].items():
                texto += "\n" + materia + ": " + str(notas)
            resultado.config(text=texto)
    tk.Button(ventana, text="Consultar historial",
              command=mostrar_historial,
              bg=COLOR_PRINCIPAL, fg=COLOR_BLANCO).pack(pady=10)

if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.title("Sistema de Gestión Académica")
    centrar_ventana(ventana, 450, 480)
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)
    tk.Label(ventana, text="Sistema de Gestión Académica",
             font=("Arial", 17, "bold"),
             bg=COLOR_FONDO, fg=COLOR_PRINCIPAL).pack(pady=25)
    botones = [
        ("Registrar estudiante", abrir_registro),
        ("Buscar estudiante", abrir_busqueda),
        ("Cargar calificaciones", abrir_calificaciones),
        ("Calcular promedios", abrir_promedios),
        ("Consultar historial", abrir_historial)
    ]
    for texto, funcion in botones:
        tk.Button(ventana, text=texto, width=30,
                  command=funcion,
                  bg=COLOR_PRINCIPAL, fg=COLOR_BLANCO,
                  font=("Arial", 10, "bold")).pack(pady=7)
    tk.Button(ventana, text="Salir", width=30,
              command=ventana.destroy).pack(pady=15)
    ventana.mainloop()
