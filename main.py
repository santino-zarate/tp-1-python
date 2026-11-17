import tkinter as tk
from tkinter import messagebox
import estudiantes
import calificaciones

COLOR_FONDO = "#F1F5F9"
COLOR_PRINCIPAL = "#203B59"
COLOR_PRINCIPAL_CLARO = "#2E5A8A"
COLOR_SECUNDARIO = "#E2E9F2"
COLOR_TEXTO = "#243447"
COLOR_BLANCO = "#FFFFFF"
COLOR_GRIS = "#5A6B7D"
COLOR_LINEA = "#D6DEE8"


# Etiqueta común, con el color de fondo y de letra del sistema.
def crear_etiqueta(ventana, texto):
    tk.Label(ventana, text=texto, bg=COLOR_FONDO,
             fg=COLOR_TEXTO).pack()


# Arma el título de una ventana y una línea fina abajo para separarlo.
def crear_titulo(ventana, texto):
    tk.Label(ventana, text=texto,
             font=("Arial", 16, "bold"),
             bg=COLOR_FONDO, fg=COLOR_PRINCIPAL).pack(pady=8)
    tk.Frame(ventana, height=1, bg=COLOR_LINEA).pack(fill="x", padx=30)


# Arma un casillero prolijo: fondo blanco, borde fino y un poco más de alto.
def crear_campo(ventana, ancho):
    campo = tk.Entry(ventana, width=ancho, bg=COLOR_BLANCO, fg=COLOR_TEXTO,
                     relief="solid", bd=1, font=("Arial", 10))
    campo.pack(ipady=4, pady=6)
    return campo


# Crea un botón con el estilo del sistema y le cambia el color al pasar el mouse.
def crear_boton(ventana, texto, comando, principal=True):
    if principal:
        fondo = COLOR_PRINCIPAL
        fondo_hover = COLOR_PRINCIPAL_CLARO
        color_letra = COLOR_BLANCO
    else:
        fondo = COLOR_BLANCO
        fondo_hover = COLOR_SECUNDARIO
        color_letra = COLOR_PRINCIPAL
    boton = tk.Button(ventana, text=texto, command=comando,
                      bg=fondo, fg=color_letra,
                      activebackground=fondo_hover,
                      activeforeground=color_letra,
                      relief="flat", cursor="hand2",
                      font=("Arial", 10, "bold"), pady=6)
    # Al entrar el mouse se pinta distinto, y al salir vuelve a su color.
    boton.bind("<Enter>", lambda evento: boton.config(bg=fondo_hover))
    boton.bind("<Leave>", lambda evento: boton.config(bg=fondo))
    return boton


def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho - ancho) // 2
    y = (pantalla_alto - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


# Le pone puntos al DNI para mostrarlo más lindo: 40123456 queda 40.123.456.
def formatear_dni(dni):
    if len(dni) == 8:
        return dni[:2] + "." + dni[2:5] + "." + dni[5:]
    if len(dni) == 7:
        return dni[0] + "." + dni[1:4] + "." + dni[4:]
    return dni


# Sección 1: ventana para cargar un estudiante nuevo.
def abrir_registro():
    ventana = tk.Toplevel()
    ventana.title("Registrar estudiante")
    centrar_ventana(ventana, 430, 500)
    ventana.configure(bg=COLOR_FONDO)
    crear_titulo(ventana, "Registrar estudiante")

    crear_etiqueta(ventana, "DNI")
    entrada_dni = crear_campo(ventana, 36)

    fila = tk.Frame(ventana, bg=COLOR_FONDO)
    fila.pack()

    columna_nombre = tk.Frame(fila, bg=COLOR_FONDO)
    columna_nombre.pack(side="left")
    crear_etiqueta(columna_nombre, "Nombre")
    entrada_nombre = crear_campo(columna_nombre, 17)

    columna_apellido = tk.Frame(fila, bg=COLOR_FONDO)
    columna_apellido.pack(side="left", padx=10)
    crear_etiqueta(columna_apellido, "Apellido")
    entrada_apellido = crear_campo(columna_apellido, 17)
    crear_etiqueta(ventana, "Fecha de nacimiento (DD/MM/AAAA)")
    entrada_fecha = crear_campo(ventana, 36)

    crear_etiqueta(ventana, "Año de ingreso")
    entrada_año = crear_campo(ventana, 36)

    # Toma lo escrito, llama a la función y muestra si salió bien o mal.
    def registrar():
        ok, mensaje = estudiantes.registrar_estudiante(
            entrada_dni.get(),
            entrada_nombre.get(),
            entrada_apellido.get(),
            entrada_fecha.get(),
            entrada_año.get()
        )
        if ok:
            messagebox.showinfo("Registrar estudiante", mensaje)
            # Vaciamos los campos para poder cargar otro estudiante.
            entrada_dni.delete(0, tk.END)
            entrada_nombre.delete(0, tk.END)
            entrada_apellido.delete(0, tk.END)
            entrada_dni.focus_set()
            entrada_fecha.delete(0, tk.END)
            entrada_año.delete(0, tk.END)
        else:
            messagebox.showerror("Registrar estudiante", mensaje)

    crear_boton(ventana, "Registrar", registrar).pack(fill="x", padx=45, pady=6)
    crear_boton(ventana, "Cerrar", ventana.destroy, principal=False).pack(fill="x", padx=45)

    # El cursor arranca en el DNI y se puede confirmar con Enter.
    entrada_dni.focus_set()
    ventana.bind("<Return>", lambda evento: registrar())


# Sección 2: ventana para buscar un estudiante por DNI o por apellido.
def abrir_busqueda():
    ventana = tk.Toplevel()
    ventana.title("Buscar estudiante")
    centrar_ventana(ventana, 470, 500)
    ventana.configure(bg=COLOR_FONDO)
    crear_titulo(ventana, "Buscar estudiante")

    # Un solo casillero: sirve tanto para el DNI como para el apellido.
    crear_etiqueta(ventana, "DNI o apellido")
    entrada_busqueda = crear_campo(ventana, 36)

    # Lista donde se van a mostrar los estudiantes encontrados.
    lista = tk.Listbox(ventana, width=44, height=8, bg=COLOR_BLANCO,
                       fg=COLOR_TEXTO, relief="solid", bd=1,
                       font=("Arial", 11),
                       selectbackground=COLOR_PRINCIPAL,
                       selectforeground=COLOR_BLANCO,
                       activestyle="none")
    lista.pack(padx=45, pady=6, fill="x")

    # Cartel chiquito con la cantidad de resultados.
    contador = tk.Label(ventana, text="", bg=COLOR_FONDO, fg=COLOR_GRIS,
                        font=("Arial", 12))
    contador.pack()

    # Conservamos los resultados actuales para operar sobre la fila seleccionada.
    resultados_actuales = []
    ultimo_termino = ""

    # Busca lo escrito, limpia la lista anterior y muestra el resultado.
    def buscar():
        nonlocal ultimo_termino
        ultimo_termino = entrada_busqueda.get()
        resultados_actuales.clear()
        lista.delete(0, tk.END)
        contador.config(text="")
        ok, resultado = estudiantes.buscar_estudiante(ultimo_termino)
        if not ok:
            messagebox.showerror("Buscar estudiante", resultado)
            return
        if len(resultado) == 0:
            messagebox.showinfo("Buscar estudiante", "No se encontraron estudiantes")
            return
        # Cada resultado se muestra como "DNI - Apellido, Nombre".
        for alumno in resultado:
            resultados_actuales.append(alumno)
            lista.insert(tk.END, formatear_dni(alumno["dni"]) + " - " + alumno["apellido"] + ", " + alumno["nombre"])
        # Avisamos cuántos encontró, en singular o en plural.
        if len(resultado) == 1:
            contador.config(text="1 estudiante encontrado")
        else:
            contador.config(text=str(len(resultado)) + " estudiantes encontrados")

    def eliminar_seleccionado():
        seleccion = lista.curselection()
        if not seleccion:
            messagebox.showwarning("Eliminar estudiante", "Seleccion\u00e1 un estudiante de la lista")
            return

        alumno = resultados_actuales[seleccion[0]]
        cantidad_materias = len(estudiantes.estudiantes[alumno["dni"]].get("materias", {}))
        confirmacion = (
            "\u00bfEliminar a " + alumno["nombre"] + " " + alumno["apellido"] +
            " (DNI " + alumno["dni"] + ")?\n\nTambi\u00e9n se eliminar\u00e1n sus materias y notas. " +
            "Tiene " + str(cantidad_materias) + " materias."
        )
        if not messagebox.askyesno("Confirmar eliminaci\u00f3n", confirmacion):
            return

        ok, mensaje = estudiantes.eliminar_estudiante(alumno["dni"])
        if ok:
            messagebox.showinfo("Eliminar estudiante", mensaje)
            entrada_busqueda.delete(0, tk.END)
            entrada_busqueda.insert(0, ultimo_termino)
            buscar()
        else:
            messagebox.showerror("Eliminar estudiante", mensaje)

    crear_boton(ventana, "Buscar", buscar).pack(fill="x", padx=45, pady=6)
    crear_boton(ventana, "Eliminar", eliminar_seleccionado, principal=False).pack(fill="x", padx=45, pady=6)
    crear_boton(ventana, "Cerrar", ventana.destroy, principal=False).pack(fill="x", padx=45)

    entrada_busqueda.focus_set()
    ventana.bind("<Return>", lambda evento: buscar())


def abrir_calificaciones():
    ventana = tk.Toplevel()
    ventana.title("Cargar calificaciones")
    centrar_ventana(ventana, 430, 500)
    ventana.configure(bg=COLOR_FONDO)
    crear_titulo(ventana, "Cargar calificación")

    crear_etiqueta(ventana, "DNI del estudiante")
    entrada_dni = crear_campo(ventana, 36)
    crear_etiqueta(ventana, "Materia")
    entrada_materia = crear_campo(ventana, 36)
    crear_etiqueta(ventana, "Nota (1 a 10)")
    entrada_nota = crear_campo(ventana, 36)

    resultado = tk.Label(ventana, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                         wraplength=330, justify="center")
    resultado.pack(pady=6)

    def guardar_nota():
        datos = calificaciones.cargar_nota(
            entrada_dni.get(),
            entrada_materia.get(),
            entrada_nota.get()
        )
        # Si vino un error lo mostramos, si no, el mensaje de que salió bien.
        if "error" in datos:
            resultado.config(text=datos["error"])
        else:
            resultado.config(text=datos["message"])

        if datos["message"] == "Nota cargada correctamente.":
            entrada_nota.delete(0, tk.END)
            entrada_nota.focus_set()

    crear_boton(ventana, "Guardar calificación", guardar_nota).pack(fill="x", padx=45, pady=6)
    crear_boton(ventana, "Cerrar", ventana.destroy, principal=False).pack(fill="x", padx=45)

    entrada_dni.focus_set()
    ventana.bind("<Return>", lambda evento: guardar_nota())


def abrir_promedios():
    ventana = tk.Toplevel()
    ventana.title("Calcular promedios")
    centrar_ventana(ventana, 430, 480)
    ventana.configure(bg=COLOR_FONDO)
    crear_titulo(ventana, "Promedios académicos")

    crear_etiqueta(ventana, "DNI del estudiante")
    entrada_dni = crear_campo(ventana, 36)

    resultado = tk.Label(ventana, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                         justify="left",font=("Arial Rounded MT Bold", 11), wraplength=330)
    resultado.pack(pady=10)

    def mostrar_promedios():
        datos = calificaciones.calcular_promedio(entrada_dni.get())
        if "error" in datos:
            resultado.config(text=datos["error"])
        else:
            texto = "Promedios por materia:\n"
            for materia, promedio in datos["promedios_materias"].items():
                texto += materia + ": " + str(promedio) + "\n"+"\n"
            texto += "\nPromedio general: " + str(datos["promedio_general"])
            resultado.config(text=texto)

    crear_boton(ventana, "Calcular promedios", mostrar_promedios).pack(fill="x", padx=45, pady=6)
    crear_boton(ventana, "Cerrar", ventana.destroy, principal=False).pack(fill="x", padx=45)

    entrada_dni.focus_set()
    ventana.bind("<Return>", lambda evento: mostrar_promedios())


def abrir_historial():
    ventana = tk.Toplevel()
    ventana.title("Historial académico")
    centrar_ventana(ventana, 430, 480)
    ventana.configure(bg=COLOR_FONDO)
    crear_titulo(ventana, "Historial académico")

    crear_etiqueta(ventana, "DNI del estudiante")
    entrada_dni = crear_campo(ventana, 36)

    resultado = tk.Label(ventana, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                         justify="left",font=("Arial Rounded MT Bold", 11), wraplength=330)
    resultado.pack(pady=10)

    def mostrar_historial():
        datos = calificaciones.obtener_historial(entrada_dni.get())
        if "error" in datos:
            resultado.config(text=datos["error"])
        else:
            texto = "Estudiante: " + datos["nombre"] + " " + datos["apellido"] + "\n"
            for materia, notas in datos["materias"].items():
                texto += "\n" + materia + ": " + str(notas)
            resultado.config(text=texto)

    crear_boton(ventana, "Consultar historial", mostrar_historial).pack(fill="x", padx=45, pady=6)
    crear_boton(ventana, "Cerrar", ventana.destroy, principal=False).pack(fill="x", padx=45)

    entrada_dni.focus_set()
    ventana.bind("<Return>", lambda evento: mostrar_historial())


if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.title("Sistema de Gestión Académica")
    centrar_ventana(ventana, 470, 450)
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)
    tk.Label(ventana, text="Sistema de Gestión Académica",
             font=("Arial", 17, "bold"),
             bg=COLOR_FONDO, fg=COLOR_PRINCIPAL).pack(pady=8)
    tk.Frame(ventana, height=1, bg=COLOR_LINEA).pack(fill="x", padx=60)

    botones = [
        ("Registrar estudiante", abrir_registro),
        ("Buscar estudiante", abrir_busqueda),
        ("Cargar calificaciones", abrir_calificaciones),
        ("Calcular promedios", abrir_promedios),
        ("Consultar historial", abrir_historial)
    ]
    for texto, funcion in botones:
        crear_boton(ventana, texto, funcion).pack(fill="x", padx=70, pady=4)
    crear_boton(ventana, "Salir", ventana.destroy, principal=False).pack(fill="x", padx=70, pady=(14, 8))
    ventana.mainloop()
