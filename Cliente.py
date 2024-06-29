from ClienteGeneral import ClienteGeneral
from ClienteVip import ClienteVip

class Cliente:

    def __init__(self,nombre,apellido,cedula,edad):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.edad = edad
        self.descuento_1 = False
        self.descuento_2 = False
        self.total_tickets_general = 0
        self.total_tickets_vip = 0
        self.total_tickets = 0
        self.total_productos = 0
        self.tickets = []
        self.productos = []

    def descuento_vampiro(self):
        num_str = str(self.cedula)
        num_digitos = len(num_str)
        mitad_digitos = num_digitos // 2

        for i in range(10 ** (mitad_digitos - 1), 10 ** mitad_digitos):
            for j in range(10 ** (mitad_digitos - 1), 10 ** mitad_digitos):
                if i * j == self.cedula and set(str(i) + str(j)) == set(num_str):
                    return True

        return False
    
    def es_perfecto(self):
        n = int(self.cedula)
        suma = 0
        for i in range(1, n):
            if n % i == 0:
                suma += i
        return suma == n

    def descuento(self):
        if self.descuento_vampiro():
            self.descuento_1 = True
            print("\nEl cliente tiene un 50% de descuento en la compra de sus tickets\n")
        if self.es_perfecto():
            self.descuento_2 = True
            print("\nEl cliente tiene un 15% de descuento en los restaurantes\n")


    def calcular_tickets(self):
        aux_1 = 0
        aux_2 = 0
        for ticket in self.tickets:
            if isinstance(ticket, ClienteGeneral):
                aux_1 += ticket.total
            else:
                aux_2 += ticket.total
        self.total_tickets_general = aux_1
        self.total_tickets_vip = aux_2
        self.total_tickets = aux_1 + aux_2

    def calcular_total(self):
        aux = 0
        for product in self.productos:
            aux += product.price
        self.total_productos = aux
        if self.descuento_2:
            self.total_productos *= 0.85

    def show_info(self):
        """Muestra la informacion del cliente
        """
        print(f"-Nombre: {self.nombre}")
        print(f"-Apellido: {self.apellido}")
        print(f"-DNI: {self.cedula}")
        print(f"-Edad: {self.edad}")
        print(f"-Descuento del 50% en la compra de tickets: {self.descuento_1}")
        print(f"-Descuento del 15% en los restaurantes: {self.descuento_2}")
        print("\n\n\tEntradas compradas")
        for i,ticket in enumerate(self.tickets):
            print(f"\n________{i+1}________")
            ticket.show_info()
        print(f"\n-Total en entradas: ${self.total_tickets}")

        if len(self.productos) > 0:
            print("\n\n\tProductos comprados")
            for j,product in enumerate(self.productos):
                product.show()
            print(f"\n-Total en productos: ${self.total_productos}")
        else:
            print("\n\n\tNo se han comprado productos")
        print(f"-Monto total gastado: ${self.total_tickets + self.total_productos}")