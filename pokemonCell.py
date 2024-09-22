from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

# Import de mes fichiers
from mypokemons import mypokemons
from type_colors import TYPE_COLORS

class PokemonCell(FloatLayout):
    def __init__(self, pokemon_data, on_click_callback, position_in_grid,**kwargs):
        super(PokemonCell, self).__init__(**kwargs)
        self.pokemon_data = pokemon_data
        self.on_click_callback = on_click_callback
        self.position_in_grid = position_in_grid
        # Déterminer la couleur de fond basée sur le type de Pokémon
        pokemon_type = self.pokemon_data.get('types', [])[0] if isinstance(self.pokemon_data.get('types'), list) else self.pokemon_data.get('types', '')
        bg_color_hex = TYPE_COLORS.get(pokemon_type, '#FFFFFF')  # Utiliser une couleur par défaut
        self.bg_color = get_color_from_hex(bg_color_hex)


        # Créer le fond
        with self.canvas.before:
            Color(*self.bg_color)
            self.bg = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])

        # Ajouter les icônes de type
        self.icones = []
        for i, icon in enumerate(self.pokemon_data['types']):
            image_path = 'ressources/types/' + icon.strip() + '.png'
            print("image path : ", image_path)
            image = Image(
                source=image_path,
                allow_stretch=True, keep_ratio=True,
                size_hint=(None, None),
                size=(self.width * 0.2, self.height * 0.2),
                pos_hint={'center_x': 0.25, 'center_y': 0.5 - 0.10 * i}
            )
            self.icones.append(image)

        for icon in self.icones:
            self.add_widget(icon)

        # Ajouter l'image du Pokémon
        self.pokemon_image = Image(
            source=self.pokemon_data.get('image_path', 'image_path2'), 
            allow_stretch=True, keep_ratio=True,
            size_hint=(None, None),
            size=(self.width * 1.5, self.height * 1.5),
            pos_hint={'center_x': 0.75, 'center_y': 0.45}
        )
        self.add_widget(self.pokemon_image)

        # Créer et ajouter le label
        self.label = Label(
            text=self.pokemon_data['nom'].upper(),
            color=(1, 1, 1, 1),
            font_name='ressources/fonts/police.ttf',
            size=(self.width * 1.3, self.height * 1.3),
            pos=(self.x, self.y),
            bold=True
        )
        print("LABEL POS : ", self.label.pos)
        self.add_widget(self.label)

        # Créer le bouton transparent pour gérer le clic
        self.clickable_area = Button(size_hint=(None, None), background_color=(0, 0, 0, 0))
        self.clickable_area.bind(on_release=self.on_cell_click)
        self.add_widget(self.clickable_area)
        

        # Planifier la mise à jour après l'initialisation
        # Mettre à jour le fond et les widgets lors du redimensionnement
        self.bind(size=self.update_bg, pos=self.update_bg)
        self.bind(size=self.update_widgets, pos=self.update_widgets)
        Clock.schedule_once(self.update_widgets, 0)


    def on_cell_click(self, instance):
        # Appeler la fonction de rappel lors du clic
        self.on_click_callback(self.pokemon_data)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def update_widgets(self, *args):
        # Mettre à jour la taille et la position du label
        self.label.size = (self.width * 1.3, self.height * 1.3)
        self.label.pos  = (self.x-30, self.y + self.height/2.5)
        print("SIZE CELLULE : ", self.size)
        print("SIZE WIDTH : ", self.width)
        print("SIZE HEIGHT : ", self.height)
        print("POS CELLULE : ", self.pos)
        print("POS LABEL : ", self.label.pos)
        print("POSITION IN GRID : ", self.position_in_grid)
        
        # Mettre à jour la taille et la position de l'image
        self.pokemon_image.size = (self.width , self.height)
        self.pokemon_image.pos = (self.x + self.width * 0.2, self.y)

        # Mettre à jour la taille et la position des icones de types
        i = 0
        for icon in self.icones:
            icon.size = (self.width * 0.4, self.height * 0.4)
            icon.pos_hint={'center_x': 0.25, 'center_y': 0.5 - 0.15 * i}
            i+=1

        # Assurez-vous que le bouton est bien positionné
        self.clickable_area.size_hint = (None, None)
        self.clickable_area.size = self.size
        self.clickable_area.pos = self.pos
