class Groupe:
    def __init__(self,id_groupes, nom_groupe, nom_responsable):
        self.nom_groupe = nom_groupe
        self.id_groupes = id_groupes
        self.nom_responsable = nom_responsable

    def __str__(self):
        return f"Groupe: {self.id_groupes} {self.nom_groupe}, Responsable: {self.nom_responsable}"
