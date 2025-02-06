import numpy as np
import random
import pygame
from MEU.parametre import *
from MEU.menu import menu_principal

# Définir les actions possibles : avancer, reculer, tourner à gauche, tourner à droite, tourner la tourelle, tirer
ACTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'TURRET_LEFT', 'TURRET_RIGHT', 'FIRE']

# Hyperparamètres du Q-learning
ALPHA = 0.1  # Taux d'apprentissage
GAMMA = 0.95  # Facteur de discount
EPSILON = 1.0  # Exploration initiale
EPSILON_DECAY = 0.995  # Décroissance d'EPSILON
EPSILON_MIN = 0.01  # Valeur minimale d'EPSILON
EPISODES = 500  # Nombre d'épisodes
MAX_STEPS = 200  # Nombre maximum de pas par épisode

# Initialiser la Q-table
q_table = np.zeros((HEIGHT * WIDTH, len(ACTIONS)))  # Simplement basé sur la taille de l'environnement

class Tank:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.turret_angle = 0
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, 50, 50)  # Représente le tank
        self.velocity = TANK_VEL

    def move(self, action):
        if action == 'UP':
            self.y -= self.velocity
        elif action == 'DOWN':
            self.y += self.velocity
        elif action == 'LEFT':
            self.x -= self.velocity
        elif action == 'RIGHT':
            self.x += self.velocity
        elif action == 'TURRET_LEFT':
            self.turret_angle -= TURRET_ROTATION_VEL
        elif action == 'TURRET_RIGHT':
            self.turret_angle += TURRET_ROTATION_VEL

        # Mettre à jour la position et l'angle
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        # Dessiner la tourelle
        pygame.draw.line(window, WHITE, (self.x + 25, self.y + 25), (self.x + 25 + 50 * np.cos(self.turret_angle), self.y + 25 + 50 * np.sin(self.turret_angle)), 5)

# Fonction pour choisir une action (épsilon-greedy)
def choose_action(state):
    if random.uniform(0, 1) < EPSILON:
        return random.choice(ACTIONS)
    else:
        return ACTIONS[np.argmax(q_table[state])]

# Fonction pour obtenir la récompense
def get_reward(tank):
    # Exemples de récompenses
    if tank.rect.colliderect(pygame.Rect(140, 140, 50, 50)):  # Si le tank heurte un obstacle
        return -100
    else:
        return -1  # Encourager le mouvement

# Mettre à jour la Q-table
def update_q_table(state, action, reward, next_state):
    action_index = ACTIONS.index(action)
    best_next_action = np.argmax(q_table[next_state])
    q_table[state, action_index] = q_table[state, action_index] + ALPHA * (reward + GAMMA * q_table[next_state, best_next_action] - q_table[state, action_index])

# Simulation d'un épisode
def run_episode(tank):
    global EPSILON
    state = tank.rect.x + tank.rect.y * WIDTH  # Calculer un état simple basé sur la position
    total_reward = 0

    for _ in range(MAX_STEPS):
        action = choose_action(state)
        tank.move(action)

        next_state = tank.rect.x + tank.rect.y * WIDTH
        reward = get_reward(tank)
        update_q_table(state, action, reward, next_state)
        state = next_state
        total_reward += reward

        if reward == -100:  # Si le tank heurte un obstacle, l'épisode se termine
            break

    if EPSILON > EPSILON_MIN:
        EPSILON *= EPSILON_DECAY
    
    return total_reward

# Fonction récursive d'entraînement
def recursive_train_q_learning(tank, window, episode=0):
    # Condition d'arrêt : on s'arrête après avoir atteint le nombre maximal d'épisodes
    if episode >= EPISODES:
        return

    # Exécuter un épisode et afficher le résultat
    reward = run_episode(tank)
    print(f"Épisode {episode + 1}/{EPISODES}, Récompense totale: {reward}")

    # Mise à jour graphique
    window.fill(BLACK)
    tank.draw(window)
    pygame.display.update()

    # Appel récursif pour l'épisode suivant
    recursive_train_q_learning(tank, window, episode + 1)

# Fonction principale d'entraînement
def train_q_learning():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jeu de Tank")

    tank = Tank(WIDTH // 2, HEIGHT // 2, BLUE)  # Initialiser un tank

    # Lancer l'entraînement de manière récursive
    recursive_train_q_learning(tank, window)

# Démarrer l'entraînement
if __name__ == "__main__":
    train_q_learning()
