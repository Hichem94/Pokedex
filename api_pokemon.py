import requests


def get_pokemon_info(name):
    try:
        url = "https://pokeapi.co/api/v2/pokemon/" + str(name).lower() + "/"
        response = requests.get(url)
        response.raise_for_status()  # Lève une exception si le statut HTTP n'est pas 2xx

        data = response.json()

    # Extraire les informations souhaitées
        nom = data['name']
        taille = data['height']
        poids = data['weight']
        #Pour la catégorie
        response2 = requests.get(data['species']['url'])
        if response2.status_code == 200:
            data2 = response2.json()
            # Parcourir les genera pour trouver la catégorie en français
            for genera in data2['genera']:
                if genera['language']['name'] == 'fr':
                    categorie = genera['genus']
        else:
            categorie = "No info"
        types = [type_info['type']['name'] for type_info in data['types']]
        image_path = "https://img.pokemondb.net/sprites/scarlet-violet/normal/" + str(name) + ".png"
        stats = data['stats']
        pv = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'hp')
        attaque = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'attack')
        defense = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'defense')
        attaque_speciale = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'special-attack')
        defense_speciale = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'special-defense')
        vitesse = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'speed')

        stats_b = {
            'pv': pv,
            'attaque': attaque,
            'defense': defense,
            'attaque_speciale': attaque_speciale,
            'defense_speciale': defense_speciale,
            'vitesse': vitesse
        }

        pokemon_info = {
            'nom': nom,
            'taille': taille,
            'poids': poids,
            'categorie': categorie,
            'types': types,
            'image_path': image_path,
            'stats': stats_b
        }
        print("############### POKEMON_INFO ####################\n")
        print("\n")
        print(pokemon_info)
        return pokemon_info

    except:
        print('No pokemon with name {name}')
        return None


# pikachu_info = get_pokemon_info('gloom')
# print(pikachu_info)
# https://img.pokemondb.net/sprites/scarlet-violet/normal/bulbasaur.png