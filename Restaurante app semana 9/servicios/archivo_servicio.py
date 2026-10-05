import json
from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class ArchivoServicio:

    def __init__(
        self,
        ruta_archivo: str,
        ruta_usuarios: str | None = None,
        ruta_ventas: str | None = None
    ) -> None:

        self.ruta_archivo = Path(ruta_archivo)

        if ruta_usuarios is None:
            self.ruta_usuarios = (
                self.ruta_archivo.parent / "usuarios.json"
            )
        else:
            self.ruta_usuarios = Path(ruta_usuarios)

        if ruta_ventas is None:
            self.ruta_ventas = (
                self.ruta_archivo.parent / "ventas.json"
            )
        else:
            self.ruta_ventas = Path(ruta_ventas)

    # =================================================
    # PRODUCTOS
    # =================================================

    def guardar_productos(
        self,
        productos: list[Producto]
    ) -> None:

        datos = [
            producto.to_dict()
            for producto in productos
        ]

        self.ruta_archivo.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.ruta_archivo,
            "w",
            encoding="utf-8"
        ) as archivo:

            json.dump(
                datos,
                archivo,
                indent=4,
                ensure_ascii=False
            )

    def cargar_productos(self) -> list[Producto]:

        try:
            with open(
                self.ruta_archivo,
                "r",
                encoding="utf-8"
            ) as archivo:

                datos = json.load(archivo)

            if not isinstance(datos, list):
                print(
                    "Error: productos.json debe contener una lista."
                )
                return []

            productos = []

            for registro in datos:
                try:
                    producto = Producto(
                        registro["codigo"],
                        registro["nombre"],
                        registro["categoria"],
                        float(registro["precio"]),
                        int(registro["stock"])
                    )

                    productos.append(producto)

                except KeyError as error:
                    print(
                        f"Error: falta el campo {error} "
                        "en productos.json."
                    )

                except ValueError as error:
                    print(
                        f"Error en los datos del producto: {error}"
                    )

            return productos

        except FileNotFoundError:
            return []

        except json.JSONDecodeError:
            print(
                "Error: productos.json contiene JSON inválido."
            )
            return []

        except PermissionError:
            print(
                "Error: no hay permisos para leer productos.json."
            )
            return []

    # =================================================
    # USUARIOS
    # =================================================

    def guardar_usuarios(
        self,
        usuarios: list[Usuario]
    ) -> None:

        datos = [
            usuario.to_dict()
            for usuario in usuarios
        ]

        self.ruta_usuarios.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.ruta_usuarios,
            "w",
            encoding="utf-8"
        ) as archivo:

            json.dump(
                datos,
                archivo,
                indent=4,
                ensure_ascii=False
            )

    def cargar_usuarios(self) -> list[Usuario]:

        try:
            with open(
                self.ruta_usuarios,
                "r",
                encoding="utf-8"
            ) as archivo:

                datos = json.load(archivo)

            if not isinstance(datos, list):
                print(
                    "Error: usuarios.json debe contener una lista."
                )
                return []

            usuarios = []

            for registro in datos:
                try:
                    usuario = Usuario(
                        registro["identificacion"],
                        registro["nombre"],
                        registro["correo"],
                        registro.get("contrasena", ""),
                        registro.get("rol", "Cliente")
                    )

                    usuarios.append(usuario)

                except KeyError as error:
                    print(
                        f"Error: falta el campo {error} "
                        "en usuarios.json."
                    )

                except ValueError as error:
                    print(
                        f"Error en los datos del usuario: {error}"
                    )

            return usuarios

        except FileNotFoundError:
            return []

        except json.JSONDecodeError:
            print(
                "Error: usuarios.json contiene JSON inválido."
            )
            return []

        except PermissionError:
            print(
                "Error: no hay permisos para leer usuarios.json."
            )
            return []

    # =================================================
    # VENTAS
    # =================================================

    def guardar_ventas(
        self,
        ventas: list[Venta]
    ) -> None:

        datos = [
            venta.to_dict()
            for venta in ventas
        ]

        self.ruta_ventas.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.ruta_ventas,
            "w",
            encoding="utf-8"
        ) as archivo:

            json.dump(
                datos,
                archivo,
                indent=4,
                ensure_ascii=False
            )

    def cargar_ventas(self) -> list[Venta]:

        try:
            with open(
                self.ruta_ventas,
                "r",
                encoding="utf-8"
            ) as archivo:

                datos = json.load(archivo)

            if not isinstance(datos, list):
                print(
                    "Error: ventas.json debe contener una lista."
                )
                return []

            ventas = []

            for registro in datos:
                try:
                    venta = Venta(
                        registro["usuario_id"],
                        registro["producto_codigo"],
                        int(registro["cantidad"]),
                        registro.get("fecha")
                    )

                    ventas.append(venta)

                except KeyError as error:
                    print(
                        f"Error: falta el campo {error} "
                        "en ventas.json."
                    )

                except ValueError as error:
                    print(
                        f"Error en los datos de la venta: {error}"
                    )

            return ventas

        except FileNotFoundError:
            return []

        except json.JSONDecodeError:
            print(
                "Error: ventas.json contiene JSON inválido."
            )
            return []

        except PermissionError:
            print(
                "Error: no hay permisos para leer ventas.json."
            )
            return []