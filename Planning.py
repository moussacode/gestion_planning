from Database import Database
from datetime import datetime
from Creneaux import Creneau
from Motifs import Motif
import csv

class Planning:
    def __init__(self,db,user):
        self.liste_creneaux = []
        self.liste_motifs = []
        self.db = db
        self.user = user

    def fetch_creneaux(self):
        """Récupère tous les créneaux depuis la base et les stocke dans self.liste_creneaux"""
        cursor = self.db.connection.cursor(dictionary=True)
        cursor.execute("SELECT id_creneaux, heure_debut, heure_fin FROM creneaux ORDER BY id_creneaux")
        rows = cursor.fetchall()
        for row in rows:
                creneau = Creneau(row["id_creneaux"], row["heure_debut"],row["heure_fin"])
                self.liste_creneaux.append(creneau)
        # Transforme chaque ligne en objet Creneau
        cursor.close()
        # self.db.fermer()
    def fetch_motif(self):
        """Récupère tous les motif depuis la base et les stocke dans self.liste_motifs"""
        cursor = self.db.connection.cursor(dictionary=True)
        cursor.execute("SELECT id_motif, nom FROM motifs ORDER BY id_motif")
        rows = cursor.fetchall()
        for row in rows:
                motif = Motif(row["id_motif"], row["nom"])
                self.liste_motifs.append(motif)
           
        # Transforme chaque ligne en objet Creneau
        cursor.close()
        # self.db.fermer()
    
    def ajout_groupe (self,nom_groupe,nom_responsable):
        cursor = self.db.connection.cursor()
        query = """
    INSERT INTO groupes (nom_groupe, nom_responsable, id_utilisateur)
    VALUES (%s, %s, %s)
    """

        cursor.execute(query, (nom_groupe, nom_responsable, self.user.id_utilisateur))
        self.db.connection.commit()

        cursor.close()
        self.db.fermer()

        print("Groupe ajouté avec succès")

    def ajout_planning (self, date_planning, id_groupe, id_creneaux, id_motif):
        cursor = self.db.connection.cursor()
        verification = """
    SELECT COUNT(*) FROM planning
    WHERE date_planning = %s
    AND id_creneaux = %s
    AND statut = 'VALIDE'
    """

        cursor.execute(verification, (date_planning, id_creneaux))
        deja_pris = cursor.fetchone()[0]
        if deja_pris > 0:
            print("Ce créneau est déjà réservé à cette date.")
            cursor.close()
            return False
        insertion = """
    INSERT INTO planning (date_planning, id_groupe, id_creneaux, id_motif)
    VALUES (%s, %s, %s, %s)
    """

        cursor.execute(insertion, (date_planning, id_groupe, id_creneaux, id_motif))
        self.db.connection.commit()

        print("Planning ajouté avec succès.")

    def vue_globale(self, date_planning):

        cursor = self.db.connection.cursor(dictionary=True)

        query = """
            SELECT 
                c.heure_debut,
                c.heure_fin,
                p.id_planning,
                p.date_planning,
                p.statut,
                g.nom_groupe,
                m.nom AS nom_motif
            FROM creneaux c
            LEFT JOIN planning p 
                ON c.id_creneaux = p.id_creneaux
                AND p.date_planning = %s
            LEFT JOIN groupes g 
                ON p.id_groupe = g.id_groupe
            LEFT JOIN motifs m 
                ON p.id_motif = m.id_motif
            ORDER BY c.heure_debut
        """

        cursor.execute(query, (date_planning,))
        result = cursor.fetchall()
        cursor.close()

        return result
    
    def vue_disponibilites(self, date_planning):

        cursor = self.db.connection.cursor(dictionary=True)

        query = """
            SELECT 
                c.heure_debut,
                c.heure_fin
            FROM creneaux c
            LEFT JOIN planning p 
                ON c.id_creneaux = p.id_creneaux
                AND p.date_planning = %s
            WHERE p.id_planning IS NULL
            ORDER BY c.heure_debut
        """

        cursor.execute(query, (date_planning,))
        result = cursor.fetchall()
        cursor.close()

        return result
    def annuler_planning(self, id_planning):

        cursor = self.db.connection.cursor()

        query = "UPDATE planning SET statut = 'ANNULE' WHERE id_planning = %s"

        cursor.execute(query, (id_planning,))
        self.db.connection.commit()
        cursor.close()

        print("Planning annulé.")
    def exporter_planning_csv(self, date_planning):

        cursor = self.db.connection.cursor(dictionary=True)

        query = """
            SELECT 
                c.heure_debut,
                c.heure_fin,
                g.nom_groupe,
                m.nom AS motif,
                g.nom_responsable
            FROM planning p
            JOIN groupes g ON p.id_groupe = g.id_groupe
            JOIN creneaux c ON p.id_creneaux = c.id_creneaux
            JOIN motifs m ON p.id_motif = m.id_motif
            WHERE p.date_planning = %s
            AND p.statut = 'VALIDE'
            ORDER BY c.heure_debut
        """

        cursor.execute(query, (date_planning,))
        result = cursor.fetchall()
        cursor.close()

        if not result:
            print("Aucune occupation validée à exporter.")
            return

        filename = f"planning_{date_planning}.csv"

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # En-tête
            writer.writerow([
                "Heure début",
                "Heure fin",
                "Groupe",
                "Motif",
                "Responsable"
            ])

            # Données
            for row in result:
                writer.writerow([
                    row["heure_debut"],
                    row["heure_fin"],
                    row["nom_groupe"],
                    row["motif"],
                    row["nom_responsable"]
                ])

        print(f"✅ Export réussi : {filename}")