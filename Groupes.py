class Groupe:
    def __init__(self, nom_groupe, nom_responsable):
        self.nom_groupe = nom_groupe
        self.nom_responsable = nom_responsable

    def __str__(self):
        return f"Groupe: {self.nom_groupe}, Responsable: {self.nom_responsable}"
