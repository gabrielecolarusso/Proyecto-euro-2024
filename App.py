from Estadio import Estadio
from Equipo import Equipo
from Partido import Partido
from InfoPartido import InfoPartido
from Producto import Producto
from Restaurante import Restaurante
from Cliente import Cliente
from ClienteGeneral import ClienteGeneral
from ClienteVip import ClienteVip
from Ticket import Ticket
import random
import requests
import pickle

#Se crea la clase App utilizada en main, se crean las listas para guardar la informacion
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
        #El parametro se utiliza para acceder a las 3 Api diferentes
        #Se retorna un diccionario con la informacion de la API
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
    #Esta funcion le pasa un parametro a la Api para acceder, crea un objeto Equipo y lo añade a una lista
        equipos = self.get_info_api("teams")
        for info_equipo in equipos:
            equipo = Equipo(info_equipo["id"], info_equipo["code"], info_equipo["name"], info_equipo["group"] )
            self.equipo.append(equipo)
            print(equipo.show())

    def registrar_estadios(self):
    #Esta funcion le pasa un parametro a la Api para acceder, crea un objeto Estadio, Restaurante y Producto
    #Estas se añaden a 3 listas diferentes para almacenar su informacion
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
    #Esta funcion le pasa un parametro a la Api para acceder, crea un objeto Partido y lo añade a una lista
        partidos = self.get_info_api("matches")
        for info_partido in partidos:
            stadium = list(filter(lambda x: x.id == info_partido["stadium_id"], self.estadio))[0]
            partido = Partido(info_partido["id"],info_partido["home"]["name"], info_partido["away"]["name"], info_partido["date"], stadium)
            self.partido.append(partido)
            print(partido.show())

    def buscar_partidos_por_pais(self):
    #Esta funcion busca partidos en la lista de partidos basada en el pais que queremos buscar
        # Se imprimen los paises para seleccionarlos
        print("Paises disponibles:")
        paises_disponibles = set(partido.equipo_Local or partido.equipo_Visitante for partido in self.partido)
        paises_disponibles = sorted(paises_disponibles)
        for i, pais in enumerate(paises_disponibles):
            print(f"{i+1}. {pais}")

        #Seleccionar un pais
        while True:
            try:
                seleccion = int(input("\nSeleccione el numero del pais que desea buscar\n> ").strip())
                if seleccion < 1 or seleccion > len(paises_disponibles):
                    raise Exception
                break
            except:
                print("\n\tOpcion invalida")

        #Buscar y mostrar todos los partidos que juega ese pais
        pais_seleccionado = list(paises_disponibles)[seleccion - 1]
        print(f"\nPartidos programados para el pais {pais_seleccionado}:\n")
        for partido in self.partido:
            if partido.equipo_Local == pais_seleccionado or partido.equipo_Visitante == pais_seleccionado:
                print(f"{partido.equipo_Local} vs {partido.equipo_Visitante}")
                print(f"Fecha: {partido.fecha}")
                print(f"Estadio: {partido.stadium.name}\n")
    
    def buscar_partidos_por_estadio(self):
    #Crea una lista de los estadios disponibles
        estadios_disponibles = []

        #Extrae los nombres de los estadios
        for partido in self.partido:
            estadios_disponibles.append(partido.stadium.name)

        # Remueve los nombres de los duplicados
        estadios_disponibles = list(set(estadios_disponibles))

        # Imprime los estadios disponibles enumerados
        print("Estadios disponibles:")
        for i, estadio in enumerate(estadios_disponibles):
            print(f"{i+1}. {estadio}")

        while True:
            try:
                seleccion = int(input("\nSeleccione el numero del estadio que desea ver los partidos\n> ").strip())
                if seleccion < 1 or seleccion > len(estadios_disponibles):
                    raise Exception
                break
            except:
                print("\n\tOpcion invalida")

        #Compara el estadio seleccionado con el de la lista
        estadio_seleccionado = estadios_disponibles[seleccion - 1]

        #Imprime los partidos en ese estadio
        print(f"\nPartidos disponibles en el estadio {estadio_seleccionado}:\n")
        for partido in self.partido:
            if partido.stadium.name == estadio_seleccionado:
                print(f"Local: {partido.equipo_Local}\nVisitante: {partido.equipo_Visitante}\nFecha: {partido.fecha}\nEstadio: {partido.stadium.name}\n")

    def buscar_partidos_por_fecha(self):
    # Se imprimen las fechas para seleccionarlas
        print("Fechas disponibles:")
        fechas_disponibles = set(partido.fecha for partido in self.partido)
        fechas_disponibles = sorted(fechas_disponibles, reverse=True)
        for i, fecha in enumerate(fechas_disponibles):
            print(f"{i+1}. {fecha}")

        # Seleccionar una fecha
        while True:
            try:
                seleccion = int(input("\nSeleccione el número de la fecha que desea buscar\n> ").strip())
                if seleccion < 1 or seleccion > len(fechas_disponibles):
                    raise Exception
                break
            except:
                print("\n\tOpción inválida")

        # Buscar y mostrar todos los partidos que se juegan en esa fecha
        fecha_seleccionada = list(fechas_disponibles)[seleccion - 1]
        print(f"\nPartidos programados para la fecha {fecha_seleccionada}:\n")
        for partido in self.partido:
            if partido.fecha == fecha_seleccionada:
                print(f"{partido.equipo_Local} vs {partido.equipo_Visitante}")
                print(f"Fecha: {partido.fecha}")
                print(f"Estadio: {partido.stadium.name}\n")   

    def merge_sort(self, mi_lista, mi_func):
    #Funcion que ordena una lista usando un algoritmo de ordenamiento
    #Merge Sort, se divide la lista en dos partes y se ordena cada una de ellas
    #Luego se ordenan las dos partes y se unen en una sola lista ordenada
    #mi_lista (list): La lista que se va a ordenar
    #mi_func (function): Una funcion que toma un elemento de la lista y devuelve un valor para ser utilizado en el ordenamiento
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
    #Funcion que busca dentro de una lista usando un algoritmo de busqueda
    #Binary Search, se divide la lista en dos partes y se busca en cada una de ellas
    #Luego se busca en la mitad de la lista y se compara con el valor buscado
    #Si el valor buscado es menor que el valor de la mitad, se busca en la parte izquierda de la lista
    #Si el valor buscado es mayor que el valor de la mitad, se busca en la parte derecha de la lista
    #Si el valor buscado es igual que el valor de la mitad, se retorna el indice de la mitad
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

    def registrar_cliente(self):
    #Esta funcion pide datos a la persona que utiliza el sistema, crea un objeto Cliente y los guarda
        print("BIENVENIDO, Ingrese los siguientes datos solicitados por el sistema: ")
        #Utilizando el algoritmo de ordenamiento merge_sort ordenamos las cedulas de los clientes en orden ascendente
        #Le pasamos el parametro self.clientes de donde busara las cedulas disponiles ya agregadas
        #La funcion lambda es utilizada para determinar el criterio del ordenamiento siendo en este caso cedula
        #Documentacion de Lambda https://www.w3schools.com/python/python_lambda.asp
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
                #Utilizando el algoritmo de busqueda binary_search buscamos si esa cedula se encuentra en la lista
                #Le pasamos el parametro self.clientes de donde busara las cedula, el indice 0 que es donde empieza, el indice len(self.clientes) - 1
                #Luego le pasamos el objetivo de busqueda que es cedula y posteriormente con lambda el criterio busqueda siendo en este caso cedula
                #Documentacion de Lambda https://www.w3schools.com/python/python_lambda.asp
                #La variable: variable se le asigna el resultado de la busqueda
                variable = self.binary_search(self.clientes, 0, len(self.clientes) - 1, cedula, lambda x: x.cedula)
                if variable != -1:
                    print("\n\tEsta cedula ya se encuentra registrada")
                    raise Exception
                break
            except:
                print("\nCedula inválida")

        while True:
            try:
                edad = int(input("\nIngrese su edad\n> ").strip())
                if edad <= 0 or edad > 125:
                    raise Exception
                break
            except:
                print("\n\tEdad inválida")

        print("\n\tEl cliente ha sido registrado con éxito\n")
        #Se guardan los datos del cliente y se le aplica el descuento
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
    #Se crea un ticket con un numero aleatorio para evitar que se repita, se verifica que de igual manera no se haya repetido
        id_del_ticket = self.tickets_id["General"] + self.tickets_id["Vip"]
        while True:
            id_del_ticket = random.randint(1000000, 99999999)
            if id_del_ticket not in self.tickets_id["General"] + self.tickets_id["Vip"]:
                break

        #Funcion para seleccionar y ver el mapa de asientos a partir del partido seleccionado   
        seat = self.ver_mapa_asientos(partido_seleccionado)

        #Verificamos el tipo del ticket y aplicamos descuentos, guardamos los datos en 2 clases dependiento del tipo del ticket
        if tipo_ticket == "General":
            ticket = ClienteGeneral(id_del_ticket, partido_seleccionado, partido_seleccionado.stadium,seat)
            ticket.descuento = cliente.descuento_1
            return ticket
    
        elif tipo_ticket == "Vip":
            ticket = ClienteVip(id_del_ticket, partido_seleccionado, partido_seleccionado.stadium,seat)
            ticket.descuento = cliente.descuento_1
            return ticket

    def comprar_ticket(self):
    #Funcion para comprar el ticket
        while True:
            try:
                print("¿Ya se encuentra registrado en nuestro sistema? Ingrese el numero asociado a su seleccion.")
                print("1. Sí")
                print("2. No")
                opt_2 = int(input("\n> ").strip())
                if opt_2 < 1 or opt_2 > 2:
                    raise Exception
                break
            except:
                print("\n\tOpcion invalida")

        if opt_2 == 1:
            while True:
                try:
                    cedula = input("\nIngrese su cedula\n> ").strip()
                    if len(cedula) == 0 or not cedula.isnumeric():
                        raise Exception
                    #Se realixa una busqueda binaria (algoritmo de busqueda) de la cedula introducida para ver si ya estaba registrada
                    if self.binary_search(self.clientes, 0, len(self.clientes) - 1, cedula, lambda x: x.cedula) == -1:
                        print("\nCedula no registrada")
                        print("\n\t¿Desea intentarlo de nuevo?")
                        print("1. Si")
                        print("2. No")
                        opt_3 = int(input("\n> ").strip())
                        if opt_3 not in range(1,3):
                            print("\nError. Ingrese 1 o 2 dependiendo de su eleccion")
                            print("\n\t¿Desea intentarlo de nuevo?")
                            print("1. Si")
                            print("2. No")
                            opt_3 = int(input("\n> ").strip())
                        if opt_3 == 1:
                            continue
                        elif opt_3 == 2:
                            return
                    break
                except:
                    print("\nCedula invalida")
                    print("\n\t¿Desea intentarlo de nuevo?")
                    print("1. Si")
                    print("2. No")
                    opt_3 = int(input("\n> ").strip())
                    if opt_3 not in range(1,3):
                        print("\nError. Ingrese 1 o 2 dependiendo de su eleccion")
                        print("\n\t¿Desea intentarlo de nuevo?")
                        print("1. Si")
                        print("2. No")
                        opt_3 = int(input("\n> ").strip())
                    if opt_3 == 1:
                        continue
                    elif opt_3 == 2:
                        return

            #Busca la cedula del cliente para asociarla con su seleccion de partido y mostrar sus datos
            i = self.binary_search(self.clientes, 0, len(self.clientes) - 1, cedula, lambda x: x.cedula)
            cliente = self.clientes[i]
            partido = self.seleccionar_partido()
            print(cliente.show_info())

        else:
            cliente = self.registrar_cliente()
            partido = self.seleccionar_partido()

        while True:
            try:
                print("\n\tTipos de entradas disponibles para los partidos:")
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
                #Creamos el ticket llamando a la funcion correspondiente y se le pasa los datos del cliente, el partido seleccionado y tipo de entrada
                ticket = self.crear_ticket(cliente, partido, "General")
                ticket.calcular_monto()
                print(f"\n\tInformación del ticket general\n")	
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
                        print("\n\tOpcion invalida")

                if opt == 1:
                    #Se guarda el ticket, los asientos para evitar que se repitan y se resta una entrada disponible, tambien se guarda el id del ticket para confirmar la asistencia
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
                        print("2. No")
                        opt_1 = int(input("\nIngrese el numero asociado a su elección\n> ").strip())
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
                #Creamos el ticket llamando a la funcion correspondiente y se le pasa los datos del cliente, el partido seleccionado y tipo de entrada
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
                    #Se guarda el ticket, los asientos para evitar que se repitan y se resta una entrada disponible, tambien se guarda el id del ticket para confirmar la asistencia
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
                        print("2. No")
                        opt_1 = int(input("\nIngrese el numero asociado a su elección\n> ").strip())
                        if opt_1 < 1 or opt_1 > 2:
                            raise Exception
                        break
                    except:
                        print("\n\tOpción inválida")

                if opt_1 == 2:
                    print("\n\tGracias por su compra!!!")
                    break
        
        #Se verifica que el cliente tenga al menos 1 ticket, se calcula su monto de los tickets, se busca y se ordena su cedula y esta informacion se guarda
        if len(cliente.tickets) > 0:
            cliente.calcular_tickets()
            self.merge_sort(self.clientes, lambda x: x.cedula)
            variable_1 = self.binary_search(self.clientes, 0, len(self.clientes) - 1, cliente.cedula, lambda x: x.cedula)
            if variable_1 == -1:
                self.clientes.append(cliente)
            print(f"\nNumero de entradas compradas: {len(cliente.tickets)}")
            print(f"Coste total de las entradas: ${cliente.total_tickets}")

    def ver_mapa_asientos(self, partido_seleccionado):
        #Se crea el mapa del estadio, se calcula la capacidad del estadio y se crea una lista con los asientos disponibles, se crea una lista con los asientos tomados
        #Se crea una lista con las letras y numeros de los asientos y se crea una lista con los asientos disponibles, se crea una lista con los asientos tomados, se crea una lista con los asientos disponibles
        mapa_del_estadio = []
        capacidad = partido_seleccionado.stadium.capacity[0] + partido_seleccionado.stadium.capacity[1]
        columnas = 10
        filas = capacidad // columnas
        variable = []
        for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            for numero in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                variable.append(letra + numero)

        seats = [f"{variable[i]}{j}" for i in range(filas) for j in range(1, columnas + 1)]
        asientos_disponibles = [seat for seat in seats if seat not in partido_seleccionado.asientos_tomados]

        #Se imrpimen las filas en el mapa del estadio
        for i in variable[:filas]:
            fila = ["|   X  " if f"{i}{j}" in partido_seleccionado.asientos_tomados else f"|  {i}{j} " for j in range(1, columnas + 1)] + ["|"]
            mapa_del_estadio.append("".join(fila))

        #Se agregan - como separadores del mapa
        for j in mapa_del_estadio:
            print("-" * len(j))
            print(j)
        print("-" * len(mapa_del_estadio[-1]))

        #Se verifica que el asiento ingresadp no este ocupado
        while True:
            try:
                seat = input("\nIngrese el asiento que desea seleccionar\n> ").strip().upper()
                if seat not in asientos_disponibles:
                    raise Exception
                break
            except:
                print("\n\tAsiento inválido")

        #Se retorna el asiento seleccionado
        print(f"\n\tAsiento seleccionado: {seat}\n")
        return seat
        
    def check_tickets(self):
    #Funcion que verifica si un ticket ya fue usado
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
                #Ordena y busca el id del ticket para mostrar su informacion asociada
                self.merge_sort(self.tickets, lambda x: x.id_ticket)
                ind = self.binary_search(self.tickets, 0, len(self.tickets) - 1, ticket_id, lambda x: x.id_ticket)
                ticket = self.tickets[ind]
                ticket.show_info()

                print("\n\t\tAsistencia registrada con exito!!!\n")

                #Ordena y busca el id del partido para mostrar su informacion asociada, agrega una visita al estadio
                self.merge_sort(self.partido, lambda x: x.id_partido)
                ind_2 = self.binary_search(self.partido, 0, len(self.partido) - 1, ticket.partido.id_partido, lambda x: x.id_partido)
                game = self.partido[ind_2]
                game.visitas_estadio += 1
            else:
                print("\n\t\tEl ticket ya fue verificado anteriormente\n")

        else:
            print("\n\t\tEl ticket ingresado no existe\n")

    def buscar_productos_por_nombre(self):
    #Funcion que busca productos por nombre en todos los restaurantes
    #Se busca el nombre de todos los productos
        estadios = self.get_info_api("stadiums")
        productos = set()
        for info_stadium in estadios:
            for info_restaurante in info_stadium["restaurants"]:
                for info_producto in info_restaurante["products"]:
                    productos.add(info_producto["name"])

        #Lo convierte en una lista para luego ser ordenada
        productos = list(productos)

        #Ordena los productos alfabeticamente
        self.merge_sort(productos, lambda x: x)
        print("\n\t\tProductos Disponibles en todos los restaurantes (Ordenados alfabéticamente):\n")
        for i, producto in enumerate(productos):
            print(f"{i+1}. {producto}")

        #Compara el nombre ingresado con el de ls productos y lo guarda para imprimir su informacion
        nombre_producto = input("\nIngrese el nombre del producto que desea buscar: ").lower()
        productos_encontrados = [
            (p["name"], p["quantity"], p["price"], p["stock"], p["adicional"], info_stadium["name"], info_restaurante["name"])
            for info_stadium in estadios
            for info_restaurante in info_stadium["restaurants"]
            for p in info_restaurante["products"]
            if nombre_producto in p["name"].lower()
        ]

        #Se verifica si hay productos con ese nombre y se imprime toda su informacion
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
    #Funcion para la busqueda de productos por tipo en todos los restaurantes
    # Se busca el tipo de todos los productos
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

        # Compara el tipo ingresado con el de los productos y los guarda para imprimir su informacion
        tipo_producto = input("\nIngrese el tipo de producto que desea buscar: ").lower()
        productos_encontrados = [
            (p["name"], p["quantity"], p["price"], p["stock"], p["adicional"], info_stadium["name"], info_restaurante["name"])
            for info_stadium in estadios
            for info_restaurante in info_stadium["restaurants"]
            for p in info_restaurante["products"]
            if tipo_producto in p["adicional"].lower()
        ]

        # Se verifica si hay productos con ese tipo y se imprime toda su informacion
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
    #Funcion para la busqueda de productos por precio en todos los restaurantes
    # Se busca el precio de todos los productos
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

        #Añade los productos deseados a una lista dependiendo de el precio y la opción escogida
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

        #Se verifica si hay productos disponibles con las especificaciones dadas y se imprimen
        if len(productos_encontrados) > 0:
            print("\n\tProductos encontrados con el precio seleccionado:")
            for i, (producto, precio) in enumerate(productos_encontrados):
                print(f"{i+1}. Producto: {producto}, Precio: {precio}")
        else:
            print("\n\tNo se encontraron productos con el precio proporcionado.")

    def comprar_productos(self):
    #Funcion para comprar productos en todos los restaurantes
        variable_2 = True
        while variable_2:
            cedula = input("\nIngrese su cedula\n> ")
            if len(cedula) == 0 or not cedula.isnumeric():
                print("\n\t\tDNI invalido\n")
            else:
                variable_2 = False

        #Busca la cedula ingresada y la asocia a los otros datos del cliente
        i = self.binary_search(self.clientes, 0, len(self.clientes) - 1, cedula, lambda x: x.cedula)
        cliente = self.clientes[i]

        if len(cliente.tickets) == 0:
            print("\n\t\tNo tiene tickets comprados\n")
            return

        #Se crea una lista y se filtran las cedulas de todos los clientes, con esta cedula se verifica cual es su tipo de ticket
        #Luego se crea una lista y se filtran los tipos de tickets verificando si es VIP o General
        if variable_2:
            cliente = list(filter(lambda x: x.cedula == cedula, self.clientes))[0]
            if list(filter(lambda x: isinstance(x, ClienteVip), cliente.tickets)) == []:
                print("\n\t\tNo puede comprar productos, no es VIP\n")
                aux = False

        #Se filtran los estadios de todos los partidos para seleccionar los restaurantes pertenecientes a cada uno
        stadiums = list(filter(lambda x: isinstance(x, Estadio), self.estadio))
        if len(stadiums) > 1:
            while True:
                try:
                    variable_1 = 0
                    print(f"\n\t\tEstadios\n")
                    for s in stadiums:
                        print(f"\n{variable_1 + 1}. {s.name}")
                        variable_1 += 1
                    stadium_number = int(input("\nIngrese el numero del estadio donde desea comprar\n> "))
                    if stadium_number < 1 or stadium_number > variable_1:
                        raise Exception
                    break
                except:
                    print("\n\t\tOpcion invalida\n")
            stadium = self.estadio[stadium_number - 1]
        else:
            stadium = self.estadio[0]

        #Se filtran los restaurantes pertenecientes al estadio seleccionado para seleccionar uno de ellos y ver sus productos
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

        #Se filtran los productos disponibles en el restaurante seleccionado para seleccionar uno de ellos y verificar si es alcoholico o no
        #Se verifica si el cliente es mayor de edad, si es asi se le mostraran las bebidas alcoholicas disponibles, si no lo es, no se mostraran
        productos = list(filter(lambda x: isinstance(x, Producto) and x.stock  > 0, restaurante.productos))
        if cliente.edad < 18:
            productos = list(filter(lambda x: x.type in ["non-alcoholic", "plate", "package"], productos))
        else:
            productos = list(filter(lambda x: x.type in ["plate", "package","non-alcoholic","alcoholic"], productos))
    
        variable_4 = True
        if len(productos) == 0:
            print("\n\t\tNo hay productos disponibles\n")
            variable_4 = False
        if variable_4:
            while True:
                #Se realiza la misma verificacion de arriba despues de revisar que hay productos disponibles
                productos = list(filter(lambda x: isinstance(x, Producto) and x.stock  > 0, restaurante.productos))
                if cliente.edad < 18:
                    productos = list(filter(lambda x: x.type in ["non-alcoholic", "plate", "package"], productos))
                else:
                    productos = list(filter(lambda x: x.type in ["plate", "package","non-alcoholic","alcoholic"], productos))
                while True:
                    try:
                        variable_1 = 0
                        print(f"\n\t\tProductos de {restaurant.name_restaurante}\n")
                        print("\n\t\t\tComidas y Bebidas\n")
                        #Se imprimen todos los productos
                        for b in productos:
                            print(f"{variable_1 + 1}. {b.name} - Categoria: {b.type} - Precio: ${b.price} - Cantidad disponible: {b.stock}")
                            variable_1 += 1
                        product_number = int(input("\nIngrese el numero del producto que desea comprar\n> "))
                        if product_number < 1 or product_number > variable_1:
                            raise Exception
                        break
                    except:
                        print("\n\t\tOpcion invalida\n")

                #Ordena y busca el producto ingresado en todos los restaaurantes
                products =  productos
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

                #Si el cliente tiene cedula perfecta, se le aplica este descuento al total a pagar
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
                        #Se aplica el descuento de cedula perfecta
                        print(f"\t\tDescuento (15%): ${real_product.price * quantity * 0.15}")
                        print(f"\t\tTotal: ${(real_product.price * quantity) - (real_product.price * quantity * 0.15)}") 

                    else:
                        print("\t\tDescuento (15%): $0")
                        print(f"\t\tTotal: ${real_product.price * quantity}")
                    print("----------------------------------------------------------------")
                    for i in range(quantity):
                        #Se agrega el producto a las compras del cliente, se cambia el stock, se calcula el monto y el total
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
            #Filtra los tickets VIP que fueron comprados y se cuenta cuantos hay
            vip_tickets = list(filter(lambda x: isinstance(x, ClienteVip), self.tickets))
            if len(vip_tickets) != 0:
                #Se calcula el monto en tickets VIP de cada cliente y se suma a el total de los productos de cada cliente para crear un promedio
                tickets_vip = list(filter(lambda cliente: type(cliente.tickets[0]) == ClienteVip, self.clientes))
                average_vip_spending = (sum([cliente.total_tickets_vip for cliente in tickets_vip]) + sum([cliente.total_productos for cliente in tickets_vip])) / len(tickets_vip)
                print(f"\nPromedio de gasto de un cliente VIP en un partido: ${average_vip_spending:.2f}")
            else:
                print("\n\t\tNo hay clientes VIP\n")

        elif option == 2:     
            #Verifica si los estadios tienen mas de 0 visitas
            variable_1 = list(filter(lambda g: g.visitas_estadio > 0, self.partido))
            if len(variable_1) != 0:
                #Ordena los estadios por visitas de mayor a menor
                self.merge_sort(variable_1, lambda x: x.visitas_estadio)
                print("\n\t\tTabla con la asistencia a los partidos de mejor a peor:\n")
                for n in range(1,len(variable_1)+1):
                    partido = variable_1[-n]
                    print(f"\n----------{n}----------")
                    partido.show()
                    #Crea la relacion asistencia venta
                    total_vendido = int(len(partido.asientos_tomados))
                    asistencia = int(partido.visitas_estadio)
                    relacion = asistencia / total_vendido
                    print(f"Relación Asistencia/Venta: {relacion}")
            else:
                print("\n\t\tNo hay asistencias a ninguno de los estadios \n")

        elif option == 3:     
            #Verifica si los estadios tienen mas de 0 visitas
            variable_1 = list(filter(lambda g: g.visitas_estadio > 0, self.partido))
            if len(variable_1) != 0:
                #Agarra el estadio con mayor asistencia gracias al Max y el parametro x.visitas_estadio
                max_asistencia_partido = max(self.partido, key=lambda x: x.visitas_estadio)
                print(f"\nPartido con mayor asistencia: {max_asistencia_partido.id_partido}")
                print(f"Equipos: {max_asistencia_partido.equipo_Local} vs {max_asistencia_partido.equipo_Visitante}")
                print(f"Estadio: {max_asistencia_partido.stadium.name}")
                print(f"Entradas Vendidas: {max_asistencia_partido.asientos_tomados}")
                print(f"Asistencia: {max_asistencia_partido.visitas_estadio}")
            else:
                print("\n\t\tNo hay asistencias a ninguno de los estadios \n")

        elif option == 4:     
            #Verifica si los estadios tienen mas de 0 tickets vendidos
            variable_2 = list(filter(lambda g: len(g.asientos_tomados) > 0, self.partido))
            if len(variable_2) != 0:
                #Agarra el estadio con mayor tickets vendidos gracias a Max y el parametro x.asientos_tomados
                max_asistencia_partido = max(self.partido, key=lambda x: len(x.asientos_tomados))
                print(f"\nPartido con mayor boletos vendidos: {max_asistencia_partido.id_partido}")
                print(f"Equipos: {max_asistencia_partido.equipo_Local} vs {max_asistencia_partido.equipo_Visitante}")
                print(f"Estadio: {max_asistencia_partido.stadium.name}")
                print(f"Entradas Vendidas: {max_asistencia_partido.asientos_tomados}")
                print(f"Asistencia: {max_asistencia_partido.visitas_estadio}")
            else:
                print("\n\t\tNo hay ventas de tickets en ninguno de los estadios \n")

        elif option == 5:
            restaurants = []
            for stadium in self.estadio:
                for restaurant in stadium.restaurantes:
                    restaurants.append(restaurant)
            
            #Ordena los restaurantes por nombre para mostrarlos en pantalla
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

            #Verifica las ventas de productos de el restaurante seleccionado si las ventas son mayores a 0, ordena las ventas de mayor a menor
            r = restaurants[opt - 1]
            prods = list(filter(lambda x: x.ventas > 0, r.productos))
            self.merge_sort(prods, lambda x: x.ventas)

            if len(prods) == 0:
                print("\n\tNo se han vendido productos en este restaurante")
            elif len(prods) <= 3:
                print(f"\n\t\tTop 3 productos mas vendidos en {r.name_restaurante}")
                for i in range(1, len(prods)+1):
                    print(f"{i}. {prods[-i].name} con {prods[-i].ventas} ventas")

        elif option == 6:     
            #Ordena a los clientes de mayor a menor por cantidad de tickets comprados y los imprime
            sorted_clientes = sorted(self.clientes, key=lambda x: len(x.tickets), reverse=True)
            top_3_clientes = sorted_clientes[:3]
            print("\nTop 3 de clientes (clientes que más compraron boletos):")
            for i, cliente in enumerate(top_3_clientes):
                print(f"{i+1}. Nombre: {cliente.nombre}")
                print(f"Cedula: {cliente.cedula}")
                print(f"Cantidad de boletos comprados: {len(cliente.tickets)}\n")

    def leer_archivos(self):
        #Funcion que lee archivos .pickle donde se guardan los datos
        #Documentacion archivos .pickle: https://docs.python.org/3/library/pickle.html
        try:
            with open("equipos.pickle", "rb") as file:
                self.equipo = pickle.load(file)
        except:
            self.registrar_equipos()
            with open("equipos.pickle", "wb") as file:
                pickle.dump(self.equipo, file)
        try:
            with open("estadio.pickle", "rb") as file:
                self.estadio = pickle.load(file)
        except:
            self.registrar_estadios()
            with open("estadio.pickle", "wb") as file:
                pickle.dump(self.estadio, file)
        try:
            with open("partido.pickle", "rb") as file:
                self.partido = pickle.load(file)
        except:
            self.registrar_partidos()
            with open("partido.pickle", "wb") as file:
                pickle.dump(self.partido, file)
        try:
            with open("clientes.pickle", "rb") as file:
                self.clientes = pickle.load(file)
        except:
            with open("clientes.pickle", "wb") as file:
                pickle.dump(self.clientes, file)
        try:
            with open("tickets.pickle", "rb") as file:
                self.tickets = pickle.load(file)
        except:
            with open("tickets.pickle", "wb") as file:
                pickle.dump(self.tickets, file)
        try:
            with open("tickets_id.pickle", "rb") as file:
                self.tickets_id = pickle.load(file)
        except:
            with open("tickets_id.pickle", "wb") as file:
                pickle.dump(self.tickets_id, file)
        try:
            with open("tickets_usados.pickle", "rb") as file:
                self.tickets_usados = pickle.load(file)
        except:
            with open("tickets_usados.pickle", "wb") as file:
                pickle.dump(self.tickets_usados, file)


    def guardar_archivos(self):
        #Funcion que guarda la informacion en los archivos .pickle para su uso cada vez que se inicie el programa
        with open("equipos.pickle", "wb") as file_1:
            pickle.dump(self.equipo, file_1)
        with open("clientes.pickle", "wb") as file_2:
            pickle.dump(self.clientes, file_2)
        with open("tickets.pickle", "wb") as file_3:
            pickle.dump(self.tickets, file_3)
        with open("tickets_id.pickle", "wb") as file_4:
            pickle.dump(self.tickets_id, file_4)
        with open("tickets_usados.pickle", "wb") as file_5:
            pickle.dump(self.tickets_usados, file_5)
        with open("estadio.pickle", "wb") as file_6:
            pickle.dump(self.estadio, file_6)
        with open("partido.pickle", "wb") as file_7:
            pickle.dump(self.partido, file_7)
            
    def menu(self):
        #Funcion que imprime el menu y permite al usuario seleccionar una opcion, lee los archivos .pickle con los datos guardados
        self.leer_archivos()
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
                        print("12.Cargar datos originales de la API")
                        print("13.Salir (Guardar los datos y salir)")

                        option = int(input("\nIngrese el numero de la opción que desea ejecutar\n> "))
                        if option not in range(1,14):
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

            elif option == 12:
                #Borra la informacion de los archivos .pickle y la reescribe con datos vacios
                while True:
                    try:
                        print("\n\t¿Estas seguro que quieres cargar los datos de la API?")
                        print("1. Sí")
                        print("2. No")
                        print("Ingresa en numero asociado a su eleccion: ")
                        opt = int(input("\n> ").strip())
                        if opt < 1 or opt > 2:
                            raise Exception
                        break
                    except:
                        print("\n\tOpcion invalida")
                if opt == 1:
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
                    self.registrar_equipos()
                    self.registrar_estadios()
                    self.registrar_partidos()
                    print("\nLOS DATOS CARGARON CORRECTAMENTE, PROGRAMA EN SU ESTADO INICIAL\n")
                else:
                    print("\n\t\tCarga cancelada\n")
                    
            elif option == 13:
                #Guarda la informacion en los archivos .pickle para su uso cada vez que se inicie el programa
                self.guardar_archivos()
                print("\n\t\tGracias por usar nuestro sistema")
                break
