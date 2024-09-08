from model import *
from gemini import Gemini
from pokemon import Pokemon
import ast


def make_pokemon(pokemon_info):
    nom       = pokemon_info['nom']
    taille    = pokemon_info['taille']
    categorie = pokemon_info['categorie']
    poids     = pokemon_info['poids']
    type      = pokemon_info['type']
    stats     = pokemon_info['stats_de_base']

    pokemon = Pokemon(nom, taille, categorie, poids, type, stats)

    return pokemon


if __name__ == "__main__":

    # Entrainer le modèle
    #model = model_training()

    #Charger le modèle
    try:
        model = load_model("pokedex.keras")
        #model.summary()
    except Exception as e:
        print("Erreur lors du chargement du modèle:", e)


    gemini  = Gemini()

    # Prediction
    pokemon_predict = make_prediction(model, sys.argv[1])
    
    # Get pokemon info
    pokemon_info = gemini.get_info(pokemon_predict)

    # Make pokemon
    pokemon = make_pokemon(pokemon_info)

    # Afficher
    pokemon.toString()
