"""Configuracion centralizada de la conexion a MongoDB."""

import os

from dotenv import load_dotenv
from pymongo import ASCENDING, MongoClient
from pymongo.errors import ConfigurationError, OperationFailure, PyMongoError


class Conexion:
    # Clase para manejar la conexión a la base de datos MongoDB, incluyendo la creación de índices y el manejo de errores de conexión.
    _cliente = None
    _db = None

    @classmethod
    def get_db(cls):
        if cls._db is not None:
            return cls._db
        # Cargar variables de entorno desde el archivo .env, sobrescribiendo cualquier variable existente.
        load_dotenv(override=True)
        # Leer variables de entorno para la conexión a MongoDB
        uri = os.getenv("MONGO_URI") or os.getenv("MONGODB_URI")
        nombre_db = os.getenv("DB_NAME") or os.getenv("MONGODB_DB") or "comerciotech"
        timeout_ms = int(os.getenv("MONGO_TIMEOUT_MS", "5000"))

        # Validar que la URI de MongoDB esté configurada, lanzando un RuntimeError si no lo está.
        if not uri:
            raise RuntimeError(
                "Falta configurar MONGO_URI en el archivo .env o en variables de entorno."
            )
        # Intentar establecer la conexión con MongoDB utilizando pymongo, manejando posibles errores de configuración o autenticación.
        try:
            # Crear una instancia de MongoClient con la URI y los parámetros de tiempo de espera, habilitando reintentos de escritura y estableciendo un nombre de aplicación.
            cls._cliente = MongoClient(
                uri,
                serverSelectionTimeoutMS=timeout_ms,
                connectTimeoutMS=timeout_ms,
                retryWrites=True,
                appname="ComercioTech",
            )
            cls._cliente.admin.command("ping")
            cls._db = cls._cliente[nombre_db]
            cls._crear_indices()
            return cls._db
        # Manejar errores específicos de autenticación y configuración, cerrando la conexión y lanzando un RuntimeError con un mensaje descriptivo.
        except OperationFailure as exc:
            cls.close()
            if exc.code == 18:
                raise RuntimeError(
                    "Credenciales incorrectas para MongoDB. Revise MONGO_URI y authSource."
                ) from exc
            raise RuntimeError(f"MongoDB rechazo la operacion: {exc}") from exc
        # Manejar errores generales de configuración y conexión, cerrando la conexión y lanzando un RuntimeError con un mensaje descriptivo.
        except (ConfigurationError, PyMongoError, ValueError) as exc:
            cls.close()
            raise RuntimeError(
                "No fue posible conectar con MongoDB. Revise MONGO_URI, el tunel SSH "
                "y que el servidor este disponible."
            ) from exc
    # Método privado para crear índices en las colecciones de MongoDB, asegurando unicidad y optimizando consultas.
    @classmethod
    def _crear_indices(cls):
        cls._db["clientes"].create_index(
            [("correo", ASCENDING)], unique=True, name="uq_clientes_correo"
        ) 
        # Crear un índice compuesto en la colección de productos para optimizar búsquedas por nombre y categoría.
        cls._db["productos"].create_index(
            [("nombre", ASCENDING), ("categoria", ASCENDING)],
            name="ix_productos_nombre_categoria",
        )
        # Crear un índice compuesto en la colección de pedidos para optimizar consultas por cliente y fecha de creación.
        cls._db["pedidos"].create_index(
            [("cliente_id", ASCENDING), ("fecha_creacion", ASCENDING)],
            name="ix_pedidos_cliente_fecha",
        )
    # Método para cerrar la conexión con MongoDB, liberando recursos y estableciendo las referencias a None.
    @classmethod
    def close(cls):
        if cls._cliente is not None:
            cls._cliente.close()
        cls._cliente = None
        cls._db = None
