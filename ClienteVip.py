from Ticket import Ticket

class ClienteVip(Ticket):
    def __init__(self, id_ticket, partido, stadium, seat):
        super().__init__(id_ticket, partido, stadium, seat)
        self.price = 75

    def calcular_monto(self):
        self.subtotal = self.price
        if self.descuento:
            self.monto_descuento = self.subtotal * 0.5
        self.total = self.subtotal - self.monto_descuento + (self.subtotal * self.taxes)

    def show(self):
        print("\tTicket General")
        super().show_info()