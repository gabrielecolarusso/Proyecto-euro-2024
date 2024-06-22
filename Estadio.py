class Estadio:

    def __init__(self, id, name, city, capacity):
        self.id = id
        self.name = name
        self.city = city
        self.capacity = capacity
        self.restaurantes = []

    def getId(self):
        return self.id
    
    def getName(self):
        return self.name
    
    def getCity(self):
        return self.city
    
    def getCapacity(self):
        return self.capacity
    

    def show(self):
        print(f"-Id: {self.id}")
        print(f"-Nombre: {self.name}")
        print(f"-Ubicación: {self.city}")
        print(f"-Capacidad: {self.capacity[0] + self.capacity[1]}")
        print(f"\n\tRestaurantes")
        for n, restaurant in enumerate(self.restaurantes):
            print(f"\n________{n+1}________")
            restaurant.show()