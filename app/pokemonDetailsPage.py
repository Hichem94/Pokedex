from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import requests
from io import BytesIO
import numpy as np
from PIL import Image as PILImage
from kivy.utils import get_color_from_hex


# Import de mes fichiers
from type_colors import TYPE_COLORS
from database import *


class PokemonDetailsPage(Screen):
    def __init__(self, **kwargs):
        super(PokemonDetailsPage, self).__init__(**kwargs)

        # Créer un FloatLayout pour l'ensemble de la page
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        self.image = Image(source='', allow_stretch=True, keep_ratio=False, size=(150, 150))

        # Dessiner un rectangle de fond blanc (derrière tout)
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)  # Couleur blanche
            self.bg_rect = Rectangle(size=Window.size, pos=(0, 0))  # Fond blanc

        # Dessiner le rectangle arrondi (toujours derrière les widgets)
        with self.layout.canvas.before:
            self.bg_color = Color(1, 0, 0, 1)  # Couleur de fond par défaut
            self.rect = RoundedRectangle(size=(Window.width - 50, Window.height - 150), pos=(30, 0), radius=[10])

        # Ajouter l'image d'en-tête en haut
        self.header = Image(source="ressources/imgs/header.png", allow_stretch=True, keep_ratio=False, size_hint=(1, None), height=150)
        self.layout.add_widget(self.header)

        # Créer une ScrollView
        self.scroll_view = ScrollView(size_hint=(1, 0.8), pos_hint={'x': 0, 'y': 0.05})
        self.layout.add_widget(self.scroll_view)

        # Créer un BoxLayout pour contenir les éléments dans la ScrollView
        self.scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))

        # Ajouter le BoxLayout à la ScrollView
        self.scroll_view.add_widget(self.scroll_layout)

        # Mettre à jour la taille du rectangle lors du redimensionnement
        Window.bind(on_resize=self.on_window_resize)

    def display_bg(self, pokemon_data):
        # Couleur de fond basée sur le type de Pokémon
        pokemon_type = pokemon_data['types'][0] if isinstance(pokemon_data['types'], list) else pokemon_data['types']
        bg_color_hex = TYPE_COLORS.get(pokemon_type, '#FFFFFF')  # Utiliser une couleur par défaut
        self.bg_color.rgba = get_color_from_hex(bg_color_hex)  # Mettre à jour la couleur du fond arrondi
    
    def download_image(self, url):
        try:
            # Télécharger l'image
            response = requests.get(url)
            # Convertir l'image en texture
            image_data = BytesIO(response.content)
            pil_image = PILImage.open(image_data).convert('RGBA')
            pil_image = pil_image.transpose(PILImage.FLIP_TOP_BOTTOM)  # Inverser si nécessaire

            image_np = np.array(pil_image)

            # Créer une texture Kivy
            texture = Texture.create(size=(image_np.shape[1], image_np.shape[0]), colorfmt='rgba')
            texture.blit_buffer(image_np.flatten(), bufferfmt='ubyte', colorfmt='rgba')

            # Créer une image Kivy avec la texture
            image_downloaded = Image(texture=texture, allow_stretch=True, keep_ratio=False, size=(150, 150))
            image_downloaded.texture = image_downloaded.texture  # Affecter la texture à la cellule
        except Exception as e:
            print(f"Error fetching image: {e}")
            image_downloaded = Image(source='ressources/imgs/hyperball.png', size=(50, 50))
        

        return image_downloaded

    def display_pokemon_info(self, pokemon_data):
        # Mettre à jour le fond avec la couleur du type de Pokémon
        self.display_bg(pokemon_data)

        # Télécharger et afficher l'image du Pokémon
        self.image = self.download_image(pokemon_data['image_path'])
        self.image.keep_ratio = True
        self.image.size_hint = (None, None)
        self.image.size = (350, 350)
        self.image.pos_hint = {'center_x': 0.5, 'top': 1}
        self.scroll_layout.add_widget(self.image)

        # Ajouter un label avec le nom du Pokémon dans le scroll_layout
        self.name_label = Label(
            text=pokemon_data['nom'].upper(),
            size_hint=(0.2, None),
            height=50,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.3}
        )
        self.scroll_layout.add_widget(self.name_label)

        # Ajouter un autre label pour les statistiques
        self.stats_label = Label(
            text="Statistiques",
            size_hint=(0.2, None),
            height=50,
            color=(1, 1, 1, 1)
        )
        self.scroll_layout.add_widget(self.stats_label)

    def on_window_resize(self, instance, width, height):
        # Ajuster les éléments en fonction de la taille de la fenêtre
        self.header.size = (width, self.header.height)
        self.header.pos = (0, height - self.header.height)

        # Mettre à jour la taille du rectangle blanc et du rectangle arrondi
        self.bg_rect.size = (width, height)  # Fond blanc qui prend tout l'écran
        self.rect.size = (width - 50, height - 150)
        self.rect.pos = ((width - self.rect.size[0]) / 2, 0)

        # Mettre à jour la position et la taille de l'image
        self.image.size = (350, 350)
        self.image.pos_hint = {'center_x': 0.5, 'top': 1}


    def on_leave(self, *args):
        # Vider le BoxLayout quand la page est quittée
        self.scroll_layout.clear_widgets()
