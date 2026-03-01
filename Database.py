import mysql.connector

from mysql.connector import Error # pour la gestion des erreurs MySQL



class Database :
    def __init__(self, host="localhost", user="root", password="", database="planning"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset="utf8mb4"
        self.use_unicode=True
        self.connection = None

    def connecter(self):
        """Etablit la connexion MySQL"""
        if self.connection and self.connection.is_connected():
            return self.connection
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset,
                use_unicode=self.use_unicode,
            )
            print("Connecte a MySQL")
            return self.connection
        except Error as e:
            print(f"Erreur de connexion : {e}")
            return None

    def fermer(self):
        """Ferme la connexion MySQL"""
        if self.connection and self.connection.is_connected():
            self.connection.close()

        
    