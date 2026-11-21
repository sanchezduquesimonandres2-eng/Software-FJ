# ============================================
# PROYECTO: SOFTWARE FJ
# ARCHIVO: entidades.py
# DESCRIPCION: Clase abstracta general
# ============================================

from abc import ABC, abstractmethod
from datetime import datetime


class Entidad(ABC):
    """Clase abstracta para las entidades del sistema."""

    def __init__(self, identificador):
        if not identificador:
            raise ValueError("El identificador es obligatorio.")

        self.__identificador = str(identificador)
        self.__fecha_creacion = datetime.now()

    @property
    def identificador(self):
        return self.__identificador

    @property
    def fecha_creacion(self):
        return self.__fecha_creacion

    @abstractmethod
    def describir(self):
        """Metodo que deben implementar las clases derivadas."""
        pass
