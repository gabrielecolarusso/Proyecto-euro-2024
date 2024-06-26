from Producto import Producto

class ProductoBebida(Producto):
    def __init__(self, name, quantity ,price, stock, type, alcoholic):
        Producto.__init__(self, name, quantity ,price, stock, type)
        self.type = "Bebida"
        self.alcoholic = alcoholic

        
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
    