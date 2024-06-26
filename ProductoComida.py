from Producto import Producto

class ProductoComida(Producto):
    def __init__(self, name, quantity ,price, stock, type, package):
        Producto.__init__(self, name, quantity ,price, stock, type)
        self.type = "Comida"
        self.package = package
        
    def show_attr(self):
        return """
Nombre: {}
Tipo: {}
Precio: {}
Cantidad: {}
Stock: {}
Tipo de comida: {}
        """.format(self.name,self.type,self.price,self.quantity,self.stock,self.es_empaque())
    