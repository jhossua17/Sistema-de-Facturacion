

import os
import tkinter as tk
from tkinter import Menu
from tkinter import messagebox
from tkinter import ttk,filedialog
#archivo donde se almacenen los usuarios
ARCHIVO_CLIENTES = "clientes.txt"
DATA_FILE="Vendedores.txt"#archivo que guarda datos de vendedores
PRODUCTO_FILE ="producto.txt"
def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"

def registrar_cliente ():
    id = entry_id.get()
    cliente = entry_cliente.get()
    direccion = entry_direccion.get()
    telefono = entry_telefono.get()
    email = entry_email.get()

    if id and cliente:
        #verifica si el usuario ya existe
        if verificar_cliente_existente(cliente):
            messagebox.showerror("Error", "el cliente ya existe")
            return
        with open(ARCHIVO_CLIENTES, "a")as file:
            file.write(f"{id},{cliente},{direccion},{telefono},{telefono},{email}\n")

        messagebox.showinfo("Exito", "Cliente registrado correctamente.")
        entry_id.delete(0,tk.END)
        entry_cliente.delete(0,tk.END)
        entry_direccion.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
        entry_email.delete(0, tk.END)

    else:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")

def verificar_cliente_existente(cliente):
    if os.path.exists(ARCHIVO_CLIENTES):
        with open(ARCHIVO_CLIENTES,"r") as file:
            for linea in file:
                datos = linea.strip().split(",")
                if datos[0] == cliente:
                    return True
    return False

def mostrar_clientes():
    if os.path.exists(ARCHIVO_CLIENTES):
        with open(ARCHIVO_CLIENTES,"r")as file:
            lista_clientes.delete("1.0",tk.END)# El valor "1.0" especifica la posicion inicial del texto a eliminar, 1 es la primera linea y 0 la primera columna
            for linea in file:
                    datos = linea.strip().split(",")
                    lista_clientes.insert(tk.END,F"Cliente: ID:{datos[0]}, Nombre:{datos[1]}, Direccion:{datos[2]}, Tel.{datos[3]}, Correo:{datos[5]}\n")

    else:
        messagebox.showerror("Error","No hay clientes registrados")



#configuracion de la interfaz grafica

root = tk.Tk()
root.title("Gestion de Clientes")
root.geometry("650x650")


#eiquetas y entradas de usuarios

tk.Label(root,text="ID Cliente:").pack() #<-Posiciona el widget en la ventana de manera automatica
entry_id=tk.Entry(root)
entry_id.pack()

tk.Label(root,text="Nombre Cliente: ").pack()
entry_cliente=tk.Entry(root)
entry_cliente.pack()

tk.Label(root,text="Direccion: ").pack()
entry_direccion=tk.Entry(root)
entry_direccion.pack()

tk.Label(root,text="Telefono: ").pack()
entry_telefono=tk.Entry(root)
entry_telefono.pack()

tk.Label(root,text="E-Mail: ").pack()
entry_email=tk.Entry(root)
entry_email.pack()

#botones de accion
def hola():
    pass

tk.Button(root,text="Registrar Cliete",command=registrar_cliente).pack(pady=5)
tk.Button(root,text="Modificar Informacion de cliente existente",command=hola).pack(pady=5)
tk.Button(root,text="Eliminar Cliente",command=hola).pack(pady=5)
tk.Button(root,text="Buscar Cliente ",command=hola).pack(pady=5)
tk.Button(root,text="Mostrar Clintes",command=mostrar_clientes).pack(pady=5)

#area de texto para listar usuarios

lista_clientes = tk.Text(root,height=10,width=100)
lista_clientes.pack(pady=5)

productos = []


def agregar_producto():
    codigo = entry_codigo.get()
    nombre = entry_nombre.get()
    precio = entry_precio.get()
    stock = entry_stock.get()

    if not codigo or not nombre or not precio or not stock:
        messagebox.showwarning("Campos Vacíos", "Todos los campos son obligatorios")
        return

    for producto in productos:
        if producto["codigo"] == codigo:
            messagebox.showerror("Código Duplicado", "El código del producto ya existe")
            return

    productos.append({"codigo": codigo, "nombre": nombre, "precio": float(precio), "stock": int(stock)})
    actualizar_lista()
    limpiar_campos()


# Función para actualizar la lista en el Treeview
def actualizar_lista():
    for item in tree.get_children():
        tree.delete(item)
    for producto in productos:
        tree.insert("", "end", values=(producto["codigo"], producto["nombre"], producto["precio"], producto["stock"]))


def eliminar_producto():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Eliminar", "Seleccione un producto para eliminar")
        return

    codigo = tree.item(selected_item, "values")[0]
    for producto in productos:
        if producto["codigo"] == codigo:
            productos.remove(producto)
            break
    actualizar_lista()


def modificar_producto():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Modificar", "Seleccione un producto para modificar")
        return

    codigo = tree.item(selected_item, "values")[0]
    for producto in productos:
        if producto["codigo"] == codigo:
            producto["nombre"] = entry_nombre.get()
            producto["precio"] = float(entry_precio.get())
            producto["stock"] = int(entry_stock.get())
            break
    actualizar_lista()
    limpiar_campos()


def buscar_producto():
    termino = entry_buscar.get().lower()
    for item in tree.get_children():
        tree.delete(item)

    for producto in productos:
        if termino in producto["codigo"].lower() or termino in producto["nombre"].lower():
            tree.insert("", "end",
                        values=(producto["codigo"], producto["nombre"], producto["precio"], producto["stock"]))


# Función para limpiar campos
def limpiar_campos():
    entry_codigo.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_stock.delete(0, tk.END)


root = tk.Tk()
root.title("Gestión de Productos")
root.geometry("800x500")

# Etiquetas y campos de entrada
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Código").grid(row=0, column=0)
entry_codigo = tk.Entry(frame)
entry_codigo.grid(row=0, column=1)

tk.Label(frame, text="Nombre").grid(row=1, column=0)
entry_nombre = tk.Entry(frame)
entry_nombre.grid(row=1, column=1)

tk.Label(frame, text="Precio").grid(row=2, column=0)
entry_precio = tk.Entry(frame)
entry_precio.grid(row=2, column=1)

tk.Label(frame, text="Stock").grid(row=3, column=0)
entry_stock = tk.Entry(frame)
entry_stock.grid(row=3, column=1)

# Botones
tk.Button(frame, text="Agregar", command=agregar_producto).grid(row=4, column=0, pady=5)
tk.Button(frame, text="Modificar", command=modificar_producto).grid(row=4, column=1)
tk.Button(frame, text="Eliminar", command=eliminar_producto).grid(row=5, column=0)
tk.Button(frame, text="Buscar", command=buscar_producto).grid(row=5, column=1)
entry_buscar = tk.Entry(frame)
entry_buscar.grid(row=6, column=0, columnspan=2, pady=5)

# Lista de productos
tree = ttk.Treeview(root, columns=("Código", "Nombre", "Precio", "Stock"), show="headings")
tree.heading("Código", text="Código")
tree.heading("Nombre", text="Nombre")
tree.heading("Precio", text="Precio")
tree.heading("Stock", text="Stock")
tree.pack(pady=10)


root.mainloop()