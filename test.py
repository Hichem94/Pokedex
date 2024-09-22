from kivy.app import App
from kivy.uix.image import Image
from PIL import Image as PILImage
from kivy.graphics.texture import Texture
from kivy.uix.floatlayout import FloatLayout

class MyApp(App):
    def build(self):
        pil_img = PILImage.open('ressources/pokemon-center/001.png').convert('L')
        texture = Texture.create(size=pil_img.size, colorfmt='rgba')
        texture.blit_buffer(pil_img.tobytes(), colorfmt='luminance', bufferfmt='ubyte')
        img = Image(texture=texture)
        
        layout = FloatLayout()
        img.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Centrer l'image
        layout.add_widget(img)
        return layout

if __name__ == '__main__':
    MyApp().run()