
import bcrypt

class Utilisateur:
    def __init__(self, id_utilisateur, nom, prenom, email, mot_de_passe, role="ADMIN"):
        self.id_utilisateur = id_utilisateur
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self._mot_de_passe = mot_de_passe  
        self.role = role

    def verifier_mot_de_passe(self, mot_de_passe):
        return bcrypt.checkpw(mot_de_passe.encode(), self._mot_de_passe.encode())

    def afficher_infos(self):
        return f"{self.nom} {self.prenom} ({self.role})"

    def is_admin(self):
        return self.role == "ADMIN"

