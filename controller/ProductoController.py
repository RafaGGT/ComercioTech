from model.Producto import Producto
from service.ProductoService import ProductoService


class ProductoController:
    def __init__(self, service=None):
        self._service = service or ProductoService()
    # Método para agregar un nuevo producto, validando los datos y manejando excepciones.
    def agregar_producto(self, nombre, descripcion, categoria, precio, stock):
        return self._service.agregar(
            Producto(nombre, descripcion, categoria, precio, stock)
        )
    # Método para obtener todos los productos de la base de datos.
    def obtener_productos(self):
        return self._service.obtener_todos()
    # Método para obtener un producto por su ID, devolviendo None si no se encuentra.
    def obtener_producto(self, producto_id):
        return self._service.obtener_por_id(producto_id)
    # Método para modificar los datos de un producto existente, validando que el producto exista y manejando excepciones.
    def modificar_producto(self, producto_id, datos):
        actual = self._service.obtener_por_id(producto_id)
        if not actual:
            return False
        for campo, valor in datos.items():
            setattr(actual, campo, valor)
        return self._service.modificar(producto_id, actual.to_document())
    # Método para eliminar un producto, validando que el producto exista y manejando excepciones.
    def eliminar_producto(self, producto_id):
        return self._service.eliminar(producto_id)
