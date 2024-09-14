import cv2
import time
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, NoTransition, RiseInTransition
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.animation import Animation



# Import de mes fichiers
from homeScreen import HomeScreen
from cameraScreen import CameraScreen
from pokedexScreen import PokedexScreen
from pokedexScreen import PokedexScreen
from pokemonDetailsPage import PokemonDetailsPage
from profilScreen import ProfilScreen
from database import *



# Classe pour le bouton rond avec une image personnalisée
class RoundButton(Button):
    source = StringProperty('')

    def __init__(self, image_source, **kwargs):
        super().__init__(**kwargs)
        self.source = image_source
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.size_hint = (None, None)

        # Ajouter l'image comme enfant du bouton
        self.image = Image(source=self.source, size=self.size, pos=self.pos)
        self.add_widget(self.image)

        # Assurer que l'image suit les modifications de position/taille du bouton
        self.bind(pos=self.update_img_pos, size=self.update_img_size)

    def update_img_pos(self, *args):
        self.image.pos = self.pos

    def update_img_size(self, *args):
        self.image.size = self.size



# Classe principale de l'application
class MainApp(App):
    def build(self):
        self.sm = ScreenManager()

        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(CameraScreen(name='camera'))
        self.sm.add_widget(PokedexScreen(name='pokedex'))
        self.sm.add_widget(ProfilScreen(name='profil'))
        self.sm.add_widget(PokemonDetailsPage(name='pokemon_info'))


        layout = FloatLayout()

        layout.add_widget(self.sm)

        # Créer la barre de navigation
        nav_bar = BoxLayout(size_hint=(1, 0.1),
                            pos_hint={'x': 0, 'y': 0},
                            orientation='horizontal',
                            padding=[20, 0, 0, 10],
                            spacing=70)

        with nav_bar.canvas.before:
            Color(1, 1, 1, 1) #RGBA
            self.rect = Rectangle(size=(Window.width, nav_bar.height), pos=(0, 0)) # Le rectangle blanc de la nav bar

            # Ombre au-dessus de la barre de navigation
            Color(0, 0, 0, 0.3) 
            self.shadow = Rectangle(size=(Window.width, 5), pos=(0, nav_bar.height))  # Taille et position de l'ombre

        # Lier la taille du rectangle à la taille de la nav_bar
        nav_bar.bind(size=lambda instance, value: setattr(self.rect, 'size', (Window.width, nav_bar.height)))
        
        # Mise à jour de la taille du rectangle et de l'ombre lorsque la fenêtre change
        def update_rect(instance, value):
            self.rect.size   = (Window.width, nav_bar.height)  # Mettre à jour la taille du rectangle blanc
            self.shadow.size = (Window.width, 5)               # L'ombre garde toujours la même hauteur
            self.shadow.pos  = (0, nav_bar.height)             # Placer l'ombre juste au-dessus de la barre de navigation

        nav_bar.bind(size=update_rect)

        # Taille des boutons de la nav_bar
        button_size = (60, 60)

        # Création des boutons de la nav_bar
        self.home_button    = RoundButton(image_source="ressources/imgs/accueil.png", size=button_size)
        self.home_button.bind(on_press=lambda x: self.switch_screen(self.sm, 'home'))

        self.camera_button  = RoundButton(image_source="ressources/imgs/camera-icon.png", size=button_size)
        self.camera_button.bind(on_press=lambda x: self.switch_screen(self.sm, 'camera'))

        self.pokedex_button = RoundButton(image_source="ressources/imgs/pokeball.png", size=button_size)
        self.pokedex_button.bind(on_press=lambda x: self.switch_screen(self.sm, 'pokedex'))

        self.profil_button  = RoundButton(image_source="ressources/imgs/profil.png", size=button_size)
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
        self.capture_button.pos_hint = {'center_x': 0.5, 'center_y': 0.10}  # Positionner au centre en bas
        self.capture_button.bind(on_press=self.capture_photo)

        layout.add_widget(self.capture_button)

        # Initialiser la visibilité du bouton
        self.sm.bind(current=self.update_button_visibility)

        # Sélectionner par défaut la page d'accueil
        self.switch_screen(self.sm, 'home')

        return layout

    def switch_screen(self, sm, screen_name):
        if screen_name == 'pokemon_info':
            sm.transition = RiseInTransition()
        else:
            sm.transition = NoTransition()  # Suppression des transitions
        sm.current = screen_name

    def capture_photo(self):
        if self.sm.current == 'camera':
            # Accéder à l'écran de la caméra
            camera_screen = self.sm.get_screen('camera')

            # Capturer une image
            ret, frame = camera_screen.capture.read()
            if ret:
                # Enregistrer l'image
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"photo_{timestamp}.png"
                cv2.imwrite(filename, frame)
                print(f"Photo sauvegardée sous {filename}")

    def update_button_visibility(self,instance, value):
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
