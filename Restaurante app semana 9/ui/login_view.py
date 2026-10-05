import tkinter as tk
from tkinter import messagebox


class LoginView:

    def __init__(
        self,
        root,
        servicio,
        mostrar_principal
    ):
        self.root = root
        self.servicio = servicio
        self.mostrar_principal = mostrar_principal

        self.frame = tk.Frame(
            root,
            padx=30,
            pady=30
        )

        self.frame.pack(
            expand=True
        )

        tk.Label(
            self.frame,
            text="Restaurante App",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        tk.Label(
            self.frame,
            text="Usuario:"
        ).pack()

        self.entrada_usuario = tk.Entry(
            self.frame
        )

        self.entrada_usuario.pack(
            pady=5
        )

        tk.Label(
            self.frame,
            text="Contraseña:"
        ).pack()

        self.entrada_contrasena = tk.Entry(
            self.frame,
            show="*"
        )

        self.entrada_contrasena.pack(
            pady=5
        )

        tk.Button(
            self.frame,
            text="Ingresar",
            command=self.ingresar
        ).pack(pady=15)

        # Evento Enter para iniciar sesión
        self.entrada_contrasena.bind(
            "<Return>",
            self.ingresar
        )

    def ingresar(self, event=None):

        identificacion = (
            self.entrada_usuario.get().strip()
        )

        contrasena = (
            self.entrada_contrasena.get().strip()
        )

        if not identificacion or not contrasena:
            messagebox.showwarning(
                "Campos vacíos",
                "Ingrese usuario y contraseña."
            )
            return

        if self.servicio.validar_acceso(
            identificacion,
            contrasena
        ):

            usuario = self.servicio.buscar_usuario(
                identificacion
            )

            self.frame.destroy()

            self.mostrar_principal(
                usuario
            )

        else:

            messagebox.showerror(
                "Acceso denegado",
                "Usuario o contraseña incorrectos."
            )