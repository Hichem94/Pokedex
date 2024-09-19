SELECT 
    mypokemons.nom, 
    mypokemons.taille, 
    mypokemons.categorie, 
    mypokemons.poids, 
    mypokemons.image_path, 
    mypokemons.pv, 
    mypokemons.attaque, 
    mypokemons.defense, 
    mypokemons.attaque_speciale, 
    mypokemons.defense_speciale, 
    mypokemons.vitesse, 
    GROUP_CONCAT(type.nom_type, ', ') AS types
FROM 
    mypokemons
JOIN 
    pokemon_type ON mypokemons.nom = pokemon_type.id_pokemon
JOIN 
    type ON pokemon_type.id_type = type.id_type
GROUP BY 
    mypokemons.nom, 
    mypokemons.taille, 
    mypokemons.categorie, 
    mypokemons.poids, 
    mypokemons.image_path, 
    mypokemons.pv, 
    mypokemons.attaque, 
    mypokemons.defense, 
    mypokemons.attaque_speciale, 
    mypokemons.defense_speciale, 
    mypokemons.vitesse;
