from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.image import Image

class RoundButton(Button):
    source = StringProperty('')

    def __init__(self, image_source, **kwargs):
        super().__init__(**kwargs)
        self.source = image_source
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.size_hint = (None, None)
        
        # Ajouter un bind pour ajuster la taille de l'image lorsque le bouton change de taille
        self.bind(size=self.update_img_size, pos=self.update_img_pos)

    def on_size(self, *args):
        # Planifier l'ajout de l'image après l'initialisation du bouton
        Clock.schedule_once(self.create_image)

    def create_image(self, *args):
        if not hasattr(self, 'image'):
            self.image = Image(source=self.source, size=self.size, pos=self.pos)
            self.add_widget(self.image)
        self.update_img_size()

    def update_img_pos(self, *args):
        if hasattr(self, 'image'):
            self.image.pos = self.pos

    def update_img_size(self, *args):
        if hasattr(self, 'image'):
            # Mettre à jour la taille de l'image tout en conservant les proportions
            self.image.size = self.size
            self.image.texture_size = self.image.texture_size  # Pour éviter la perte de proportion
