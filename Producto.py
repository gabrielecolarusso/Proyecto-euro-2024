class Producto():

    def __init__(self, name, quantity ,price, stock, type):
        self.name = name
        self.quantity = quantity
        self.price = float(price)
        self.stock = int(stock)
        self.type = type
        self.ventas = 0
        self.monto_total = 0

    def calcular_monto(self):
        self.monto_total = self.ventas * self.price * 1.16

    def cambiar_cantidad(self, cantidad):
        cantidad_nueva = self.stock - cantidad
        self.stock = cantidad_nueva

        if cantidad_nueva < 0:
            self.stock = 0
            print("No hay suficiente stock")
            return
        else:
            return self.stock


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