
# =====================================================
# PROYECTO: SOFTWARE FJ
# ARCHIVO: main.py
# AUTOR: Simon Andres Sanchez
# DESCRIPCION: Sistema integral de gestion empresarial
# =====================================================

from clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from reservas import Reserva
from excepciones import (
    ErrorSoftwareFJ,
    DatosInvalidosError,
    ClienteExistenteError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError
)
from logs import RegistroEventos


class SistemaSoftwareFJ:
    """Clase principal para administrar toda la empresa."""

    def __init__(self):
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

        RegistroEventos.registrar_evento(
            "Sistema Software FJ iniciado correctamente."
        )

    # =================================================
    # GESTION DE CLIENTES
    # =================================================

    def registrar_cliente(self, cliente):
        try:
            if not isinstance(cliente, Cliente):
                raise DatosInvalidosError("El objeto cliente no es valido.")

            for existente in self.__clientes:
                if existente.documento == cliente.documento:
                    raise ClienteExistenteError(
                        "Ya existe un cliente con ese documento."
                    )

            self.__clientes.append(cliente)

        except ErrorSoftwareFJ as error:
            RegistroEventos.registrar_error(
                "Error al registrar cliente", error
            )
            raise

        else:
            RegistroEventos.registrar_evento(
                f"Cliente registrado: {cliente.nombre}"
            )
            print("Cliente registrado correctamente.")

        finally:
            print("Operacion de registro de cliente finalizada.")

    # =================================================
    # GESTION DE SERVICIOS
    # =================================================

    def registrar_servicio(self, servicio):
        try:
            if not hasattr(servicio, "calcular_costo"):
                raise DatosInvalidosError("El servicio no es valido.")

            for existente in self.__servicios:
                if existente.identificador == servicio.identificador:
                    raise DatosInvalidosError(
                        "Ya existe un servicio con ese identificador."
                    )

            self.__servicios.append(servicio)

        except Exception as error:
            RegistroEventos.registrar_error(
                "Error al registrar servicio", error
            )
            raise

        else:
            RegistroEventos.registrar_evento(
                f"Servicio registrado: {servicio.nombre}"
            )
            print("Servicio registrado correctamente.")

        finally:
            print("Operacion de registro de servicio finalizada.")

    # =================================================
    # GESTION DE RESERVAS
    # =================================================

    def crear_reserva(self, identificador, documento, id_servicio, duracion):
        try:
            cliente = next(
                (c for c in self.__clientes
                 if c.documento == documento),
                None
            )

            servicio = next(
                (s for s in self.__servicios
                 if s.identificador == id_servicio),
                None
            )

            if cliente is None:
                raise ReservaInvalidaError(
                    "No se encontro el cliente solicitado."
                )

            if servicio is None:
                raise ReservaInvalidaError(
                    "No se encontro el servicio solicitado."
                )

            for reserva in self.__reservas:
                if reserva.identificador == identificador:
                    raise ReservaInvalidaError(
                        "El identificador de reserva ya existe."
                    )

            reserva = Reserva(
                identificador,
                cliente,
                servicio,
                duracion
            )

            self.__reservas.append(reserva)

        except Exception as error:
            RegistroEventos.registrar_error(
                "Error al crear reserva", error
            )
            raise

        else:
            RegistroEventos.registrar_evento(
                f"Reserva creada: {identificador}"
            )
            print("Reserva creada correctamente.")
            return reserva

        finally:
            print("Proceso de creacion de reserva finalizado.")

    def confirmar_reserva(self, identificador, impuesto=0, descuento=0):
        try:
            reserva = self.__buscar_reserva(identificador)

            costo = reserva.confirmar(impuesto, descuento)

        except Exception as error:
            RegistroEventos.registrar_error(
                "Error al confirmar reserva", error
            )
            raise

        else:
            RegistroEventos.registrar_evento(
                f"Reserva {identificador} confirmada. "
                f"Costo: ${costo:,.2f}"
            )
            print(f"Reserva confirmada. Total: ${costo:,.2f}")
            return costo

        finally:
            print("Proceso de confirmacion finalizado.")

    def cancelar_reserva(self, identificador):
        try:
            reserva = self.__buscar_reserva(identificador)
            reserva.cancelar()

        except Exception as error:
            RegistroEventos.registrar_error(
                "Error al cancelar reserva", error
            )
            raise

        else:
            RegistroEventos.registrar_evento(
                f"Reserva {identificador} cancelada."
            )
            print("Reserva cancelada correctamente.")

        finally:
            print("Proceso de cancelacion finalizado.")

    def __buscar_reserva(self, identificador):
        for reserva in self.__reservas:
            if reserva.identificador == identificador:
                return reserva

        raise ReservaInvalidaError(
            f"No existe la reserva {identificador}."
        )

    # =================================================
    # CONSULTAS
    # =================================================

    def mostrar_clientes(self):
        print("\n========== CLIENTES ==========")

        if not self.__clientes:
            print("No hay clientes registrados.")
            return

        for cliente in self.__clientes:
            print(cliente.describir())

    def mostrar_servicios(self):
        print("\n========== SERVICIOS ==========")

        if not self.__servicios:
            print("No hay servicios registrados.")
            return

        for servicio in self.__servicios:
            print(servicio.describir())

    def mostrar_reservas(self):
        print("\n========== RESERVAS ==========")

        if not self.__reservas:
            print("No hay reservas registradas.")
            return

        for reserva in self.__reservas:
            print(reserva.describir())

    # =================================================
    # DEMOSTRACION AUTOMATICA
    # =================================================

    def ejecutar_pruebas(self):
        print("\n")
        print("=" * 55)
        print(" DEMOSTRACION AUTOMATICA - SOFTWARE FJ ")
        print("=" * 55)

        exitosas = 0
        fallidas = 0

        def ejecutar(numero, descripcion, operacion):
            nonlocal exitosas, fallidas

            print(f"\nPRUEBA {numero}: {descripcion}")

            try:
                operacion()

            except Exception as error:
                fallidas += 1
                RegistroEventos.registrar_error(
                    f"Prueba {numero} fallida: {descripcion}",
                    error
                )
                print(f"ERROR CONTROLADO: {error}")

            else:
                exitosas += 1
                print("RESULTADO: Operacion exitosa.")

            finally:
                print(f"Prueba {numero} finalizada.")

        # PRUEBA 1: Registrar cliente valido
        cliente1 = Cliente(
            "C001",
            "Simon Sanchez",
            "1234567890",
            "simon@gmail.com",
            "3001234567"
        )

        ejecutar(
            1,
            "Registro de cliente valido",
            lambda: self.registrar_cliente(cliente1)
        )

        # PRUEBA 2: Registrar cliente con correo incorrecto
        def cliente_invalido():
            Cliente(
                "C002",
                "Carlos Perez",
                "1234567891",
                "correo_incorrecto",
                "3001234568"
            )

        ejecutar(
            2,
            "Registro de cliente con correo invalido",
            cliente_invalido
        )

        # PRUEBA 3: Registrar segundo cliente
        cliente2 = Cliente(
            "C003",
            "Maria Lopez",
            "1234567892",
            "maria@gmail.com",
            "3001234569"
        )

        ejecutar(
            3,
            "Registro de segundo cliente",
            lambda: self.registrar_cliente(cliente2)
        )

        # PRUEBA 4: Intentar registrar documento duplicado
        cliente_duplicado = Cliente(
            "C004",
            "Pedro Gomez",
            "1234567890",
            "pedro@gmail.com",
            "3001234570"
        )

        ejecutar(
            4,
            "Deteccion de cliente duplicado",
            lambda: self.registrar_cliente(cliente_duplicado)
        )

        # PRUEBA 5: Crear servicio de salas
        sala = ReservaSala(
            "S001",
            "Sala de reuniones",
            50000,
            20
        )

        ejecutar(
            5,
            "Creacion de servicio de reserva de salas",
            lambda: self.registrar_servicio(sala)
        )

        # PRUEBA 6: Crear servicio de equipos
        equipo = AlquilerEquipo(
            "S002",
            "Computador portatil",
            15000,
            10
        )

        ejecutar(
            6,
            "Creacion de servicio de alquiler de equipos",
            lambda: self.registrar_servicio(equipo)
        )

        # PRUEBA 7: Crear servicio de asesoria
        asesoria = Asesoria(
            "S003",
            "Asesoria informatica",
            80000,
            "Desarrollo de software"
        )

        ejecutar(
            7,
            "Creacion de servicio de asesoria",
            lambda: self.registrar_servicio(asesoria)
        )

        # PRUEBA 8: Crear servicio incorrecto
        def servicio_invalido():
            ReservaSala(
                "S004",
                "Sala incorrecta",
                -50000,
                0
            )

        ejecutar(
            8,
            "Creacion de servicio con parametros incorrectos",
            servicio_invalido
        )

        # PRUEBA 9: Crear reserva correctamente
        def reserva_correcta():
            self.crear_reserva(
                "R001",
                "1234567890",
                "S001",
                2
            )

        ejecutar(
            9,
            "Creacion de reserva valida",
            reserva_correcta
        )

        # PRUEBA 10: Confirmar reserva
        ejecutar(
            10,
            "Confirmacion de reserva",
            lambda: self.confirmar_reserva(
                "R001",
                impuesto=19,
                descuento=10
            )
        )

        # PRUEBA 11: Intentar confirmar reserva inexistente
        ejecutar(
            11,
            "Confirmacion de reserva inexistente",
            lambda: self.confirmar_reserva("R999")
        )

        # PRUEBA 12: Crear reserva con servicio no disponible
        def reserva_no_disponible():
            equipo.cambiar_disponibilidad(False)

            self.crear_reserva(
                "R002",
                "1234567892",
                "S002",
                3
            )

            self.confirmar_reserva("R002")

        ejecutar(
            12,
            "Intento de reserva con servicio no disponible",
            reserva_no_disponible
        )

        # PRUEBA 13: Cancelar reserva
        ejecutar(
            13,
            "Cancelacion de reserva",
            lambda: self.cancelar_reserva("R001")
        )

        # PRUEBA 14: Intentar cancelar reserva inexistente
        ejecutar(
            14,
            "Cancelacion de reserva inexistente",
            lambda: self.cancelar_reserva("R999")
        )

        # PRUEBA 15: Calculo de costo con descuento e impuesto
        def calcular_costo():
            total = sala.calcular_costo(
                3,
                impuesto=19,
                descuento=10
            )
            print(f"Costo calculado: ${total:,.2f}")

        ejecutar(
            15,
            "Calculo de costos con impuestos y descuentos",
            calcular_costo
        )

        # PRUEBA 16: Calculo con parametros incorrectos
        ejecutar(
            16,
            "Calculo con impuesto invalido",
            lambda: sala.calcular_costo(
                2,
                impuesto=150
            )
        )

        # PRUEBA 17: Procesar reserva cancelada
        ejecutar(
            17,
            "Procesamiento de reserva cancelada",
            lambda: self.__buscar_reserva("R001").procesar()
        )

        # Resumen final
        print("\n")
        print("=" * 55)
        print(" RESUMEN DE LAS PRUEBAS ")
        print("=" * 55)
        print(f"Operaciones exitosas: {exitosas}")
        print(f"Operaciones con errores controlados: {fallidas}")
        print(f"Total de operaciones: {exitosas + fallidas}")
        print("=" * 55)

        RegistroEventos.registrar_evento(
            f"Demostracion terminada. "
            f"Exitosas: {exitosas}. Fallidas: {fallidas}."
        )

        print("\nEl sistema continua funcionando.")
        print("Los eventos y errores se guardaron en logs.txt.")

        self.mostrar_clientes()
        self.mostrar_servicios()
        self.mostrar_reservas()


# =====================================================
# MENU PRINCIPAL
# =====================================================

def mostrar_menu():
    print("\n")
    print("=" * 50)
    print("          EMPRESA SOFTWARE FJ")
    print("       SISTEMA DE GESTION EMPRESARIAL")
    print("=" * 50)
    print("1. Registrar cliente")
    print("2. Registrar servicio")
    print("3. Crear reserva")
    print("4. Confirmar reserva")
    print("5. Cancelar reserva")
    print("6. Mostrar clientes")
    print("7. Mostrar servicios")
    print("8. Mostrar reservas")
    print("9. Ejecutar demostracion automatica")
    print("0. Salir")
    print("=" * 50)


def iniciar_sistema():
    sistema = SistemaSoftwareFJ()

    print("\nBienvenido al sistema Software FJ.")

    while True:
        mostrar_menu()

        try:
            opcion = input("Seleccione una opcion: ").strip()

            if opcion == "1":
                cliente = Cliente(
                    input("Identificador: "),
                    input("Nombre: "),
                    input("Documento: "),
                    input("Correo: "),
                    input("Telefono: ")
                )

                sistema.registrar_cliente(cliente)

            elif opcion == "2":
                print("\nTipos de servicios:")
                print("1. Reserva de salas")
                print("2. Alquiler de equipos")
                print("3. Asesorias")

                tipo = input("Seleccione el tipo: ").strip()

                identificador = input("Identificador: ")
                nombre = input("Nombre del servicio: ")
                tarifa = float(input("Tarifa por hora: "))

                if tipo == "1":
                    capacidad = int(input("Capacidad de la sala: "))

                    servicio = ReservaSala(
                        identificador,
                        nombre,
                        tarifa,
                        capacidad
                    )

                elif tipo == "2":
                    cantidad = int(input("Cantidad de equipos: "))

                    servicio = AlquilerEquipo(
                        identificador,
                        nombre,
                        tarifa,
                        cantidad
                    )

                elif tipo == "3":
                    especialidad = input("Especialidad: ")

                    servicio = Asesoria(
                        identificador,
                        nombre,
                        tarifa,
                        especialidad
                    )

                else:
                    raise DatosInvalidosError(
                        "El tipo de servicio seleccionado no existe."
                    )

                sistema.registrar_servicio(servicio)

            elif opcion == "3":
                sistema.crear_reserva(
                    input("Identificador de reserva: "),
                    input("Documento del cliente: "),
                    input("Identificador del servicio: "),
                    float(input("Duracion en horas: "))
                )

            elif opcion == "4":
                identificador = input("Identificador de reserva: ")
                impuesto = float(input("Impuesto (%): "))
                descuento = float(input("Descuento (%): "))

                sistema.confirmar_reserva(
                    identificador,
                    impuesto,
                    descuento
                )

            elif opcion == "5":
                identificador = input("Identificador de reserva: ")
                sistema.cancelar_reserva(identificador)

            elif opcion == "6":
                sistema.mostrar_clientes()

            elif opcion == "7":
                sistema.mostrar_servicios()

            elif opcion == "8":
                sistema.mostrar_reservas()

            elif opcion == "9":
                sistema.ejecutar_pruebas()

            elif opcion == "0":
                RegistroEventos.registrar_evento(
                    "El usuario cerro el sistema."
                )
                print("Gracias por utilizar Software FJ.")
                break

            else:
                raise DatosInvalidosError(
                    "Seleccione una opcion valida del menu."
                )

        except (ValueError, TypeError, ErrorSoftwareFJ) as error:
            print(f"\nERROR CONTROLADO: {error}")
            RegistroEventos.registrar_error(
                "Error durante la ejecucion del menu",
                error
            )

        except Exception as error:
            print(f"\nERROR INESPERADO: {error}")
            RegistroEventos.registrar_error(
                "Error inesperado en el sistema",
                error
            )

            print("El sistema seguira funcionando.")

        finally:
            print("\nFin de la operacion solicitada.")


# =====================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# =====================================================

if __name__ == "__main__":
    try:
        iniciar_sistema()

    except Exception as error:
        RegistroEventos.registrar_error(
            "Error critico al iniciar Software FJ",
            error
        )

        print(f"No se pudo iniciar el sistema: {error}")

    finally:
        print("\nSoftware FJ - Programa finalizado.")
