import pygame
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.clock import Clock
import requests
import os

# Initialize pygame mixer
pygame.mixer.init()

class MusicWidget(BoxLayout):
    
    def __init__(self, pokedex_number, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.playing = False  # To track if music is playing or paused
        self.paused = False   # To track if music is paused
        self.music_length = 0  # Store the length of the music
        self.music_position = 0  # Current position in milliseconds
        self.slider = None  # Reference to the slider widget
        self.pokedex_number = pokedex_number
        self.temp_sound_path = 'ressources/pokemonCries/' + str(pokedex_number) + '.wav'  # Path to save the temporary sound file

        self.build()

    def build(self):
        # Download pokemon cry
        #self.download_sound()

        # Load the sound file
        self.music = pygame.mixer.Sound(self.temp_sound_path)
        self.music_length = self.music.get_length()  # Get the length of the music

        # Create the play button
        self.play_button = Button(text='Play', size_hint=(None, None), size=(100, 50))
        self.play_button.bind(on_press=self.on_click)

        # Create the progress slider with a fixed width
        self.slider = Slider(min=0, max=self.music_length, value=0,
                             size_hint=(None, None), width=200, height=50)  # Set width to 200 pixels
        
        # Add widgets to the layout
        self.add_widget(self.play_button)
        self.add_widget(self.slider)

        # Schedule the update of the slider
        Clock.schedule_interval(self.update_slider, 0.1)


    def on_click(self, instance):
        if not self.playing and not self.paused:
            # Play music from the start if not already playing or paused
            pygame.mixer.music.load(self.temp_sound_path)
            pygame.mixer.music.play()
            self.playing = True
            self.paused = False
        elif self.playing:
            # Pause the music if currently playing
            pygame.mixer.music.pause()
            self.playing = False
            self.paused = True
        elif self.paused:
            # Unpause the music if it was paused
            pygame.mixer.music.unpause()
            self.playing = True
            self.paused = False

    def update_slider(self, dt):
        if self.playing:
            # Update the slider position based on the current music position
            self.music_position = pygame.mixer.music.get_pos() / 1000.0  # Get current position in seconds
            self.slider.value = self.music_position

    def on_stop(self):
        # Clean up temporary files
        if os.path.exists(self.temp_sound_path):
            os.remove(self.temp_sound_path)
        super().on_stop()
