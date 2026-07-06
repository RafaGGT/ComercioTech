class Producto:
    # Constructor de la clase Producto
    def __init__(self, nombre, descripcion, categoria, precio, stock, id=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
  
    # Método estático para validar y limpiar texto
    @staticmethod
    def _texto(valor, campo):
        valor = str(valor).strip()
        if not valor:
            raise ValueError(f"{campo} no puede estar vacío.")
        return valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = self._texto(valor, "El nombre")

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self._descripcion = self._texto(valor, "La descripción")

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        self._categoria = self._texto(valor, "La categoría")

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        try:
            valor = round(float(valor), 2)
        except (TypeError, ValueError) as exc:
            raise ValueError("El precio debe ser numérico.") from exc
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = valor

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        try:
            valor = int(valor)
        except (TypeError, ValueError) as exc:
            raise ValueError("El stock debe ser un número entero.") from exc
        if valor < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._stock = valor

    # Métodos para convertir a y desde un documento (diccionario) para almacenamiento en base de datos
    def to_document(self):
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock,
        }
    # Método de clase para crear una instancia de Producto a partir de un documento (diccionario)
    @classmethod
    def from_document(cls, documento):
        return cls(
            documento["nombre"],
            documento["descripcion"],
            documento["categoria"],
            documento["precio"],
            documento["stock"],
            id=str(documento["_id"]) if documento.get("_id") else None,
        )
    # Método para representar el objeto Producto como una cadena de texto
    def __str__(self):
        return (
            f"Producto [{self.id or '-'}]: {self.nombre} | {self.categoria} | "
            f"${self.precio:,.2f} | stock: {self.stock}"
        )
