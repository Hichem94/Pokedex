from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image as KivyImage
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import requests
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
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

        # Image pour le Pokémon
        self.pokemon_image = KivyImage(source='', allow_stretch=True, keep_ratio=False, size=(150, 150))

        # Dessiner un rectangle de fond blanc (derrière tout)
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)  # Couleur blanche
            self.bg_rect = Rectangle(size=Window.size, pos=(0, 0))  # Fond blanc

        # Dessiner le rectangle arrondi (toujours derrière les widgets)
        with self.layout.canvas.before:
            self.bg_color = Color(1, 0, 0, 1)  # Couleur de fond par défaut
            self.rect = RoundedRectangle(size=(Window.width - 50, Window.height - 150), pos=(30, 0), radius=[10])

        # Ajouter l'image d'en-tête en haut
        self.header = KivyImage(source="/home/rigolo/Pokedex/ressources/imgs/header.png", allow_stretch=True, keep_ratio=False, size_hint=(1, None), height=150)
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
            image_downloaded = KivyImage(texture=texture, allow_stretch=True, keep_ratio=False, size=(150, 150))
        except Exception as e:
            print(f"Error fetching image: {e}")
            image_downloaded = KivyImage(source='/home/rigolo/Pokedex/ressources/imgs/hyperball.png', size=(50, 50))
        
        return image_downloaded

    def display_pokemon_info(self, pokemon_data):
        # Mettre à jour le fond avec la couleur du type de Pokémon
        self.display_bg(pokemon_data)

        # Télécharger et afficher l'image du Pokémon
        pokemon_img = self.download_image(pokemon_data['image_path'])
        pokemon_img.keep_ratio = True
        pokemon_img.size_hint = (None, None)
        image_size = min(Window.width * 0.6, Window.height * 0.6)  # Taille maximale de l'image
        pokemon_img.size = (image_size, image_size)
        pokemon_img.pos_hint = {'center_x': 0.5, 'top': 1}
        self.scroll_layout.add_widget(pokemon_img)

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

        self.make_diagram(pokemon_data)

    def on_window_resize(self, instance, width, height):
        # Ajuster les éléments en fonction de la taille de la fenêtre
        if hasattr(self, 'header'):
            self.header.size = (width, self.header.height)
            self.header.pos = (0, height - self.header.height)

        if hasattr(self, 'bg_rect'):
            # Mettre à jour la taille du rectangle blanc qui prend tout l'écran
            self.bg_rect.size = (width, height)

        if hasattr(self, 'rect'):
            # Mettre à jour la taille et la position du rectangle arrondi
            self.rect.size = (width - 50, height - 150)
            self.rect.pos = ((width - self.rect.size[0]) / 2, 0)

        if hasattr(self, 'image'):
            # Mettre à jour la taille et la position de l'image
            image_size = min(width * 0.6, height * 0.6)  # Taille maximale de l'image en fonction de la taille de la fenêtre
            self.image.size = (image_size, image_size)
            self.image.pos = ((width - image_size) / 2, height - image_size - 20)  # Ajuster la position de l'image


    def make_diagram(self, pokemon_data):

        # Dans la méthode make_diagram
        with self.canvas.before:
            Color(1, 0, 0, 1)  # Couleur rouge pour le cadre
            self.rect = Rectangle(size=(300, 300), pos=(self.x, self.y))

        num_vars = 6
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        values = [pokemon_data['stats']['pv'], pokemon_data['stats']['attaque'], pokemon_data['stats']['defense'],
                pokemon_data['stats']['attaque_speciale'], pokemon_data['stats']['defense_speciale'], pokemon_data['stats']['vitesse']]
        values += values[:1]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.fill(angles, values, color='blue', alpha=0.25)
        ax.plot(angles, values, color='blue', linewidth=2)
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(['PV', 'ATT', 'DEF', 'ATT SPE', 'DEF SPE', 'VIT'])

        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)

        # Charger l'image depuis le buffer
        try:
            img = CoreImage(buf, ext='png')
            img_texture = img.texture
        except Exception as e:
            print(f"Erreur lors de la création de la texture : {e}")
            return

        if img_texture is None:
            print("Erreur : la texture est None.")
            return

        # Créer un widget Image avec la texture
        diagram_image = KivyImage(texture=img_texture, allow_stretch=True, keep_ratio=False, size=(300, 300))
        self.scroll_layout.add_widget(diagram_image)



    def on_leave(self, *args):
        # Vider le BoxLayout quand la page est quittée
        self.scroll_layout.clear_widgets()
