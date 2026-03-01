CREATE TABLE utilisateurs (
    id_utilisateur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    role ENUM('ADMIN') NOT NULL DEFAULT 'ADMIN',
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

CREATE TABLE creneaux (
    id_creneaux INT AUTO_INCREMENT PRIMARY KEY,
    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL,
    id_utilisateur INT,
    
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur),
    
    CONSTRAINT unique_creneau UNIQUE (heure_debut, heure_fin)
);

CREATE TABLE groupes (
    id_groupe INT AUTO_INCREMENT PRIMARY KEY,
    nom_groupe VARCHAR(100) NOT NULL,
    nom_responsable VARCHAR(100) NOT NULL,
    id_utilisateur INT,
    FOREIGN KEY (id_utilisateur)
        REFERENCES utilisateurs(id_utilisateur)
);

CREATE TABLE planning (
    id_planning INT AUTO_INCREMENT PRIMARY KEY,
    date_planning DATE NOT NULL,
    id_groupe INT NOT NULL,
    id_creneaux INT NOT NULL,
    id_motif INT NOT NULL,

    statut ENUM('VALIDE','ANNULE','TERMINE') 
        NOT NULL DEFAULT 'VALIDE',

    -- colonne technique pour l'unicité conditionnelle
    actif TINYINT AS (
        CASE 
            WHEN statut = 'VALIDE' THEN 1
            ELSE NULL
        END
    ) STORED,

    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_groupe)
        REFERENCES groupes(id_groupe),
    FOREIGN KEY (id_creneaux)
        REFERENCES creneaux(id_creneaux),
    FOREIGN KEY (id_motif)
        REFERENCES motifs(id_motif),
    CONSTRAINT unique_planning UNIQUE (date_planning, id_creneaux, actif)
);


CREATE TABLE motifs (
    id_motif INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    id_utilisateur INT,
    
    FOREIGN KEY (id_utilisateur)
        REFERENCES utilisateurs(id_utilisateur)
);