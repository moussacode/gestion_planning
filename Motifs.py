class Motif:
    def __init__(self,id_motif, nom):
        self.id_motif = id_motif
        self.nom = nom

    def __str__(self):
        return f"Motif {self.id_motif} : {self.nom}"


    @staticmethod
    def list_all(cursor):
        cursor.execute("SELECT * FROM motifs")
        return cursor.fetchall()