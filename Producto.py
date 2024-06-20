class Producto():

    def __init__(self, name, quantity ,price, stock, type):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.stock = stock
        self.type = type

        if self.type == "non-alcoholic":
            self.type = "Bebida no alcoholica"
        if self.type == "alcoholic":
            self.type = "Bebida alcoholica"
        if self.type == "plate":
            self.type = "Comida de preparacion"
        if self.type == "package":
            self.type = "Comida de empaque"


    def show(self):
        return f"""
Nombre: {self.name}
Cantidad: {self.quantity}
Precio: {self.price}
Stock: {self.stock}
Tipo: {self.type}
"""