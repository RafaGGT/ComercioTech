from service.PedidoService import PedidoService


class PedidoController:
    def __init__(self, service=None):
        self._service = service or PedidoService()
    # Método para crear un nuevo pedido, validando los datos y manejando excepciones.
    def crear_pedido(self, cliente_correo, metodo_pago, direccion_envio, items):
        return self._service.crear(
            cliente_correo, metodo_pago, direccion_envio, items
        )
    # Método para obtener todos los pedidos de la base de datos.
    def obtener_pedidos(self):
        return self._service.obtener_todos()
    # Método para obtener un pedido por su ID, devolviendo None si no se encuentra.
    def obtener_pedido(self, pedido_id):
        return self._service.obtener_por_id(pedido_id)
    # Método para cambiar el estado de un pedido, validando que el pedido exista y manejando excepciones.
    def cambiar_estado(self, pedido_id, estado):
        return self._service.cambiar_estado(pedido_id, estado)
    # Método para eliminar un pedido, validando que el pedido exista y manejando excepciones.
    def eliminar_pedido(self, pedido_id):
        return self._service.eliminar(pedido_id)
