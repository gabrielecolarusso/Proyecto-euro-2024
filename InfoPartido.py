class InfoPartido():
    def __init__(self, equipo_Local, equipo_Visitante, fecha_partido, stadium_id):
        self.equipo_Local = equipo_Local
        self.equipo_Visitante = equipo_Visitante
        self.fecha_partido = fecha_partido
        self.stadium_id = stadium_id
        self.tickets_generales = stadium_id[0]
        self.tickets_vip = stadium_id[1]
        self.asientos_tomados = []
        self.visitas_estadio = 0
    

    def show(self):
        return f"""
INFORMACION DEL PARTIDO:
Equipo Local: {self.equipo_Local}
Equipo Visitante: {self.equipo_Visitante}
Fecha del partido: {self.fecha_partido}
Estadio: {self.stadium_id}
"""
