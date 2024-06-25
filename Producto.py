class Producto():

    def __init__(self, name, quantity ,price, stock, type):
        self.name = name
        self.quantity = quantity
        self.price = float(price) * 1.16
        self.stock = int(stock)
        self.type = type
        self.ventas = 0
        self.monto_total = 0

    def calcular_monto(self):
        self.monto_total = self.ventas * self.price

    def cambiar_cantidad(self, cantidad):
        self.stock -= cantidad
        self.ventas += cantidad

    def show(self):
        return f"""
Nombre: {self.name}
Cantidad: {self.quantity}
Precio: {self.price}
Stock: {self.stock}
Tipo: {self.type}
Vendidos: {self.ventas}
Monto total: {self.monto_total}
"""