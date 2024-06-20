from Estadio import Estadio
from ProductoComida import ProductoComida
from Equipo import Equipo
from Partido import Partido
from InfoPartido import InfoPartido
from Producto import Producto
from ProductoBebida import ProductoBebida
from Restaurante import Restaurante
from Cliente import Cliente
from ClienteGeneral import ClienteGeneral
from ClienteVip import ClienteVip
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

    def registrar_cliente(self):
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

        print("\n\tCliente registrado con éxito")
        cliente = Cliente(nombre, apellido, cedula, edad)
        cliente.descuento()
        return cliente

    def seleccionar_partido(self):
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
        return partido_seleccionado
    
    def crear_ticket(self, cliente, partido_seleccionado, tipo_ticket):
        id_del_ticket = self.tickets_id["General"] + self.tickets_id["Vip"]
        while True:
            id_del_ticket = random.randint(1000000, 99999999)
            if id_del_ticket not in self.tickets_id["General"] + self.tickets_id["Vip"]:
                break

        seat = self.ver_mapa_asientos(partido_seleccionado)

        if tipo_ticket == "General":
            ticket = ClienteGeneral(id_del_ticket, partido_seleccionado, partido_seleccionado.stadium_id,seat)
            ticket.descuento = cliente.descuento_1
            return ticket
    
        elif tipo_ticket == "Vip":
            ticket = ClienteVip(id_del_ticket, partido_seleccionado, partido_seleccionado.stadium_id,seat)
            ticket.descuento = cliente.descuento_1
            return ticket


    def comprar_ticket(self):
        while True:
            try:
                print("¿Desea registrarse en nuestro sistema? Ingrese el numero asociado a su seleecion.")
                print("1. Sí")
                print("2. No")
                opt_2 = int(input("\n> ").strip())
                if opt_2 < 1 or opt_2 > 2:
                    raise Exception
                break
            except:
                print("\n\tOpción inválida")
                
        if opt_2 == 1:
            cliente = self.registrar_cliente()
            partido = self.seleccionar_partido()
        while True:
            try:
                print("\n\tTipos de entradas disponibles")
                print("1.General")
                print("2.Vip")
                option = int(input("\nSeleccione el tipo de entrada\n> ").strip())
                if option < 1 or option > 2:
                    raise Exception
                break
            except:
                print("\n\tOpción inválida")
                
        if option == 1:
            while True: 
                ticket = self.crear_ticket(cliente, partido, "General")
                ticket.calcular_monto()
                print(f"\n\tInformación del ticket general\n")	
                ticket.show_info()

                while True:
                    try:
                        print("\n\t¿Desea confirmar su compra?")
                        print("-Sí (ingrese 1)")
                        print("-No (ingrese 2)")
                        opt = int(input("\n> ").strip())
                        if opt < 1 or opt > 2:
                            raise Exception
                        break
                    except:
                        print("\n\tOpción inválida")

                if opt == 1:
                    cliente.tickets.append(ticket)
                    self.tickets.append(ticket)
                    partido.asientos_tomados.append(ticket.seat)
                    self.tickets_id["General"].append(ticket.id_ticket)
                    print("\n\tCompra realizada con éxito!") 

                else:
                    print("\n\tCompra cancelada")
                    break
                
                if partido.tickets_generales == 0:
                    print("\n\tNo hay más entradas General disponibles")
                    break

                while True:
                    try:
                        print("\n\t¿Desea comprar otra entrada?")
                        print("-Sí (ingrese 1)")
                        print("-No (ingrese 2)")
                        opt_1 = int(input("\nIngrese el numero de la opcion que desea ejecutar\n> ").strip())
                        if opt_1 < 1 or opt_1 > 2:
                            raise Exception
                        break
                    except:
                        print("\n\tOpción inválida")

                if opt_1 == 2:
                    print("\n\tGracias por su compra!!!")
                    break
                
        else:
            while True:
                ticket = self.crear_ticket(cliente, partido, "Vip")
                ticket.calcular_monto()
                print(f"\n\tInformación del ticket vip\n")	
                ticket.show_info()

                while True:
                    try:
                        print("\n\t¿Desea confirmar su compra?")
                        print("-Sí (ingrese 1)")
                        print("-No (ingrese 2)")
                        opt = int(input("\n> ").strip())
                        if opt < 1 or opt > 2:
                            raise Exception
                        break
                    except:
                        print("\n\tOpción inválida")

                if opt == 1:
                    cliente.tickets.append(ticket)
                    self.tickets.append(ticket)
                    partido.asientos_tomados.append(ticket.seat)
                    self.tickets_id["Vip"].append(ticket.id_ticket)
                    print("\n\tCompra realizada con éxito!")
                else:
                    print("\n\tCompra cancelada")
                    break
                
                if partido.tickets_vip == 0:
                    print("\n\tNo hay más entradas Vip disponibles")
                    break

                while True:
                    try:
                        print("\n\t¿Desea comprar otra entrada?")
                        print("-Sí (ingrese 1)")
                        print("-No (ingrese 2)")
                        opt_1 = int(input("\nIngrese el numero de la opcion que desea ejecutar\n> ").strip())
                        if opt_1 < 1 or opt_1 > 2:
                            raise Exception
                        break
                    except:
                        print("\n\tOpción inválida")

                if opt_1 == 2:
                    print("\n\tGracias por su compra!!!")
                    break
        
        if len(cliente.tickets) > 0:
            cliente.calcular_tickets()
            self.merge_sort(self.clientes, lambda x: x.cedula)
            aux_1 = self.binary_search(self.clientes, 0, len(self.clientes) - 1, cliente.cedula, lambda x: x.cedula)
            if aux_1 == -1:
                self.clientes.append(cliente)
            print(f"\nEntradas compradas en total: {len(cliente.tickets)}")
            print(f"Monto total: ${cliente.total_tickets}")


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


    def ver_mapa_asientos(self, partido_seleccionado):
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
                row = int(input("Selecciona el numero de fila: "))
                seat = int(input("Selecciona el numero de asiento: "))
                if row < 1 or row > 10 or seat < 1 or seat > 10:
                    print("Error. Numero de asiento invalido.")
                    continue
                if seating_map[row][seat - 1] != ' ':
                    print("Error. Asiento ya ocupado.")
                    continue
                break
            except ValueError:
                print("Error. Invalid input.")
                continue

        seating_map[seat] = f"{partido_seleccionado}"
        return seat

    def merge_sort(self, my_list, my_func = lambda x: x):
        """Ordena una lista de menor a mayor, usando el algoritmo de merge sort
        Args:
            my_list (List): lista a ordenar
            my_func: función que se aplicará a cada elemento de la lista
        """
        if len(my_list) > 1:
            mid = len(my_list) // 2
            left = my_list[:mid]
            right = my_list[mid:]
            self.merge_sort(left, my_func)
            self.merge_sort(right, my_func)
            i = j = k = 0

            while i < len(left) and j < len(right):
                if my_func(left[i]) <= my_func(right[j]):
                  my_list[k] = left[i]
                  i += 1
                else:
                    my_list[k] = right[j]
                    j += 1
                k += 1

            while i < len(left):
                my_list[k] = left[i]
                i += 1
                k += 1

            while j < len(right):
                my_list[k] = right[j]
                j += 1
                k += 1

    def binary_search(self, arr, low, high, x, my_func = lambda x: x):
        """Busca un elemento en una lista, usando el algoritmo de búsqueda binaria
        Args:
            arr (List): lista en la que se buscará el elemento
            low (Int): índice inferior de la lista
            high (Int): índice superior de la lista
            x: elemento a buscar
            my_func: función que se aplicará a cada elemento de la lista
        Returns:
            Int: índice del elemento en la lista
        """
        if high >= low:
            mid = (high + low) // 2
            if my_func(arr[mid]) == x:
                return mid
            elif my_func(arr[mid]) > x:
                return self.binary_search(arr, low, mid - 1, x, my_func)
            else:
                return self.binary_search(arr, mid + 1, high, x, my_func)
        else:
            return -1
            
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
            self.comprar_ticket()
