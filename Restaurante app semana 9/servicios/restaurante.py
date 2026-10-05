from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class Restaurante:

    def __init__(self) -> None:
        # ========================================
        # COLECCIONES PRINCIPALES
        # ========================================

        self.productos: list[Producto] = []
        self.usuarios: list[Usuario] = []
        self.ventas: list[Venta] = []

        # ========================================
        # ÍNDICES AUXILIARES
        # ========================================

        self.indice_productos: dict[str, Producto] = {}
        self.indice_usuarios: dict[str, Usuario] = {}
        self.ventas_por_usuario: dict[str, list[Venta]] = {}

        # ========================================
        # MENÚ
        # ========================================

        self.opciones_menu: tuple[str, ...] = (
            "Registrar producto",
            "Buscar producto",
            "Actualizar producto",
            "Eliminar producto",
            "Listar productos",
            "Registrar usuario",
            "Listar usuarios",
            "Realizar venta",
            "Consultar ventas por usuario",
            "Mostrar categorías",
            "Salir"
        )

        self.menu: dict[int, str] = {
            1: "Registrar producto",
            2: "Buscar producto",
            3: "Actualizar producto",
            4: "Eliminar producto",
            5: "Listar productos",
            6: "Registrar usuario",
            7: "Listar usuarios",
            8: "Realizar venta",
            9: "Consultar ventas por usuario",
            10: "Mostrar categorías",
            11: "Salir"
        }

    # ========================================
    # PRODUCTOS
    # ========================================

    def registrar_producto(self, producto: Producto) -> bool:
        if producto.codigo in self.indice_productos:
            return False

        self.productos.append(producto)
        self.indice_productos[producto.codigo] = producto

        return True

    def buscar_producto(self, codigo: str) -> Producto | None:
        return self.indice_productos.get(codigo)

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int | None = None
    ) -> bool:

        producto = self.buscar_producto(codigo)

        if producto is None:
            return False

        if precio < 0:
            return False

        if stock is not None and stock < 0:
            return False

        producto.nombre = nombre
        producto.categoria = categoria
        producto.precio = precio

        if stock is not None:
            producto.stock = stock

        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)

        if producto is None:
            return False

        self.productos.remove(producto)
        del self.indice_productos[codigo]

        return True

    def listar_productos(self) -> list[Producto]:
        return self.productos.copy()

    def cargar_productos(self, productos: list[Producto]) -> None:
        self.productos = productos.copy()

        self.indice_productos = {
            producto.codigo: producto
            for producto in self.productos
        }

    # ========================================
    # USUARIOS
    # ========================================

    def registrar_usuario(self, usuario: Usuario) -> bool:
        if usuario.identificacion in self.indice_usuarios:
            return False

        self.usuarios.append(usuario)

        self.indice_usuarios[usuario.identificacion] = usuario

        self.ventas_por_usuario.setdefault(
            usuario.identificacion,
            []
        )

        return True

    def buscar_usuario(
        self,
        identificacion: str
    ) -> Usuario | None:

        return self.indice_usuarios.get(identificacion)

    def listar_usuarios(self) -> list[Usuario]:
        return self.usuarios.copy()

    def actualizar_usuario(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        rol: str,
        contrasena: str | None = None
    ) -> bool:

        usuario = self.buscar_usuario(identificacion)

        if usuario is None:
            return False

        if rol not in (
            "Administrador",
            "Empleado",
            "Cliente"
        ):
            return False

        usuario.nombre = nombre
        usuario.correo = correo
        usuario.rol = rol

        if contrasena:
            usuario.contrasena = contrasena

        return True

    def eliminar_usuario(
        self,
        identificacion: str,
        identificacion_actual: str | None = None
    ) -> bool:

        usuario = self.buscar_usuario(identificacion)

        if usuario is None:
            return False

        # Evita que el administrador elimine
        # accidentalmente su propia cuenta.
        if (
            identificacion_actual is not None
            and identificacion == identificacion_actual
        ):
            return False

        self.usuarios.remove(usuario)
        del self.indice_usuarios[identificacion]

        self.ventas_por_usuario.pop(
            identificacion,
            None
        )

        return True

    def cargar_usuarios(self, usuarios: list[Usuario]) -> None:
        self.usuarios = usuarios.copy()

        self.indice_usuarios = {
            usuario.identificacion: usuario
            for usuario in self.usuarios
        }

        for usuario in self.usuarios:
            self.ventas_por_usuario.setdefault(
                usuario.identificacion,
                []
            )

    # ========================================
    # PERMISOS
    # ========================================

    def es_administrador(
        self,
        identificacion: str
    ) -> bool:

        usuario = self.buscar_usuario(identificacion)

        if usuario is None:
            return False

        return usuario.rol == "Administrador"

    # ========================================
    # VALIDAR ACCESO
    # ========================================

    def validar_acceso(
        self,
        identificacion: str,
        contrasena: str
    ) -> bool:

        usuario = self.buscar_usuario(identificacion)

        if usuario is None:
            return False

        return usuario.contrasena == contrasena

    # ========================================
    # VENTAS
    # ========================================

    def vender_producto(
        self,
        codigo_producto: str,
        identificacion_usuario: str,
        cantidad: int
    ) -> bool:

        usuario = self.buscar_usuario(
            identificacion_usuario
        )

        producto = self.buscar_producto(
            codigo_producto
        )

        if usuario is None or producto is None:
            return False

        if cantidad <= 0:
            return False

        if producto.stock < cantidad:
            return False

        venta = Venta(
            usuario.identificacion,
            producto.codigo,
            cantidad
        )

        self.ventas.append(venta)

        self.ventas_por_usuario.setdefault(
            usuario.identificacion,
            []
        ).append(venta)

        producto.vender(cantidad)

        return True

    def listar_ventas(self) -> list[Venta]:
        return self.ventas.copy()

    def cargar_ventas(
        self,
        ventas: list[Venta]
    ) -> None:

        self.ventas = ventas.copy()
        self.ventas_por_usuario = {}

        for venta in self.ventas:
            self.ventas_por_usuario.setdefault(
                venta.usuario_id,
                []
            ).append(venta)

    def consultar_ventas_usuario(
        self,
        identificacion_usuario: str
    ) -> list[Venta]:

        return self.ventas_por_usuario.get(
            identificacion_usuario,
            []
        ).copy()

    # ========================================
    # CATEGORÍAS
    # ========================================

    def obtener_categorias(self) -> set[str]:
        return {
            producto.categoria
            for producto in self.productos
        }

    # ========================================
    # MENÚ DE CONSOLA
    # ========================================

    def mostrar_menu(self) -> None:
        print("\n========================================")
        print("        SISTEMA DE RESTAURANTE")
        print("========================================")

        for numero, opcion in self.menu.items():

            if numero == 6:
                print("----------------------------------------")

            if numero == 8:
                print("----------------------------------------")

            if numero == 10:
                print("----------------------------------------")

            print(f"{numero}. {opcion}")