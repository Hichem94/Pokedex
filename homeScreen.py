from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from database import *



# Classe pour l'écran d'accueil
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Ajouter l'image de fond
        self.background_down = Image(source="ressources/imgs/login-bg.jpg", allow_stretch=True, keep_ratio=False,
                                     size_hint=(1, 1))
        layout.add_widget(self.background_down)

        # Ajouter l'image d'en-tête
        self.background_top = Image(source="ressources/imgs/header.png", 
                                    allow_stretch=True, 
                                    keep_ratio=False,
                                    size_hint=(1, None))
        layout.add_widget(self.background_top)

        self.background_pokedex_font = Image(source="ressources/imgs/pokedex_font.png", allow_stretch=True, keep_ratio=False,
                                     size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(self.background_pokedex_font)
        
        self.background_starters_img = Image(source="ressources/imgs/starters.png", allow_stretch=True, keep_ratio=False,
                                     size_hint=(0.7, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.55})
        layout.add_widget(self.background_starters_img)

        self.add_widget(layout)

    def update_header_position(self):
        if self.background_top:
            self.background_top.size = (self.width, self.background_top.texture_size[1])
            self.background_top.pos = (0, self.height - self.background_top.height)

    def on_size(self, *args):
        self.update_header_position()

    def on_texture(self, *args):
        self.update_header_position()
