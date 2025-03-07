import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

# Archivos de almacenamiento
ARCHIVO_CLIENTES = "clientes.txt"
ARCHIVO_VENDEDORES = "vendedores.txt"
ARCHIVO_PRODUCTOS = "productos.txt"
ARCHIVO_FACTURAS = "facturas.txt"
ARCHIVO_USUARIOS = "usuarios.txt"
ARCHIVO_PEDIDOS = "pedidos.txt"

# Lista global de productos
productos = []
pedidos = []

# Función para cargar productos desde el archivo
def cargar_productos():
    if os.path.exists(ARCHIVO_PRODUCTOS):
        with open(ARCHIVO_PRODUCTOS, "r") as file:
            for linea in file:
                codigo, nombre, precio, stock = linea.strip().split(",")
                productos.append({"codigo": codigo, "nombre": nombre, "precio": float(precio), "stock": int(stock)})

# Función para guardar productos en el archivo
def guardar_productos():
    with open(ARCHIVO_PRODUCTOS, "w") as file:
        for producto in productos:
            file.write(f"{producto['codigo']},{producto['nombre']},{producto['precio']},{producto['stock']}\n")

# Función para cargar pedidos desde el archivo
def cargar_pedidos():
    if os.path.exists(ARCHIVO_PEDIDOS):
        with open(ARCHIVO_PEDIDOS, "r") as file:
            for linea in file:
                cliente, producto, cantidad, estado = linea.strip().split(",")
                pedidos.append({"cliente": cliente, "producto": producto, "cantidad": int(cantidad), "estado": estado})

# Función para guardar pedidos en el archivo
def guardar_pedidos():
    with open(ARCHIVO_PEDIDOS, "w") as file:
        for pedido in pedidos:
            file.write(f"{pedido['cliente']},{pedido['producto']},{pedido['cantidad']},{pedido['estado']}\n")

# Función para iniciar sesión
def iniciar_sesion():
    usuario = entry_usuario_login.get()
    contraseña = entry_contraseña_login.get()

    if os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, "r") as file:
            for linea in file:
                datos = linea.strip().split(",")
                if datos[0] == usuario and datos[1] == contraseña:
                    messagebox.showinfo("Éxito", "Inicio de sesión exitoso")

                    mostrar_modulo_segun_rol(datos[2])  # datos[2] es el rol (admin, vendedor, cliente)
                    entry_usuario_login.delete(0, tk.END)#limpia los campos para iniciar sesion al cerrar sesion
                    entry_contraseña_login.delete(0,tk.END)
                    return
    messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Función para mostrar el módulo según el rol
def mostrar_modulo_segun_rol(rol):
    frame_login.pack_forget()
    if rol == "admin":
        notebook.pack(fill="both", expand=True)
    elif rol == "vendedor":
        frame_vendedores.pack(fill="both", expand=True)
        notebook.pack()
    elif rol == "cliente":
        frame_clientes.pack(fill="both", expand=True)
    boton_cerrar_sesion.pack(side="top", pady=5)

# Función para cerrar sesión
def cerrar_sesion():
    # Ocultar todos los módulos
    notebook.pack_forget()
    frame_vendedores.pack_forget()
    frame_clientes.pack_forget()
    boton_cerrar_sesion.pack_forget()
    # Mostrar la pantalla de inicio de sesión
    frame_login.pack(fill="both", expand=True)

# Función para registrar un cliente

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

def eliminar_cliente():
    id_eliminar = entry_id.get()

    if id_eliminar:
        clientes_actualizados = []
        cliente_encontrado = False

        if os.path.exists(ARCHIVO_CLIENTES):
            with open(ARCHIVO_CLIENTES, "r") as file:
                for linea in file:
                    datos = linea.strip().split(",")
                    if datos[0] == id_eliminar:
                        cliente_encontrado = True
                    else:
                        clientes_actualizados.append(linea)

            entry_id.delete(0, tk.END)

            if cliente_encontrado:
                with open(ARCHIVO_CLIENTES, "w") as file:
                    file.writelines(clientes_actualizados)
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
            else:
                messagebox.showerror("Error", "Cliente no encontrado.")
    else:
        messagebox.showerror("Error", "Por favor, ingrese el ID del cliente a eliminar.")

def buscar_cliente():
    id_buscar = entry_id.get()

    if id_buscar:
        if os.path.exists(ARCHIVO_CLIENTES):
            with open(ARCHIVO_CLIENTES, "r") as file:
                cliente_encontrado = False
                for linea in file:
                    datos = linea.strip().split(",")
                    if datos[0] == id_buscar:
                        cliente_encontrado = True
                        messagebox.showinfo("Cliente encontrado",
                                           f"ID: {datos[0]}\nNombre: {datos[1]}\nDirección: {datos[2]}\nTeléfono: {datos[3]}\nEmail: {datos[5]}")
                        break

                entry_id.delete(0, tk.END)

                if not cliente_encontrado:
                    messagebox.showerror("Error", "Cliente no encontrado.")
        else:
            messagebox.showerror("Error", "No hay clientes registrados.")
    else:
        messagebox.showerror("Error", "Por favor, ingrese el ID del cliente a buscar.")

def modificar_cliente():
    id_modificar = entry_id.get()
    nuevo_cliente = entry_cliente.get()
    nueva_direccion = entry_direccion.get()
    nuevo_telefono = entry_telefono.get()
    nuevo_email = entry_email.get()

    if id_modificar:
        clientes_actualizados = []
        cliente_encontrado = False

        if os.path.exists(ARCHIVO_CLIENTES):
            with open(ARCHIVO_CLIENTES, "r") as file:
                for linea in file:
                    datos = linea.strip().split(",")
                    if datos[0] == id_modificar:
                        cliente_encontrado = True
                        # Actualizar los datos si se proporcionan nuevos valores
                        if nuevo_cliente:
                            datos[1] = nuevo_cliente
                        if nueva_direccion:
                            datos[2] = nueva_direccion
                        if nuevo_telefono:
                            datos[3] = nuevo_telefono
                        if nuevo_email:
                            datos[4] = nuevo_email
                        clientes_actualizados.append(",".join(datos) + "\n")
                    else:
                        clientes_actualizados.append(linea)

            entry_id.delete(0, tk.END)
            entry_cliente.delete(0, tk.END)
            entry_direccion.delete(0, tk.END)
            entry_telefono.delete(0, tk.END)
            entry_email.delete(0, tk.END)

            if cliente_encontrado:
                with open(ARCHIVO_CLIENTES, "w") as file:
                    file.writelines(clientes_actualizados)
                messagebox.showinfo("Éxito", "Cliente modificado correctamente.")
            else:
                messagebox.showerror("Error", "Cliente no encontrado.")
        else:
            messagebox.showerror("Error", "No hay clientes registrados.")
    else:
        messagebox.showerror("Error", "Por favor, ingrese el ID del cliente a modificar.")


# Función para registrar un vendedor
def registrar_vendedor():
    id = entry_id_vendedor.get()
    vendedor = entry_nombre_vendedor.get()
    direccion = entry_direccion_vendedor.get()
    telefono = entry_telefono_vendedor.get()
    email = entry_email_vendedor.get()

    if id and vendedor:
        if verificar_vendedor_existente(vendedor):
            messagebox.showerror("Error", "El vendedor ya existe")
            return
        with open(ARCHIVO_VENDEDORES, "a") as file:
            file.write(f"{id},{vendedor},{direccion},{telefono},{email}\n")
        messagebox.showinfo("Éxito", "Vendedor registrado correctamente.")
        limpiar_campos_vendedores()
    else:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")

# Función para verificar si un vendedor ya existe
def verificar_vendedor_existente(vendedor):
    if os.path.exists(ARCHIVO_VENDEDORES):
        with open(ARCHIVO_VENDEDORES, "r") as file:
            for linea in file:
                datos = linea.strip().split(",")
                if datos[1] == vendedor:
                    return True
    return False

# Función para limpiar los campos de vendedores
def limpiar_campos_vendedores():
    entry_id_vendedor.delete(0, tk.END)
    entry_nombre_vendedor.delete(0, tk.END)
    entry_direccion_vendedor.delete(0, tk.END)
    entry_telefono_vendedor.delete(0, tk.END)
    entry_email_vendedor.delete(0, tk.END)

# Función para mostrar los vendedores
def mostrar_vendedores():
    if os.path.exists(ARCHIVO_VENDEDORES):
        with open(ARCHIVO_VENDEDORES, "r") as file:
            lista_vendedores.delete("1.0", tk.END)
            for linea in file:
                datos = linea.strip().split(",")
                lista_vendedores.insert(tk.END, f"Vendedor: ID:{datos[0]}, Nombre:{datos[1]}, Dirección:{datos[2]}, Tel:{datos[3]}, Correo:{datos[4]}\n")
    else:
        messagebox.showerror("Error", "No hay vendedores registrados")

# Función para registrar un usuario
def registrar_usuario():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    rol = combo_rol.get()

    if usuario and contraseña and rol:
        if verificar_usuario_existente(usuario):
            messagebox.showerror("Error", "El usuario ya existe")
            return
        with open(ARCHIVO_USUARIOS, "a") as file:
            file.write(f"{usuario},{contraseña},{rol}\n")
        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
        limpiar_campos_usuarios()
    else:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")

# Función para verificar si un usuario ya existe
def verificar_usuario_existente(usuario):
    if os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, "r") as file:
            for linea in file:
                datos = linea.strip().split(",")
                if datos[0] == usuario:
                    return True
    return False

# Función para limpiar los campos de usuarios
def limpiar_campos_usuarios():
    entry_usuario.delete(0, tk.END)
    entry_contraseña.delete(0, tk.END)
    combo_rol.set("")

# Función para registrar un producto
def agregar_producto():
    codigo = entry_codigo_producto.get()
    nombre = entry_nombre_producto.get()
    precio = entry_precio_producto.get()
    stock = entry_stock_producto.get()

    if not codigo or not nombre or not precio or not stock:
        messagebox.showwarning("Campos Vacíos", "Todos los campos son obligatorios")
        return

    for producto in productos:
        if producto["codigo"] == codigo:
            messagebox.showerror("Código Duplicado", "El código del producto ya existe")
            return

    productos.append({"codigo": codigo, "nombre": nombre, "precio": float(precio), "stock": int(stock)})
    guardar_productos()
    actualizar_lista_productos()
    limpiar_campos_productos()

# Función para actualizar la lista de productos en el Treeview
def actualizar_lista_productos():
    for item in tree_productos.get_children():
        tree_productos.delete(item)
    for producto in productos:
        tree_productos.insert("", "end", values=(producto["codigo"], producto["nombre"], producto["precio"], producto["stock"]))

# Función para limpiar los campos de productos
def limpiar_campos_productos():
    entry_codigo_producto.delete(0, tk.END)
    entry_nombre_producto.delete(0, tk.END)
    entry_precio_producto.delete(0, tk.END)
    entry_stock_producto.delete(0, tk.END)

# Función para registrar un pedido
def registrar_pedido():
    cliente = entry_cliente_pedido.get()
    producto = entry_producto_pedido.get()
    cantidad = int(entry_cantidad_pedido.get())

    producto_info = next((p for p in productos if p["codigo"] == producto), None)
    if not producto_info:
        messagebox.showerror("Error", "Producto no encontrado")
        return

    if producto_info["stock"] < cantidad:
        messagebox.showerror("Error", "Stock insuficiente")
        return

    producto_info["stock"] -= cantidad
    pedidos.append({"cliente": cliente, "producto": producto, "cantidad": cantidad, "estado": "Pendiente"})
    guardar_pedidos()
    guardar_productos()
    actualizar_lista_pedidos()
    messagebox.showinfo("Éxito", "Pedido registrado correctamente")

# Función para actualizar la lista de pedidos en el Treeview
def actualizar_lista_pedidos():
    for item in tree_pedidos.get_children():
        tree_pedidos.delete(item)
    for pedido in pedidos:
        tree_pedidos.insert("", "end", values=(pedido["cliente"], pedido["producto"], pedido["cantidad"], pedido["estado"]))

# Función para despachar un pedido
def despachar_pedido():
    selected_item = tree_pedidos.selection()
    if not selected_item:
        messagebox.showwarning("Error", "Seleccione un pedido para despachar")
        return

    pedido = tree_pedidos.item(selected_item, "values")
    for p in pedidos:
        if p["cliente"] == pedido[0] and p["producto"] == pedido[1] and p["cantidad"] == int(pedido[2]):
            p["estado"] = "Despachado"
            break
    guardar_pedidos()
    actualizar_lista_pedidos()
    messagebox.showinfo("Éxito", "Pedido despachado correctamente")

# Función para registrar factura
def registrar_factura():
    cliente_id = entry_cliente_id.get()
    vendedor_id = entry_vendedor_id.get()
    productos_seleccionados = obtener_productos_seleccionados()

    if not cliente_id or not vendedor_id or not productos_seleccionados:
        messagebox.showwarning("Campos Vacíos", "Todos los campos son obligatorios.")
        return

    # Validar cliente
    cliente_valido = verificar_cliente_existente(cliente_id)
    if not cliente_valido:
        messagebox.showerror("Error", "El cliente seleccionado no existe.")
        return

    # Validar vendedor
    vendedor_valido = verificar_vendedor_existente(vendedor_id)
    if not vendedor_valido:
        messagebox.showerror("Error", "El vendedor seleccionado no existe.")
        return

    # Validar productos y calcular el total
    total_factura = 0
    for producto, cantidad in productos_seleccionados:
        if not verificar_producto_existente(producto):
            messagebox.showerror("Error", f"El producto {producto} no existe.")
            return
        if not verificar_stock_producto(producto, cantidad):
            messagebox.showerror("Error", f"No hay suficiente stock del producto {producto}.")
            return
        precio_unitario = obtener_precio_producto(producto)
        total_factura += precio_unitario * cantidad

        # Descontar stock
        descontar_stock_producto(producto, cantidad)

    # Crear y guardar la factura
    fecha_factura = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    factura_detalles = f"Factura ID:{fecha_factura}, Cliente:{cliente_id}, Vendedor:{vendedor_id}, Total:{total_factura}\n"
    for producto, cantidad in productos_seleccionados:
        factura_detalles += f"Producto:{producto}, Cantidad:{cantidad}, Precio Unitario:{obtener_precio_producto(producto)}\n"

    with open(ARCHIVO_FACTURAS, "a") as file:
        file.write(factura_detalles)

    messagebox.showinfo("Éxito", "Factura registrada correctamente.")
    limpiar_campos_factura()
    actualizar_lista_facturas()


def obtener_productos_seleccionados():
    productos_seleccionados = []
    # Asumimos que tienes un control para seleccionar productos y cantidades
    for item in tree_productos.selection():
        producto_codigo = tree_productos.item(item, "values")[0]
        cantidad = entry_cantidad.get()
        productos_seleccionados.append((producto_codigo, int(cantidad)))
    return productos_seleccionados


# Función para verificar si un cliente existe
def verificar_cliente_existente(cliente_id):
    if os.path.exists(ARCHIVO_CLIENTES):
        with open(ARCHIVO_CLIENTES, "r") as file:
            for linea in file:
                datos = linea.strip().split(",")
                if datos[0] == cliente_id:
                    return True
    return False


# Función para verificar si un vendedor existe
def verificar_vendedor_existente(vendedor_id):
    if os.path.exists(ARCHIVO_VENDEDORES):
        with open(ARCHIVO_VENDEDORES, "r") as file:
            for linea in file:
                datos = linea.strip().split(",")
                if datos[0] == vendedor_id:
                    return True
    return False


# Función para verificar si un producto existe
def verificar_producto_existente(codigo_producto):
    if os.path.exists(ARCHIVO_PRODUCTOS):
        with open(ARCHIVO_PRODUCTOS, "r") as file:
            for linea in file:
                datos = linea.strip().split(",")
                if datos[0] == codigo_producto:
                    return True
    return False


# Función para obtener el precio de un producto
def obtener_precio_producto(codigo_producto):
    if os.path.exists(ARCHIVO_PRODUCTOS):
        with open(ARCHIVO_PRODUCTOS, "r") as file:
            for linea in file:
                datos = linea.strip().split(",")
                if datos[0] == codigo_producto:
                    return float(datos[2])  # Suponiendo que el precio está en la posición 2
    return 0.0


# Función para verificar si hay suficiente stock
def verificar_stock_producto(codigo_producto, cantidad):
    if os.path.exists(ARCHIVO_PRODUCTOS):
        with open(ARCHIVO_PRODUCTOS, "r") as file:
            for linea in file:
                datos = linea.strip().split(",")
                if datos[0] == codigo_producto:
                    stock = int(datos[3])  # Suponiendo que el stock está en la posición 3
                    return stock >= cantidad
    return False


# Función para descontar el stock
def descontar_stock_producto(codigo_producto, cantidad):
    lineas = []
    with open(ARCHIVO_PRODUCTOS, "r") as file:
        lineas = file.readlines()

    with open(ARCHIVO_PRODUCTOS, "w") as file:
        for linea in lineas:
            datos = linea.strip().split(",")
            if datos[0] == codigo_producto:
                stock_actual = int(datos[3])
                stock_actual -= cantidad
                datos[3] = str(stock_actual)
            file.write(",".join(datos) + "\n")


# Función para mostrar facturas
def mostrar_facturas():
    if os.path.exists(ARCHIVO_FACTURAS):
        with open(ARCHIVO_FACTURAS, "r") as file:
            lista_facturas.delete("1.0", tk.END)
            for linea in file:
                lista_facturas.insert(tk.END, linea)
    else:
        messagebox.showerror("Error", "No hay facturas registradas")


# Actualizar la lista de facturas
def actualizar_lista_facturas():
    lista_facturas.delete("1.0", tk.END)
    if os.path.exists(ARCHIVO_FACTURAS):
        with open(ARCHIVO_FACTURAS, "r") as file:
            for linea in file:
                lista_facturas.insert(tk.END, linea)


# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Facturación")
root.geometry("800x600")

# Frame de inicio de sesión
frame_login = ttk.Frame(root)
frame_login.pack(fill="both", expand=True)

tk.Label(frame_login, text="Usuario:").pack()
entry_usuario_login = tk.Entry(frame_login)
entry_usuario_login.pack()

tk.Label(frame_login, text="Contraseña:").pack()
entry_contraseña_login = tk.Entry(frame_login, show="*")
entry_contraseña_login.pack()

tk.Button(frame_login, text="Iniciar Sesión", command=iniciar_sesion).pack(pady=5)

# Botón de cerrar sesión (inicialmente oculto)
boton_cerrar_sesion = tk.Button(root, text="Cerrar Sesión", command=cerrar_sesion)

# Notebook para los módulos
notebook = ttk.Notebook(root)

# Frame para clientes
frame_clientes = ttk.Frame(notebook)
notebook.add(frame_clientes, text="Clientes")

# Widgets para clientes

tk.Label(frame_clientes,text="ID Cliente:").pack() #<-Posiciona el widget en la ventana de manera automatica
entry_id=tk.Entry(frame_clientes)
entry_id.pack()

tk.Label(frame_clientes,text="Nombre Cliente: ").pack()
entry_cliente=tk.Entry(frame_clientes)
entry_cliente.pack()

tk.Label(frame_clientes,text="Direccion: ").pack()
entry_direccion=tk.Entry(frame_clientes)
entry_direccion.pack()

tk.Label(frame_clientes,text="Telefono: ").pack()
entry_telefono=tk.Entry(frame_clientes)
entry_telefono.pack()

tk.Label(frame_clientes,text="E-Mail: ").pack()
entry_email=tk.Entry(frame_clientes)
entry_email.pack()

#botones de accion


tk.Button(frame_clientes,text="Registrar Cliete",command=registrar_cliente).pack(pady=5)
tk.Button(frame_clientes,text="Modificar Informacion de cliente existente",command=modificar_cliente).pack(pady=5)
tk.Button(frame_clientes,text="Eliminar Cliente",command=eliminar_cliente).pack(pady=5)
tk.Button(frame_clientes,text="Buscar Cliente ",command=buscar_cliente).pack(pady=5)
tk.Button(frame_clientes,text="Mostrar Clientes",command=mostrar_clientes).pack(pady=5)

#area de texto para listar clientes

lista_clientes = tk.Text(frame_clientes,height=10,width=100)
lista_clientes.pack(pady=5)

# Frame para vendedores
frame_vendedores = ttk.Frame(notebook)
notebook.add(frame_vendedores, text="Vendedores")

# Widgets para vendedores
tk.Label(frame_vendedores, text="ID Vendedor:").pack()
entry_id_vendedor = tk.Entry(frame_vendedores)
entry_id_vendedor.pack()

tk.Label(frame_vendedores, text="Nombre Vendedor:").pack()
entry_nombre_vendedor = tk.Entry(frame_vendedores)
entry_nombre_vendedor.pack()

tk.Label(frame_vendedores, text="Dirección:").pack()
entry_direccion_vendedor = tk.Entry(frame_vendedores)
entry_direccion_vendedor.pack()

tk.Label(frame_vendedores, text="Teléfono:").pack()
entry_telefono_vendedor = tk.Entry(frame_vendedores)
entry_telefono_vendedor.pack()

tk.Label(frame_vendedores, text="E-Mail:").pack()
entry_email_vendedor = tk.Entry(frame_vendedores)
entry_email_vendedor.pack()

tk.Button(frame_vendedores, text="Registrar Vendedor", command=registrar_vendedor).pack(pady=5)
tk.Button(frame_vendedores, text="Mostrar Vendedores", command=mostrar_vendedores).pack(pady=5)

lista_vendedores = tk.Text(frame_vendedores, height=10, width=80)
lista_vendedores.pack(pady=5)

# Frame para productos
frame_productos = ttk.Frame(notebook)
notebook.add(frame_productos, text="Productos")

# Widgets para productos
tk.Label(frame_productos, text="Código:").grid(row=0, column=0)
entry_codigo_producto = tk.Entry(frame_productos)
entry_codigo_producto.grid(row=0, column=1)

tk.Label(frame_productos, text="Nombre:").grid(row=1, column=0)
entry_nombre_producto = tk.Entry(frame_productos)
entry_nombre_producto.grid(row=1, column=1)

tk.Label(frame_productos, text="Precio:").grid(row=2, column=0)
entry_precio_producto = tk.Entry(frame_productos)
entry_precio_producto.grid(row=2, column=1)

tk.Label(frame_productos, text="Stock:").grid(row=3, column=0)
entry_stock_producto = tk.Entry(frame_productos)
entry_stock_producto.grid(row=3, column=1)

tk.Button(frame_productos, text="Agregar Producto", command=agregar_producto).grid(row=4, column=0, pady=5)

tree_productos = ttk.Treeview(frame_productos, columns=("Código", "Nombre", "Precio", "Stock"), show="headings")
tree_productos.heading("Código", text="Código")
tree_productos.heading("Nombre", text="Nombre")
tree_productos.heading("Precio", text="Precio")
tree_productos.heading("Stock", text="Stock")
tree_productos.grid(row=5, column=0, columnspan=2, pady=5)

# Frame para pedidos
frame_pedidos = ttk.Frame(notebook)
notebook.add(frame_pedidos, text="Pedidos")

# Widgets para pedidos
tk.Label(frame_pedidos, text="Cliente:").pack()
entry_cliente_pedido = tk.Entry(frame_pedidos)
entry_cliente_pedido.pack()

tk.Label(frame_pedidos, text="Código Producto:").pack()
entry_producto_pedido = tk.Entry(frame_pedidos)
entry_producto_pedido.pack()

tk.Label(frame_pedidos, text="Cantidad:").pack()
entry_cantidad_pedido = tk.Entry(frame_pedidos)
entry_cantidad_pedido.pack()

tk.Button(frame_pedidos, text="Registrar Pedido", command=registrar_pedido).pack(pady=5)

tree_pedidos = ttk.Treeview(frame_pedidos, columns=("Cliente", "Producto", "Cantidad", "Estado"), show="headings")
tree_pedidos.heading("Cliente", text="Cliente")
tree_pedidos.heading("Producto", text="Producto")
tree_pedidos.heading("Cantidad", text="Cantidad")
tree_pedidos.heading("Estado", text="Estado")
tree_pedidos.pack(pady=5)

tk.Button(frame_pedidos, text="Despachar Pedido", command=despachar_pedido).pack(pady=5)

# Frame para usuarios
frame_usuarios = ttk.Frame(notebook)
notebook.add(frame_usuarios, text="Usuarios")

# Widgets para usuarios
tk.Label(frame_usuarios, text="Usuario:").pack()
entry_usuario = tk.Entry(frame_usuarios)
entry_usuario.pack()

tk.Label(frame_usuarios, text="Contraseña:").pack()
entry_contraseña = tk.Entry(frame_usuarios, show="*")
entry_contraseña.pack()

tk.Label(frame_usuarios, text="Rol:").pack()
combo_rol = ttk.Combobox(frame_usuarios, values=["admin", "vendedor", "cliente"])
combo_rol.pack()

tk.Button(frame_usuarios, text="Registrar Usuario", command=registrar_usuario).pack(pady=5)

#Frame para Factura
frame_factura = ttk.Frame(notebook)
notebook.add(frame_factura, text="Facturas")

tk.Label(frame_factura, text="ID Cliente:").grid(row=0, column=0)
entry_cliente_id = tk.Entry(frame_factura)
entry_cliente_id.grid(row=0, column=1)

tk.Label(frame_factura, text="ID Vendedor:").grid(row=1, column=0)
entry_vendedor_id = tk.Entry(frame_factura)
entry_vendedor_id.grid(row=1, column=1)

tk.Label(frame_factura, text="Cantidad de Producto:").grid(row=2, column=0)
entry_cantidad = tk.Entry(frame_factura)
entry_cantidad.grid(row=2, column=1)

tk.Button(frame_factura, text="Registrar Factura", command=registrar_factura).grid(row=3, column=0, pady=5)
tk.Button(frame_factura, text="Mostrar Facturas", command=mostrar_facturas).grid(row=3, column=1, pady=5)

lista_facturas = tk.Text(frame_factura, height=10, width=100)
lista_facturas.grid(pady=5)

# Treeview de productos
columns = ("Código", "Nombre", "Precio", "Stock")
tree_productos = ttk.Treeview(frame_factura, columns=columns, show="headings", height=10)
tree_productos.grid(pady=10)

for col in columns:
    tree_productos.heading(col, text=col)

# Cargar datos al inicio
cargar_productos()
cargar_pedidos()
actualizar_lista_productos()
actualizar_lista_pedidos()

# Iniciar la aplicación
root.mainloop()