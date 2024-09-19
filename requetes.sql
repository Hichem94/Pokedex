SELECT nom, taille, categorie, poids, image_path, pv, attaque, defense, attaque_speciale, defense_speciale, vitesse, nom_type
FROM mypokemons, pokemon_type, type
WHERE mypokemons.id = pokemon_type.id_pokemon
AND type.id_type = pokemon_type.id_type