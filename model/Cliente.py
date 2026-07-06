import re


class Cliente:
    # Expresiones regulares para validación
    EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    TELEFONO_RE = re.compile(r"^\+?[0-9]{8,15}$")
    # Constructor de la clase Cliente
    def __init__(self, nombre, apellido, correo, telefono, direccion, id=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.telefono = telefono
        self.direccion = direccion
    # Método estático para validación de texto
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
    def apellido(self):
        return self._apellido

    @apellido.setter
    def apellido(self, valor):
        self._apellido = self._texto(valor, "El apellido")

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        valor = self._texto(valor, "El correo").lower()
        if not self.EMAIL_RE.fullmatch(valor):
            raise ValueError("El correo no tiene un formato válido.")
        self._correo = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        valor = self._texto(valor, "El teléfono").replace(" ", "")
        if not self.TELEFONO_RE.fullmatch(valor):
            raise ValueError("El teléfono debe contener entre 8 y 15 dígitos.")
        self._telefono = valor

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, valor):
        self._direccion = self._texto(valor, "La dirección")

    # Método para modificar los atributos del cliente
    def modificar_cliente(
        self, nombre=None, apellido=None, correo=None, telefono=None, direccion=None
    ):
        for campo, valor in {
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "telefono": telefono,
            "direccion": direccion,
        }.items():
            if valor is not None:
                setattr(self, campo, valor)
    # Método para representar el objeto Cliente como un diccionario (documento)
    def to_document(self):
        return {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "correo": self.correo,
            "telefono": self.telefono,
            "direccion": self.direccion,
        }
    
    registrar_cliente = to_document
    # Método de clase para crear una instancia de Cliente a partir de un documento (diccionario)
    @classmethod
    def from_document(cls, documento):
        return cls(
            documento["nombre"],
            documento["apellido"],
            documento["correo"],
            documento["telefono"],
            documento["direccion"],
            id=str(documento["_id"]) if documento.get("_id") else None,
        )
    # Método para representar el objeto Cliente como una cadena de texto
    def __str__(self):
        return (
            f"Cliente [{self.id or '-'}]: {self.nombre} {self.apellido} | "
            f"{self.correo} | {self.telefono} | {self.direccion}"
        )
