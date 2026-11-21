
# ============================================
# PROYECTO: SOFTWARE FJ
# ARCHIVO: excepciones.py
# DESCRIPCION: Excepciones personalizadas
# ============================================

class ErrorSoftwareFJ(Exception):
    """Excepcion base del sistema Software FJ."""
    pass


class DatosInvalidosError(ErrorSoftwareFJ):
    """Se presenta cuando los datos ingresados son incorrectos."""
    pass


class ClienteExistenteError(ErrorSoftwareFJ):
    """Se presenta cuando un cliente ya esta registrado."""
    pass


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se presenta cuando un servicio no esta disponible."""
    pass


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se presenta cuando una reserva no cumple los requisitos."""
    pass


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se presenta cuando una operacion no esta permitida."""
    pass


class CalculoInvalidoError(ErrorSoftwareFJ):
    """Se presenta cuando existe un error en un calculo."""
    pass
