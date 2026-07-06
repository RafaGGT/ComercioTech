# Análisis de cumplimiento EV4 — ComercioTech

## Resultado

El proyecto original cumplía parcialmente el paso 6 de la pauta: tenía conexión
a MongoDB y CRUD de clientes. No implementaba CRUD de productos ni pedidos y no
incluía configuración segura o desplegable.

La versión corregida cubre el componente de software solicitado:

| Requisito de la pauta | Estado | Evidencia |
|---|---|---|
| Desarrollo en Python | Cumple | `app.py` y módulos MVC |
| Conexión a MongoDB | Cumple | `model/Conexion.py` |
| CRUD de clientes | Cumple | modelo, servicio, controlador y menú |
| CRUD de productos | Cumple | modelo, servicio, controlador y menú |
| CRUD de pedidos | Cumple | creación, listado, cambio de estado y eliminación |
| Seguridad de conexión | Parcial | URI por entorno y sin credenciales almacenadas en el código |
| Eficiencia e integridad | Cumple | índices, correo único, validación y control de stock |
| Entorno virtualizado | Pendiente | debe instalarse y documentarse MongoDB en VirtualBox |
| Informe técnico completo | Pendiente | debe prepararse y entregarse separadamente |

## Requisitos funcionales implementados

1. Registrar, listar, modificar y eliminar clientes.
2. Impedir correos duplicados.
3. Registrar, listar, modificar y eliminar productos.
4. Crear pedidos para clientes existentes.
5. Validar disponibilidad y descontar stock.
6. Conservar en el pedido el nombre y precio histórico del producto.
7. Gestionar los estados pendiente, enviado, entregado y cancelado.
8. Reponer stock cuando se cancela o elimina un pedido pendiente.

## Requisitos no funcionales abordados

- Configuración mediante variables de entorno.
- URI preparada para autenticación de MongoDB en la máquina virtual.
- Puerto de MongoDB publicado únicamente en la interfaz local.
- Índices para correo y consultas frecuentes.
- Validación de entradas en los modelos.
- Separación en capas: modelo, servicio, controlador y vista.
- Pruebas unitarias de reglas de dominio.

## Modelo documental

Ejemplo de `clientes`:

```json
{
  "nombre": "Ana",
  "apellido": "Pérez",
  "correo": "ana@ejemplo.cl",
  "telefono": "+56912345678",
  "direccion": "Santiago"
}
```

Ejemplo de `productos`:

```json
{
  "nombre": "Teclado mecánico",
  "descripcion": "Teclado USB",
  "categoria": "Periféricos",
  "precio": 49990,
  "stock": 20
}
```

Ejemplo abreviado de `pedidos`:

```json
{
  "cliente_id": "ana@ejemplo.cl",
  "items": [
    {
      "producto_id": "ID_OBJECTID",
      "nombre": "Teclado mecánico",
      "cantidad": 1,
      "precio_unitario": 49990,
      "subtotal": 49990
    }
  ],
  "estado": "pendiente",
  "total": 49990
}
```

## Evidencia pendiente para la entrega académica

El repositorio no puede demostrar por sí solo los siguientes puntos. Deben
incorporarse al informe con capturas, comandos ejecutados y justificación:

1. Diagnóstico del volumen actual y crecimiento proyectado.
2. Selección y justificación del sistema operativo.
3. Configuración real de la máquina virtual en VirtualBox.
4. Instalación, usuarios, roles, TLS, respaldo y restricciones de red.
5. Pruebas CRUD ejecutadas contra la instancia MongoDB.
6. Diagrama del modelo y decisiones de embebido/referencia.
7. Tratamiento de datos personales, retención, acceso y obligaciones aplicables.
8. Conclusiones técnicas, normativas y éticas.
