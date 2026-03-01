from Menu import Menu
from Database import Database
from Authentification import Authentification
#Main Application
db = Database()
db.connecter()

class Menu_Auth :
    def __init__(self): 
        self.auth = Authentification(db)
 
    def menu_authentification(self):
        print("================= MENU AUTHENTIFICATION ======================")
        

        while True:
            print('')
            print("1 - Se connecter")
            print("2 - S'inscrire ")
            print("3 - Quitter")
            print('')

            choix = input("Veuillez choisir une des options (1-3) : ").strip()

            if choix == "1":
                user = self.auth.connexion()
                if user:
                    menu = Menu(db,user)
                    menu.menu()

            if choix == '2' :
                    self.auth.inscription()
            elif choix == '3':
                exit()
            else:
                print("Choix invalide. Veuillez entrer 1, 2 ou 3.")


menu = Menu_Auth()

menu.menu_authentification()