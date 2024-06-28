class Equipo:
    def __init__(self, id, code, name, group):
        self.id = id
        self.code = code
        self.name = name
        self.group = group
    
    def show(self):
        return f"ID: {self.id}\nCode: {self.code}\nName: {self.name}\nGroup: {self.group} \n"