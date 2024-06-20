from Producto import Producto

class ProductoBebida(Producto):
    def __init__(self, name, quantity ,price, stock, type, alcoholic):
        Producto.__init__(self, name, quantity ,price, stock, type)
        self.type = "Bebida"
        self.alcoholic = alcoholic

    def change_quantity(self, cantidad):
        cantidad_nueva = self.quantity - cantidad
        self.quantity = cantidad_nueva

        if cantidad_nueva < 0:
            self.quantity = 0
            print("No hay suficiente stock")
            return
        else:
            return self.quantity
        
    def restore_quantity(self, cantidad):
        cantidad_nueva = self.quantity + cantidad
        self.quantity = cantidad_nueva

        if cantidad_nueva < 0:
            self.quantity = 0
            print("No hay suficiente stock")
            return
        else:
            return self.quantity
        
    def getName(self):
        return self.name
    
    def getQuantity(self):
        return self.quantity
    
    def getPrice(self):
        return self.price
    
    def getType(self):
        return self.type

    def getStock(self):
        return self.stock
    
    def getAlcoholic(self):
        return self.alcoholic
    
    def es_alcoholico(self):
        if self.alcoholic == True:
            return "Bebida alcoholica"
        else:
            return "Bebida no alcoholica"
        
    def show(self):
        return """
Nombre Restaurante: {}
Nombre: {}
Tipo: {}
Precio: {}
Cantidad: {}
Stock: {}
Tipo de bebida: {}
        """.format(self.name,self.type,self.price,self.quantity,self.stock,self.es_alcoholico())
    