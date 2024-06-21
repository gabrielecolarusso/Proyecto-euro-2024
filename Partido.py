class Partido():
    def __init__(self, id_partido, equipo_Local, equipo_Visitante, fecha, stadium_id):
        self.id_partido = id_partido
        self.equipo_Local = equipo_Local
        self.equipo_Visitante = equipo_Visitante
        self.fecha = fecha
        self.stadium_id = stadium_id
        self.tickets_generales = stadium_id[0]
        self.tickets_vip = stadium_id[1]
        self.asientos_tomados = []
        self.visitas_estadio = 0
    

    def get_date(self):
        return self.fecha

    def show(self):
        return f"Partido: {self.equipo_Local} vs. {self.equipo_Visitante}\nEstadio: {self.stadium_id()}\nFecha: {self.fecha}"