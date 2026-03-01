import re
import bcrypt
from Database import Database
from Utilisateur import Utilisateur

class Authentification:
    regex_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    regex_mdp = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"

    def __init__(self, db):
        self.db = db
        self.current_user = None

    # Vérifie si l'email existe
    def email_existe(self, email):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT 1 FROM utilisateurs WHERE email = %s", (email,))
        return cursor.fetchone() is not None
    def max_user(self):
        cursor = self.db.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM utilisateurs")
        rows = cursor.fetchall()
        taille = len(rows)
        return taille

    def verifier_insc_admin(self):
        code_secret = input("Saisir Code ")
        if code_secret == "12345678":
            print('code verifier')
            return True
        else:
            print("Vous voulez quoi ici ")
            return False
        
    # Inscription d'un nouvel utilisateur
    def inscription(self):
        if self.verifier_insc_admin() == False:
            return

        cursor = self.db.connection.cursor()
        
        
        
        nom = input("Nom : ").strip()
        prenom = input("Prénom : ").strip()

        while True:
            email = input("Email : ").strip()
            if re.match(self.regex_email, email):
                if not self.email_existe(email):
                    break
                else:
                    print("Email déjà utilisé.")
            else:
                print("Email invalide.")

        while True:
            mot_de_passe = input("Mot de passe : ").strip()
            if re.match(self.regex_mdp, mot_de_passe):
                break
            print("Mot de passe invalide (8 caractères minimum, majuscule, minuscule, chiffre)")

        # Hashage du mot de passe
        hash_mdp = bcrypt.hashpw(mot_de_passe.encode(), bcrypt.gensalt()).decode()

        try:
            cursor.execute(
                "INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe) VALUES (%s,%s,%s,%s)",
                (nom, prenom, email, hash_mdp)
            )
            self.db.connection.commit()
            print("Inscription réussie !")
            
        except Exception as e:
            print(f"Erreur inscription : {e}")

    # Connexion d'un utilisateur
    def connexion(self):
        cursor = self.db.connection.cursor(dictionary=True)
        print("=== CONNEXION ===")

        while True:
            email = input("Email : ").strip()
            if not re.match(self.regex_email, email):
                print("Email invalide.")
                continue
            if not self.email_existe(email):
                print("Email non trouvé.")
                continue
            break

        mdp = input("Mot de passe : ").strip()
        cursor.execute(
            "SELECT id_utilisateur, nom, prenom, email, mot_de_passe, role FROM utilisateurs WHERE email = %s",
            (email,)
        )
        data = cursor.fetchone()
        if data:
            user = Utilisateur(
                        id_utilisateur=data["id_utilisateur"],
                        nom=data["nom"],
                        prenom=data["prenom"],
                        email=data["email"],
                        mot_de_passe=data["mot_de_passe"],
                        role=data["role"]
                    )
            if user.verifier_mot_de_passe(mdp):
                self.current_user = user
                print(f"Bienvenue {user.nom} !")
                return user
        print("Identifiants invalides.")
        return None