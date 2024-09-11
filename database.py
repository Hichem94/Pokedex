import sqlite3

# Créer connexion à la BD ou connexion si elle existe
conn = sqlite3.connect('pokedex.db') 
cursor = conn.cursor()

# Créer la table 'mypokemons'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mypokemons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        taille INTEGER,
        categorie TEXT,
        poids INTEGER,
        image_path TEXT,
        pv INTEGER,
        attaque INTEGER,
        defense INTEGER,
        attaque_speciale INTEGER,
        defense_speciale INTEGER,
        vitesse INTEGER            
    )
''')
conn.commit()

# Création de la table "Type"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS type (
        id_type INTEGER PRIMARY KEY,
        nom_type TEXT,
        description TEXT
    )
''')
conn.commit()


# Données à insérer (tous les types de Pokémon)
types = [
    (1, 'Eau', 'Les Pokémon de type Eau sont forts contre les Pokémon de type Feu et Vol.'),
    (2, 'Feu', 'Les Pokémon de type Feu sont forts contre les Pokémon de type Plante et Insecte.'),
    (3, 'Plante', 'Les Pokémon de type Plante sont forts contre les Pokémon de type Eau et Roche.'),
    (4, 'Électrik', 'Les Pokémon de type Électrik sont forts contre les Pokémon de type Eau et Vol.'),
    (5, 'Normal', 'Les Pokémon de type Normal ne sont forts ni faibles contre aucun type particulier.'),
    (6, 'Combat', 'Les Pokémon de type Combat sont forts contre les Pokémon de type Roche et Glace.'),
    (7, 'Poison', 'Les Pokémon de type Poison sont forts contre les Pokémon de type Plante et Insecte.'),
    (8, 'Terre', 'Les Pokémon de type Terre sont forts contre les Pokémon de type Feu, Électrik et Roche.'),
    (9, 'Vol', 'Les Pokémon de type Vol sont forts contre les Pokémon de type Plante et Insecte.'),
    (10, 'Psy', 'Les Pokémon de type Psy sont forts contre les Pokémon de type Combat et Poison.'),
    (11, 'Insecte', 'Les Pokémon de type Insecte sont forts contre les Pokémon de type Plante et Psy.'),
    (12, 'Roche', 'Les Pokémon de type Roche est fort contre les Pokémon de type Feu, Glace et Vol.'),
    (13, 'Ciel', 'Les Pokémon de type Ciel est fort contre les Pokémon de type Combat et Psy.'),
    (14, 'Glace', 'Les Pokémon de type Glace est fort contre les Pokémon de type Plante, Vol et Dragon.'),
    (15, 'Dragon', 'Les Pokémon de type Dragon est fort contre les Pokémon de type Dragon.'),
    (16, 'Ténèbres', 'Les Pokémon de type Ténèbres est fort contre les Pokémon de type Psy et Fantôme.'),
    (17, 'Fée', 'Les Pokémon de type Fée est fort contre les Pokémon de type Combat, Dragon et Ténèbres.'),
    (18, 'Acier', 'Les Pokémon de type Acier est fort contre les Pokémon de type Glace, Roche et Fée.')
]
sql = '''
    INSERT OR IGNORE INTO type (id_type, nom_type, description)
    VALUES (?, ?, ?)
'''
cursor.executemany(sql, types)
conn.commit()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS pokemon_type (
    id_pokemon INT,
    id_type INT,
    PRIMARY KEY (id_pokemon, id_type),
    FOREIGN KEY (id_pokemon) REFERENCES pokemon(id_pokemon),
    FOREIGN KEY (id_type) REFERENCES type(id_type)
    );
''')
conn.commit()

conn.close()


# Fonction pour ajouter un nouveau Pokémon
def ajouter_pokemon(pokemon_info):
    """pokemon_info est un dictionnaire"""
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO mypokemons (nom, taille, categorie, poids, image_path, pv, attaque, defense, attaque_speciale, defense_speciale, vitesse)\
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (pokemon_info['nom'], pokemon_info['taille'], pokemon_info['categorie'], pokemon_info['poids'],
                    pokemon_info['image_path'], pokemon_info['stats']['pv'], pokemon_info['stats']['attaque'], pokemon_info['stats']['defense'],
                    pokemon_info['stats']['attaque_speciale'], pokemon_info['stats']['defense_speciale'], pokemon_info['stats']['vitesse'],)
                   )
    conn.commit()
    pokemon_id = cursor.lastrowid

    # Récupérer les ID de/des type(s) du pokemon
    types_du_pokemon = pokemon_info['types']
    cursor.execute(f"SELECT type_id FROM type WHERE nom_type in {types_du_pokemon}")
    type_ids = [row[0] for row in cursor.fetchall()]

    # Insertion des type-Pokémon
    for type_id in type_ids:
        cursor.execute("INSERT INTO pokemon_type (id_pokemon, id_type) VALUES (?, ?)", (pokemon_id, type_id))

    conn.commit()
    conn.close()


# Fonction pour lister tous les Pokémon
def lister_tous_les_pokemons():
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()

    cursor.execute("SELECT nom, taille, categorie, poids, type, image_path, pv, attaque, defense, attaque_speciale, defense_speciale, vitesse\
                    FROM mypokemons")

    conn.commit()
    pokemons = cursor.fetchall()
    conn.close()
    return pokemons


# Fonction pour lister tous les Pokémon
def lister_un_pokemon(pokemon_name):
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()

    cursor.execute("SELECT nom, taille, categorie, poids, type, image_path, pv, attaque, defense, attaque_speciale, defense_speciale, vitesse\
                    FROM mypokemons\
                    WHERE nom={pokemon_name}")

    pokemon = cursor.fetchall()

    conn.close()
    return pokemon