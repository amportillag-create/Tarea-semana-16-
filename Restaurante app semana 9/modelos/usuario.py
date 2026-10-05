class Usuario:
    def __init__(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        contrasena: str = "",
        rol: str = "Cliente"
    ) -> None:

        if rol not in ("Administrador", "Empleado", "Cliente"):
            raise ValueError(
                "El rol debe ser Administrador, Empleado o Cliente."
            )

        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.rol = rol

    def __str__(self) -> str:
        return (
            f"ID: {self.identificacion} | "
            f"Nombre: {self.nombre} | "
            f"Correo: {self.correo} | "
            f"Rol: {self.rol}"
        )

    def to_dict(self) -> dict:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "contrasena": self.contrasena,
            "rol": self.rol
        }