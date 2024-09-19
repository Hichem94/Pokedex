import cv2
import tempfile
import os
import time
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, NoTransition, RiseInTransition, FadeTransition
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.gridlayout import GridLayout
from roundButton import RoundButton


# Import de mes fichiers
from homeScreen import HomeScreen
from cameraScreen import CameraScreen
from pokedexScreen import PokedexScreen
from pokedexScreen import PokedexScreen
from pokemonDetailsPage import PokemonDetailsPage
from profilScreen import ProfilScreen
from api_pokemon import get_pokemon_info
from prediction_utils import make_prediction, charge_model
from database import *









class MainApp(App):
    def build(self):
        self.sm = ScreenManager()

        # Dictionnaire pour stocker les informations du Pokémon
        self.pokemon_data = {}

        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(CameraScreen(name='camera'))
        self.sm.add_widget(PokedexScreen(name='pokedex'))
        self.sm.add_widget(ProfilScreen(name='profil'))
        self.sm.add_widget(PokemonDetailsPage(name='pokemon_info'))

        layout = FloatLayout()

        layout.add_widget(self.sm)

        # Créer la barre de navigation avec GridLayout
        nav_bar = GridLayout(cols=4,  # Nombre de colonnes égal au nombre de boutons
                            size_hint=(1, None),
                            height=80,  # Hauteur de la barre de navigation
                            padding=[10, 10],  # Espacement interne
                            spacing=45)  # Espacement entre les boutons

        with nav_bar.canvas.before:
            Color(1, 1, 1, 1)  # Couleur de fond blanche
            self.rect = Rectangle(size=(Window.width, nav_bar.height), pos=(0, 0))  # Rectangle de la nav bar

            # Ombre au-dessus de la barre de navigation
            Color(0, 0, 0, 0.3)
            self.shadow = Rectangle(size=(Window.width, 5), pos=(0, nav_bar.height))  # Ombre au-dessus

        # Lier la taille du rectangle à la taille de la nav_bar
        nav_bar.bind(size=lambda instance, value: setattr(self.rect, 'size', (Window.width, nav_bar.height)))
        
        # Mise à jour de la taille du rectangle et de l'ombre lorsque la fenêtre change
        def update_rect(instance, value):
            self.rect.size = (Window.width, nav_bar.height)  # Mettre à jour la taille du rectangle blanc
            self.shadow.size = (Window.width, 5)             # L'ombre garde toujours la même hauteur
            self.shadow.pos = (0, nav_bar.height)            # Placer l'ombre juste au-dessus de la barre de navigation

        nav_bar.bind(size=update_rect)

        # Création des boutons de la nav_bar avec size_hint pour ajuster automatiquement
        button_size = (60, 60)  # Taille des boutons

        # Création des boutons de la nav_bar
        self.home_button = RoundButton(image_source="ressources/imgs/accueil.png", size_hint=(None, None), size=button_size)
        self.home_button.bind(on_press=lambda x: self.switch_screen(self.sm, 'home'))

        self.camera_button = RoundButton(image_source="ressources/imgs/camera-icon.png", size_hint=(None, None), size=button_size)
        self.camera_button.bind(on_press=lambda x: self.switch_screen(self.sm, 'camera'))

        self.pokedex_button = RoundButton(image_source="ressources/imgs/pokeball.png", size_hint=(None, None), size=button_size)
        self.pokedex_button.bind(on_press=lambda x: self.switch_screen(self.sm, 'pokedex'))

        self.profil_button = RoundButton(image_source="ressources/imgs/profil.png", size_hint=(None, None), size=button_size)
        self.profil_button.bind(on_press=lambda x: self.switch_screen(self.sm, 'profil'))

        # Ajouter les boutons à la nav_bar
        nav_bar.add_widget(self.home_button)
        nav_bar.add_widget(self.camera_button)
        nav_bar.add_widget(self.pokedex_button)
        nav_bar.add_widget(self.profil_button)

        # Ajouter la nav_bar au layout principal
        layout.add_widget(nav_bar)

        # Ajouter un bouton global visible sur toutes les pages. Il permettra de prendre une photo sur la page camera
        self.capture_button = RoundButton(image_source="ressources/imgs/button_image.png", size=(100, 100))
        self.capture_button.pos_hint = {'center_x': 0.5, 'center_y': 0.12}  # Positionner au centre en bas
        self.capture_button.bind(on_press=self.capture_photo)

        layout.add_widget(self.capture_button)

        # Initialiser la visibilité du bouton
        self.sm.bind(current=self.update_button_visibility)

        # Sélectionner par défaut la page d'accueil
        self.switch_screen(self.sm, 'home')

        return layout

    def switch_screen(self, sm, screen_name):
        sm.transition = NoTransition()  # Suppression des transitions
        sm.current = screen_name

    
    def capture_photo(self, instance=None):
        if self.sm.current == 'camera':
            camera_screen = self.sm.get_screen('camera')
            ret, self.frame = camera_screen.capture.read()
            if ret:
                # Charger le modèle
                self.model = charge_model("pokedex.keras")
                
                if self.model is None:
                    print("Erreur : Le modèle n'a pas pu être chargé.")
                    return
                
                # Sauvegarder l'image temporairement
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                    img_path = temp_file.name
                    cv2.imwrite(img_path, self.frame)
                    print("Image temporaire sauvegardée.")
                    
                # Effectuer la prédiction
                pokemon_predicted = make_prediction(self.model, img_path)
                if pokemon_predicted is None:
                    print("Erreur lors de la prédiction.")
                    os.remove(img_path)
                    return
                
                # Récupérer les informations sur le Pokémon
                self.pokemon_info = get_pokemon_info(pokemon_predicted)
                if self.pokemon_info is None:
                    print("Erreur lors de la récupération des informations sur le Pokémon.")
                    os.remove(img_path)
                    return
                
                ajouter_pokemon(self.pokemon_info)
                
                print("Informations sur le Pokémon récupérées.")
                
                # Supprimer le fichier temporaire après utilisation
                os.remove(img_path)
                
                # Créer un nom de fichier avec un timestamp
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"photo_{timestamp}.png"
                cv2.imwrite(filename, self.frame)
                print(f"Photo sauvegardée sous {filename}")

                # Accéder à l'écran Pokedex et lui transmettre les infos du Pokémon
                pokedex_screen = self.sm.get_screen('pokedex')
                pokedex_screen.update_pokemon_info(self.pokemon_info)

                # Passer à l'écran Pokedex
                self.switch_screen(self.sm, 'pokedex')



    def update_button_visibility(self, instance, value):
        if self.sm.current == 'camera':
            anim = Animation(opacity=1, duration=0.5)
            anim.start(self.capture_button)
            self.capture_button.disabled = False
        else:
            anim = Animation(opacity=0.5, duration=0.5)
            anim.start(self.capture_button)
            self.capture_button.disabled = True

if __name__ == '__main__':
    Window.size = (400, 700)  # Taille de la fenêtre
    MainApp().run()

