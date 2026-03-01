
class Creneau:
    def __init__(self, id_creneaux, heure_debut, heure_fin):
        self.id_creneaux = id_creneaux
        self.heure_debut = heure_debut
        self.heure_fin = heure_fin

    def __str__(self):
        return f"Creneau {self.id_creneaux}: {self.heure_debut} - {self.heure_fin}"
    
    
    


