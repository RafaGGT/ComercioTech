from model.Conexion import Conexion
from model.Pedido import Pedido
from service.ContadorService import ContadorService

class PedidoService:
    # Constructor de la clase PedidoService, que recibe una instancia de la base de datos.
    def __init__(self, db=None):
        self._db = db if db is not None else Conexion.get_db()
        self._pedidos = self._db["pedidos"]
        self._clientes = self._db["clientes"]
        self._productos = self._db["productos"]
        self._contador_service = ContadorService(self._db)

    @staticmethod
    def _id(valor, entidad="pedido"):
        try:
            return int(valor)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"El ID de {entidad} no es válido.") from exc
        
    # Método estático para validar y convertir un valor a ObjectId, lanzando un ValueError si no es válido.
    def crear(self, cliente_correo, metodo_pago, direccion_envio, items):
        correo = cliente_correo.strip().lower()
        if not self._clientes.find_one({"correo": correo}):
            raise ValueError("El cliente indicado no existe.")
        if not items:
            raise ValueError("El pedido debe incluir al menos un producto.")
        # Validar y procesar los items del pedido, reservando stock y calculando el total.
        detalle = []
        reservados = []
        try:
            for item in items:
                producto_id = self._id(item["producto_id"], "producto")
                cantidad = int(item["cantidad"])
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor que cero.")

                producto = self._productos.find_one_and_update(
                    {"_id": producto_id, "stock": {"$gte": cantidad}},
                    {"$inc": {"stock": -cantidad}},
                )
                if not producto:
                    raise ValueError(
                        f"Producto {item['producto_id']} inexistente o sin stock suficiente."
                    )
                reservados.append((producto_id, cantidad))
                detalle.append(
                    {
                        "producto_id": producto_id,
                        "nombre": producto["nombre"],
                        "cantidad": cantidad,
                        "precio_unitario": float(producto["precio"]),
                        "subtotal": round(float(producto["precio"]) * cantidad, 2),
                    }
                )

            total = round(sum(item["subtotal"] for item in detalle), 2)

            # Obtener el siguiente ID para el pedido antes de crear el objeto Pedido
            nuevo_id = self._contador_service.obtener_siguiente_id("pedidos")

            pedido = Pedido(
                correo,
                metodo_pago,
                direccion_envio,
                items=detalle,
                total=total,
            )
            documento = pedido.to_document()
            documento["_id"] = nuevo_id 
            
            self._pedidos.insert_one(documento)
            pedido.id = nuevo_id
            return pedido
        except Exception:
            for producto_id, cantidad in reservados:
                self._productos.update_one(
                    {"_id": producto_id}, {"$inc": {"stock": cantidad}}
                )
            raise
    # Método para obtener todos los pedidos de la base de datos, ordenados por fecha de creación descendente.
    def obtener_todos(self):
        return [
            Pedido.from_document(doc)
            for doc in self._pedidos.find().sort("fecha_creacion", -1)
        ]
    # Método para obtener un pedido por su ID, devolviendo None si no se encuentra.
    def obtener_por_id(self, pedido_id):
        doc = self._pedidos.find_one({"_id": self._id(pedido_id)})
        return Pedido.from_document(doc) if doc else None
    # Método para cambiar el estado de un pedido, verificando que la transición de estado sea válida y actualizando el stock si se cancela el pedido.
    def cambiar_estado(self, pedido_id, estado):
        oid = self._id(pedido_id)
        actual = self._pedidos.find_one({"_id": oid})
        if not actual:
            return False
        # Validar la transición de estado según las reglas definidas en la clase Pedido
        estado_nuevo = Pedido("cliente", "pago", "direccion", estado=estado).estado
        estado_actual = actual.get("estado", "pendiente")
        # Definir las transiciones de estado permitidas
        transiciones = {
            "pendiente": {"enviado", "cancelado"},
            "enviado": {"entregado"},
            "entregado": set(),
            "cancelado": set(),
        }
        # Verificar si la transición de estado es válida
        if estado_nuevo == estado_actual:
            return True
        if estado_nuevo not in transiciones.get(estado_actual, set()):
            raise ValueError(
                f"No se permite cambiar un pedido de {estado_actual} a {estado_nuevo}."
            )
        # Actualizar el estado del pedido en la base de datos
        resultado = self._pedidos.update_one(
            {"_id": oid, "estado": estado_actual}, {"$set": {"estado": estado_nuevo}}
        )
        # Verificar si la actualización afectó algún documento; si no, significa que el pedido fue modificado por otra operación
        if not resultado.matched_count:
            raise RuntimeError("El pedido fue modificado por otra operación.")
        # Si el nuevo estado es "cancelado", devolver el stock de los productos del pedido
        if estado_nuevo == "cancelado":
            for item in actual.get("items", []):
                self._productos.update_one(
                    {"_id": self._id(item["producto_id"], "producto")},
                    {"$inc": {"stock": int(item["cantidad"])}},
                )
        return True
    # Método para eliminar un pedido, verificando que esté en estado "pendiente" o "cancelado" y devolviendo el stock si es necesario.
    def eliminar(self, pedido_id):
        oid = self._id(pedido_id)
        pedido = self._pedidos.find_one({"_id": oid})
        # Verificar si el pedido existe y si su estado permite la eliminación
        if not pedido:
            return False
        if pedido.get("estado") not in {"pendiente", "cancelado"}:
            raise ValueError("Solo se pueden eliminar pedidos pendientes o cancelados.")
        if pedido.get("estado") == "pendiente":
            for item in pedido.get("items", []):
                self._productos.update_one(
                    {"_id": self._id(item["producto_id"], "producto")},
                    {"$inc": {"stock": int(item["cantidad"])}},
                )
        return self._pedidos.delete_one({"_id": oid}).deleted_count > 0
