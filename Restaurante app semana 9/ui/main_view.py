import tkinter as tk
from tkinter import ttk, messagebox

from modelos.producto import Producto
from modelos.usuario import Usuario


class MainView:
    def __init__(
        self,
        root,
        servicio,
        cerrar_sesion,
        guardar_productos,
        guardar_usuarios,
        guardar_ventas,
        usuario_actual
    ):
        self.root = root
        self.servicio = servicio
        self.cerrar_sesion = cerrar_sesion
        self.guardar_productos = guardar_productos
        self.guardar_usuarios = guardar_usuarios
        self.guardar_ventas = guardar_ventas
        self.usuario_actual = usuario_actual

        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(fill="both", expand=True)

        self.contenido = tk.Frame(self.frame)
        self.contenido.pack(fill="both", expand=True)

        self.crear_menu()
        self.mostrar_inicio()

    # =========================================================
    # MENÚ PRINCIPAL
    # =========================================================

    def crear_menu(self):
        encabezado = tk.Frame(self.frame)
        encabezado.pack(fill="x", pady=(0, 15))

        tk.Label(
            encabezado,
            text="Sistema de Restaurante",
            font=("Arial", 20, "bold")
        ).pack(side="left")

        nombre_usuario = (
            f"{self.usuario_actual.nombre} "
            f"({self.usuario_actual.rol})"
        )

        tk.Label(
            encabezado,
            text=nombre_usuario,
            font=("Arial", 10)
        ).pack(side="right")

        menu = tk.Frame(self.frame)
        menu.pack(fill="x", pady=(0, 10))

        tk.Button(
            menu,
            text="Productos",
            width=15,
            command=self.mostrar_productos
        ).pack(side="left", padx=5)

        self.boton_usuarios = tk.Button(
            menu,
            text="Usuarios",
            width=15,
            command=self.mostrar_usuarios
        )
        self.boton_usuarios.pack(side="left", padx=5)

        tk.Button(
            menu,
            text="Ventas",
            width=15,
            command=self.mostrar_ventas
        ).pack(side="left", padx=5)

        tk.Button(
            menu,
            text="Cerrar sesión",
            width=15,
            command=self.cerrar
        ).pack(side="right", padx=5)

        # Solo el administrador puede gestionar usuarios
        if self.usuario_actual.rol != "Administrador":
            self.boton_usuarios.config(state="disabled")

    # =========================================================
    # INICIO
    # =========================================================

    def limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):
        self.limpiar_contenido()

        tk.Label(
            self.contenido,
            text="Menú principal",
            font=("Arial", 18, "bold")
        ).pack(pady=30)

        tk.Label(
            self.contenido,
            text=f"Bienvenido/a, {self.usuario_actual.nombre}",
            font=("Arial", 13)
        ).pack(pady=10)

        tk.Label(
            self.contenido,
            text=f"Rol: {self.usuario_actual.rol}",
            font=("Arial", 12)
        ).pack(pady=5)

        if self.usuario_actual.rol == "Administrador":
            mensaje = "Tiene acceso a la gestión de productos, usuarios y ventas."
        else:
            mensaje = "Puede consultar las opciones disponibles del sistema."

        tk.Label(
            self.contenido,
            text=mensaje,
            wraplength=600,
            justify="center"
        ).pack(pady=10)

    # =========================================================
    # PRODUCTOS
    # =========================================================

    def mostrar_productos(self):
        self.limpiar_contenido()

        tk.Label(
            self.contenido,
            text="Gestión de productos",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        formulario = tk.Frame(self.contenido)
        formulario.pack(fill="x", pady=10)

        tk.Label(formulario, text="Código:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        self.entrada_codigo = tk.Entry(formulario)
        self.entrada_codigo.grid(
            row=0, column=1, padx=5, pady=5
        )

        tk.Label(formulario, text="Nombre:").grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        self.entrada_nombre_producto = tk.Entry(formulario)
        self.entrada_nombre_producto.grid(
            row=1, column=1, padx=5, pady=5
        )

        tk.Label(formulario, text="Categoría:").grid(
            row=2, column=0, padx=5, pady=5, sticky="e"
        )
        self.entrada_categoria = tk.Entry(formulario)
        self.entrada_categoria.grid(
            row=2, column=1, padx=5, pady=5
        )

        tk.Label(formulario, text="Precio:").grid(
            row=3, column=0, padx=5, pady=5, sticky="e"
        )
        self.entrada_precio = tk.Entry(formulario)
        self.entrada_precio.grid(
            row=3, column=1, padx=5, pady=5
        )

        tk.Label(formulario, text="Stock:").grid(
            row=4, column=0, padx=5, pady=5, sticky="e"
        )
        self.entrada_stock = tk.Entry(formulario)
        self.entrada_stock.grid(
            row=4, column=1, padx=5, pady=5
        )

        tk.Button(
            formulario,
            text="Registrar producto",
            command=self.registrar_producto
        ).grid(
            row=5, column=0, columnspan=2, pady=10
        )

        columnas = (
            "codigo",
            "nombre",
            "categoria",
            "precio",
            "stock"
        )

        self.tabla_productos = ttk.Treeview(
            self.contenido,
            columns=columnas,
            show="headings",
            height=10
        )

        self.tabla_productos.heading("codigo", text="Código")
        self.tabla_productos.heading("nombre", text="Nombre")
        self.tabla_productos.heading("categoria", text="Categoría")
        self.tabla_productos.heading("precio", text="Precio")
        self.tabla_productos.heading("stock", text="Stock")

        self.tabla_productos.column("codigo", width=100)
        self.tabla_productos.column("nombre", width=180)
        self.tabla_productos.column("categoria", width=150)
        self.tabla_productos.column("precio", width=100)
        self.tabla_productos.column("stock", width=100)

        self.tabla_productos.pack(
            fill="both",
            expand=True,
            pady=10
        )

        self.actualizar_tabla_productos()

    def registrar_producto(self):
        codigo = self.entrada_codigo.get().strip()
        nombre = self.entrada_nombre_producto.get().strip()
        categoria = self.entrada_categoria.get().strip()
        precio_texto = self.entrada_precio.get().strip()
        stock_texto = self.entrada_stock.get().strip()

        if not codigo or not nombre or not categoria:
            messagebox.showwarning(
                "Campos vacíos",
                "Complete todos los campos del producto."
            )
            return

        try:
            precio = float(precio_texto)
            stock = int(stock_texto)
        except ValueError:
            messagebox.showerror(
                "Datos inválidos",
                "Precio debe ser decimal y stock debe ser entero."
            )
            return

        try:
            producto = Producto(
                codigo,
                nombre,
                categoria,
                precio,
                stock
            )
        except ValueError as error:
            messagebox.showerror(
                "Error",
                str(error)
            )
            return

        if not self.servicio.registrar_producto(producto):
            messagebox.showerror(
                "Producto existente",
                "Ya existe un producto con ese código."
            )
            return

        self.guardar_productos()
        self.actualizar_tabla_productos()

        self.entrada_codigo.delete(0, tk.END)
        self.entrada_nombre_producto.delete(0, tk.END)
        self.entrada_categoria.delete(0, tk.END)
        self.entrada_precio.delete(0, tk.END)
        self.entrada_stock.delete(0, tk.END)

        messagebox.showinfo(
            "Registro exitoso",
            "Producto registrado correctamente."
        )

    def actualizar_tabla_productos(self):
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)

        for producto in self.servicio.listar_productos():
            self.tabla_productos.insert(
                "",
                tk.END,
                values=(
                    producto.codigo,
                    producto.nombre,
                    producto.categoria,
                    f"${producto.precio:.2f}",
                    producto.stock
                )
            )

    # =========================================================
    # USUARIOS
    # =========================================================

    def mostrar_usuarios(self):
        if self.usuario_actual.rol != "Administrador":
            messagebox.showerror(
                "Acceso denegado",
                "Solo el Administrador puede gestionar usuarios."
            )
            return

        self.limpiar_contenido()

        tk.Label(
            self.contenido,
            text="Gestión de usuarios",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        formulario = tk.Frame(self.contenido)
        formulario.pack(fill="x", pady=10)

        # Identificación
        tk.Label(
            formulario,
            text="Identificación:"
        ).grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )

        self.entrada_identificacion = tk.Entry(formulario)
        self.entrada_identificacion.grid(
            row=0, column=1, padx=5, pady=5
        )

        # Nombre
        tk.Label(
            formulario,
            text="Nombre:"
        ).grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )

        self.entrada_nombre_usuario = tk.Entry(formulario)
        self.entrada_nombre_usuario.grid(
            row=1, column=1, padx=5, pady=5
        )

        # Correo
        tk.Label(
            formulario,
            text="Correo:"
        ).grid(
            row=2, column=0, padx=5, pady=5, sticky="e"
        )

        self.entrada_correo = tk.Entry(formulario)
        self.entrada_correo.grid(
            row=2, column=1, padx=5, pady=5
        )

        # Contraseña
        tk.Label(
            formulario,
            text="Contraseña:"
        ).grid(
            row=3, column=0, padx=5, pady=5, sticky="e"
        )

        self.entrada_contrasena = tk.Entry(
            formulario,
            show="*"
        )
        self.entrada_contrasena.grid(
            row=3, column=1, padx=5, pady=5
        )

        # Rol
        tk.Label(
            formulario,
            text="Rol:"
        ).grid(
            row=4, column=0, padx=5, pady=5, sticky="e"
        )

        self.combo_rol = ttk.Combobox(
            formulario,
            values=(
                "Administrador",
                "Empleado",
                "Cliente"
            ),
            state="readonly",
            width=17
        )
        self.combo_rol.grid(
            row=4, column=1, padx=5, pady=5
        )
        self.combo_rol.set("Cliente")

        # Evento del Combobox
        self.combo_rol.bind(
            "<<ComboboxSelected>>",
            self.cambio_rol
        )

        self.label_rol = tk.Label(
            formulario,
            text="Rol seleccionado: Cliente"
        )
        self.label_rol.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=3
        )

        # Botones
        botones = tk.Frame(formulario)
        botones.grid(
            row=6,
            column=0,
            columnspan=2,
            pady=10
        )

        tk.Button(
            botones,
            text="Registrar",
            width=12,
            command=self.registrar_usuario
        ).pack(side="left", padx=3)

        tk.Button(
            botones,
            text="Actualizar",
            width=12,
            command=self.actualizar_usuario
        ).pack(side="left", padx=3)

        tk.Button(
            botones,
            text="Eliminar",
            width=12,
            command=self.eliminar_usuario
        ).pack(side="left", padx=3)

        tk.Button(
            botones,
            text="Limpiar",
            width=12,
            command=self.limpiar_usuario
        ).pack(side="left", padx=3)

        # Tabla
        columnas = (
            "identificacion",
            "nombre",
            "correo",
            "rol"
        )

        self.tabla_usuarios = ttk.Treeview(
            self.contenido,
            columns=columnas,
            show="headings",
            height=10
        )

        self.tabla_usuarios.heading(
            "identificacion",
            text="Identificación"
        )
        self.tabla_usuarios.heading(
            "nombre",
            text="Nombre"
        )
        self.tabla_usuarios.heading(
            "correo",
            text="Correo"
        )
        self.tabla_usuarios.heading(
            "rol",
            text="Rol"
        )

        self.tabla_usuarios.column(
            "identificacion",
            width=120
        )
        self.tabla_usuarios.column(
            "nombre",
            width=180
        )
        self.tabla_usuarios.column(
            "correo",
            width=220
        )
        self.tabla_usuarios.column(
            "rol",
            width=120
        )

        self.tabla_usuarios.pack(
            fill="both",
            expand=True,
            pady=10
        )

        # Evento Treeview
        self.tabla_usuarios.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_usuario
        )

        # Eventos de teclado
        self.entrada_identificacion.bind(
            "<Return>",
            self.registrar_usuario
        )
        self.entrada_nombre_usuario.bind(
            "<Return>",
            self.registrar_usuario
        )
        self.entrada_correo.bind(
            "<Return>",
            self.registrar_usuario
        )
        self.entrada_contrasena.bind(
            "<Return>",
            self.registrar_usuario
        )
        self.combo_rol.bind(
            "<Return>",
            self.registrar_usuario
        )

        self.entrada_identificacion.bind(
            "<Escape>",
            self.evento_escape_usuario
        )
        self.entrada_nombre_usuario.bind(
            "<Escape>",
            self.evento_escape_usuario
        )
        self.entrada_correo.bind(
            "<Escape>",
            self.evento_escape_usuario
        )
        self.entrada_contrasena.bind(
            "<Escape>",
            self.evento_escape_usuario
        )
        self.combo_rol.bind(
            "<Escape>",
            self.evento_escape_usuario
        )
        self.tabla_usuarios.bind(
            "<Escape>",
            self.evento_escape_usuario
        )

        self.actualizar_tabla_usuarios()

    # ---------------------------------------------------------
    # EVENTO DEL COMBOBOX
    # ---------------------------------------------------------

    def cambio_rol(self, event=None):
        rol = self.combo_rol.get()

        self.label_rol.config(
            text=f"Rol seleccionado: {rol}"
        )

    # ---------------------------------------------------------
    # EVENTO TREEVIEW
    # ---------------------------------------------------------

    def seleccionar_usuario(self, event=None):
        seleccion = self.tabla_usuarios.selection()

        if not seleccion:
            return

        item = seleccion[0]
        valores = self.tabla_usuarios.item(
            item,
            "values"
        )

        if not valores:
            return

        identificacion = valores[0]

        # Se consulta el usuario mediante su identificación
        usuario = self.servicio.buscar_usuario(
            identificacion
        )

        if usuario is None:
            return

        self.entrada_identificacion.config(
            state="normal"
        )
        self.entrada_identificacion.delete(
            0,
            tk.END
        )
        self.entrada_identificacion.insert(
            0,
            usuario.identificacion
        )
        self.entrada_identificacion.config(
            state="readonly"
        )

        self.entrada_nombre_usuario.delete(
            0,
            tk.END
        )
        self.entrada_nombre_usuario.insert(
            0,
            usuario.nombre
        )

        self.entrada_correo.delete(
            0,
            tk.END
        )
        self.entrada_correo.insert(
            0,
            usuario.correo
        )

        self.entrada_contrasena.delete(
            0,
            tk.END
        )
        self.entrada_contrasena.insert(
            0,
            usuario.contrasena
        )

        self.combo_rol.set(
            usuario.rol
        )

        self.label_rol.config(
            text=f"Rol seleccionado: {usuario.rol}"
        )

    # ---------------------------------------------------------
    # REGISTRAR USUARIO
    # ---------------------------------------------------------

    def registrar_usuario(self, event=None):
        identificacion = (
            self.entrada_identificacion.get().strip()
        )
        nombre = (
            self.entrada_nombre_usuario.get().strip()
        )
        correo = (
            self.entrada_correo.get().strip()
        )
        contrasena = (
            self.entrada_contrasena.get().strip()
        )
        rol = self.combo_rol.get().strip()

        if not identificacion or not nombre or not correo:
            messagebox.showwarning(
                "Campos vacíos",
                "Complete identificación, nombre y correo."
            )
            return

        if not contrasena:
            messagebox.showwarning(
                "Contraseña requerida",
                "Ingrese una contraseña."
            )
            return

        if not rol:
            messagebox.showwarning(
                "Rol requerido",
                "Seleccione un rol."
            )
            return

        try:
            usuario = Usuario(
                identificacion,
                nombre,
                correo,
                contrasena,
                rol
            )
        except ValueError as error:
            messagebox.showerror(
                "Error",
                str(error)
            )
            return

        if not self.servicio.registrar_usuario(usuario):
            messagebox.showerror(
                "Usuario existente",
                "Ya existe un usuario con esa identificación."
            )
            return

        self.guardar_usuarios()
        self.actualizar_tabla_usuarios()
        self.limpiar_usuario()

        messagebox.showinfo(
            "Registro exitoso",
            "Usuario registrado correctamente."
        )

    # ---------------------------------------------------------
    # ACTUALIZAR USUARIO
    # ---------------------------------------------------------

    def actualizar_usuario(self):
        identificacion = (
            self.entrada_identificacion.get().strip()
        )
        nombre = (
            self.entrada_nombre_usuario.get().strip()
        )
        correo = (
            self.entrada_correo.get().strip()
        )
        contrasena = (
            self.entrada_contrasena.get().strip()
        )
        rol = self.combo_rol.get().strip()

        if not identificacion:
            messagebox.showwarning(
                "Seleccione un usuario",
                "Seleccione un usuario de la tabla."
            )
            return

        if not nombre or not correo:
            messagebox.showwarning(
                "Campos vacíos",
                "Complete nombre y correo."
            )
            return

        if not rol:
            messagebox.showwarning(
                "Rol requerido",
                "Seleccione un rol."
            )
            return

        if not self.servicio.actualizar_usuario(
            identificacion,
            nombre,
            correo,
            rol,
            contrasena if contrasena else None
        ):
            messagebox.showerror(
                "Error",
                "No se pudo actualizar el usuario."
            )
            return

        self.guardar_usuarios()
        self.actualizar_tabla_usuarios()
        self.limpiar_usuario()

        messagebox.showinfo(
            "Actualización exitosa",
            "Usuario actualizado correctamente."
        )

    # ---------------------------------------------------------
    # ELIMINAR USUARIO
    # ---------------------------------------------------------

    def eliminar_usuario(self):
        identificacion = (
            self.entrada_identificacion.get().strip()
        )

        if not identificacion:
            messagebox.showwarning(
                "Seleccione un usuario",
                "Seleccione un usuario de la tabla."
            )
            return

        if identificacion == self.usuario_actual.identificacion:
            messagebox.showerror(
                "Operación no permitida",
                "No puede eliminar al usuario administrador "
                "que está actualmente conectado."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Está seguro de eliminar este usuario?"
        )

        if not confirmar:
            return

        if not self.servicio.eliminar_usuario(
            identificacion,
            self.usuario_actual.identificacion
        ):
            messagebox.showerror(
                "Error",
                "No se pudo eliminar el usuario."
            )
            return

        self.guardar_usuarios()
        self.actualizar_tabla_usuarios()
        self.limpiar_usuario()

        messagebox.showinfo(
            "Eliminación exitosa",
            "Usuario eliminado correctamente."
        )

    # ---------------------------------------------------------
    # LIMPIAR FORMULARIO
    # ---------------------------------------------------------

    def limpiar_usuario(self):
        self.entrada_identificacion.config(
            state="normal"
        )

        self.entrada_identificacion.delete(
            0,
            tk.END
        )
        self.entrada_nombre_usuario.delete(
            0,
            tk.END
        )
        self.entrada_correo.delete(
            0,
            tk.END
        )
        self.entrada_contrasena.delete(
            0,
            tk.END
        )

        self.combo_rol.set("Cliente")

        self.label_rol.config(
            text="Rol seleccionado: Cliente"
        )

        self.entrada_identificacion.focus()

        if hasattr(self, "tabla_usuarios"):
            seleccion = self.tabla_usuarios.selection()

            if seleccion:
                self.tabla_usuarios.selection_remove(
                    seleccion
                )

    def evento_escape_usuario(self, event=None):
        self.limpiar_usuario()

    def actualizar_tabla_usuarios(self):
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)

        for usuario in self.servicio.listar_usuarios():
            # La contraseña NO se muestra en la tabla
            self.tabla_usuarios.insert(
                "",
                tk.END,
                values=(
                    usuario.identificacion,
                    usuario.nombre,
                    usuario.correo,
                    usuario.rol
                )
            )

    # =========================================================
    # VENTAS
    # =========================================================

    def mostrar_ventas(self):
        self.limpiar_contenido()

        tk.Label(
            self.contenido,
            text="Gestión de ventas",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        formulario = tk.Frame(self.contenido)
        formulario.pack(fill="x", pady=10)

        # Usuario
        tk.Label(
            formulario,
            text="Usuario:"
        ).grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )

        self.combo_usuario_venta = ttk.Combobox(
            formulario,
            state="readonly",
            width=25
        )
        self.combo_usuario_venta.grid(
            row=0, column=1, padx=5, pady=5
        )

        # Producto
        tk.Label(
            formulario,
            text="Producto:"
        ).grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )

        self.combo_producto_venta = ttk.Combobox(
            formulario,
            state="readonly",
            width=25
        )
        self.combo_producto_venta.grid(
            row=1, column=1, padx=5, pady=5
        )

        # Cantidad
        tk.Label(
            formulario,
            text="Cantidad:"
        ).grid(
            row=2, column=0, padx=5, pady=5, sticky="e"
        )

        self.entrada_cantidad = tk.Entry(formulario)
        self.entrada_cantidad.grid(
            row=2, column=1, padx=5, pady=5
        )

        tk.Button(
            formulario,
            text="Registrar venta",
            command=self.registrar_venta
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            pady=10
        )

        self.combo_usuario_venta["values"] = [
            usuario.identificacion
            for usuario in self.servicio.listar_usuarios()
        ]

        self.combo_producto_venta["values"] = [
            producto.codigo
            for producto in self.servicio.listar_productos()
        ]

        columnas = (
            "usuario",
            "producto",
            "cantidad",
            "fecha"
        )

        self.tabla_ventas = ttk.Treeview(
            self.contenido,
            columns=columnas,
            show="headings",
            height=10
        )

        self.tabla_ventas.heading(
            "usuario",
            text="Usuario"
        )
        self.tabla_ventas.heading(
            "producto",
            text="Producto"
        )
        self.tabla_ventas.heading(
            "cantidad",
            text="Cantidad"
        )
        self.tabla_ventas.heading(
            "fecha",
            text="Fecha"
        )

        self.tabla_ventas.column(
            "usuario",
            width=130
        )
        self.tabla_ventas.column(
            "producto",
            width=130
        )
        self.tabla_ventas.column(
            "cantidad",
            width=100
        )
        self.tabla_ventas.column(
            "fecha",
            width=180
        )

        self.tabla_ventas.pack(
            fill="both",
            expand=True,
            pady=10
        )

        self.actualizar_tabla_ventas()

    def registrar_venta(self):
        usuario = self.combo_usuario_venta.get().strip()
        producto = self.combo_producto_venta.get().strip()
        cantidad_texto = self.entrada_cantidad.get().strip()

        if not usuario or not producto or not cantidad_texto:
            messagebox.showwarning(
                "Campos vacíos",
                "Complete todos los campos de la venta."
            )
            return

        try:
            cantidad = int(cantidad_texto)
        except ValueError:
            messagebox.showerror(
                "Cantidad inválida",
                "La cantidad debe ser un número entero."
            )
            return

        if cantidad <= 0:
            messagebox.showwarning(
                "Cantidad inválida",
                "La cantidad debe ser mayor que cero."
            )
            return

        if not self.servicio.vender_producto(
            producto,
            usuario,
            cantidad
        ):
            messagebox.showerror(
                "Error en la venta",
                "No se pudo realizar la venta. "
                "Verifique el usuario, producto y stock disponible."
            )
            return

        self.guardar_productos()
        self.guardar_ventas()

        self.actualizar_tabla_ventas()

        self.combo_usuario_venta.set("")
        self.combo_producto_venta.set("")
        self.entrada_cantidad.delete(
            0,
            tk.END
        )

        messagebox.showinfo(
            "Venta registrada",
            "La venta se registró correctamente."
        )

    def actualizar_tabla_ventas(self):
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)

        for venta in self.servicio.listar_ventas():
            self.tabla_ventas.insert(
                "",
                tk.END,
                values=(
                    venta.usuario_id,
                    venta.producto_codigo,
                    venta.cantidad,
                    venta.fecha
                )
            )

    # =========================================================
    # CERRAR SESIÓN
    # =========================================================

    def cerrar(self):
        confirmar = messagebox.askyesno(
            "Cerrar sesión",
            "¿Desea cerrar la sesión?"
        )

        if confirmar:
            self.cerrar_sesion()