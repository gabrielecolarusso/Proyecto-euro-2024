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
        for n, restaurant in enumerate(self.restaurantes):
            print(f"\n________{n+1}________")
            restaurant.show()
            return f"----Info Estadio----\nID: {self.id}\nEstadio: {self.name}\nCiudad: {self.city}\nCapacidad: {self.capacity[0], self.capacity[1]}\n\n ----Restaurantes del estadio----\n"