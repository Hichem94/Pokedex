from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.graphics.texture import Texture
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex
from kivy.uix.label import Label
import requests
from io import BytesIO
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image as PILImage
from musicWidget import MusicWidget

# Import de mes fichiers
from type_colors import TYPE_COLORS
from musicWidget import MusicWidget

class PokemonDetailsPage(Screen):
    def __init__(self, **kwargs):
        super(PokemonDetailsPage, self).__init__(**kwargs)

        # Créer un FloatLayout pour l'ensemble de la page
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Dessiner un rectangle de fond blanc (derrière tout)
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)  # Couleur blanche
            self.bg_rect = Rectangle(size=Window.size, pos=(0, 0))  # Fond blanc

        # Dessiner le rectangle arrondi (toujours derrière les widgets)
        with self.layout.canvas.before:
            self.bg_color = Color(1, 0, 0, 1)  # Couleur de fond par défaut
            self.rect = RoundedRectangle(size=(Window.width - 50, Window.height - 150), pos=(30, 0), radius=[10])

        # Ajouter l'image d'en-tête en haut
        self.background_top = Image(source="ressources/imgs/header.png", 
                                    allow_stretch=True, 
                                    keep_ratio=False,
                                    size_hint=(1, None))
        self.layout.add_widget(self.background_top)

        # Créer une ScrollView
        self.scroll_view = ScrollView(size_hint=(1, 0.8), pos_hint={'x': 0, 'y': 0.1})
        self.layout.add_widget(self.scroll_view)

        # Créer un BoxLayout pour contenir les éléments dans la ScrollView
        self.scroll_layout = BoxLayout(orientation='vertical', padding=0, spacing=20, size_hint_y=None)
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
        except Exception as e:
            print(f"Error fetching image: {e}")
            image_downloaded = Image(source='ressources/imgs/hyperball.png', size=(50, 50))
        
        return image_downloaded

    def make_diagram(self, pokemon_data):
        # Création du diagramme radar
        num_vars = 6
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        values = [
            pokemon_data['stats']['pv'], pokemon_data['stats']['attaque'], 
            pokemon_data['stats']['defense'], pokemon_data['stats']['attaque_speciale'], 
            pokemon_data['stats']['defense_speciale'], pokemon_data['stats']['vitesse']
        ]
        values += values[:1]
        angles += angles[:1]

        # Création de la figure
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.fill(angles, values, color='blue', alpha=0.25)
        ax.plot(angles, values, color='blue', linewidth=2)
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(['PV', 'ATT', 'DEF', 'ATT SPE', 'DEF SPE', 'VIT'])

        # Sauvegarde de la figure dans un fichier sur disque
        image_path = "/diagramme_pokemon.png"
        plt.savefig(image_path, format='png', bbox_inches='tight')
        plt.close(fig)

        print(f"Diagramme sauvegardé à {image_path}")

        # Vérifier que le fichier a bien été créé
        if not os.path.exists(image_path):
            print(f"Erreur : le fichier {image_path} n'existe pas.")
            return

        # Charger l'image depuis le fichier
        try:
            # Créer un widget Image avec la texture
            self.diagram_image = Image(source=image_path, allow_stretch=False, keep_ratio=False, size=(300, 300))
            print(f"Diagramme chargé avec succès : {image_path}")
        except Exception as e:
            print(f"Erreur lors du chargement de l'image : {e}")
            return

    def display_pokemon_info(self, pokemon_data):
        # Mettre à jour le fond avec la couleur du type de Pokémon
        self.display_bg(pokemon_data)

        # # Ajouter le diagramme après les autres widgets
        # if hasattr(self, 'diagram_image'):
        #     self.scroll_layout.add_widget(self.diagram_image)

        # Télécharger et afficher l'image du Pokémon
        self.pokemon_img = self.download_image(pokemon_data['image_path'])
        self.pokemon_img.keep_ratio = True
        self.pokemon_img.size_hint = (None, None)
        image_size = min(Window.width * 0.6, Window.height * 0.6)  # Taille maximale de l'image
        self.pokemon_img.size = (image_size, image_size)
        self.pokemon_img.pos_hint = {'center_x': 0.5, 'top': 1}
        self.scroll_layout.add_widget(self.pokemon_img)

        # Créer et ajouter le label nom
        self.name_label = Label(
            text=pokemon_data['nom'].upper(),
            font_size=30,
            color=(1, 1, 1, 1),
            font_name='ressources/fonts/police.ttf',
            size_hint=(None, None),  # Désactive la taille automatique
            size=(self.scroll_layout.width * 0.8, self.scroll_layout.height * 0.2),  # Ajustez la largeur et la hauteur du label
            pos_hint={'center_x': 0.5, 'center_y': 0.4},  # Centre le label
            bold=True
        )
        self.scroll_layout.add_widget(self.name_label)

        # Crie du pokemon
        self.pokemon_cry = MusicWidget(pokemon_data['pokedex_number'])
        self.scroll_layout.add_widget(self.pokemon_cry)

    def update_header_position(self):
        if self.background_top:
            self.background_top.size = (self.width, self.background_top.texture_size[1])
            self.background_top.pos = (0, self.height - self.background_top.height)
        
        if self.bg_rect:
            self.bg_rect.size = (self.width, self.height)
        
        if self.rect:
            self.rect.size = (Window.width - 50, Window.height - 150)

        if self.pokemon_img:
            image_size = min(Window.width * 0.6, Window.height * 0.6)
            self.pokemon_img.size = (image_size, image_size)



    def on_size(self, *args):
        self.update_header_position()

    def on_texture(self, *args):
        self.update_header_position()


    def on_window_resize(self, instance, width, height):
        # Ajuster les éléments en fonction de la taille de la fenêtre

        if hasattr(self, 'bg_rect'):
            self.bg_rect.size = (width, height)

        if hasattr(self, 'rect'):
            self.rect.size = (width - 50, height - 150)
            self.rect.pos = ((width - self.rect.size[0]) / 2, 0)

        if hasattr(self, 'diagram_image'):
            self.diagram_image.size = (width * 0.8, width * 0.8)
            self.diagram_image.pos = ((width - self.diagram_image.size[0]) / 2, height - self.diagram_image.size[1] - 80)

        if hasattr(self, 'audio_slider'):
            # Ajuster la taille et la position du slider audio
            self.audio_slider.size = (width / 2.5, 40)  # Ajuster la taille du slider
            self.audio_slider.pos = (width / 2 - self.audio_slider.size[0] / 2, height * 0.1)  # Ajuster la position du slider

        if hasattr(self, 'play_button'):
            # Ajuster la position du bouton play/pause
            self.play_button.size = (100, 50)
            self.play_button.pos = (width / 2 - self.play_button.size[0] / 2, height * 0.05)  # Ajuster la position du bouton

        if hasattr(self, 'name_label'):
                # Ajuster la taille et la position du label nom
                self.name_label.size = (width * 0.8, height * 0.2)  # Ajuster la largeur et la hauteur du label
                self.name_label.pos = (width * 0.1, height * 0.7)  # Ajuster la position du label

    def on_leave(self, *args):
        # Vider le BoxLayout quand la page est quittée
        self.scroll_layout.clear_widgets()
