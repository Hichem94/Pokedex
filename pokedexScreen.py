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

from database import lister_tous_les_pokemons

class PokedexScreen(Screen):
    def __init__(self, **kwargs):
        super(PokedexScreen, self).__init__(**kwargs)
        
        layout = FloatLayout()

        # Dessiner un rectangle blanc en arrière-plan
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # Blanc opaque
            self.rect = Rectangle(size=Window.size, pos=(0, 0))

        # Ajouter l'image d'en-tête en haut
        self.background_top = Image(source="ressources/imgs/header.png", 
                                    allow_stretch=True, 
                                    keep_ratio=False,
                                    size_hint=(1, None))
        layout.add_widget(self.background_top)
        
        # Créer un ScrollView pour contenir la grille des Pokémons
        self.scroll_view = ScrollView(size_hint=(1, 0.78), pos_hint={'x': 0, 'y': 0.035})
        
        # Créer la grille pour afficher les Pokémons
        self.grid = GridLayout(
            cols=2,
            padding=[20, 20, 20, 20],
            spacing=[15, 15],
            size_hint_y=None
        )
        self.grid.bind(minimum_height=self.grid.setter('height'))


        self.load_pokemons()

        # Ajouter la grille dans le ScrollView
        self.scroll_view.add_widget(self.grid)
        layout.add_widget(self.scroll_view)

        # Ajouter le layout au screen
        self.add_widget(layout)

        # # Assurer que la mise à jour du header est effectuée après la création des widgets
        # Window.bind(on_resize=self.on_window_resize)
        # Clock.schedule_once(self.update_header, 0)


    def update_header_position(self):
        if self.background_top:
            self.background_top.size = (self.width, self.background_top.texture_size[1])
            self.background_top.pos = (0, self.height - self.background_top.height)

        if self.rect:
            self.rect.size = (self.width, self.height)
        
    def on_size(self, *args):
        self.update_header_position()

    def on_texture(self, *args):
        self.update_header_position()


    def get_next_cell_position(self):
        # Compte le nombre actuel de cellules
        current_cell_count = len(self.grid.children)
        
        # Détermine la ligne et la colonne pour la prochaine cellule
        row = current_cell_count // self.grid.cols
        col = current_cell_count % self.grid.cols
        
        # Calcule les dimensions des cellules
        cell_width = self.grid.width / self.grid.cols
        cell_height = (self.grid.height - (self.grid.padding[1] + self.grid.padding[3]) - (self.grid.spacing[1] * (self.grid.cols - 1))) / ((current_cell_count // self.grid.cols) + 1)
        
        # Calcule les positions en pixels
        x_position = col * (cell_width + self.grid.spacing[0]) + self.grid.padding[0]
        y_position = (self.grid.height - self.grid.padding[1]) - ((row + 1) * cell_height + row * self.grid.spacing[1])
        
        # Retourne les coordonnées en colonne, ligne et position en pixels
        return col, row, (x_position, y_position)



    def load_pokemons(self): 
        # Vider la grille avant de la remplir
        self.grid.clear_widgets()

        pokemons = lister_tous_les_pokemons()
        print("######## POKEMON LOAD : ")
        print(pokemons)
        for pokemon in reversed(pokemons):
            print(pokemon)
            print('\n')
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

            # Calculer la position de la prochaine cellule
            row, col, pos = self.get_next_cell_position()

            # Créer la cellule du Pokémon
            pokemon_cell = PokemonCell(
                pokemon,
                on_click_callback=self.show_pokemon_info,
                position_in_grid=(row, col, pos),
                size_hint=(None, None),
                size=(Window.width/4.5, 100)
            )
            pokemon_cell.pokemon_image.texture = pokemon_cell_image.texture  # Affecter la texture à la cellule
            self.grid.add_widget(pokemon_cell)

        # Planifier la mise à jour des positions des cellules après le chargement
        Clock.schedule_once(self.update_cell_positions, 0)


    def update_cell_positions(self, dt):
        for cell in self.grid.children:
            cell.update_widgets()
    
    def show_pokemon_info(self, pokemon_data):
        details_page = self.manager.get_screen('pokemon_info')
        details_page.display_pokemon_info(pokemon_data)
    
        self.manager.transition = RiseInTransition()
        self.manager.current = 'pokemon_info'
