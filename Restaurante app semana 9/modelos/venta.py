from datetime import datetime


class Venta:
    def __init__(
        self,
        usuario_id: str,
        producto_codigo: str,
        cantidad: int,
        fecha: str | None = None
    ) -> None:

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.cantidad = cantidad

        if fecha is None:
            self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.fecha = fecha

    def __str__(self) -> str:
        return (
            f"Usuario: {self.usuario_id} | "
            f"Producto: {self.producto_codigo} | "
            f"Cantidad: {self.cantidad} | "
            f"Fecha: {self.fecha}"
        )

    def to_dict(self) -> dict:
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad,
            "fecha": self.fecha
        }