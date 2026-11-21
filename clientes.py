
# ============================================
# PROYECTO: SOFTWARE FJ
# ARCHIVO: clientes.py
# DESCRIPCION: Gestion y validacion de clientes
# ============================================

import re
from entidades import Entidad
from excepciones import DatosInvalidosError


class Cliente(Entidad):
    """Representa un cliente de Software FJ."""

    def __init__(self, identificador, nombre, documento, correo, telefono):
        super().__init__(identificador)

        self.__nombre = self.__validar_nombre(nombre)
        self.__documento = self.__validar_documento(documento)
        self.__correo = self.__validar_correo(correo)
        self.__telefono = self.__validar_telefono(telefono)

    @staticmethod
    def __validar_nombre(nombre):
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise DatosInvalidosError(
                "El nombre debe tener minimo 3 caracteres."
            )

        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+", nombre.strip()):
            raise DatosInvalidosError(
                "El nombre contiene caracteres no permitidos."
            )

        return nombre.strip()

    @staticmethod
    def __validar_documento(documento):
        documento = str(documento).strip()

        if not documento.isdigit() or not (5 <= len(documento) <= 15):
            raise DatosInvalidosError(
                "El documento debe contener entre 5 y 15 digitos."
            )

        return documento

    @staticmethod
    def __validar_correo(correo):
        if not isinstance(correo, str):
            raise DatosInvalidosError("El correo debe ser texto.")

        correo = correo.strip().lower()

        patron = patron = r"^[\w.+-]+@[\w-]+\.[A-Za-z]{2,}$"

        if not re.fullmatch(patron, correo):
            raise DatosInvalidosError("El correo electronico no es valido.")

        return correo

    @staticmethod
    def __validar_telefono(telefono):
        telefono = str(telefono).strip()

        if not telefono.isdigit() or len(telefono) != 10:
            raise DatosInvalidosError(
                "El telefono debe contener exactamente 10 digitos."
            )

        return telefono

    @property
    def nombre(self):
        return self.__nombre

    @property
    def documento(self):
        return self.__documento

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def describir(self):
        return (
            f"Cliente: {self.__nombre} | "
            f"Documento: {self.__documento} | "
            f"Correo: {self.__correo}"
        )

    def __str__(self):
        return self.describir()
