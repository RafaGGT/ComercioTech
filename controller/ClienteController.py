from model.Cliente import Cliente
from service.ClienteService import ClienteService


class ClienteController:
    def __init__(self, service=None):
        self._service = service or ClienteService()

    def agregar_cliente(self, nombre, apellido, correo, telefono, direccion):
        return self._service.agregar(
            Cliente(nombre, apellido, correo, telefono, direccion)
        )

    def obtener_clientes(self):
        return self._service.obtener_todos()

    def obtener_cliente_por_correo(self, correo):
        return self._service.obtener_por_correo(correo)

    def obtener_cliente(self, cliente_id):
        return self._service.obtener_por_id(cliente_id)

    def modificar_cliente(self, correo, datos):
        actual = self._service.obtener_por_correo(correo)
        if not actual:
            return False
        actual.modificar_cliente(**datos)
        return self._service.modificar(correo, actual.to_document())

    def eliminar_cliente(self, correo):
        return self._service.eliminar(correo)
