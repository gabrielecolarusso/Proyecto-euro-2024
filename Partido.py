class Partido():
    def __init__(self, id_partido, equipo_Local, equipo_Visitante, fecha, stadium):
        self.id_partido = id_partido
        self.equipo_Local = equipo_Local
        self.equipo_Visitante = equipo_Visitante
        self.fecha = fecha
        self.stadium = stadium
        self.tickets_generales = stadium.capacity[0]
        self.tickets_vip = stadium.capacity[1]
        self.asientos_tomados = []
        self.visitas_estadio = 0
    

    def show(self):
        print(f"-Id: {self.id_partido}")
        print(f"-{self.equipo_Local} vs {self.equipo_Visitante}")
        print(f"-Fecha: {self.fecha}")
        print(f"-Estadio: {self.stadium.name}")
        print(f"-Capacidad: {self.stadium.capacity[0] + self.stadium.capacity[1]} asientos")
        print(f"-Tickets vendidos: {len(self.asientos_tomados)}")
        print(f"-Tickets disponibles: {self.tickets_generales + self.tickets_vip}")
        print(f"-Asistencia: {self.visitas_estadio}\n")
