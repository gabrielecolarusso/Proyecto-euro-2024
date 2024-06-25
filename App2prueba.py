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

            for info_restaurante in info_stadium["restaurants"]:
                restaurante = Restaurante(info_restaurante["name"])
                self.restaurantes.append(restaurante)
                stadium.restaurantes.append(restaurante)

                for info_producto in info_restaurante["products"]:
                    producto = Producto(info_producto["name"], info_producto["quantity"], info_producto["price"], info_producto["stock"], info_producto["adicional"] )
                    self.productos.append(producto)
                    restaurante.productos.append(producto)

            self.estadio.append(stadium)

    def registrar_partidos(self):
        partidos = self.get_info_api("matches")
        for info_partido in partidos:
            stadium = list(filter(lambda x: x.id == info_partido["stadium_id"], self.estadio))[0]
            partido = Partido(info_partido["id"],info_partido["home"]["name"], info_partido["away"]["name"], info_partido["date"], stadium)
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
                print(f"Local: {partido.equipo_Local}\nVisitante: {partido.equipo_Visitante}\nFecha: {partido.fecha}\nEstadio: {partido.stadium.name}\n")
        else:   
            print(f"\n\t\tNo se encontraron partidos para el país {pais}.")
    
    def buscar_partidos_por_estadio(self):
        estadios = self.get_info_api("stadiums")
        for info_stadium in estadios:
            print(info_stadium["name"])
        estadio_id = input("Introduzca el nombre del estadio que desea buscar: ")

        partidos_encontrados = []
        for partido in self.partido:
            if partido.stadium.name == estadio_id:
                partidos_encontrados.append(partido)

        if partidos_encontrados:
            print(f"\n\t\tPartidos encontrados en el estadio con ID {estadio_id}:\n")
            for partido in partidos_encontrados:
                print(f"Local: {partido.equipo_Local}\nVisitante: {partido.equipo_Visitante}\nFecha: {partido.fecha}\nEstadio: {partido.stadium.name}\n")
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
            if partido.fecha == fecha:
                partidos_encontrados.append(partido)

        if partidos_encontrados:
            print(f"\n\t\tPartidos encontrados para la fecha {fecha}:\n")
            for partido in partidos_encontrados:
                print(f"Local: {partido.equipo_Local}\nVisitante: {partido.equipo_Visitante}\nFecha: {partido.fecha}\nEstadio: {partido.stadium.name}\n")
        else:   
            print(f"\n\t\tNo se encontraron partidos para la fecha {fecha}.")

    def registrar_cliente(self):
        print("BIENVENIDO, Ingrese los siguientes datos solicitados por el sistema: ")
        self.merge_sort(self.clientes, lambda x:x.cedula)
        while True:
            try:
                nombre = input("\nIngrese su nombre\n> ").strip().capitalize()
                if nombre == "" or not nombre.isalpha():
                    raise Exception
                break
            except:
                print("\n\tNombre inválido")
        
        while True:
            try:
                apellido = input("\nIngrese su apellido\n> ").strip().capitalize()
                if apellido == "" or not apellido.isalpha():
                    raise Exception
                break
            except:
                print("\n\tApellido inválido")
            
        while True:
            try:
                cedula = input("\nIngrese su Cedula\n> ").strip()
                if len(cedula) == 0 or not cedula.isnumeric():
                    raise Exception
                aux = self.binary_search(self.clientes, 0, len(self.clientes) - 1, cedula, lambda x: x.cedula)
                if aux != -1:
                    print("\n\tEsta cedula ya se encuentra registrada")
                    raise Exception
                break
            except:
                print("\n\Cedula inválida")

        while True:
            try:
                edad = int(input("\nIngrese su edad\n> ").strip())
                if edad <= 0 or edad > 125:
                    raise Exception
                break
            except:
                print("\n\tEdad inválida")

        print("\n\tEl cliente ha sido registrado con éxito\n")
        cliente = Cliente(nombre, apellido, cedula, edad)
        cliente.descuento()
        self.clientes.append(cliente)
        return cliente

    def seleccionar_partido(self):
        #Se imprimen los partidos disponibles para comprar las entradas
        print("Partidos disponibles:")
        for i, partido in enumerate(self.partido):
            print(f"{i+1}. {partido.equipo_Local} vs {partido.equipo_Visitante}")
            print(f"Fecha: {partido.fecha}")
            print(f"Estadio: {partido.stadium.name}\n")
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
        print(f"Ha seleccionado el partido: {partido_seleccionado.equipo_Local} vs {partido_seleccionado.equipo_Visitante}, {partido_seleccionado.fecha}, {partido_seleccionado.stadium.name}")
        return partido_seleccionado
    
    def crear_ticket(self, cliente, partido_seleccionado, tipo_ticket):
        id_del_ticket = self.tickets_id["General"] + self.tickets_id["Vip"]
        while True:
            id_del_ticket = random.randint(1000000, 99999999)
            if id_del_ticket not in self.tickets_id["General"] + self.tickets_id["Vip"]:
                break

        seat = self.ver_mapa_asientos(partido_seleccionado)

        if tipo_ticket == "General":
            ticket = ClienteGeneral(id_del_ticket, partido_seleccionado, partido_seleccionado.stadium,seat)
            ticket.descuento = cliente.descuento_1
            return ticket
    
        elif tipo_ticket == "Vip":
            ticket = ClienteVip(id_del_ticket, partido_seleccionado, partido_seleccionado.stadium,seat)
            ticket.descuento = cliente.descuento_1
            return ticket

    def comprar_ticket(self):
        while True:
            try:
                print("¿Ya se encuenta registrado en nuestro sistema? Ingrese el numero asociado a su seleccion.")
                print("1. Sí")
                print("2. No")
                opt_2 = int(input("\n> ").strip())
                if opt_2 < 1 or opt_2 > 2:
                    raise Exception
                break
            except:
                print("\n\tOpción inválida")

        if opt_2 == 1:
            while True:
                try:
                    cedula = input("\nIngrese su cedula\n> ").strip()
                    if len(cedula) == 0 or not cedula.isnumeric():
                        raise Exception
                    if self.binary_search(self.clientes, 0, len(self.clientes) - 1, cedula, lambda x: x.cedula) == -1:
                        print("\n\tDNI no registrado")
                        raise Exception
                    break
                except:
                    print("\n\tDNI inválido")

            i = self.binary_search(self.clientes, 0, len(self.clientes) - 1, cedula, lambda x: x.cedula)
            cliente = self.clientes[i]
            partido = self.seleccionar_partido()
            print(cliente.show_info())

        else:
            cliente = self.registrar_cliente()
            partido = self.seleccionar_partido()

        while True:
            try:
                print("\n\tTipos de entradas disponibles")
                print("1.General")
                print("2.Vip")
                option = int(input("\nSeleccione el tipo de entrada que desea comprar\n> ").strip())
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
                        print("\n\t¿Desea continuar con su compra?")
                        print("1. Sí ")
                        print("2. No ")
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
                    partido.tickets_generales -= 1
                    print("\n\tLa compra de su ticket ha sido realizada con éxito!") 

                else:
                    print("\n\tCompra cancelada")
                    break
                
                if partido.tickets_generales == 0:
                    print("\n\tNo hay más entradas del tipo General disponibles")
                    break

                while True:
                    try:
                        print("\n\t¿Desea comprar otra entrada?")
                        print("1. Sí ")
                        print("2. No ")
                        opt_1 = int(input("\nIngrese el numero asociado a su eleccion\n> ").strip())
                        if opt_1 < 1 or opt_1 > 2:
                            raise Exception
                        break
                    except:
                        print("\n\tOpción inválida")

                if opt_1 == 2:
                    print("\n\tGracias por la compra de sus boletos!")
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
                        print("1. Sí ")
                        print("2. No")
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
                    partido.tickets_vip -= 1
                    print("\n\tLa compra de su ticket ha sido realizada con éxito!")
                else:
                    print("\n\tCompra cancelada")
                    break
                
                if partido.tickets_vip == 0:
                    print("\n\tNo hay más entradas del tipo Vip disponibles")
                    break

                while True:
                    try:
                        print("\n\t¿Desea comprar otra entrada?")
                        print("1. Sí ")
                        print("2. No ")
                        opt_1 = int(input("\nIngrese el numero asociado a su eleccion\n> ").strip())
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
                print(cliente.show_info())
                self.clientes.append(cliente)
                print(cliente.show_info())
            print(f"\nEntradas totales compradas: {len(cliente.tickets)}")
            print(f"Monto total de las entradas: ${cliente.total_tickets}")

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
    

    def merge_sort(self, mi_lista, mi_func):
        if len(mi_lista) > 1:
            medio = len(mi_lista) // 2
            izquierda = mi_lista[:medio]
            derecha = mi_lista[medio:]
            self.merge_sort(izquierda, mi_func)
            self.merge_sort(derecha, mi_func)
            i = j = k = 0
            while i < len(izquierda) and j < len(derecha):
                if mi_func(izquierda[i]) <= mi_func(derecha[j]):
                    mi_lista[k] = izquierda[i]
                    i += 1
                else:
                    mi_lista[k] = derecha[j]
                    j += 1
                k += 1
            while i < len(izquierda):
                mi_lista[k] = izquierda[i]
                i += 1
                k += 1
            while j < len(derecha):
                mi_lista[k] = derecha[j]
                j += 1
                k += 1

    def binary_search(self, arr, bajo, alto, x, mi_func):
        if alto >= bajo:
            medio = (alto + bajo) // 2
            if mi_func(arr[medio]) == x:
                return medio
            elif mi_func(arr[medio]) > x:
                return self.binary_search(arr, bajo, medio - 1, x, mi_func)
            else:
                return self.binary_search(arr, medio + 1, alto, x, mi_func)
        else:
            return -1
        
    def check_tickets(self):
        while True:
            try:
                ticket_id = int(input("\nIngresa el ID del ticket para su verificacion: "))
                break
            except:
                print("\nIngreso invalido, intente de nuevo\n")
        
        tickets_id = [t for t in self.tickets_id["General"] + self.tickets_id["Vip"]]

        if ticket_id in tickets_id:
            if ticket_id not in self.tickets_usados:
                self.tickets_usados.append(ticket_id)
                print("\n\t\tTicket verificado con exito!!!\n")
                self.merge_sort(self.tickets, lambda x: x.id_ticket)
                ind = self.binary_search(self.tickets, 0, len(self.tickets) - 1, ticket_id, lambda x: x.id_ticket)
                ticket = self.tickets[ind]
                ticket.show_info()

                print("\n\t\tAsistencia registrada con exito!!!\n")

                self.merge_sort(self.partido, lambda x: x.id_partido)
                ind_2 = self.binary_search(self.partido, 0, len(self.partido) - 1, ticket.partido.id_partido, lambda x: x.id_partido)
                game = self.partido[ind_2]
                game.visitas_estadio += 1
            else:
                print("\n\t\tEl ticket ya fue verificado anteriormente\n")

        else:
            print("\n\t\tEl ticket ingresado no existe\n")

    def buscar_productos_por_nombre(self):
        estadios = self.get_info_api("stadiums")
        productos = set()
        for info_stadium in estadios:
            for info_restaurante in info_stadium["restaurants"]:
                for info_producto in info_restaurante["products"]:
                    productos.add(info_producto["name"])

        # Convert the set back to a list for sorting and printing
        productos = list(productos)

        # Sort the products alphabetically
        self.merge_sort(productos, lambda x: x)
        print("\n\t\tProductos Disponibles en todos los restaurantes (Ordenados alfabéticamente):\n")
        for i, producto in enumerate(productos):
            print(f"{i+1}. {producto}")

        nombre_producto = input("\nIngrese el nombre del producto que desea buscar: ").lower()
        productos_encontrados = [
            (p["name"], p["quantity"], p["price"], p["stock"], p["adicional"], info_stadium["name"], info_restaurante["name"])
            for info_stadium in estadios
            for info_restaurante in info_stadium["restaurants"]
            for p in info_restaurante["products"]
            if nombre_producto in p["name"].lower()
        ]

        if len(productos_encontrados) > 0:
            print("\n\tProductos encontrados con ese nombre en los diferentes restaurantes:")
            for i, (producto, quantity, price, stock, adicional, estadio, restaurante) in enumerate(productos_encontrados):
                print(f"{i+1}. Producto: {producto}")
                print(f"Cantidad: {quantity}")
                print(f"Precio: {price}")
                print(f"Stock: {stock}")
                print(f"Tipo: {adicional}")
                print(f"Estadio: {estadio}")
                print(f"Restaurante: {restaurante}\n")
        else:
            print("\n\tNo se encontraron productos con el nombre proporcionado.")

    def buscar_productos_por_tipo(self):
        estadios = self.get_info_api("stadiums")
        productos = set()
        for info_stadium in estadios:
            for info_restaurante in info_stadium["restaurants"]:
                for info_producto in info_restaurante["products"]:
                    productos.add(info_producto["adicional"])

        # Se convierte en lista para ordenarse e imprimirse
        productos = list(productos)

        # Ordena las opciones alfabeticamente
        self.merge_sort(productos, lambda x: x)
        print("\n\t\tTipos de productos disponibles en los restaurantes:\n")
        for i, producto in enumerate(productos):
            print(f"{i+1}. {producto}")

        tipo_producto = input("\nIngrese el tipo de producto que desea buscar: ").lower()
        productos_encontrados = [
            (p["name"], p["quantity"], p["price"], p["stock"], p["adicional"], info_stadium["name"], info_restaurante["name"])
            for info_stadium in estadios
            for info_restaurante in info_stadium["restaurants"]
            for p in info_restaurante["products"]
            if tipo_producto in p["adicional"].lower()
        ]

        if len(productos_encontrados) > 0:
            print("\n\tProductos encontrados con ese tipo en los diferentes restaurantes:")
            for i, (producto, quantity, price, stock, adicional, estadio, restaurante) in enumerate(productos_encontrados):
                print(f"{i+1}.Producto: {producto}")
                print(f"Cantidad: {quantity}")
                print(f"Precio: {price}")
                print(f"Stock: {stock}")
                print(f"Tipo: {adicional}")
                print(f"Estadio: {estadio}")
                print(f"Restaurante: {restaurante}\n")
        else:
            print("\n\tNo se encontraron productos con el tipo proporcionado.")

    def buscar_productos_por_precio(self):
        estadios = self.get_info_api("stadiums")
        productos = set()
        for info_stadium in estadios:
            for info_restaurante in info_stadium["restaurants"]:
                for info_producto in info_restaurante["products"]:
                    productos.add((info_producto["name"], float(info_producto["price"])))

        # Convert the set back to a list for sorting and printing
        productos = list(productos)

        # Sort the products by price
        self.merge_sort(productos, lambda x: x[1])
        print("\n\t\tProductos Disponibles en los restaurantes (Ordenados por precio):\n")
        for i, (producto, precio) in enumerate(productos):
            print(f"{i+1}. Producto: {producto}, Precio: {precio}")

        while True:
            try:
                print("\n\t\tSeleeciona la opción de precio que desea buscar:")
                print("1. Menor que X precio")
                print("2. Igual a X precio")
                print("3. Mayor que X precio")

                option = int(input("\nIngrese el número de la opción que desea ejecutar\n> "))
                if option not in range(1, 4):
                    raise Exception
                break
            except:
                print("\nOpción invalida\n")

        if option == 1:
            precio_x = float(input("\nIngrese el precio máximo que desea buscar: "))
            productos_encontrados = [
                (p[0], p[1])
                for p in productos
                if p[1] < precio_x
            ]

        elif option == 2:
            precio_x = float(input("\nIngrese el precio que desea buscar: "))
            productos_encontrados = [
                (p[0], p[1])
                for p in productos
                if p[1] == precio_x
            ]

        elif option == 3:
            precio_x = float(input("\nIngrese el precio mínimo que desea buscar: "))
            productos_encontrados = [
                (p[0], p[1])
                for p in productos
                if p[1] > precio_x
            ]

        if len(productos_encontrados) > 0:
            print("\n\tProductos encontrados con el precio seleccionado:")
            for i, (producto, precio) in enumerate(productos_encontrados):
                print(f"{i+1}. Producto: {producto}, Precio: {precio}")
        else:
            print("\n\tNo se encontraron productos con el precio proporcionado.")

    def comprar_productos(self):
        aux_2 = True
        while aux_2:
            cedula = input("\nIngrese su cedula\n> ")
            if len(cedula) == 0 or not cedula.isnumeric():
                print("\n\t\tDNI invalido\n")
            else:
                aux_2 = False

        i = self.binary_search(self.clientes, 0, len(self.clientes) - 1, cedula, lambda x: x.cedula)
        cliente = self.clientes[i]

        if len(cliente.tickets) == 0:
            print("\n\t\tNo tiene tickets comprados\n")
            return

        if aux_2:
            cliente = list(filter(lambda x: x.cedula == cedula, self.clientes))[0]
            if list(filter(lambda x: isinstance(x, ClienteVip), cliente.tickets)) == []:
                print("\n\t\tNo puede comprar productos, no es VIP\n")
                aux = False

        stadiums = list(filter(lambda x: isinstance(x, Estadio), self.estadio))
        if len(stadiums) > 1:
            while True:
                try:
                    aux_1 = 0
                    print(f"\n\t\tEstadios\n")
                    for s in stadiums:
                        print(f"\n{aux_1 + 1}. {s.name}")
                        aux_1 += 1
                    stadium_number = int(input("\nIngrese el numero del estadio donde desea comprar\n> "))
                    if stadium_number < 1 or stadium_number > aux_1:
                        raise Exception
                    break
                except:
                    print("\n\t\tOpcion invalida\n")
            stadium = self.estadio[stadium_number - 1]
        else:
            stadium = self.estadio[0]

        if len(stadium.restaurantes) > 1:
            while True:
                try:
                    print(f"\n\t\tRestaurantes del estadio {stadium.name}\n")
                    for i, restaurant in enumerate(stadium.restaurantes):
                        print(f"\n{i+1}. {restaurant.name_restaurante}")
                    print("\nElija el restaurante donde desea comprar")
                    opt = int(input("> "))
                    if opt < 1 or opt > len(stadium.restaurantes):
                        raise Exception
                    break
                except:
                    print("\n\t\tOpcion invalida\n")
            restaurante = stadium.restaurantes[opt-1]
        else:
            restaurante = stadium.restaurantes[0]

        beverages = list(filter(lambda x: isinstance(x, Producto) and x.stock  > 0, restaurante.productos))
        if cliente.edad < 18:
            beverages = list(filter(lambda x: x.type in ["non-alcoholic", "plate", "package"], beverages))
        else:
            beverages = list(filter(lambda x: x.type in ["plate", "package"], beverages))
    
        aux_4 = True
        if len(beverages) == 0:
            print("\n\t\tNo hay productos disponibles\n")
            aux_4 = False
        if aux_4:
            while True:
                beverages = list(filter(lambda x: isinstance(x, Producto) and x.stock  > 0, restaurante.productos))
                if cliente.edad < 18:
                    beverages = list(filter(lambda x: x.type in ["non-alcoholic", "plate", "package"], beverages))
                else:
                    beverages = list(filter(lambda x: x.type in ["plate", "package"], beverages))
                while True:
                    try:
                        aux_1 = 0
                        print(f"\n\t\tProductos de {restaurant.name_restaurante}\n")
                        print("\n\t\t\tComidas y Bebidas\n")
                        for b in beverages:
                            print(f"{aux_1 + 1}. {b.name} - Categoria: {b.type} - Precio: ${b.price} - Cantidad disponible: {b.stock}")
                            aux_1 += 1
                        product_number = int(input("\nIngrese el numero del producto que desea comprar\n> "))
                        if product_number < 1 or product_number > aux_1:
                            raise Exception
                        break
                    except:
                        print("\n\t\tOpcion invalida\n")

                products =  beverages
                product = products[product_number - 1]
                self.merge_sort(restaurante.productos, lambda x: x.name)
                ind_2 = self.binary_search(restaurante.productos, 0, len(restaurante.productos) - 1, product.name, lambda x: x.name)
                real_product = restaurante.productos[ind_2]

                while True:
                    try:
                        quantity = int(input("\nIngrese la cantidad que desea comprar\n> "))
                        if quantity < 1 or quantity > real_product.stock:
                            raise Exception
                        break
                    except:
                        print("\n\t\tCantidad invalida\n")

                if cliente.descuento_2:
                    amount = real_product.price * quantity * 0.85
                    print(f"\n\t\tEl total a pagar es de ${amount}\n")
                else:
                    amount = real_product.price * quantity
                    print(f"\n\t\tEl total a pagar es de ${amount}\n")

                while True:
                    try:
                        print("\n\t\tDesea confirmar la compra?")
                        print("\n1.Si")
                        print("2.No")
                        opt = int(input("> "))
                        if opt < 1 or opt > 2:
                            raise Exception
                        break
                    except:
                        print("\n\t\tOpcion invalida\n")

                if opt == 1:
                    print("_"*70)
                    print("\n\t\tCompra realizada con exito!!!\n")
                    print("\t\tInformacion de la compra\n")
                    print(f"\t\tNombre del producto: {real_product.name}")
                    print(f"\t\tCantidad comprada: {quantity}")
                    print(f"\t\tPrecio unitario (Incluye el IVA): ${real_product.price}")
                    print(f"\t\tSubtotal: ${real_product.price * quantity}")
                    if cliente.descuento_2:
                        print(f"\t\tDescuento (15%): ${real_product.price * quantity * 0.15}")
                        print(f"\t\tTotal: ${(real_product.price * quantity) - (real_product.price * quantity * 0.15)}") 

                    else:
                        print("\t\tDescuento (15%): $0")
                        print(f"\t\tTotal: ${real_product.price * quantity}")
                    print("_"*70)
                    for i in range(quantity):
                        cliente.productos.append(real_product)
                    real_product.cambiar_cantidad(quantity)
                    real_product.calcular_monto()
                    cliente.calcular_total()

                while True:
                    try:
                        print("\n\t\tDesea comprar otro producto?")
                        print("\n1.Si")
                        print("2.No")
                        opt = int(input("> "))
                        if opt < 1 or opt > 2:
                            raise Exception
                        break
                    except:
                        print("\n\t\tOpcion invalida\n")
                if opt == 2:
                    break

    def mostrar_estadisticas(self):
        while True:
            try:
                print("\n\t\tSeleeciona la opción de precio que desea buscar:")
                print("1. Promedio de gasto de un cliente VIP en un partido")
                print("2. Tabla con la asistencia a los partidos de mejor a peor")
                print("3. Partido con mayor asistencia")
                print("4. Partido con mayor boletos vendidos")
                print("5. Top 3 productos más vendidos en el restaurante")
                print("6. Top 3 de clientes (clientes que más compraron boletos)")

                option = int(input("\nIngrese el número de la opción que desea ejecutar\n> "))
                if option not in range(1, 7):
                    raise Exception
                break
            except:
                print("\nOpción invalida\n")

        if option == 1:     
            vip_tickets = list(filter(lambda x: isinstance(x, ClienteVip), self.tickets))
            total_vip_spending = sum(map(lambda x: x.total, vip_tickets))
            average_vip_spending = total_vip_spending / len(vip_tickets) if vip_tickets else 0
            print(f"\nPromedio de gasto de un cliente VIP en un partido: ${average_vip_spending:.2f}")

        if option == 2:     
            sorted_partidos = sorted(self.partido, key=lambda x: x.visitas_estadio, reverse=True)
            print("\nTabla con la asistencia a los partidos de mejor a peor:")
            for i,partido in enumerate(sorted_partidos):
                print(f"{i+1}. {partido.equipo_Local} vs {partido.equipo_Visitante}")
                print(f"Estadio: {partido.stadium.name}")
                print(f"Entradas Vendidas: {partido.asientos_tomados}")
                print(f"Asistencia: {partido.visitas_estadio}")
                print(f"Relación Asistencia/Venta: {partido.visitas_estadio/partido.asientos_tomados if partido.asientos_tomados else 0:.2f}\n")

        if option == 3:     
            max_asistencia_partido = max(self.partido, key=lambda x: x.visitas_estadio)
            print(f"\nPartido con mayor asistencia: {max_asistencia_partido.id_partido}")
            print(f"Equipos: {max_asistencia_partido.equipo_Local} vs {max_asistencia_partido.equipo_Visitante}")
            print(f"Estadio: {max_asistencia_partido.stadium.name}")
            print(f"Entradas Vendidas: {max_asistencia_partido.asientos_tomados}")
            print(f"Asistencia: {max_asistencia_partido.visitas_estadio}")

        if option == 4:     
            max_boletos_partido = max(self.partido, key=lambda x: x.asientos_tomados)
            print(f"\nPartido con mayor boletos vendidos: {max_boletos_partido.id_partido}")
            print(f"Equipos: {max_boletos_partido.equipo_Local} vs {max_boletos_partido.equipo_Visitante}")
            print(f"Estadio: {max_boletos_partido.stadium.name}")
            print(f"Entradas Vendidas: {max_boletos_partido.asientos_tomados}")
            print(f"Asistencia: {max_boletos_partido.visitas_estadio}")

        elif opt == 5:
            restaurants = []
            for stadium in self.estadio:
                for restaurant in stadium.restaurantes:
                    restaurants.append(restaurant)
            
            self.merge_sort(restaurants, lambda x: x.name_restaurante)
            print("\n\n\n\t\tRestaurantes\n")
            while True:
                try:
                    for i, restaurant in enumerate(restaurants):
                        print(f"{i+1}. {restaurant.name_restaurante}")
                    print("\nIngrese el numero del restaurante donde desea ver los productos mas vendidos")
                    opt = int(input("> ").strip())
                    if opt < 1 or opt > len(restaurants):
                        raise Exception
                    break
                except:
                    print("\n\tOpción inválida")

            r = restaurants[opt - 1]
            prods = list(filter(lambda x: x.ventas > 0, r.productos))
            self.merge_sort(prods, lambda x: x.ventas)

            if len(prods) == 0:
                print("\n\tNo se han vendido productos en este restaurante")
            elif len(prods) <= 3:
                print(f"\n\t\tTop 3 productos mas vendidos en {r.name}")
                for i in range(1, len(prods)+1):
                    print(f"{i}. {prods[-i].name} con {prods[-i].ventas} ventas")

        if option == 6:     
            sorted_clientes = sorted(self.clientes, key=lambda x: len(x.tickets), reverse=True)
            top_3_clientes = sorted_clientes[:3]
            print("\nTop 3 de clientes (clientes que más compraron boletos):")
            print("Nombre\t\tCedula\t\tCantidad de Boletos Comprados")
            for cliente in top_3_clientes:
                print(f"{cliente.name}\t\t{cliente.cedula}\t\t{len(cliente.tickets)}")

            
    def menu(self):
        self.registrar_equipos()
        self.registrar_estadios()
        self.registrar_partidos()
        while True:
            print('\n\n\n-- EUROCOPA 2024 --\n Bienvenido/a')
            while True:
                    try:
                        print("\n\t\tSeleeciona el numero asociado a tu eleccion:\n")
                        print("1.Ver todos los partidos de la Euro 2024")
                        print("2.Buscar todos los partidos de un país")
                        print("3.Buscar todos los partidos que se jugarán en un estadio específico")
                        print("4.Buscar todos los partidos que se jugarán en una fecha determinada")
                        print("5.Comprar tickets")
                        print("6.Verificar tickets y registrar asistencia")
                        print("7.Buscar productos por nombre")
                        print("8.Buscar productos por tipo")
                        print("9.Buscar productos por precio")
                        print("10.Comprar productos")
                        print("11.Mostrar estadísticas")
                        print("12.Cargar datos de la API (Cargar los datos a su estado inicial)")
                        print("13.Salir")

                        option = int(input("\nIngrese el numero de la opción que desea ejecutar\n> "))
                        if option not in range(1,12):
                            raise Exception
                        break
                    except:
                        print("\nOpción invalida\n")
                
            if option == 1:
                print("\n\t\tLista de todos los partidos:\n")
                self.merge_sort(self.partido, lambda x: x.fecha)
                for i, partido in enumerate(self.partido):
                    print(f"\n----------{i + 1}----------")
                    partido.show()

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

            elif option == 6:
                print("\n\t\tVerificar tickets y registrar asistencia\n")
                self.check_tickets()

            elif option == 7:
                print("\n\t\tBuscar productos por nombre\n")
                self.buscar_productos_por_nombre()

            elif option == 8:
                print("\n\t\tBuscar productos por tipo\n")
                self.buscar_productos_por_tipo()

            elif option == 9:
                print("\n\t\tBuscar productos por precio\n")
                self.buscar_productos_por_precio()
                
            elif option == 10:
                print("\n\t\tComprar productos\n")
                self.comprar_productos()

            elif option == 11:
                print("\n\t\tMostrar estadísticas\n")
                self.mostrar_estadisticas()