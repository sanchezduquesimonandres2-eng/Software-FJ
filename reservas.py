
# ============================================
# PROYECTO: SOFTWARE FJ
# ARCHIVO: reservas.py
# DESCRIPCION: Gestion integral de reservas
# ============================================

from entidades import Entidad
from excepciones import (
    DatosInvalidosError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ServicioNoDisponibleError,
    CalculoInvalidoError
)


class Reserva(Entidad):
    """Representa una reserva realizada por un cliente."""

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA")

    def __init__(self, identificador, cliente, servicio, duracion):
        super().__init__(identificador)

        if cliente is None:
            raise DatosInvalidosError("Debe seleccionar un cliente.")

        if servicio is None:
            raise DatosInvalidosError("Debe seleccionar un servicio.")

        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise DatosInvalidosError("La duracion debe ser numerica.")

        if duracion <= 0:
            raise DatosInvalidosError("La duracion debe ser mayor que cero.")

        if not hasattr(cliente, "describir"):
            raise DatosInvalidosError("El cliente no es valido.")

        if not hasattr(servicio, "calcular_costo"):
            raise DatosInvalidosError("El servicio no es valido.")

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "PENDIENTE"
        self.__costo = 0.0

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    @property
    def costo(self):
        return self.__costo

    def confirmar(self, impuesto=0, descuento=0):
        """Confirma una reserva y calcula su costo."""

        if self.__estado == "CANCELADA":
            raise OperacionNoPermitidaError(
                "No se puede confirmar una reserva cancelada."
            )

        if self.__estado == "CONFIRMADA":
            raise OperacionNoPermitidaError(
                "La reserva ya se encuentra confirmada."
            )

        try:
            self.__servicio.validar_disponibilidad()

            costo_calculado = self.__servicio.calcular_costo(
                self.__duracion,
                impuesto,
                descuento
            )

            if costo_calculado <= 0:
                raise CalculoInvalidoError(
                    "El costo de la reserva debe ser positivo."
                )

        except ServicioNoDisponibleError as error:
            raise ReservaInvalidaError(
                "No se puede confirmar porque el servicio no esta disponible."
            ) from error

        except Exception as error:
            raise ReservaInvalidaError(
                "Ocurrio un problema al procesar la reserva."
            ) from error

        else:
            self.__costo = costo_calculado
            self.__estado = "CONFIRMADA"
            return self.__costo

        finally:
            print(f"Procesamiento finalizado para reserva {self.identificador}.")

    def cancelar(self):
        """Cancela una reserva pendiente o confirmada."""

        if self.__estado == "CANCELADA":
            raise OperacionNoPermitidaError(
                "La reserva ya esta cancelada."
            )

        self.__estado = "CANCELADA"
        return True

    def procesar(self):
        """Procesa la reserva verificando su estado."""

        if self.__estado == "CANCELADA":
            raise ReservaInvalidaError(
                "No se puede procesar una reserva cancelada."
            )

        if self.__estado == "CONFIRMADA":
            return (
                f"Reserva {self.identificador} procesada correctamente. "
                f"Costo: ${self.__costo:,.2f}"
            )

        raise ReservaInvalidaError(
            "La reserva debe estar confirmada antes de procesarse."
        )

    def describir(self):
        return (
            f"Reserva: {self.identificador} | "
            f"Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | "
            f"Duracion: {self.__duracion} horas | "
            f"Estado: {self.__estado} | "
            f"Costo: ${self.__costo:,.2f}"
        )

    def __str__(self):
        return self.describir()
