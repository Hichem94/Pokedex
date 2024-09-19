from keras.models import load_model

try:
    model = load_model("pokedex.keras")
    print("Modèle chargé avec succès.")
except Exception as e:
    print(f"Erreur lors du chargement du modèle : {e}")
