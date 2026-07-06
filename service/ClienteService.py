from pymongo.errors import DuplicateKeyError

from model.Cliente import Cliente
from model.Conexion import Conexion
from service.ContadorService import ContadorService


class ClienteService:
    def __init__(self, db=None):
        self._db = db if db is not None else Conexion.get_db()
        self._collection = self._db["clientes"]
        self._contador_service = ContadorService(self._db)

    # Método estático para validar y convertir un valor a int, lanzando un ValueError si no es válido.
    @staticmethod
    def _id(valor):
        try:
            return int(valor)
        except (TypeError, ValueError) as exc:
            raise ValueError("El ID del cliente no es valido.") from exc
        
    # Método para agregar un nuevo cliente a la base de datos, validando que no exista un cliente con el mismo correo.
    def agregar(self, cliente):
        try:
            nuevo_id = self._contador_service.obtener_siguiente_id("clientes")
            documento = cliente.to_document()
            documento["_id"] = nuevo_id
            self._collection.insert_one(documento)
            cliente.id = nuevo_id
            return cliente
        except DuplicateKeyError as exc:
            raise ValueError("Ya existe un cliente con ese correo.") from exc
        
    # Método para obtener todos los clientes de la base de datos, ordenados por apellido y nombre.
    def obtener_todos(self):
        return [
            Cliente.from_document(doc)
            for doc in self._collection.find().sort([("apellido", 1), ("nombre", 1)])
        ]
    
    # Método para obtener un cliente por su correo, devolviendo None si no se encuentra.
    def obtener_por_correo(self, correo):
        doc = self._collection.find_one({"correo": correo.strip().lower()})
        return Cliente.from_document(doc) if doc else None
    
    # Método para obtener un cliente por su ID, devolviendo None si no se encuentra.
    def obtener_por_id(self, cliente_id):
        doc = self._collection.find_one({"_id": self._id(cliente_id)})
        return Cliente.from_document(doc) if doc else None
    
    # Método para modificar los datos de un cliente existente en la base de datos, actualizando también los pedidos si se cambia el correo.
    def modificar(self, correo, datos):
        datos.pop("_id", None)
        correo_actual = correo.strip().lower()
        if "correo" in datos:
            datos["correo"] = datos["correo"].strip().lower()
        try:
            # Actualizar el cliente en la colección de clientes
            resultado = self._collection.update_one(
                {"correo": correo_actual}, {"$set": datos}
            ) # Si se actualizó el cliente y se cambió el correo, actualizar los pedidos asociados al cliente
            if (
                resultado.matched_count
                and "correo" in datos
                and datos["correo"] != correo_actual
            ):
                self._db["pedidos"].update_many(
                    {"cliente_id": correo_actual},
                    {"$set": {"cliente_id": datos["correo"]}},
                )
            # Devolver True si se actualizó el cliente, False si no se encontró el cliente
            return resultado.matched_count > 0
        except DuplicateKeyError as exc:
            raise ValueError("Ya existe un cliente con ese correo.") from exc
        
    # Método para eliminar un cliente de la base de datos, verificando que no tenga pedidos asociados antes de eliminarlo.
    def eliminar(self, correo):
        if self._db["pedidos"].count_documents(
            {"cliente_id": correo.strip().lower()}, limit=1
        ):
            raise ValueError("No se puede eliminar un cliente que tiene pedidos.")
        resultado = self._collection.delete_one({"correo": correo.strip().lower()})
        return resultado.deleted_count > 0