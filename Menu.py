import re
from datetime import datetime
from Authentification import Authentification
from Planning import Planning
class Menu:

    def __init__(self,db,user):
        self.planning = Planning(db,user)
        self.user = user
    
    def saisir_date(self):
        date_format = r"^\d{4}-\d{2}-\d{2}$"

        while True:
            date_str = input("Entrer la date (YYYY-MM-DD) : ")

            if not re.match(date_format, date_str):
                print("Format invalide. Utiliser YYYY-MM-DD")
                continue
            # Vérifie si la date existe réellement
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                print("Date invalide ")
    def menu(self):
        self.planning.fetch_creneaux()
        self.planning.fetch_motif()


        while True:
            
            print("===========MENU===========") 
            print('')
            print(f"Bienvenue {self.user.nom}")
            print("1 - Afficher les creneaux ")
            print("2 - Ajouter un groupe ")
            print("3 - Afficher les groupes")
            print("4 - Ajouter un planning ")
            print("5 - Afficher planning vue global")
            print("6 - Afficher planning Vue Disponibilités")
            print("7 - Annuler planning ")
            print("8 - Exporter planning journalier (CSV)")

            print("0. Quitter")
            print("")
            choix = input("Veuillez choisir une des options  : ").strip()
            print('')


            match choix:
                case "1":
                    for c in self.planning.liste_creneaux:
                        print(c)
                case "2":
                    nom_groupe = input("Nom Groupe : ").strip()
                    nom_responsable = input("Nom Responsable : ").strip()
                    self.planning.ajout_groupe(nom_groupe,nom_responsable)
                case "3":
                    print("\nListe des groupes :")
                    groupe = self.planning.fetch_groupe()
                    for g in groupe:
                        print(f"{g["id_groupe"]} {g["nom_groupe"]} {g["nom_responsable"]}")
                case "4":
                    try:
                        # Saisie de la date
                        date_planning = self.saisir_date()

                        # Affichage des groupes
                        print("\nListe des groupes :")
                        groupes = self.planning.fetch_groupe()
                        for g in groupes:
                            print(f"{g['id_groupe']} - {g['nom_groupe']} - {g['nom_responsable']}")
                        id_groupe = input("Saisir le ID GROUPE : ").strip()

                        # Affichage des créneaux
                        print("\nListe des créneaux :")
                        lc = self.planning.liste_creneaux
                        for c in lc:
                            print(f"{c.id_creneaux} - {c.heure_debut} / {c.heure_fin}")

                        # Saisie des créneaux multiples
                        choix_creneaux = []
                        while True:
                            id_creneaux = input("Choisir id créneau (ou 'q' pour quitter) : ").strip()
                            if id_creneaux.lower() == "q":
                                break
                            elif id_creneaux in choix_creneaux:
                                print("Déjà choisi !")
                            else:
                                choix_creneaux.append(id_creneaux)

                        # Affichage des motifs
                        print("\nListe des motifs :")
                        for m in self.planning.liste_motifs:
                            print(f"{m.id_motif} - {m.nom}")
                        id_motif = input("Choisir l'id du motif : ").strip()

                        # Tentative d'ajout multiple
                        self.planning.ajout_multiple_planning(date_planning, id_groupe, choix_creneaux, id_motif)

                    except ValueError:
                        print(" Entrée invalide. Veuillez saisir des nombres valides pour les IDs.")
                    except Exception as e:
                        print(" Une erreur est survenue lors de l'ajout du planning.")
                        print("Détail :", e) 
                      
                case "5":
                    date_planning = self.saisir_date()
                    planning_list = self.planning.vue_globale(date_planning)

                    if not planning_list:
                        print("Aucun créneau trouvé")
                    else:
                        print(f"\nPlanning du {date_planning} :\n")

                        for p in planning_list:

                            # Créneau libre
                            if p["id_planning"] is None:
                                print(
                                    f" {p['heure_debut']} - {p['heure_fin']} | LIBRE"
                                    )

                            # Créneau annulé
                            elif p["statut"] == "ANNULE":
                                print(
                                    f"{p["id_planning"]} | {p['heure_debut']} - {p['heure_fin']} | "
                                    f"{p['nom_groupe']} | {p['nom_motif']} {p["statut"]}"
                                    )

                            # Créneau réservé
                            else:
                                print(
                                    f"{p["id_planning"]} | {p['heure_debut']} - {p['heure_fin']} | "
                                    f"{p['nom_groupe']} | {p['nom_motif']}"
                                    )
                
                case "6":
                    date_planning = self.saisir_date()
                    planning_list = self.planning.vue_disponibilites(date_planning)

                    if not planning_list:
                        print("Aucun créneau trouvé")
                    else:
                        print(f"\nPlanning du {date_planning} :\n")

                        dispos = self.planning.vue_disponibilites(date_planning)

                        print(f"\nCréneaux disponibles le {date_planning}\n")

                        if not dispos:
                            print("Aucun créneau libre.")
                        else:
                            for d in dispos:
                                print(f"{d['heure_debut']} - {d['heure_fin']}")
                case "7":
                    id_plan = int(input("Entrez l'ID du planning à annuler : "))
                    self.planning.annuler_planning(id_plan)
                
                case "8":
                    date = self.saisir_date()
                    self.planning.exporter_planning_csv(date)
                case "0":
                    print("Au revoir.") 

                    exit()              

class Couleur:
    VERT = "\033[92m"
    ROUGE = "\033[91m"
    BLEU = "\033[94m"
    RESET = "\033[0m"