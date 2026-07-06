from controller.ClienteController import ClienteController
from controller.PedidoController import PedidoController
from controller.ProductoController import ProductoController

class Menu:
    def __init__(self):
        self.clientes = ClienteController()
        self.productos = ProductoController()
        self.pedidos = PedidoController()

    def mostrar_menu(self):
        acciones = {
            "1": self.menu_clientes,
            "2": self.menu_productos,
            "3": self.menu_pedidos,
        }
        while True:
            print("""
╔════════════════════════════╗
║        ComercioTech        ║
╠════════════════════════════╣
║  1. Clientes               ║
║  2. Productos              ║
║  3. Pedidos                ║
║  0. Salir                  ║
╚════════════════════════════╝
        """)
            opcion = input("Seleccione una opcion: ").strip()
            if opcion == "0":
                return
            accion = acciones.get(opcion)
            if not accion:
                print("Opcion invalida.")
                continue
            try:
                accion()
            except (ValueError, RuntimeError) as exc:
                print(f"Error: {exc}")

    def menu_clientes(self):
        print("""
╔══════════════════════════════════╗
║   ComercioTech - Menú Clientes   ║
╠══════════════════════════════════╣
║  1. Crear                        ║
║  2. Listar                       ║
║  3. Buscar por ID                ║
║  4. Modificar                    ║
║  5. Eliminar                     ║
║  0. Volver                       ║
╚══════════════════════════════════╝
""")
        opcion = input("Seleccione una opcion: ").strip()
        if opcion == "1":
            cliente = self.clientes.agregar_cliente(
                input("Nombre: "),
                input("Apellido: "),
                input("Correo (Ejemplo@dominio.com): "),
                input("Teléfono (8 a 15 dígitos, '+' opcional. Ej: +56912345678): "),
                input("Direccion: "),
            )
            print(f"Creado: {cliente}")
        elif opcion == "2":
            self._imprimir(self.clientes.obtener_clientes(), "clientes")
        elif opcion == "3":
            cliente = self.clientes.obtener_cliente(input("ID del cliente: "))
            print(cliente if cliente else "Cliente no encontrado.")
        elif opcion == "4":
            correo = input("Correo (Ejemplo@dominio.com): ")
            print("Campos: nombre, apellido, correo, telefono, direccion")
            campo = input("Campo a modificar: ").strip().lower()
            if campo not in {"nombre", "apellido", "correo", "telefono", "direccion"}:
                raise ValueError("Campo invalido.")
            actualizado = self.clientes.modificar_cliente(
                correo, {campo: input("Nuevo valor: ")}
            )
            print("Cliente actualizado." if actualizado else "Cliente no encontrado.")
        elif opcion == "5":
            correo = input("Correo: ")
            consentimiento = input("¿Está seguro que desea eliminar el cliente? escribe s para confirmar: ").strip().lower()
            if consentimiento == "s":
                eliminado = self.clientes.eliminar_cliente(correo)
                print("Cliente eliminado." if eliminado else "Cliente no encontrado.")
            else:
                print("Operación cancelada.")
        elif opcion == "0":
            return
        else:
            print("Opcion invalida.")

    def menu_productos(self):
        print("""
╔══════════════════════════════════╗
║   ComercioTech - Menú Productos  ║
╠══════════════════════════════════╣
║  1. Crear                        ║
║  2. Listar                       ║
║  3. Buscar por ID                ║
║  4. Modificar                    ║
║  5. Eliminar                     ║
║  0. Volver                       ║
╚══════════════════════════════════╝
""")
        opcion = input("Seleccione una opcion: ").strip()
        if opcion == "1":
            producto = self.productos.agregar_producto(
                input("Nombre: "),
                input("Descripcion: "),
                input("Categoria: "),
                input("Precio: "),
                input("Stock: "),
            )
            print(f"Creado: {producto}")
        elif opcion == "2":
            self._imprimir(self.productos.obtener_productos(), "productos")
        elif opcion == "3":
            producto = self.productos.obtener_producto(input("ID del producto: "))
            print(producto if producto else "Producto no encontrado.")
        elif opcion == "4":
            producto_id = input("ID del producto: ")
            print("Campos: nombre, descripcion, categoria, precio, stock")
            campo = input("Campo a modificar: ").strip().lower()
            if campo not in {"nombre", "descripcion", "categoria", "precio", "stock"}:
                raise ValueError("Campo invalido.")
            actualizado = self.productos.modificar_producto(
                producto_id, {campo: input("Nuevo valor: ")}
            )
            print("Producto actualizado." if actualizado else "Producto no encontrado.")
        elif opcion == "5":
            producto_id = input("ID del producto: ")
            consentimiento = input("¿Está seguro que desea eliminar el producto? escribe s para confirmar: ").strip().lower()
            if consentimiento == "s":
                eliminado = self.productos.eliminar_producto(producto_id)
                print("Producto eliminado." if eliminado else "Producto no encontrado.")
            else:
                print("Operación cancelada.")
        elif opcion == "0":
            return
        else:
            print("Opcion invalida.")

    def menu_pedidos(self):
        print("""
╔══════════════════════════════════╗
║   ComercioTech - Menú Pedidos    ║
╠══════════════════════════════════╣
║  1. Crear                        ║
║  2. Listar                       ║
║  3. Buscar por ID                ║
║  4. Cambiar estado               ║
║  5. Eliminar                     ║
║  0. Volver                       ║
╚══════════════════════════════════╝
""")
        opcion = input("Seleccione una opcion: ").strip()
        if opcion == "1":
            items = []
            while True:
                producto_id = input("ID producto (vacio para terminar): ").strip()
                if not producto_id:
                    break
                items.append(
                    {
                        "producto_id": producto_id,
                        "cantidad": input("Cantidad: "),
                    }
                )
            pedido = self.pedidos.crear_pedido(
                input("Correo del cliente: "),
                input("Metodo de pago: "),
                input("Direccion de envio: "),
                items,
            )
            print(f"Creado: {pedido}")
        elif opcion == "2":
            self._imprimir(self.pedidos.obtener_pedidos(), "pedidos")
        elif opcion == "3":
            pedido = self.pedidos.obtener_pedido(input("ID del pedido: "))
            print(pedido if pedido else "Pedido no encontrado.")
        elif opcion == "4":
            actualizado = self.pedidos.cambiar_estado(
                input("ID del pedido: "), input("Nuevo estado: ")
            )
            print("Pedido actualizado." if actualizado else "Pedido no encontrado.")
        elif opcion == "5":
            pedido = input("ID del pedido: ")
            consentimiento = input("¿Está seguro que desea eliminar el pedido? escribe s para confirmar: ").strip().lower()
            if consentimiento == "s":
                eliminado = self.pedidos.eliminar_pedido(pedido)
                print("Pedido eliminado." if eliminado else "Pedido no encontrado.")
            else:
                print("Operación cancelada.")
        elif opcion == "0":
            return
        else:
            print("Opcion invalida.")

    @staticmethod
    def _imprimir(elementos, nombre):
        if not elementos:
            print(f"No hay {nombre} registrados.")
            return
        for elemento in elementos:
            print(elemento)
