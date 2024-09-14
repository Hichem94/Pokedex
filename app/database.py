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
types_fr = [
    (1, 'eau', 'Les Pokémon de type Eau sont forts contre les Pokémon de type Feu et Vol.'),
    (2, 'feu', 'Les Pokémon de type Feu sont forts contre les Pokémon de type Plante et Insecte.'),
    (3, 'plante', 'Les Pokémon de type Plante sont forts contre les Pokémon de type Eau et Roche.'),
    (4, 'électrik', 'Les Pokémon de type Électrik sont forts contre les Pokémon de type Eau et Vol.'),
    (5, 'normal', 'Les Pokémon de type Normal ne sont forts ni faibles contre aucun type particulier.'),
    (6, 'combat', 'Les Pokémon de type Combat sont forts contre les Pokémon de type Roche et Glace.'),
    (7, 'poison', 'Les Pokémon de type Poison sont forts contre les Pokémon de type Plante et Insecte.'),
    (8, 'terre', 'Les Pokémon de type Terre sont forts contre les Pokémon de type Feu, Électrik et Roche.'),
    (9, 'vol', 'Les Pokémon de type Vol sont forts contre les Pokémon de type Plante et Insecte.'),
    (10, 'psy', 'Les Pokémon de type Psy sont forts contre les Pokémon de type Combat et Poison.'),
    (11, 'insecte', 'Les Pokémon de type Insecte sont forts contre les Pokémon de type Plante et Psy.'),
    (12, 'roche', 'Les Pokémon de type Roche est fort contre les Pokémon de type Feu, Glace et Vol.'),
    (13, 'ciel', 'Les Pokémon de type Ciel est fort contre les Pokémon de type Combat et Psy.'),
    (14, 'glace', 'Les Pokémon de type Glace est fort contre les Pokémon de type Plante, Vol et Dragon.'),
    (15, 'dragon', 'Les Pokémon de type Dragon est fort contre les Pokémon de type Dragon.'),
    (16, 'ténèbres', 'Les Pokémon de type Ténèbres est fort contre les Pokémon de type Psy et Fantôme.'),
    (17, 'fée', 'Les Pokémon de type Fée est fort contre les Pokémon de type Combat, Dragon et Ténèbres.'),
    (18, 'acier', 'Les Pokémon de type Acier est fort contre les Pokémon de type Glace, Roche et Fée.')
]
types_en = [
    (1, 'water', 'Les Pokémon de type Eau sont forts contre les Pokémon de type Feu et Vol.'),
    (2, 'fire', 'Les Pokémon de type Feu sont forts contre les Pokémon de type Plante et Insecte.'),
    (3, 'grass', 'Les Pokémon de type Plante sont forts contre les Pokémon de type Eau et Roche.'),
    (4, 'electric', 'Les Pokémon de type Électrik sont forts contre les Pokémon de type Eau et Vol.'),
    (5, 'normal', 'Les Pokémon de type Normal ne sont forts ni faibles contre aucun type particulier.'),
    (6, 'fighting', 'Les Pokémon de type Combat sont forts contre les Pokémon de type Roche et Glace.'),
    (7, 'poison', 'Les Pokémon de type Poison sont forts contre les Pokémon de type Plante et Insecte.'),
    (8, 'ground', 'Les Pokémon de type Terre sont forts contre les Pokémon de type Feu, Électrik et Roche.'),
    (9, 'flying', 'Les Pokémon de type Vol sont forts contre les Pokémon de type Plante et Insecte.'),
    (10, 'psychic', 'Les Pokémon de type Psy sont forts contre les Pokémon de type Combat et Poison.'),
    (11, 'bug', 'Les Pokémon de type Insecte sont forts contre les Pokémon de type Plante et Psy.'),
    (12, 'rock', 'Les Pokémon de type Roche est fort contre les Pokémon de type Feu, Glace et Vol.'),
    (13, 'fairy', 'Les Pokémon de type Ciel est fort contre les Pokémon de type Combat et Psy.'),  # Correction : Ciel -> Fairy
    (14, 'ice', 'Les Pokémon de type Glace est fort contre les Pokémon de type Plante, Vol et Dragon.'),
    (15, 'dragon', 'Les Pokémon de type Dragon est fort contre les Pokémon de type Dragon.'),
    (16, 'dark', 'Les Pokémon de type Ténèbres est contre les Pokémon de type Psy et Fantôme.'),
    (17, 'fairy', 'Les Pokémon de type Fée est contre les Pokémon de type Combat, Dragon et Ténèbres.'),
    (18, 'steel', 'Les Pokémon de type Acier est contre les Pokémon de type Glace, Roche et Fée.')
]
sql = '''
    INSERT OR IGNORE INTO type (id_type, nom_type, description)
    VALUES (?, ?, ?)
'''
cursor.executemany(sql, types_en)
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
    types_du_pokemon = tuple(pokemon_info['types'])

    cursor.execute(f"SELECT id_type FROM type WHERE nom_type IN ({','.join('?' * len(types_du_pokemon))})", types_du_pokemon)
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

    cursor.execute("SELECT nom, taille, categorie, poids, image_path, pv, attaque, defense, attaque_speciale, defense_speciale, vitesse\
                    FROM mypokemons")

    conn.commit()
    pokemons = cursor.fetchall()
    conn.close()
    return pokemons


# Fonction pour lister un Pokémon
def lister_un_pokemon(pokemon_name):
    conn = sqlite3.connect('pokedex.db')
    cursor = conn.cursor()

    # Utilisation de paramètres de requête pour éviter l'injection SQL
    cursor.execute("SELECT nom, taille, categorie, poids, image_path, pv, attaque, defense, attaque_speciale, defense_speciale, vitesse\
                    FROM mypokemons\
                    WHERE nom=?", (pokemon_name,))
    
    pokemon = cursor.fetchall()

    conn.close()
    return pokemon