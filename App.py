from Estadio import Estadio
from ProductoComida import ProductoComida
from Equipo import Equipo
from Partido import Partido
from InfoPartido import InfoPartido
from Producto import Producto
from ProductoBebida import ProductoBebida
from Restaurante import Restaurante
from Cliente import Cliente
from Ticket import Ticket
import random
import requests


class App():
    def __init__(self):
        self.estadio = []
        self.productos = []
        self.equipo = []
        self.partido = []
        self.paises = []
        self.restaurantes = []
        self.clientes = []
        self.tickets = []
        self.tickets_usados = []
        self.tickets_id = {
            "General": [],
            "Vip": []
        }

    def get_info_api(self, parametro):
        # parametro de la API (String): puede ser 'matches', 'teams' o 'stadiums' accediendo a todos los datos
        # Retorno (Dictionary): diccionario con la informacion de la API
        url = f"https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/{parametro}.json"
        if parametro == "stadiums":
            response = requests.request("GET", url)
            return response.json()
        elif parametro == "teams":
            response = requests.request("GET", url)
            return response.json()
        else:
            response = requests.request("GET", url)
            return response.json()
        
    def registrar_equipos(self):
        equipos = self.get_info_api("teams")
        for info_equipo in equipos:
            equipo = Equipo(info_equipo["id"], info_equipo["code"], info_equipo["name"], info_equipo["group"] )
            self.equipo.append(equipo)
            print(equipo.show())

    def registrar_estadios(self):
        estadios = self.get_info_api("stadiums")
        for info_stadium in estadios:
            stadium = Estadio(info_stadium["id"], info_stadium["name"], info_stadium["city"], info_stadium["capacity"])
            self.estadio.append(stadium)
            print(stadium.show())

            for info_restaurante in info_stadium["restaurants"]:
                restaurante = Restaurante(info_restaurante["name"])
                self.restaurantes.append(restaurante)

                for info_producto in info_restaurante["products"]:
                    producto = Producto(info_producto["name"], info_producto["quantity"], info_producto["price"], info_producto["stock"], info_producto["adicional"] )
                    self.productos.append(producto)

    def registrar_partidos(self):
        partidos = self.get_info_api("matches")
        for info_partido in partidos:
            partido = InfoPartido(info_partido["home"]["name"], info_partido["away"]["name"], info_partido["date"], info_partido["stadium_id"])
            self.partido.append(partido)
            print(partido.show())

    def buscar_partidos_por_pais(self):
        equipos = self.get_info_api("teams")
        for info_equipo in equipos:
            print(info_equipo["name"])
        while True:
            try:
                pais = input("Escriba el nombre del país que desea buscar: ")
                if not pais.isalpha():
                    print("Error.")
                    continue
                else:
                    break
            except:
                print("Error. Introduzca un nombre de país válido.")

        partidos_encontrados = []
        for partido in self.partido:
            if partido.equipo_Local == pais or partido.equipo_Visitante == pais:
                partidos_encontrados.append(partido)

        if partidos_encontrados:
            print(f"\n\t\tPartidos encontrados para {pais}:\n")
            for partido in partidos_encontrados:
                print(f"Local: {partido.equipo_Local}\nVisitante: {partido.equipo_Visitante}\nFecha: {partido.fecha_partido}\nEstadio: {partido.stadium_id}\n")
        else:   
            print(f"\n\t\tNo se encontraron partidos para el país {pais}.")
    
    def buscar_partidos_por_estadio(self):
        estadios = self.get_info_api("stadiums")
        for info_stadium in estadios:
            print(info_stadium["id"])
        estadio_id = input("Introduzca el ID del estadio que desea buscar: ")

        partidos_encontrados = []
        for partido in self.partido:
            if partido.stadium_id == estadio_id:
                partidos_encontrados.append(partido)

        if partidos_encontrados:
            print(f"\n\t\tPartidos encontrados en el estadio con ID {estadio_id}:\n")
            for partido in partidos_encontrados:
                print(f"Local: {partido.equipo_Local}\nVisitante: {partido.equipo_Visitante}\nFecha: {partido.fecha_partido}\nEstadio: {partido.stadium_id}\n")
        else:   
            print(f"\n\t\tNo se encontraron partidos en el estadio con ID {estadio_id}.") 

    def buscar_partidos_por_fecha(self):
        partidos = self.get_info_api("matches")
        fechas = set()

        for info_partido in partidos:
            fecha = info_partido["date"]
            fechas.add(fecha)

        fechas = sorted(fechas, reverse=True) 

        print("Fechas disponibles:")
        for fecha in fechas:
            print(fecha)

        fecha = input("Introduzca la fecha que desea buscar (formato: AAAA-MM-DD): ")

        partidos_encontrados = []
        for partido in self.partido:
            if partido.fecha_partido == fecha:
                partidos_encontrados.append(partido)

        if partidos_encontrados:
            print(f"\n\t\tPartidos encontrados para la fecha {fecha}:\n")
            for partido in partidos_encontrados:
                print(f"Local: {partido.equipo_Local}\nVisitante: {partido.equipo_Visitante}\nFecha: {partido.fecha_partido}\nEstadio: {partido.stadium_id}\n")
        else:   
            print(f"\n\t\tNo se encontraron partidos para la fecha {fecha}.")

    def comprar_entradas(self):
        print("BIENVENIDO, Ingrese los siguientes datos solicitados por el sistema: ")
        nombre = input("Introduzca su nombre: ").title()
        apellido = input("Introduzca su apellido: ").title()
        while True:
            try: 
                cedula = input("Introduzca su cedula: ")
                cedula = int(cedula)
                if cedula < 0:
                    print("Error. La cedula no debe ser negativa.")
                    continue
                break
            except ValueError:
                print("Error. Introduzca un numero valido.")
                continue
        while True:
            try: 
                edad = input("Introduzca su edad: ")
                edad = int(edad)
                if edad < 0:
                    print("Error. La edad no debe ser negativa.")
                    continue
                break
            except ValueError:
                print("Error. Introduzca un numero valido.")
                continue

        #Se imprimen los partidos disponibles para comprar las entradas
        print("Partidos disponibles:")
        for i, partido in enumerate(self.partido):
            print(f"{i+1}. {partido.equipo_Local} vs {partido.equipo_Visitante}, {partido.fecha_partido}")
            print(f"Estadio: {partido.stadium_id}\n")
        #Seleccionar un partido disponible
        while True:
            try:
                seleccion = int(input("Seleccione el numero del partido que desea comprar la entrada: "))
                if seleccion < 1 or seleccion > len(self.partido):
                    print("Error. Seleccione un numero valido.")
                    continue
                else:
                    break
            except:
                print("Error. Introduzca un numero valido")
                continue

        #Comprar la entrada al partido
        partido_seleccionado = self.partido[seleccion - 1]
        print(f"Ha seleccionado el partido: {partido_seleccionado.equipo_Local} vs {partido_seleccionado.equipo_Visitante}, {partido_seleccionado.fecha_partido}")

        # Permite al usuario seleccionar su tipo de entrada
        while True:
            tipo_de_entrada = input("""Ingresa el tipo de entrada la cual quieres comprar para el partido: 
1. General 
2. Vip 
""")
            if tipo_de_entrada != "1" and tipo_de_entrada != "2":
                print("Error. Tipo de entrada invalido")
                continue
            else:
                break

        if tipo_de_entrada == "1":
            self.ver_mapa_asientos(partido_seleccionado, "General", nombre, apellido)
            precio_entrada = 35
        else:
            self.ver_mapa_asientos(partido_seleccionado, "Vip", nombre, apellido)
            precio_entrada = 75

        # Calcular el precio de la entrada verificando si el id es un numero vampiro
        if cedula < 10 or cedula % 2 == 0:
            descuento = 0
            mensaje_descuento = "Su entrada no tiene un descuento ya que no es un numero vampiro"

        for i in range(2, int(cedula ** 0.5) + 1):
            if cedula % i == 0:
                mitad_izq = [int(digit) for digit in str(i)]
                mitad_der = [int(digit) for digit in str(cedula // i) if int(digit) not in mitad_izq]
                if len(mitad_izq) > 0 and len(mitad_der) > 0:
                    product = int(''.join(str(digit) for digit in mitad_izq + mitad_der))
                    if product == cedula:
                        descuento = 0.5
                        mensaje_descuento = "Su entrada tiene un descuento del 50% por ser un número vampiro."
                    else:
                        descuento = 0
                        mensaje_descuento = "Su entrada no tiene un descuento ya que no es un numero vampiro"

        subtotal = precio_entrada * (1 - descuento)
        iva = subtotal * 0.16
        total = subtotal + iva

        print(f"\nCosto de la entrada:")
        print(f"Subtotal: ${subtotal}")
        print(mensaje_descuento)
        print(f"IVA: ${iva}")
        print(f"Total: ${total}")

        # Preguntar al cliente si desea proceder con el pago
        while True:
            pagar = input("\n¿Desea proceder con el pago? (s/n): ")
            if pagar.lower() == "s":
                print("\nPago exitoso!")
                break
            elif pagar.lower() == "n":
                print("\nPago cancelado.")
                return
            else:
                print("Error. Opción invalida.")


    def ver_mapa_asientos(self, partido_seleccionado, tipo_de_entrada, nombre, apellido):
        #Crea un mapa de asientos
        seating_map = {}
        for row in range(1, 11):
            seating_map[row] = [' ' for _ in range(1, 11)]

        #Imprime el mapa de los asientos
        print("Seating Map:")
        print("  ", end="")
        for seat in range(1, 11):
            print(f" {seat}", end="")
        print()
        for row, seats in seating_map.items():
            print(f"{row} {' '.join(seats)}")

        #Codigo para seleccionar el asiento
        while True:
            try:
                row = int(input("Enter the row number: "))
                seat = int(input("Enter the seat number: "))
                if row < 1 or row > 10 or seat < 1 or seat > 10:
                    print("Error. Invalid seat number.")
                    continue
                if seating_map[row][seat - 1] != ' ':
                    print("Error. Seat already occupied.")
                    continue
                break
            except ValueError:
                print("Error. Invalid input.")
                continue

        seating_map[seat] = f"{nombre} {apellido}"
        return print(f"\nEl asiento {seat} en la fila {row} ha sido seleccionado.")

    def menu(self):
        self.registrar_equipos()
        self.registrar_partidos()
        self.registrar_estadios
        print('-- EUROCOPA 2024 --\n Bienvenido/a')
        while True:
                try:
                    print("\n\t\tSeleeciona el numero asociado a tu eleccion:\n")
                    print("1.Ver todos los partidos de la Euro 2024")
                    print("2.Buscar todos los partidos de un país")
                    print("3.Buscar todos los partidos que se jugarán en un estadio específico")
                    print("4.Buscar todos los partidos que se jugarán en una fecha determinada")
                    print("5.Comprar tickets")
                    print("6.Verificar tickets y registrar asistencia")
                    print("7.Comprar productos")
                    print("8.Buscar productos")
                    print("9.Mostrar estadísticas")
                    print("10.Cargar datos de la API (Cargar los datos a su estado inicial)")
                    print("11.Salir")

                    option = int(input("\nIngrese el numero de la opción que desea ejecutar\n> "))
                    if option not in range(1,12):
                        raise Exception
                    break
                except:
                    print("\nOpción invalida\n")
                
        if option == 1:
            print("\n\t\tLista de todos los partidos:\n")
            self.registrar_partidos()

        elif option == 2:
            print("\n\t\tBuscar todos los partidos de un país\n")
            self.buscar_partidos_por_pais()
            
        elif option == 3:
            print("\n\t\tBuscar todos los partidos que se jugarán en un estadio específico\n")
            self.buscar_partidos_por_estadio()

        elif option == 4:
            print("\n\t\tBuscar todos los partidos que se jugarán en una fecha determinada\n")
            self.buscar_partidos_por_fecha()

        elif option == 5:
            print("\n\t\tComprar tickets\n")
            self.comprar_entradas()


from Equipo import Equipo

class Partido(Equipo):
    def __init__(self, id, equipo_Local, equipo_Visitante, fecha, stadium_id):
        super().__init__(id, equipo_Local, equipo_Visitante)
        self.fecha = fecha
        self.stadium_id = stadium_id
        self.general_tickets = [0]
        self.vip_tickets = stadium.capacity[1]
        self.seats_taken = []
        self.stadium_attendance = 0
    

    def get_date(self):
        return self.fecha

    def show(self):
        return f"Partido: {self.equipo_Local} vs. {self.equipo_Visitante}\nEstadio: {self.stadium_id()}\nFecha: {self.fecha}"