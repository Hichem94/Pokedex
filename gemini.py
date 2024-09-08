import google.generativeai as genai
import os
import ast
from pokemon import Pokemon


class Gemini():

    def __init__(self):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    
    def get_info(self, prediction):
        # Demande d'informations sur le pokemon
        request  = "Je veux le nom en français, la taille, la catégorie, le poids, le type et les stats de base de ce pokemon : " + prediction
        request += ". Une réponse sous forme de dictionnaire python avec les clés taille, categorie, poids, type, stats_de_base."
        request += "Les stats_de_base seront également au format dictionnaire python avec les clés pv, attaque, defense, attaque_speciale, defense_speciale, vitesse"
        request += "Je veux seulement le dictionnaire, rien autour. N'oublis pas le nom du pokemon"
        response = self.model.generate_content(request)
        
        # Pour la convertiion en dictionnaire python
        res = response.text.split("```python")[1]
        res = res.split("```")[0]

        return ast.literal_eval(res)
        