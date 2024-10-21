class Gruppe:
    def __init__(self, name):
        self.name = name
        self.mitglieder = []

    def add(self, person):
        self.mitglieder.append(person)
        
    def __str__(self):
        return self.name