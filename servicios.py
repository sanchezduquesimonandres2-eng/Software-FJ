
# ============================================
# PROYECTO: SOFTWARE FJ
# ARCHIVO: servicios.py
# DESCRIPCION: Servicios especializados
# ============================================

from abc import abstractmethod
from entidades import Entidad
from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
    CalculoInvalidoError
)


class Servicio(Entidad):
    """Clase abstracta que representa un servicio."""

    def __init__(self, identificador, nombre, tarifa, disponible=True):
        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio.")

        if isinstance(tarifa, bool) or not isinstance(tarifa, (int, float)):
            raise DatosInvalidosError("La tarifa debe ser numerica.")

        if tarifa <= 0:
            raise DatosInvalidosError("La tarifa debe ser mayor que cero.")

        if not isinstance(disponible, bool):
            raise DatosInvalidosError("La disponibilidad debe ser verdadera o falsa.")

        self.__nombre = nombre.strip()
        self.__tarifa = float(tarifa)
        self.__disponible = disponible

    @property
    def nombre(self):
        return self.__nombre

    @property
    def tarifa(self):
        return self.__tarifa

    @property
    def disponible(self):
        return self.__disponible

    def cambiar_disponibilidad(self, estado):
        if not isinstance(estado, bool):
            raise DatosInvalidosError("El estado debe ser booleano.")

        self.__disponible = estado

    def validar_disponibilidad(self):
        if not self.__disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self.__nombre} no esta disponible."
            )

    @staticmethod
    def validar_duracion(duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise DatosInvalidosError("La duracion debe ser numerica.")

        if duracion <= 0:
            raise DatosInvalidosError("La duracion debe ser mayor que cero.")

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        """
        Calcula el costo con parametros opcionales.
        Permite calcular con tarifa normal, impuesto o descuento.
        """

        self.validar_duracion(duracion)

        if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)):
            raise CalculoInvalidoError("El impuesto debe ser numerico.")

        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)):
            raise CalculoInvalidoError("El descuento debe ser numerico.")

        if not 0 <= impuesto <= 100:
            raise CalculoInvalidoError("El impuesto debe estar entre 0 y 100.")

        if not 0 <= descuento <= 100:
            raise CalculoInvalidoError("El descuento debe estar entre 0 y 100.")

        subtotal = self.tarifa * duracion
        valor_descuento = subtotal * (descuento / 100)
        subtotal_con_descuento = subtotal - valor_descuento
        valor_impuesto = subtotal_con_descuento * (impuesto / 100)

        total = subtotal_con_descuento + valor_impuesto

        if total < 0:
            raise CalculoInvalidoError("El calculo produjo un valor negativo.")

        return round(total, 2)

    @abstractmethod
    def validar_parametros(self):
        pass

    @abstractmethod
    def describir(self):
        pass


# ============================================
# SERVICIO 1: RESERVA DE SALAS
# ============================================

class ReservaSala(Servicio):

    def __init__(self, identificador, nombre, tarifa, capacidad, disponible=True):
        super().__init__(identificador, nombre, tarifa, disponible)
        self.__capacidad = capacidad
        self.validar_parametros()

    @property
    def capacidad(self):
        return self.__capacidad

    def validar_parametros(self):
        if isinstance(self.__capacidad, bool) or not isinstance(self.__capacidad, int):
            raise DatosInvalidosError("La capacidad debe ser un numero entero.")

        if self.__capacidad <= 0:
            raise DatosInvalidosError("La capacidad debe ser mayor que cero.")

    def describir(self):
        return (
            f"Sala: {self.nombre} | "
            f"Capacidad: {self.__capacidad} personas | "
            f"Tarifa por hora: ${self.tarifa:,.2f}"
        )


# ============================================
# SERVICIO 2: ALQUILER DE EQUIPOS
# ============================================

class AlquilerEquipo(Servicio):

    def __init__(self, identificador, nombre, tarifa, cantidad, disponible=True):
        super().__init__(identificador, nombre, tarifa, disponible)
        self.__cantidad = cantidad
        self.validar_parametros()

    @property
    def cantidad(self):
        return self.__cantidad

    def validar_parametros(self):
        if isinstance(self.__cantidad, bool) or not isinstance(self.__cantidad, int):
            raise DatosInvalidosError("La cantidad debe ser un numero entero.")

        if self.__cantidad <= 0:
            raise DatosInvalidosError("La cantidad debe ser mayor que cero.")

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        self.validar_parametros()
        return super().calcular_costo(duracion, impuesto, descuento)

    def describir(self):
        return (
            f"Equipo: {self.nombre} | "
            f"Cantidad disponible: {self.__cantidad} | "
            f"Tarifa por hora: ${self.tarifa:,.2f}"
        )


# ============================================
# SERVICIO 3: ASESORIAS ESPECIALIZADAS
# ============================================

class Asesoria(Servicio):

    def __init__(self, identificador, nombre, tarifa, especialidad, disponible=True):
        super().__init__(identificador, nombre, tarifa, disponible)
        self.__especialidad = especialidad
        self.validar_parametros()

    @property
    def especialidad(self):
        return self.__especialidad

    def validar_parametros(self):
        if not isinstance(self.__especialidad, str):
            raise DatosInvalidosError("La especialidad debe ser texto.")

        if len(self.__especialidad.strip()) < 3:
            raise DatosInvalidosError("La especialidad es demasiado corta.")

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        self.validar_parametros()
        return super().calcular_costo(duracion, impuesto, descuento)

    def describir(self):
        return (
            f"Asesoria: {self.nombre} | "
            f"Especialidad: {self.__especialidad} | "
            f"Tarifa por hora: ${self.tarifa:,.2f}"
        )
