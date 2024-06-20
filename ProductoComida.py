from Producto import Producto

class ProductoComida(Producto):
    def __init__(self, name, quantity ,price, stock, type, package):
        Producto.__init__(self, name, quantity ,price, stock, type)
        self.type = "Comida"
        self.package = package

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
        return self.package
    
    def es_empaque(self):
        if self.package == True:
            return "Comida de empaque"
        else:
            return "Comida de preparacion"
        
    def show_attr(self):
        return """
Nombre: {}
Tipo: {}
Precio: {}
Cantidad: {}
Stock: {}
Tipo de comida: {}
        """.format(self.name,self.type,self.price,self.quantity,self.stock,self.es_empaque())
    