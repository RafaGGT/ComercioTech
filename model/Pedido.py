from datetime import datetime, timezone


class Pedido:
    # Definición de los estados válidos para un pedido
    ESTADOS = {"pendiente", "enviado", "entregado", "cancelado"}
    # Constructor de la clase Pedido
    def __init__(
        self,
        cliente_id,
        metodo_pago,
        direccion_envio,
        items=None,
        estado="pendiente",
        total=0,
        fecha_creacion=None,
        id=None,
    ):
        self.id = id
        self.cliente_id = self._texto(cliente_id, "El cliente")
        self.metodo_pago = self._texto(metodo_pago, "El método de pago")
        self.direccion_envio = self._texto(direccion_envio, "La dirección de envío")
        self.items = list(items or [])
        self.estado = estado
        self.total = float(total)
        self.fecha_creacion = fecha_creacion or datetime.now(timezone.utc)
    # Método estático para validar y limpiar texto
    @staticmethod
    def _texto(valor, campo):
        valor = str(valor).strip()
        if not valor:
            raise ValueError(f"{campo} no puede estar vacío.")
        return valor

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        valor = str(valor).strip().lower()
        if valor not in self.ESTADOS:
            raise ValueError(f"Estado inválido. Use: {', '.join(sorted(self.ESTADOS))}.")
        self._estado = valor
    # Método para representar el objeto Pedido como un diccionario (documento)
    def to_document(self):
        return {
            "cliente_id": self.cliente_id,
            "metodo_pago": self.metodo_pago,
            "direccion_envio": self.direccion_envio,
            "items": self.items,
            "estado": self.estado,
            "total": round(self.total, 2),
            "fecha_creacion": self.fecha_creacion,
        }
    # Método de clase para crear una instancia de Pedido a partir de un documento (diccionario)
    @classmethod
    def from_document(cls, documento):
        return cls(
            documento["cliente_id"],
            documento["metodo_pago"],
            documento["direccion_envio"],
            items=documento.get("items", []),
            estado=documento.get("estado", "pendiente"),
            total=documento.get("total", 0),
            fecha_creacion=documento.get("fecha_creacion"),
            id=str(documento["_id"]) if documento.get("_id") else None,
        )
    # Método para representar el objeto Pedido como una cadena de texto
    def __str__(self):
        return (
            f"Pedido [{self.id or '-'}] | cliente: {self.cliente_id} | "
            f"estado: {self.estado} | total: ${self.total:,.2f} | "
            f"ítems: {len(self.items)}"
        )
