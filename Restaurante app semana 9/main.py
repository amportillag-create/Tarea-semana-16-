import tkinter as tk

from servicios.restaurante import Restaurante
from servicios.archivo_servicio import ArchivoServicio

from ui.login_view import LoginView
from ui.main_view import MainView


class Aplicacion:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Restaurante App"
        )

        self.root.geometry(
            "900x700"
        )

        self.root.resizable(
            False,
            False
        )

        # ========================================
        # SERVICIOS
        # ========================================

        self.restaurante = Restaurante()

        self.archivo = ArchivoServicio(
            "datos/productos.json"
        )

        # ========================================
        # CARGAR PRODUCTOS
        # ========================================

        productos_cargados = (
            self.archivo.cargar_productos()
        )

        self.restaurante.cargar_productos(
            productos_cargados
        )

        # ========================================
        # CARGAR USUARIOS
        # ========================================

        usuarios_cargados = (
            self.archivo.cargar_usuarios()
        )

        self.restaurante.cargar_usuarios(
            usuarios_cargados
        )

        # ========================================
        # CARGAR VENTAS
        # ========================================

        ventas_cargadas = (
            self.archivo.cargar_ventas()
        )

        self.restaurante.cargar_ventas(
            ventas_cargadas
        )

        # ========================================
        # MOSTRAR LOGIN
        # ========================================

        self.mostrar_login()

    # ========================================
    # LIMPIAR VENTANA
    # ========================================

    def limpiar_ventana(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    # ========================================
    # GUARDAR PRODUCTOS
    # ========================================

    def guardar_productos(self):

        self.archivo.guardar_productos(
            self.restaurante.listar_productos()
        )

    # ========================================
    # GUARDAR USUARIOS
    # ========================================

    def guardar_usuarios(self):

        self.archivo.guardar_usuarios(
            self.restaurante.listar_usuarios()
        )

    # ========================================
    # GUARDAR VENTAS
    # ========================================

    def guardar_ventas(self):

        self.archivo.guardar_ventas(
            self.restaurante.listar_ventas()
        )

    # ========================================
    # LOGIN
    # ========================================

    def mostrar_login(self):

        self.limpiar_ventana()

        LoginView(
            self.root,
            self.restaurante,
            self.mostrar_principal
        )

    # ========================================
    # PRINCIPAL
    # ========================================

    def mostrar_principal(
        self,
        usuario_actual
    ):

        self.limpiar_ventana()

        MainView(
            self.root,
            self.restaurante,
            self.mostrar_login,
            self.guardar_productos,
            self.guardar_usuarios,
            self.guardar_ventas,
            usuario_actual
        )


def main():

    root = tk.Tk()

    Aplicacion(root)

    root.mainloop()


if __name__ == "__main__":
    main()