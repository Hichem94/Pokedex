import requests


def get_pokemon_info(name):
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        response = requests.get(url)
        response.raise_for_status()  # Lève une exception si le statut HTTP n'est pas 2xx

        data = response.json()

    # Extraire les informations souhaitées
        nom = data['name']
        taille = data['height']
        poids = data['weight']
        categorie = data['species']['name']
        types = [type_info['type']['name'] for type_info in data['types']]
        image_path = data['sprites']['front_default']  # URL de l'image

        stats = data['stats']
        pv = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'hp')
        attaque = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'attack')
        defense = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'defense')
        attaque_speciale = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'special-attack')
        defense_speciale = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'special-defense')
        vitesse = next(stat['base_stat'] for stat in stats if stat['stat']['name'] == 'speed')

        stats_b = {
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
            'pv': pv,
            'stats': stats_b
        }
        return pokemon_info

    except:
        print('No pokemon with name {name}')
        return None


pikachu_info = get_pokemon_info('pikachu')
print(pikachu_info)