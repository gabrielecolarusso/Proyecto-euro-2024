class Restaurante():

    def __init__(self, name_restaurante):
        self.name_restaurante = name_restaurante
        self.productos = []

    def show(self):
        print("")
        print("Nombre Restaurante: {}".format(self.name_restaurante))
        print("-------Productos-------")
        for p,producto in enumerate(self.productos):
            print(f"\n________{p+1}________")
            print(f"Nombre: {producto.name}")
            print(f"Cantidad: {producto.quantity}")
            print(f"Precio: {producto.price}")
            print(f"Sotck: {producto.stock}")
            print(f"Tipo: {producto.type}")
