import logging
import os


# Crear el archivo de registros en la carpeta del proyecto
RUTA_LOG = os.path.join(
	os.path.dirname(os.path.abspath(__file__)),
	"logs.txt"
)


# Configuracion del sistema de registros
logging.basicConfig(
	filename=RUTA_LOG,
	level=logging.INFO,
	format="%(asctime)s | %(levelname)s | %(message)s",
	encoding="utf-8",
	force=True
)


class RegistroEventos:
	"""Administra los eventos y errores del sistema."""

	@staticmethod
	def registrar_evento(mensaje):
		try:
			logging.info(mensaje)
		except OSError as error:
			print(f"Error al registrar evento: {error}")

	@staticmethod
	def registrar_error(mensaje, error=None):
		try:
			if error is not None:
				logging.exception(
					f"{mensaje}: {error}",
					exc_info=error
				)
			else:
				logging.error(mensaje)

		except OSError as problema:
			print(f"No se pudo guardar el error: {problema}")

	@staticmethod
	def registrar_advertencia(mensaje):
		try:
			logging.warning(mensaje)
		except OSError as error:
			print(f"Error al registrar advertencia: {error}")
