from model import *
from gemini import *

if __name__ == "__main__":

    # Entrainer le modèle
    #model = model_training()

    #Charger le modèle complet
    try:
        model = load_model("pokedex.keras")
        #model.summary()
    except Exception as e:
        print("Erreur lors du chargement du modèle:", e)

    # # Prediction
    for picture_path in sys.argv[1:]: make_prediction(model, img_path = picture_path)

