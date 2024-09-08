import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf
import sys

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential, load_model


batch_size = 32
img_height = 180
img_width  = 180

def model_training():

    # Utilisons 80% des images pour la formation et 20% pour la validation.
    train_ds = tf.keras.utils.image_dataset_from_directory(
    'dataset_popular',
    validation_split = 0.2,
    subset = "training",
    seed = 123,
    image_size = (img_height, img_width),
    batch_size = batch_size)

    val_ds = tf.keras.utils.image_dataset_from_directory(
    'dataset_popular',
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size)


    class_names = train_ds.class_names
    print(class_names)

    # Configurer l'ensemble de données pour les performances
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # Creation du modèle
    num_classes = len(class_names)

    # Explication du modèle
    """
    model = Sequential([
    Normaliser les valeurs des canaux RGB pour qu'elles soient dans la
    plage [0, 1] au lieu de [0, 255]
    layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
    
    Cette couche est une couche de convolution 2D. 
    Elle applique 16 filtres de taille 3x3 sur les images. 
    Le paramètre padding='same' garantit que la taille de l'image de sortie
    est la même que celle de l'image d'entrée. La fonction d'activation relu 
    est utilisée pour introduire de la non-linéarité dans le modèle.
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    Cette couche effectue un sous-échantillonnage en réduisant la taille
    de l'image tout en conservant les informations les plus importantes.
    layers.MaxPooling2D(),

    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),

    Cette couche transforme la sortie 3D des couches précédentes en
    une représentation 1D, nécessaire pour les couches entièrement connectées.
    layers.Flatten(),
    Une couche entièrement connectée avec 128 neurones, utilisant la fonction
    d'activation relu
    layers.Dense(128, activation='relu'),
    La couche de sortie, avec num_classes neurones. Cette couche produit les
    probabilités pour chaque classe.
    layers.Dense(num_classes)
    ])
    """

    num_classes = len(class_names)

    #add data augmentation for more accurate results
    data_augmentation = keras.Sequential(
        [layers.RandomFlip("horizontal",
            input_shape=(img_height,img_width,3)),
            layers.RandomRotation(0.1),
            layers.RandomZoom(0.1)]
        )


    model = Sequential([
    data_augmentation,
    layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes)
    ])


    # Compiler le modèle
    """ Cette méthode prépare le modèle pour l'entraînement en spécifiant l'optimiseur,
    la fonction de perte et les métriques à suivre."""
    model.compile(optimizer='adam',
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])


    # Entrainer le modèle
    epochs=12
    history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs
    )

    
    # Visualiser les résultats d'entrainement
    # acc = history.history['accuracy']
    # val_acc = history.history['val_accuracy']

    # loss = history.history['loss']
    # val_loss = history.history['val_loss']

    # epochs_range = range(epochs)

    # plt.figure(figsize=(8, 8))
    # plt.subplot(1, 2, 1)
    # plt.plot(epochs_range, acc, label='Training Accuracy')
    # plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    # plt.legend(loc='lower right')
    # plt.title('Training and Validation Accuracy')

    # plt.subplot(1, 2, 2)
    # plt.plot(epochs_range, loss, label='Training Loss')
    # plt.plot(epochs_range, val_loss, label='Validation Loss')
    # plt.legend(loc='upper right')
    # plt.title('Training and Validation Loss')
    # plt.show()

    model.save("pokedex.keras")
    #model.export("TFLITE_pokedex_model.keras")
    return model


def make_prediction(model, img_path):
    img = keras.preprocessing.image.load_img(
        img_path, target_size=(img_height, img_width)
    )
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    class_names = ['Bulbasaur', 'Charmander', 'Mewtwo', 'Pikachu', 'Squirtle']
    #result_string = "Likely {} with {:.2f}% confidence.".format(class_names[np.argmax(score)], 100 * np.max(score))
    return class_names[np.argmax(score)]