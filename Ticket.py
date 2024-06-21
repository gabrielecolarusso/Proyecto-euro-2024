class Ticket():
    def __init__(self, id_ticket, partido, stadium, seat):
        self.id_ticket = id_ticket
        self.partido = partido
        self.stadium = stadium
        self.seat = seat
        self.descuento = False
        self.subtotal = 0
        self.monto_descuento = 0
        self.taxes = 0.16
        self.total = 0
    
    def show_info(self):
        print(f"-Ticket ID: {self.id_ticket}")
        print(f"-Partido: {self.partido.equipo_Local} vs {self.partido.equipo_Visitante}")
        print(f"-Estadio: {self.stadium}")
        print(f"-Asiento: {self.seat}")
        print(f"-Descuento (50%): {self.descuento}")
        if self.descuento:
            print(f"-Descuento: ${self.monto_descuento}")
        print(f"-Subtotal: ${self.subtotal}")
        print(f"-Impuestos (16%): ${self.subtotal * self.taxes}")
        print(f"-Total: ${self.total}")