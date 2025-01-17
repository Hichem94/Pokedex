# Pokedex
Pokedex

[![Language](https://img.shields.io/badge/language-python-blue.svg?style=flat)](https://www.python.org)
[![Modules](https://img.shields.io/badge/modules-pygame%2C%20kivy%2C%20tensorflow%2C%20sqlite3-brightgreen.svg)](https://kivy.org/)
[![Release](https://img.shields.io/badge/release-v1.0-orange.svg?style=flat)](https://github.com/Hichem94/Pokedex)

## A propos
Bienvenue dans l'application Pokedex !

Pokedex est une application interactive qui vous permet de capturer des Pokémon et de les sauvegarder dans votre propre Pokédex. Chaque fois que vous attrapez un Pokémon, il est ajouté à votre liste personnelle, vous permettant de suivre vos progrès.

Cette application vous permet de :

Capturer et Identifier : Prenez des photos de Pokémon et laissez le modèle de reconnaissance vous dire quel Pokémon est sur votre image.

Écouter les cris des Pokémon : Chaque Pokémon a son propre cri ! Écoutez-le grâce après l'avoir capturé !

Sauvegarde automatique : Chaque Pokémon capturé est enregistré dans votre Pokédex.

Attrapez-les tous !

<img src="/ressources/imgs/git_home.jpg" width="200" height="400" />  <img src="/ressources/imgs/git_camera.jpg" width="200" height="400"/>  <img src="/ressources/imgs/git_pokedex.jpg" width="200" height="400"/>  <img src="/ressources/imgs/git_profil.jpg" width="200" height="400"/>


## Le modèle

Le modèle de reconnaissance des Pokémon a été développé avec TensorFlow et entraîné sur les images des 151 Pokémon de la première génération, disponibles dans le dossier dataset. Je me suis basé sur un tutoriel que vous pouvez consulter ici : [Tutoriel Tensorflow](https://www.tensorflow.org/tutorials/images/classification?hl=fr).

## Performance

Ajouter le tableau

## Difficultés

Bien que la précision du modèle soit satisfaisante (précision > 0,9), j'ai constaté que l'utilisation de l'appareil photo posait problème. En effet, même lorsque je prends en photo une image du dataset, le Pokémon prédit par le modèle n'est souvent pas correct. En revanche, lorsque je passe la même image au modèle via la ligne de commande, j'obtiens le bon résultat.


## Comment jouer

- Éxécuter le programme dans l'invite de commande / terminal.

```bash
cd Pokedex
python3 main.py
```

## A faire

Visualiser les Statistiques : Obtenez des graphiques des statistiques de chaque Pokémon attrapés.

## Remerciements

Cette application Pokedex a été inspirée graphiquement par le travail de [Adrian Twarog](https://www.youtube.com/@AdrianTwarog)
