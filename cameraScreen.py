import cv2
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from database import *

# Classe pour l'écran de la caméra
class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)

        layout = FloatLayout()

        # Ajouter l'image de fond
        self.background_down = Image(
            source="ressources/imgs/bg_camera.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )
        layout.add_widget(self.background_down)

        # Ajouter l'image d'en-tête en haut
        self.background_top = Image(
            source="ressources/imgs/header.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, None)
        )
        layout.add_widget(self.background_top)

        # Créer un FloatLayout pour la caméra
        self.camera_layout = FloatLayout(size_hint=(1, 1))
        layout.add_widget(self.camera_layout)

        # Ajouter la vue de la caméra
        self.camera_view = Image(
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(0.82, 0.35),
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        self.camera_layout.add_widget(self.camera_view)

        self.add_widget(layout)

        # Bind de la fonction de redimensionnement
        Window.bind(on_resize=self.on_window_resize)

        # Planifier la mise à jour de la vue de la caméra
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def on_window_resize(self, instance, width, height):
        # Mettre à jour la taille et la position de l'image d'en-tête
        self.background_top.size = (width, self.background_top.texture_size[1])
        self.background_top.pos = (0, height - self.background_top.height)

        # Mettre à jour la taille et la position de la vue de la caméra
        self.camera_view.size = (width * 0.8, height * 0.6)
        self.camera_view.pos = ((width - self.camera_view.width) / 2, (height - self.camera_view.height) / 2)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 0)  # Inverser l'image si nécessaire
            buf = frame.tobytes()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, bufferfmt='ubyte', colorfmt='bgr')
            self.camera_view.texture = image_texture

    def on_stop(self):
        self.capture.release()
