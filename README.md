# 🛒 ComercioTech

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4.4-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![PyMongo](https://img.shields.io/badge/PyMongo-4.x-13AA52?style=for-the-badge&logo=mongodb&logoColor=white)
![CLI](https://img.shields.io/badge/Interfaz-CLI-lightgrey?style=for-the-badge)
![Status](https://img.shields.io/badge/Estado-Terminado-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/Licencia-MIT-green?style=for-the-badge)

Aplicación de consola en **Python** para administrar clientes, productos y pedidos, persistidos en **MongoDB**. Desarrollada con arquitectura en capas (Modelo - Vista - Controlador - Servicio).

## 📋 Tabla de contenidos

- [Características](#-características)
- [Arquitectura del proyecto](#-arquitectura-del-proyecto)
- [Requisitos](#-requisitos)
- [Abrir el túnel SSH](#-abrir-el-túnel-ssh)
- [Configurar variables](#-configurar-variables)
- [Instalar dependencias](#-instalar-dependencias)
- [Ejecutar](#-ejecutar)
- [Colecciones](#-colecciones)
- [Operaciones CRUD](#-operaciones-crud)
- [Ejemplo de prueba CRUD](#-ejemplo-de-prueba-crud)
- [Manejo de errores](#-manejo-de-errores)
- [Estructura de carpetas](#-estructura-de-carpetas)
- [Autores](#-autores)

## ✨ Características

- **Gestión de clientes**: alta, listado, búsqueda por ID, modificación y eliminación, con validación de correo y teléfono.
- **Gestión de productos**: catálogo con categoría, precio y stock.
- **Gestión de pedidos**: asociados al correo del cliente, con copia del detalle de productos para conservar el historial y control de estado (pendiente, enviado, etc.).
- **Persistencia en MongoDB**, con índices únicos y compuestos para optimizar las consultas.
- **Manejo robusto de errores**: conexión, credenciales, IDs inválidos y datos incorrectos.

## 🏗 Arquitectura del proyecto

El proyecto sigue el patrón **MVC** con una capa adicional de **servicios** para el acceso a datos:

```
Vista (Menu) → Controlador → Servicio → Modelo → MongoDB
```

- **`view/`**: menú interactivo por consola.
- **`controller/`**: orquesta la lógica entre la vista y los servicios.
- **`service/`**: lógica de acceso a datos y operaciones sobre MongoDB.
- **`model/`**: entidades del dominio (Cliente, Producto, Pedido) y configuración de la conexión (`Conexion.py`).

## ⚙️ Requisitos

- Python 3.10 o superior
- MongoDB 4.4.31 ejecutándose en la VM Ubuntu Server
- Túnel SSH desde Windows hacia la VM

## 🔐 Abrir el túnel SSH

Ejecuta este comando en una terminal de Windows y déjala abierta mientras uses la aplicación:

```powershell
ssh -N -L 27018:127.0.0.1:27017 comercio@127.0.0.1 -p 2222
```

También puedes ejecutarlo desde el script incluido:

```powershell
.\abrir_tunel.ps1
```

## 🔧 Configurar variables

Crea un archivo `.env` en la raíz del proyecto usando `.env.example` como base:

```env
MONGO_URI=mongodb://<usuario>:<contraseña>@127.0.0.1:27018/comerciotech?authSource=admin
DB_NAME=comerciotech
```

La aplicación lee `MONGO_URI` y `DB_NAME` con `python-dotenv`. Por compatibilidad también acepta `MONGODB_URI` y `MONGODB_DB`.

> ⚠️ **Importante**: el archivo `.env` incluido en este proyecto contiene una credencial real de MongoDB. Antes de subir el proyecto a un repositorio público:
> - Verifica que `.env` esté listado en `.gitignore` (ya lo está) y que **nunca** haya quedado incluido en un commit.
> - Cambia la contraseña de la base de datos si el archivo llegó a subirse alguna vez.
> - Usa `.env.example` únicamente con valores de ejemplo, no con credenciales reales.

## 📦 Instalar dependencias

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## ▶️ Ejecutar

```powershell
py app.py
```

## 🗄 Colecciones

- **`clientes`**: datos personales del cliente; `correo` tiene índice único.
- **`productos`**: catálogo, categoría, precio y stock.
- **`pedidos`**: pedidos asociados al correo del cliente, con copia del detalle de productos para conservar el historial.

## 🔄 Operaciones CRUD

Desde el menú de consola puedes:

- Crear clientes, productos y pedidos.
- Listar registros.
- Buscar clientes, productos y pedidos por ID.
- Actualizar clientes, productos y estado de pedidos.
- Eliminar clientes, productos y pedidos.

## 🧪 Ejemplo de prueba CRUD

1. Abre el túnel SSH.
2. Ejecuta `py app.py`.
3. En `Clientes`, crea un cliente y luego usa `Listar` para copiar su ID.
4. Usa `Buscar por ID` con el ID del cliente.
5. Usa `Modificar` para cambiar un campo del cliente.
6. Crea un producto desde `Productos`, lista y copia su ID.
7. Crea un pedido desde `Pedidos` usando el correo del cliente y el ID del producto.
8. Lista pedidos, cambia el estado a `enviado` o elimina el pedido si sigue `pendiente`.

## 🛡 Manejo de errores

El programa informa errores de conexión a MongoDB, credenciales incorrectas, IDs inválidos, documentos no encontrados y datos inválidos. La conexión se cierra al salir del programa.

## 📁 Estructura de carpetas

```
ComercioTech/
├── app.py                       # Punto de entrada de la aplicación
├── requirements.txt              # Dependencias del proyecto
├── .env.example                  # Plantilla de variables de entorno
├── docs/
│   └── ANALISIS_EV4.md           # Documentación / análisis del proyecto
├── model/
│   ├── Cliente.py
│   ├── Producto.py
│   ├── Pedido.py
│   └── Conexion.py               # Configuración centralizada de conexión a MongoDB
├── service/
│   ├── ClienteService.py
│   ├── ProductoService.py
│   ├── PedidoService.py
│   └── ContadorService.py
├── controller/
│   ├── ClienteController.py
│   ├── ProductoController.py
│   └── PedidoController.py
└── view/
    └── Menu.py                   # Menú interactivo por consola
```

## 👨‍💻 Autores

| Nombre    | GitHub |
|-----------|--------|
| Rafa      | [@RafaGGT](https://github.com/RafaGGT) |
| Lucas     | [@LFP2002](https://github.com/LFP2002) |
| Gamaniel  | [@gamanielm85-beep](https://github.com/gamanielm85-beep) |

---

Proyecto desarrollado con fines educativos como práctica de arquitectura en capas, persistencia con MongoDB y buenas prácticas de manejo de errores en Python.
