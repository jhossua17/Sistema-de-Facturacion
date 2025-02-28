

import os
import tkinter as tk
from tkinter import Menu
from tkinter import messagebox
from tkinter import ttk,filedialog

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"

def agregar_clientes():
    def agregar():
        try:
            vnombre = nombre.get()
            vtelefono = telefono.get()
            vemail = email.get()

            #Creo y/o abre el archivo contactos.txt de modo que haga un append
            with open(DATA_FILE, "a") as file:
                file.write(f"{vnombre},{vtelefono},{vemail}\n")
                messagebox.showinfo("Contacto Agregado", "El contacto fue agregado exitosamente")
                print("Contacto agregado exitosamente")
        except FileNotFoundError:
            print(f"Error: el aarchivo {file} no fue encontrado")

#Genera una nueva ventana emergente o secundaria en la aplicación de Tkinter
#===========================================================================
    window_agregar_contactos = tk.Toplevel(root)
    window_agregar_contactos.title("Agregar contactos")
    window_agregar_contactos.geometry("400x300")

# Crear las etiquetas
    label = tk.Label(window_agregar_contactos,text="Introduce el nombre:")
    label.grid(row=0,column=0,padx=10,pady=10)
#Crear un cuadro de texto
    nombre = tk.Entry(window_agregar_contactos)
    nombre.grid(row=0,column=1,padx=10,pady=10)
#Cada vez que se presione Enter en el widget nombre y cambia el foco al siguiente widget,
#según el orden de tabulación configurado
    nombre.bind("<Return>",focus_next_widget)
    label2 = tk.Label(window_agregar_contactos,text="Introduce el telefono:")
    label2.grid(row=1,column=0,padx=10,pady=10)
    telefono = tk.Entry(window_agregar_contactos)
    telefono.grid(row=1, column=1, padx=10, pady=10)
    telefono.bind("<Return>", focus_next_widget)

    label3 = tk.Label(window_agregar_contactos,text="Introduce el email:")
    label3.grid(row=2,column=0,padx=10,pady=10)
    email = tk.Entry(window_agregar_contactos)
    email.grid(row=2, column=1, padx=10, pady=10)
    email.bind("<Return>", focus_next_widget)

    button=tk.Button(window_agregar_contactos,text="Agregar",command=agregar)
    button.grid(row=3, column=0,columnspan=2,pady=10)
