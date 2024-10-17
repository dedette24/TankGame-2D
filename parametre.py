import pygame
import sys
import math
from pygame.time import get_ticks
import random

# Initialisation de Pygame
pygame.init()

# Constantes de configuration
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (100, 255, 100)
BLUE = (0, 190, 255)
RED = (255, 0, 0)

WIDTH, HEIGHT = 800, 600
FPS = 75  # Fixer le FPS à 100
TANK_VEL = 4
TANK_VEL_IA = 4
ROTATION_VEL = 2.5
TURRET_ROTATION_VEL = 3
BULLET_VEL = 8
FIRE_DELAY = 1000  # 2 seconde
VIE = 3

# Configuration des touches pour chaque joueur
Z_P1 = pygame.K_z
S_P1 = pygame.K_s
Q_P1 = pygame.K_q
D_P1 = pygame.K_d
A_P1 = pygame.K_a
E_P1 = pygame.K_e

Z_P2 = pygame.K_i
S_P2 = pygame.K_k
Q_P2 = pygame.K_j
D_P2 = pygame.K_l
A_P2 = pygame.K_u
E_P2 = pygame.K_o

# Configuration de la fenêtre
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Jeu De Tank")

# Polices pour l'affichage
fps_font = pygame.font.SysFont(None, 64)
status_font = pygame.font.SysFont(None, 32)
fps_surface = fps_font.render('0', True, WHITE)

color_P1 = tuple(random.randint(0, 255) for i in range(3))
color_P2 = tuple(random.randint(0, 255) for i in range(3))

# Boutons
bouton_debut = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 100)
quitter_bouton = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 100)
parametre = pygame.Rect((11), (11), 100 , 70)

# Fonts
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)
parametre_font = pygame.font.Font(None, 20)