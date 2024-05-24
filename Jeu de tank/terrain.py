import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter
import os
import random

def generate_random_terrain(size, scale):
    """
    Génère un terrain aléatoire de dimensions spécifiées.

    Args:
    size (tuple): Dimensions du terrain (largeur, hauteur).
    scale (float): Échelle pour la génération des altitudes.

    Returns:
    np.ndarray: Tableau 2D représentant les altitudes du terrain.
    """
    width, height = size
    terrain = np.random.normal(loc=0, scale=scale, size=(width, height))
    for i in range(1, width):
        for j in range(1, height):
            terrain[i, j] += terrain[i-1, j] * 0.5 + terrain[i, j-1] * 0.5

    return terrain

def save_terrain_image(terrain, save_path):
    """
    Enregistre le terrain à l'aide de matplotlib sans l'afficher.

    Args:
    terrain (np.ndarray): Tableau 2D représentant les altitudes du terrain.
    save_path (str): Chemin pour enregistrer l'image.
    bbox_inches : garanti qu'il ne reste pas d'espace blanc indésirable
    """
    list_style = [
    'viridis', 'plasma', 'inferno', 'magma', 'cividis', 'twilight', 'twilight_shifted',
    'gray', 'bone', 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
    'hot', 'afmhot', 'gist_heat', 'copper', 'binary', 'gist_yarg', 'gist_gray', 'bone',
    'pink', 'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia', 'hot', 'afmhot',
    'gist_heat', 'copper', 'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu',
    'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic', 'hsv', 'Pastel1', 'Pastel2',
    'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b',
    'tab20c', 'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'gnuplot',
    'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'hsv', 'gist_rainbow', 'rainbow', 'jet',
    'nipy_spectral', 'gist_ncar'
]

    choosen_one = random.choice(list_style)
    plt.imshow(terrain, cmap=choosen_one)
    plt.axis('off')
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    plt.close()
    
    return choosen_one
    

def apply_filter(image_path, filter_type, save_path):
    """
    Applique un filtre à une image et enregistre le résultat.

    Args:
    image_path (str): Chemin de l'image source.
    filter_type (ImageFilter): Type de filtre à appliquer.
    save_path (str): Chemin pour enregistrer l'image filtrée.
    """
    image = Image.open(image_path)
    filtered_image = image.filter(filter_type)
    filtered_image.save(save_path)
    print(f"Image filtrée enregistrée sous {save_path}")

if __name__ == "__main__":
    size = (800, 600)
    scale = 5.0
    save_path = 'Jeu de tank/terrain.png'

    # Vérifiez si le répertoire existe, sinon créez-le
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    try:
        terrain = generate_random_terrain(size, scale)
        lui = save_terrain_image(terrain, save_path)
        print(f"Image de terrain enregistrée sous {save_path} avec le modele {lui}")
    except Exception as e:
        print(f"Erreur lors de la génération ou de l'enregistrement du terrain: {e}")

    image_path = 'Jeu de tank/terrain.png'
    filtered_save_path = 'Jeu de tank/terrain_filtered.png'
    filter_type = ImageFilter.CONTOUR(7)

    try:
        apply_filter(image_path, filter_type, filtered_save_path)
    except Exception as e:
        print(f"Erreur lors de l'application du filtre: {e}")
