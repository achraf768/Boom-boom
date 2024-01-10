import flask
import sqlite3


app = flask.Flask(__name__, template_folder='views')
app.secret_key = 'secret-key'


@app.route('/', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        pseudo_utilisateur = flask.request.values.get('pseudo_utilisateur')
        mot_de_passe = flask.request.values.get('mot_de_passe')

        connection = sqlite3.connect('db/boom-boom.db')
        cursor = connection.cursor()
        cursor.execute('SELECT id_utilisateur FROM Utilisateurs WHERE pseudo_utilisateur=? and mdp_utilisateur = ?', (pseudo_utilisateur, mot_de_passe))
        tuple_id_utilisateur = cursor.fetchone()
        connection.close()

        if tuple_id_utilisateur is not None:
            id_utilisateur = tuple_id_utilisateur[0]
            flask.session['user_id'] = id_utilisateur
            flask.session['pseudo_user'] = pseudo_utilisateur
            return flask.redirect('/dashboard')

        else:
            return flask.render_template('error_page.html', message="L'identifiant ou le mot de passe est incorrect ! ")
    
    else:
        return flask.render_template('login.html')  

    
@app.route('/dashboard', methods=['GET', 'POST'])
def home():
    if flask.request.method == 'POST':
        genre = flask.request.values.get('genre')
        artiste = flask.request.values.get('artist')
        album = flask.request.values.get('album')

        # Ici on stocke les valeurs des filtres dans la session Flask
        flask.session['selected_genre'] = genre
        flask.session['selected_artiste'] = artiste
        flask.session['selected_album'] = album

        return flask.redirect('/dashboard')

    else:
        pseudo_utilisateur = flask.session.get("pseudo_user")
        # Ici on récupère les valeurs des filtre depuis la session
        selected_genre = flask.session.get('selected_genre')
        selected_artiste = flask.session.get('selected_artiste')
        selected_album = flask.session.get('selected_album')

        connection = sqlite3.connect('db/boom-boom.db')
        cursor = connection.cursor()

        requete_de_base = '''
            SELECT u.pseudo_utilisateur, ab.nom_album, ar.nom_artiste, g.nom_genre  
            FROM PreferencesMusique pm
            JOIN Utilisateurs u ON pm.id_utilisateur = u.id_utilisateur
            LEFT JOIN Artistes ar ON  pm.id_artiste = ar.id_artiste
            LEFT JOIN Genres g ON pm.id_genre = g.id_genre
            LEFT JOIN Albums ab ON  pm.id_album = ab.id_album
        '''

        parameters = []

        # On Ajoute des conditions de filtrage a notre requete de base en fonction des valeurs sélectionnées par l'utilisateur
        if selected_genre and selected_genre != 'aucun':
            requete_de_base += ' WHERE g.nom_genre = ?'
            parameters.append(selected_genre)

        if selected_artiste and selected_artiste != 'aucun':
            if 'WHERE' in requete_de_base:
                requete_de_base += ' AND ar.nom_artiste = ?'
            else:
                requete_de_base += ' WHERE ar.nom_artiste = ?'
            parameters.append(selected_artiste)

        if selected_album and selected_album != 'aucun':
            if 'WHERE' in requete_de_base:
                requete_de_base += ' AND ab.nom_album = ?'
            else:
                requete_de_base += ' WHERE ab.nom_album = ?'
            parameters.append(selected_album)
        
        if 'WHERE' in requete_de_base:
            requete_de_base += ' AND u.pseudo_utilisateur NOT LIKE ?'
        else:
             requete_de_base += ' WHERE u.pseudo_utilisateur NOT LIKE ?'
        parameters.append(pseudo_utilisateur)

        cursor.execute(requete_de_base, tuple(parameters))
        preferences_utilisateurs = cursor.fetchall()

        # On récupère les listes de genres, artistes et albums
        cursor.execute('SELECT nom_genre FROM Genres')
        genres = cursor.fetchall()

        cursor.execute('SELECT nom_album FROM Albums')
        albums = cursor.fetchall()

        cursor.execute('SELECT nom_artiste FROM Artistes')
        artistes = cursor.fetchall()

        connection.close()

        liste_genres = [genre[0] for genre in genres]
        liste_genres.sort()

        liste_artistes = [artiste[0] for artiste in artistes]
        liste_artistes.sort()

        liste_albums = [album[0] for album in albums]
        liste_albums.sort()

        # Ici on réinitialise les filtres dans la session après utilisation pour éviter d'avoir les résultats d'un ancien filtrage lorsqu'on reviendra sur cette page
        flask.session['selected_genre'] = 'aucun'
        flask.session['selected_artiste'] = 'aucun'
        flask.session['selected_album'] = 'aucun'

        return flask.render_template('index.html', preferences_utilisateurs=preferences_utilisateurs, liste_genres=liste_genres, liste_albums=liste_albums, liste_artistes=liste_artistes, pseudo_utilisateur=pseudo_utilisateur)


@app.route('/add_user', methods=['GET', 'POST'])
def add_person():
    if flask.request.method == 'POST':

        nom = flask.request.values.get('nom')
        prenom = flask.request.values.get('prenom')
        pseudo = flask.request.values.get('pseudo')
        mdp = flask.request.values.get('mdp')
        age = flask.request.values.get('age')
        genre = flask.request.values.get('genre')
        email = flask.request.values.get('mail')

        connection = sqlite3.connect('db/boom-boom.db')
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM utilisateurs WHERE pseudo_utilisateur = ?', (pseudo,))
        pseudo_existe = cursor.fetchone()[0] > 0
        connection.close()

        if pseudo_existe:
            return flask.render_template('error_page.html', message='Ce pseudo est déjà pris ! ')
            # return flask.render_template('add_user.html')

        else:
            connection = sqlite3.connect('db/boom-boom.db')
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO utilisateurs (nom_utilisateur, prenom_utilisateur, pseudo_utilisateur, mdp_utilisateur, date_naissance_utilisateur, genre_utilisateur, email_utilisateur)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (nom, prenom, pseudo, mdp, age, genre, email))
            connection.commit()
            connection.close()
            return flask.redirect('/')

    else:
        return flask.render_template('add_user.html')
    

@app.route('/add_band', methods=['GET', 'POST'])
def add_band():
    if flask.request.method == 'POST':
        nom_artiste = flask.request.values.get('artist')
    
        connection = sqlite3.connect('db/boom-boom.db')
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM Artistes WHERE nom_artiste = ?', (nom_artiste.strip(),))
        artiste_existe = cursor.fetchone()[0] > 0

        if artiste_existe:
            return flask.render_template('error_page.html', message='Cet artiste existe déjà dans la base ! ')
        else:
            cursor.execute('INSERT INTO Artistes (nom_artiste) VALUES (?)', (nom_artiste,))
            connection.commit()
            connection.close()
            return flask.redirect('/dashboard')

    else:
        return flask.render_template('add_band.html')
    

@app.route('/add_album', methods=['GET', 'POST'])
def add_album():
    if flask.request.method == 'POST':
        nom_album = flask.request.values.get('nom_album')
        date_sortie = flask.request.values.get('date_sortie')
        nom_genre = flask.request.values.get('genre')
        nom_artiste = flask.request.values.get('nom_artiste')

        connection = sqlite3.connect('db/boom-boom.db')
        cursor = connection.cursor()
        cursor.execute('SELECT id_genre FROM Genres WHERE nom_genre=?', (nom_genre,))
        tuple_id_genre = cursor.fetchone()
        id_genre = tuple_id_genre[0]
        connection.close()

        connection = sqlite3.connect('db/boom-boom.db')
        cursor = connection.cursor()
        cursor.execute('SELECT id_artiste FROM Artistes WHERE nom_artiste = ?', (nom_artiste,))
        tuple_id_artiste = cursor.fetchone()
        connection.close()

        if tuple_id_artiste:
            id_artiste = tuple_id_artiste[0]
        else:
            return flask.render_template('error_page.html', message='Cet artiste n\'existe pas dans la base !')
    
        connection = sqlite3.connect('db/boom-boom.db')
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM Albums WHERE nom_album = ? and id_artiste = ?', (nom_album.strip(), id_artiste))
        album_existe = cursor.fetchone()[0] > 0

        if album_existe:
            return flask.render_template('error_page.html', message='Cet album existe déjà dans la base ! ') 
        
        else:
            cursor.execute('INSERT INTO Albums (nom_album, date_sortie, id_genre, id_artiste) VALUES (?, ?, ?, ?)', (nom_album, date_sortie, id_genre, id_artiste ))
            connection.commit()
            connection.close()
            return flask.redirect('/dashboard')

    else:
        connection = sqlite3.connect('db/boom-boom.db')
        cursor = connection.cursor()
        cursor.execute('SELECT nom_genre FROM Genres')
        genres = cursor.fetchall()
        connection.close()

        liste_genres = []

        for genre in genres:
            liste_genres.append(genre[0])

        return flask.render_template('add_album.html', liste_genres=liste_genres)
    

@app.route('/add_genre', methods=['GET', 'POST'])
def add_genre():
    if flask.request.method == 'POST':
        nom_genre = flask.request.values.get('genre')
    
        connection = sqlite3.connect('db/boom-boom.db')
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM Genres WHERE nom_genre = ?', (nom_genre.strip(),))
        genre_existe = cursor.fetchone()[0] > 0

        if genre_existe:
            return flask.render_template('error_page.html', message='Ce genre musical est déjà enregistré dans la base ! ') 
        
        else:
            cursor.execute('INSERT INTO Genres (nom_genre) VALUES (?)', (nom_genre,))
            connection.commit()
            connection.close()
            return flask.redirect('/dashboard')

    else:
        return flask.render_template('add_genre.html')


@app.route('/add_preferences', methods=['GET', 'POST'])
def add_preferences():
    id_utilisateur = flask.session.get("user_id")
    
    if flask.request.method == 'POST':

        genre = flask.request.values.get('genre')
        artiste = flask.request.values.get('artist')
        album = flask.request.values.get('album')

        connection = sqlite3.connect('db/boom-boom.db')
        cursor = connection.cursor()

        cursor.execute('SELECT id_genre FROM Genres WHERE nom_genre = ?', (genre,))
        tuple_id_genre = cursor.fetchone()
        id_genre = tuple_id_genre[0] if tuple_id_genre else None
      
        cursor.execute('SELECT id_artiste FROM Artistes WHERE nom_artiste = ?', (artiste,))
        tuple_id_artiste = cursor.fetchone()
        id_artiste = tuple_id_artiste[0] if tuple_id_artiste else None
     
        cursor.execute('SELECT id_album FROM Albums WHERE nom_album = ?', (album,))
        tuple_id_album = cursor.fetchone()
        id_album = tuple_id_album[0] if tuple_id_album else None

        cursor.execute('SELECT COUNT(*) FROM PreferencesMusique pm JOIN Genres g ON pm.id_genre = g.id_genre WHERE pm.id_utilisateur = ? and g.id_genre = ?', (id_utilisateur, id_genre))
        genre_existe_deja_dans_preferences = cursor.fetchone()[0] > 0

        cursor.execute('SELECT COUNT(*) FROM PreferencesMusique pm JOIN Artistes a ON pm.id_artiste = a.id_artiste WHERE pm.id_utilisateur = ? and a.id_artiste = ?', (id_utilisateur, id_artiste))
        artiste_existe_deja_dans_preferences = cursor.fetchone()[0] > 0

        cursor.execute('SELECT COUNT(*) FROM PreferencesMusique pm JOIN Albums alb ON pm.id_album = alb.id_album WHERE pm.id_utilisateur = ? and alb.id_album = ?', (id_utilisateur, id_album))
        album_existe_deja_dans_preferences = cursor.fetchone()[0] > 0

        if genre_existe_deja_dans_preferences or artiste_existe_deja_dans_preferences or album_existe_deja_dans_preferences:
            return flask.render_template('error_page.html', message="L'un des éléments sélectionné fait déjà parti de vos préférences !")

        cursor.execute('INSERT INTO PreferencesMusique (id_utilisateur, id_album, id_genre, id_artiste) VALUES (?,?,?,?)', (id_utilisateur, id_album, id_genre, id_artiste))
        connection.commit()

        connection.close()


        return flask.redirect('/dashboard')

    else:
        connection = sqlite3.connect('db/boom-boom.db')
        cursor = connection.cursor()
        cursor.execute('''SELECT alb.nom_album, ar.nom_artiste, g.nom_genre
                       FROM PreferencesMusique pm
                       LEFT JOIN Albums alb ON pm.id_album = alb.id_album
                       LEFT JOIN Artistes ar ON pm.id_artiste = ar.id_artiste
                       LEFT JOIN Genres g ON pm.id_genre = g.id_genre
                       WHERE pm.id_utilisateur = ?
                       ''', (id_utilisateur,))
        preferences = cursor.fetchall()

        cursor.execute('SELECT nom_genre FROM Genres')
        genres = cursor.fetchall()
        cursor.execute('SELECT nom_album FROM Albums')
        albums = cursor.fetchall()
        cursor.execute('SELECT nom_artiste FROM Artistes')
        artistes = cursor.fetchall()
        connection.close()

        liste_genres = []
        for genre in genres:
            liste_genres.append(genre[0])
            liste_genres.sort()

        liste_artistes = []
        for artiste in artistes:
            liste_artistes.append(artiste[0])
            liste_artistes.sort()

        liste_albums = []
        for album in albums:
            liste_albums.append(album[0])
            liste_albums.sort()

        return flask.render_template('add_preferences.html',preferences=preferences, liste_genres=liste_genres, liste_albums=liste_albums, liste_artistes= liste_artistes)

        

