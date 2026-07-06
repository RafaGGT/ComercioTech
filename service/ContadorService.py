from pymongo import ReturnDocument

class ContadorService:
    def __init__(self, db):
        self.db = db

    # Método para obtener el siguiente ID de una colección específica, utilizando un documento contador en la colección "counters".
    def obtener_siguiente_id(self, nombre_coleccion):
        # Buscar y actualizar el documento contador correspondiente a la colección, incrementando su secuencia en 1.
        contador = self.db.counters.find_one_and_update(
            # Filtro para encontrar el documento contador de la colección especificada
            {"_id": nombre_coleccion},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        # Devolver el valor actualizado de la secuencia, que será el siguiente ID disponible para la colección.
        return contador["seq"]