import sqlite3

connection = sqlite3.connect('db/boom-boom.db')
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Utilisateurs(
               id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
               nom_utilisateur VARCHAR(50) NOT NULL,
               prenom_utilisateur VARCHAR(50) NOT NULL,
               pseudo_utilisateur VARCHAR(50) NOT NULL UNIQUE,
               mdp_utilisateur VARCHAR(50) NOt NULL,
               date_naissance_utilisateur DATE NOT NULL,
               genre_utilisateur VARCHAR(20) NOT NULL,
               email_utilisateur TEXT NOT NULL        
)
                ''')
connection.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS Artistes(
               id_artiste INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
               nom_artiste VARCHAR(50) NOT NULL UNIQUE
)
               ''')

connection.commit()

cursor.execute(''' CREATE TABLE IF NOT EXISTS Genres(
               id_genre INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
               nom_genre VARCHAR(50) NOT NULL UNIQUE
)
               
''')
connection.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS Albums (
               id_album INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
               nom_album VARCHAR(50) NOT NULL,
               date_sortie INT NOT NULL,
               id_genre INTEGER NOT NULL,
               id_artiste INTEGER NOT NULL,
               FOREIGN KEY (id_genre) REFERENCES Genres(id_genre),
               FOREIGN KEY (id_artiste) REFERENCES Artistes(id_artiste)

)
               
               ''')
connection.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS PreferencesMusique (
               id_preference INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
               id_utilisateur INT NOT NULL,
               id_album INT,
               id_genre INT,
               id_artiste INT,
               FOREIGN KEY(id_utilisateur) REFERENCES Utilisateurs(id_utilisateur),
               FOREIGN KEY(id_album) REFERENCES Albums(id_album),
               FOREIGN KEY(id_genre) REFERENCES Genres(id_genre),
               FOREIGN KEY(id_artiste) REFERENCES Artistes(id_artiste)
)
               
               ''')
connection.commit()

cursor.execute("INSERT INTO Genres (nom_genre) VALUES ('rock'), ('rap'), ('électro'), ('métal'), ('pop'), ('classique'), ('jazz')")
connection.commit()

cursor.execute("INSERT INTO Artistes (nom_artiste) VALUES ('Michael Jackson'), ('Beyoncé'), ('The Beatles'), ('Bob Marley'), ('Madonna'), ('Eminem'), ('Taylor Swift'), ('Drake'), ('AC/DC'), ('The Stranglers')")
connection.commit()

cursor.execute('''
    INSERT INTO Albums (nom_album, date_sortie, id_genre, id_artiste)
    VALUES 
    ('Thriller', 1982, 5, 1), 
    ('Lemonade', 2016, 6, 2), 
    ('Abbey Road', 1969, 1, 3), 
    ('Legend', 1984, 4, 4), 
    ('Like a Virgin', 1984, 5, 5), 
    ('Elvis Presley', 1956, 1, 6),
    ('Hells Bells', 1980, 1, 9)
''')


cursor.execute('''
    INSERT INTO Utilisateurs 
    (nom_utilisateur, prenom_utilisateur, pseudo_utilisateur, mdp_utilisateur, date_naissance_utilisateur, genre_utilisateur, email_utilisateur)
    VALUES 
    ('Doe', 'John', 'john_doe', 'mdp', '1990-01-01', 'Homme', 'john.doe@example.com'),
    ('Smith', 'Alice', 'alice_smith', 'mdp', '1995-05-15', 'Femme', 'alice.smith@example.com'),
    ('Johnson', 'Bob', 'bob_johnson', 'mdp', '1988-08-08', 'Homme', 'bob.johnson@example.com'),
    ('Claire', 'Nurdin', 'Claire', 'mdp', '1992-10-10', 'Femme', 'claire@claire.fr')
''')
connection.commit()

connection.close()





