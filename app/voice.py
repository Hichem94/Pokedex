# import edge_tts

# async def main():
#     communicate = edge_tts.Communicate(
#         text='Pikachu est un pokémonne électrique',
#         voice='fr-FR-HenriNeural'
#     )
#     await communicate.save('output.mp3')  # Sauvegarde du fichier audio

# import asyncio
# asyncio.run(main())


from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
 
 
# our main window class
class MusicWindow(App):
 
    def build(self):
        # load the mp3 music
        music = SoundLoader.load('/home/rigolo/Pokedex/output.mp3')
 
        # check the exisitence of the music
        if music:
            music.play()
 
        return Label(text="Music is playing")
 
 
if __name__ == "__main__":
    window = MusicWindow()
    window.run()