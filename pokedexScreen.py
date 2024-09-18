import cv2
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, RiseInTransition
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from database import *
import requests
from io import BytesIO
import numpy as np
from PIL import Image as PILImage
from pokemonCell import PokemonCell

from database import *

class PokedexScreen(Screen):
    def __init__(self, pokemon_data=None, **kwargs):
        super(PokedexScreen, self).__init__(**kwargs)
        # Si aucun pokemon_data n'est fourni, utiliser une liste vide par défaut
        if pokemon_data is None:
            pokemon_data = []
        
        layout = FloatLayout()



        # Dessiner un rectangle blanc en arrière-plan
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # Blanc opaque
            self.rect = Rectangle(size=Window.size, pos=(0, 0))

        # Ajouter l'image d'en-tête en haut
        self.header = Image(
            source="ressources/imgs/header.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, None),
            height=150
        )
        layout.add_widget(self.header)

        # Créer un ScrollView pour contenir la grille des Pokémons
        self.scroll_view = ScrollView(size_hint=(1, 0.78), pos_hint={'x': 0, 'y': 0.035})
        
        # Créer la grille pour afficher les Pokémons
        self.grid = GridLayout(
            cols=1,
            padding=[20, 20, 20, 65],
            spacing=[15, 15],
            size_hint_y=None
        )
        self.grid.bind(minimum_height=self.grid.setter('height'))

        if pokemon_data:
            self.load_pokemons(pokemon_data)

        # Ajouter la grille dans le ScrollView
        self.scroll_view.add_widget(self.grid)
        layout.add_widget(self.scroll_view)

        # Ajouter le layout au screen
        self.add_widget(layout)

        # Mettre à jour la taille du rectangle lors du redimensionnement
        Window.bind(on_resize=self.on_window_resize)
    
    def load_pokemons(self, pokemon_data):
        for pokemon in pokemon_data:
            url = pokemon['image_path']

            try:
                # Télécharger l'image
                response = requests.get(url)
                if response.status_code == 200:
                    # Convertir l'image en texture
                    image_data = BytesIO(response.content)
                    pil_image = PILImage.open(image_data).convert('RGBA')
                    pil_image = pil_image.transpose(PILImage.FLIP_TOP_BOTTOM)  # Inverser si nécessaire

                    image_np = np.array(pil_image)

                    # Créer une texture Kivy
                    texture = Texture.create(size=(image_np.shape[1], image_np.shape[0]), colorfmt='rgba')
                    texture.blit_buffer(image_np.flatten(), bufferfmt='ubyte', colorfmt='rgba')

                    # Créer une image Kivy avec la texture
                    pokemon_cell_image = Image(texture=texture, allow_stretch=True, keep_ratio=False, size=(150, 150))
            except Exception as e:
                print(f"Error fetching image: {e}")
                pokemon_cell_image = Image(source='ressources/imgs/hyperball.png', size=(100, 100))

            # Créer la cellule du Pokémon
            pokemon_cell = PokemonCell(
                pokemon,
                on_click_callback=self.show_pokemon_info,
                size_hint=(None, None),
                size=(Window.width - 40, 220)
            )
            pokemon_cell.pokemon_image.texture = pokemon_cell_image.texture  # Affecter la texture à la cellule
            self.grid.add_widget(pokemon_cell)

        # Planifier la mise à jour des positions des cellules après le chargement
        Clock.schedule_once(self.update_cell_positions, 0)

    def update_pokemon_info(self, pokemon_data):
        # Mettre à jour l'affichage avec les nouvelles informations du Pokémon
        self.load_pokemons([pokemon_data])

    def update_cell_positions(self, dt):
        for cell in self.grid.children:
            cell.update_widgets()
    
    def on_window_resize(self, instance, width, height):
        # Ajuster les éléments en fonction de la taille de la fenêtre
        self.header.size = (width, self.header.height)
        self.header.pos = (0, height - self.header.height)

        # Redimensionner les cellules en fonction de la largeur de la fenêtre
        for child in self.grid.children:
            child.size = (width - 40, child.height)

        # Mettre à jour la taille du rectangle de fond
        self.rect.size = (width, height)

    def show_pokemon_info(self, pokemon_data):
        details_page = self.manager.get_screen('pokemon_info')
        details_page.display_pokemon_info(pokemon_data)

        self.manager.transition = RiseInTransition()
        self.manager.current = 'pokemon_info'
