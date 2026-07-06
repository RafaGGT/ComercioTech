from model.Conexion import Conexion
from model.Producto import Producto
from service.ContadorService import ContadorService


class ProductoService:
    # Constructor de la clase ProductoService, que recibe una instancia de la base de datos.
    def __init__(self, db=None):
        database = db if db is not None else Conexion.get_db()
        self._collection = database["productos"]
        self._contador_service = ContadorService(database)

    # Método estático para validar y convertir un valor a int, lanzando un ValueError si no es válido.
    @staticmethod
    def _id(valor):
        try:
            return int(valor)
        except (TypeError, ValueError) as exc:
            raise ValueError("El ID del producto no es válido.") from exc

    # Método para agregar un nuevo producto a la base de datos.
    def agregar(self, producto):
        nuevo_id = self._contador_service.obtener_siguiente_id("productos")
        documento = producto.to_document()
        documento["_id"] = nuevo_id
        self._collection.insert_one(documento)
        producto.id = nuevo_id
        return producto

    # Método para obtener todos los productos de la base de datos, ordenados por nombre.
    def obtener_todos(self):
        return [
            Producto.from_document(doc)
            for doc in self._collection.find().sort("nombre", 1)
        ]

    # Método para obtener un producto por su ID, devolviendo None si no se encuentra.
    def obtener_por_id(self, producto_id):
        doc = self._collection.find_one({"_id": self._id(producto_id)})
        return Producto.from_document(doc) if doc else None

    # Método para modificar los datos de un producto existente en la base de datos.
    def modificar(self, producto_id, datos):
        datos.pop("_id", None)
        resultado = self._collection.update_one(
            {"_id": self._id(producto_id)}, {"$set": datos}
        )
        return resultado.matched_count > 0

    # Método para eliminar un producto de la base de datos.
    def eliminar(self, producto_id):
        resultado = self._collection.delete_one({"_id": self._id(producto_id)})
        return resultado.deleted_count > 0