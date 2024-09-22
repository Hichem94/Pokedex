from model import *
import model as m
from pokemon import Pokemon
from api_pokemon import get_pokemon_info
from database import ajouter_pokemon, lister_tous_les_pokemons, lister_un_pokemon
from keras.models import load_model as keras_load_model

def load_model(filepath):
    try:
        model = keras_load_model(filepath)
        print(f"Modèle chargé avec succès à partir de {filepath}.")
        return model
    except Exception as e:
        print(f"Erreur lors du chargement du modèle : {e}")
        return None


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


def charge_model(model_path):
    # Entrainer le modèle
    #model = model_training()

    #Charger le modèle
    #"/home/rigolo/Pokedex/app/pokedex.keras"
    try:
        modele = keras_load_model(model_path)
        #model.summary()
        print('Modele chargé.')
        return modele
    except Exception as e:
        print("Erreur lors du chargement du modèle:", e)
        return None

#model_training()

#modele = load_model('pokedex.keras')

# # Prediction
#pokemon_predict = make_prediction(modele, 'dataset/Arcanine/0af612d6c81c4cf8bb346df0d1ee02ea.jpg')
#print("POKEMON PREDICTED : ", pokemon_predict)

# # Get pokemon infoz
# pokemon_info = get_pokemon_info(pokemon_predict)

# # Ajouter le pokemon dans la base
# ajouter_pokemon(pokemon_info)


# # Make pokemon
# pokemon = make_pokemon(pokemon_info)
# # Afficher
# pokemon.toString()
