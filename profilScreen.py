import cv2
import time
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, RiseInTransition
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.animation import Animation
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from database import *
import requests
from io import BytesIO
import numpy as np
from kivy.utils import get_color_from_hex
from kivy.graphics.texture import Texture
from PIL import Image as PILImage
from database import is_pokemon_in_pokedex
from kivy.uix.widget import Widget



class ImageWithBorder(Widget):
    def __init__(self, image_source, **kwargs):
        super().__init__(**kwargs)
        self.image = Image(source=image_source, 
                           allow_stretch=True, 
                           keep_ratio=True,
                           size_hint=(None, None),  
                           size=(70, 70))

        with self.canvas.before:
            Color(0, 1, 0, 0.2)  # Vert opaque
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        self.add_widget(self.image)

    def update_rect(self, *args):
        self.image.pos  = self.pos
        self.image.size = self.size
        self.rect.pos   = self.pos
        self.rect.size  = self.size


# Classe pour la page Profil
class ProfilScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        # Dessiner un rectangle blanc en arrière-plan
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # Blanc opaque
            self.rect = Rectangle(size=Window.size, pos=(0, 0))

        # Ajouter l'image d'en-tête
        self.background_top = Image(source="ressources/imgs/header.png", 
                                    allow_stretch=True, 
                                    keep_ratio=False,
                                    size_hint=(1, None))
        layout.add_widget(self.background_top)
        

      # Créer un ScrollView pour contenir la grille des Pokémons
        self.scroll_view = ScrollView(size_hint=(1, 0.80), pos_hint={'x': 0, 'y': 0.015})
        print(f"ScrollView size: {self.scroll_view.size}")

        # Créer la grille pour afficher les Pokémons
        self.grid = GridLayout(
            cols=5,
            padding=[20, 20, 20, 65],
            spacing=[5, 5],
            size_hint_y=None
        )
        self.grid.bind(minimum_height=self.grid.setter('height'))
        print(f"GridLayout height: {self.grid.height}")


        self.afficher_les_images()


        # Ajouter la grille dans le ScrollView
        self.scroll_view.add_widget(self.grid)
        layout.add_widget(self.scroll_view)


        self.add_widget(layout)



    def afficher_les_images(self):
        self.grid.clear_widgets()
        for i in range(1, 152):
            path = 'ressources/pokemon-center/' + str(i).zfill(3) + '.png'
            print(f"Loading image from: {path}")  # Debugging line
            try:
                box_layout = BoxLayout(size_hint=(None, None), size=(70, 70), orientation='vertical')

                if is_pokemon_in_pokedex(i):
                    print("IN POKEDEX : ", i)
                    # Créer une instance du widget ImageWithBorder pour afficher le carré vert
                    bordered_image = ImageWithBorder(path)
                    bordered_image.size_hint = (None, None)
                    bordered_image.size = (70, 70)
                    box_layout.add_widget(bordered_image) 
                else:
                    # Si le Pokémon n'est pas dans le Pokédex, n'affichez que l'image
                    img = Image(source=path, 
                                allow_stretch=True, 
                                keep_ratio=True,
                                size_hint=(None, None),  
                                size=(70, 70))
                    box_layout.add_widget(img)

                # Ajouter le BoxLayout à la grille
                self.grid.add_widget(box_layout)

                print(f"Image {i} added successfully.")
            except Exception as e:
                print(f"Error loading image {i}: {e}")


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

    
