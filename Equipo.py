class Equipo:
    def __init__(self, id, code, name, group):
        self.id = id
        self.code = code
        self.name = name
        self.group = group

    def get_id(self):
        return self.id
    
    def get_code(self):
        return self.code
    
    def get_name(self):
        return self.name
    
    def get_group(self):
        return self.group
    
    def show(self):
        return f"ID: {self.id}\nCode: {self.code}\nName: {self.name}\nGroup: {self.group} \n"