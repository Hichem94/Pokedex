from model import *
import model
from pokemon import Pokemon
from api_pokemon import get_pokemon_info
from database import ajouter_pokemon, lister_tous_les_pokemons, lister_un_pokemon


# Construire une instance de Pokemon
def make_pokemon(pokemon_info):
    nom       = pokemon_info['nom']
    taille    = pokemon_info['taille']
    categorie = pokemon_info['categorie']
    poids     = pokemon_info['poids']
    stats     = pokemon_info['stats']
    image_path= pokemon_info['image_path']

    pokemon = Pokemon(nom, taille, categorie, poids, stats, image_path)

    return pokemon


def load_model(model_path):
    # Entrainer le modèle
    #model = model_training()

    #Charger le modèle
    #"/home/rigolo/Pokedex/app/pokedex.keras"
    try:
        model = load_model(model_path)
        #model.summary()
        return model
    except Exception as e:
        print("Erreur lors du chargement du modèle:", e)
        return None
    

# # Prediction
# pokemon_predict = make_prediction(model, sys.argv[1])

# # Get pokemon info
# pokemon_info = get_pokemon_info(pokemon_predict)

# # Ajouter le pokemon dans la base
# ajouter_pokemon(pokemon_info)


# # Make pokemon
# pokemon = make_pokemon(pokemon_info)
# # Afficher
# pokemon.toString()
