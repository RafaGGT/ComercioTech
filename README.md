# ComercioTech

Aplicacion de consola en Python para administrar clientes, productos y pedidos
persistidos en MongoDB.

## Requisitos

- Python 3.10 o superior
- MongoDB 4.4.31 ejecutandose en la VM Ubuntu Server
- Tunel SSH desde Windows hacia la VM

## Abrir el tunel SSH

Ejecuta este comando en una terminal de Windows y dejala abierta mientras uses
la aplicacion:

```powershell
ssh -N -L 27018:127.0.0.1:27017 comercio@127.0.0.1 -p 2222
```

Tambien puedes ejecutarlo desde el script incluido:

```powershell
.\abrir_tunel.ps1
```

## Configurar variables

Crea un archivo `.env` en la raiz del proyecto usando `.env.example` como base:

```env
MONGO_URI=mongodb://adminComercio:Inacap2026@127.0.0.1:27018/comerciotech?authSource=admin
DB_NAME=comerciotech
```

La aplicacion lee `MONGO_URI` y `DB_NAME` con `python-dotenv`. Por compatibilidad
tambien acepta `MONGODB_URI` y `MONGODB_DB`.

## Instalar dependencias

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecutar

```powershell
py app.py
```

## Colecciones

- `clientes`: datos personales del cliente; `correo` tiene indice unico.
- `productos`: catalogo, categoria, precio y stock.
- `pedidos`: pedidos asociados al correo del cliente, con copia del detalle de
  productos para conservar el historial.

## Operaciones CRUD

Desde el menu de consola puedes:

- Crear clientes, productos y pedidos.
- Listar registros.
- Buscar clientes, productos y pedidos por ID.
- Actualizar clientes, productos y estado de pedidos.
- Eliminar clientes, productos y pedidos.

## Ejemplo de prueba CRUD

1. Abre el tunel SSH.
2. Ejecuta `py app.py`.
3. En `Clientes`, crea un cliente y luego usa `Listar` para copiar su ID.
4. Usa `Buscar por ID` con el ID del cliente.
5. Usa `Modificar` para cambiar un campo del cliente.
6. Crea un producto desde `Productos`, lista y copia su ID.
7. Crea un pedido desde `Pedidos` usando el correo del cliente y el ID del
   producto.
8. Lista pedidos, cambia el estado a `enviado` o elimina el pedido si sigue
   `pendiente`.

## Manejo de errores

El programa informa errores de conexion a MongoDB, credenciales incorrectas,
IDs invalidos, documentos no encontrados y datos invalidos. La conexion se
cierra al salir del programa.
