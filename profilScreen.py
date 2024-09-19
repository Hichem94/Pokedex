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
from PIL import Image as PILImage
from kivy.utils import get_color_from_hex

# Classe pour la page Profil
class ProfilScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Ajouter une image ou tout autre contenu pour la page Profil
        self.background_down = Image(source="", allow_stretch=True, keep_ratio=False,
                                     size_hint=(1, 1))
        layout.add_widget(self.background_down)

        self.add_widget(layout)
