import sqlite3

connection = sqlite3.connect('db/boom-boom.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Preference (
                id_preference INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                id_utilisateur INTEGER NOT NULL,
                id_album INTEGER NOT NULL,
                id_genre INTEGER NOT NULL,
                id_artiste INTEGER NOT NULL,
                FOREIGN KEY (id_utilisateur) REFERENCES Utilisateurs(id_utilisateur),
                FOREIGN KEY (id_album) REFERENCES Albums(id_album),
                FOREIGN KEY (id_genre) REFERENCES Genres(id_genre),
                FOREIGN KEY (id_artiste) REFERENCES Artistes(id_artiste)

)
               
               ''')
connection.commit()
connection.close()