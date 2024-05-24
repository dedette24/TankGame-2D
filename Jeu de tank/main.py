import pygame
import sys
import math
from pygame.time import get_ticks
from PIL import Image, ImageFilter
import random

# Initialisation de Pygame
pygame.init()

# Constantes de configuration
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 190, 255)

WIDTH, HEIGHT = 800, 600
FPS = 40
TANK_VEL = 4
ROTATION_VEL = 2.5
TURRET_ROTATION_VEL = 2
BULLET_VEL = 8
FIRE_DELAY = 3000  # 3 secondes

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

def apply_color_filter(image_path, color, save_path):
    """
    Applique une teinte de couleur à une image et enregistre le résultat en conservant la transparence.

    Args:
    image_path (str): Chemin de l'image source.
    color (tuple): Couleur à appliquer (R, G, B).
    save_path (str): Chemin pour enregistrer l'image filtrée.
    """
    image = Image.open(image_path).convert("RGBA")
    r, g, b, a = image.split()
    
    # Créer une nouvelle image remplie avec la couleur donnée
    color_image = Image.new("RGBA", image.size, color + (0,))
    cr, cg, cb, _ = color_image.split()
    
    # Fusionner les canaux de couleur de l'image d'origine et de l'image colorée
    r = Image.blend(r, cr, 0.5)
    g = Image.blend(g, cg, 0.5)
    b = Image.blend(b, cb, 0.5)
    
    # Réassembler les canaux avec la transparence d'origine
    blended_image = Image.merge("RGBA", (r, g, b, a))
    blended_image.save(save_path)

# Générer des couleurs aléatoires pour chaque joueur
color_P1 = tuple(random.randint(0, 255) for i in range(3))
color_P2 = tuple(random.randint(0, 255) for i in range(3))

# Appliquer les filtres de couleur aux images de la base et de la tourelle des chars
apply_color_filter('Jeu de tank/assets/MainCharacters/Tank/NoBG_Base.png', color_P1, 'Jeu de tank/assets/MainCharacters/Tank/tank_base_P1.png')
apply_color_filter('Jeu de tank/assets/MainCharacters/Tank/NoBG_Base.png', color_P2, 'Jeu de tank/assets/MainCharacters/Tank/tank_base_P2.png')
apply_color_filter('Jeu de tank/assets/MainCharacters/Tank/NoBG_Touret.png', color_P1, 'Jeu de tank/assets/MainCharacters/Tank/tank_turret_P1.png')
apply_color_filter('Jeu de tank/assets/MainCharacters/Tank/NoBG_Touret.png', color_P2, 'Jeu de tank/assets/MainCharacters/Tank/tank_turret_P2.png')


class Turret:
    def __init__(self, x, y, angle, image_path):
        self.x = x
        self.y = y
        self.angle = angle
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (130, 60))
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, window):
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        window.blit(rotated_image, new_rect.topleft)

    def rotate(self, angle):
        self.angle = (self.angle + angle) % 360

class Bullet:
    def __init__(self, x, y, angle, size, color):
        self.x = x
        self.y = y
        self.angle = angle
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))

    def move(self):
        radians = math.radians(self.angle)
        self.x += BULLET_VEL * math.cos(radians)
        self.y -= BULLET_VEL * math.sin(radians)
        self.rect.center = (self.x, self.y)

    def draw(self, window):
        window.blit(self.image, self.rect.topleft)

class Tank:
    def __init__(self, x, y, width, height, color, base_image_path, turret_image_path, avancer, reculer, droit, gauche, aiguille, c_aiguille, angle):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.angle = angle
        self.turret = Turret(x, y, angle, turret_image_path)
        self.image = pygame.image.load(base_image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.last_fire_time = 0
        self.avancer = avancer
        self.reculer = reculer
        self.droit = droit
        self.gauche = gauche
        self.aiguille = aiguille
        self.c_aiguille = c_aiguille
        
    def draw(self, window):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        window.blit(rotated_image, new_rect.topleft)
        self.turret.draw(window)

    def move(self, keys):
        if keys[self.gauche]:
            self.angle = (self.angle + ROTATION_VEL) % 360
            self.turret.rotate(ROTATION_VEL)
        if keys[self.droit]:
            self.angle = (self.angle - ROTATION_VEL) % 360
            self.turret.rotate(-ROTATION_VEL)
        if keys[self.avancer]:
            radians = math.radians(self.angle)
            new_x = self.x + TANK_VEL * math.cos(radians)
            new_y = self.y - TANK_VEL * math.sin(radians)
            self.collision_realiste(new_x, new_y)
        if keys[self.reculer]:
            radians = math.radians(self.angle)
            new_x = self.x - TANK_VEL * math.cos(radians)
            new_y = self.y + TANK_VEL * math.sin(radians)
            self.collision_realiste(new_x, new_y)
        if keys[self.c_aiguille]:
            self.turret.rotate(TURRET_ROTATION_VEL)
        if keys[self.aiguille]:
            self.turret.rotate(-TURRET_ROTATION_VEL)
        self.rect.center = (self.x, self.y)
        self.turret.rect.center = (self.x, self.y)
        
    def collision_realiste(self, new_x, new_y):
    # Vérifie si le nouveau déplacement dépasse les bords de l'écran
    #je tiens a préciser que ca ne vient pas de moi et que je ne comprend pas trop ce bout de code
        if new_x < 0:
            self.x = 0
        elif new_x > WIDTH - self.width:
            self.x = WIDTH - self.width
        else:
            self.x = new_x
        
        if new_y < 0:
            self.y = 0
        elif new_y > HEIGHT - self.height:
            self.y = HEIGHT - self.height
        else:
            self.y = new_y

    def fire(self):
        current_time = get_ticks()
        if current_time - self.last_fire_time >= FIRE_DELAY:
            radians = math.radians(self.turret.angle)
            bullet_x = self.x + (self.width // 2) * math.cos(radians)
            bullet_y = self.y - (self.width // 2) * math.sin(radians)
            bullet = Bullet(bullet_x, bullet_y, self.turret.angle, 10, WHITE)
            self.last_fire_time = current_time
            return bullet
        return None

    def get_reload_status(self):
        current_time = get_ticks()
        time_since_last_fire = current_time - self.last_fire_time
        if time_since_last_fire >= FIRE_DELAY:
            return "Ready to fire"
        else:
            remaining_time = (FIRE_DELAY - time_since_last_fire) / 1000
            return f"Reloading: {remaining_time:.1f}s"
        
class Boite:
    def __init__(self, size):
        self.size = size
        self.x = random.randint(200, WIDTH - 200)
        self.y = random.randint(200, HEIGHT - 200)
        self.image = pygame.image.load('Jeu de tank/assets/Items/Boxes/Box2/Idle.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(center=(size, size))

    def draw(self, window):
        window.blit(self.image, self.rect.topleft)

    def check_collision(self, bullets, tanks):
        for bullet in bullets:
            if self.rect.colliderect(bullet.rect):
                bullets.remove(bullet)

        for tank in tanks:
            if self.rect.colliderect(tank.rect):
                # Vecteur de la collision
                dx = min(abs(self.rect.left - tank.rect.right), abs(self.rect.right - tank.rect.left))
                dy = min(abs(self.rect.top - tank.rect.bottom), abs(self.rect.bottom - tank.rect.top))

                # Déplacer le tank dans la direction opposée à la collision
                if dx < dy:
                    if tank.x < self.x:
                        tank.x -= dx
                    else:
                        tank.x += dx
                else:
                    if tank.y < self.y:
                        tank.y -= dy
                    else:
                        tank.y += dy

                # Ajuster la position du rectangle du tank
                tank.rect.center = (tank.x, tank.y)
                tank.turret.rect.center = (tank.x, tank.y)

def main(window, clock, fps_surface):
    tank_P1 = Tank(100, HEIGHT // 2, 120, 80, GREEN, 'Jeu de tank/assets/MainCharacters/Tank/tank_base_P1.png', 'Jeu de tank/assets/MainCharacters/Tank/tank_turret_P1.png', Z_P1, S_P1, D_P1, Q_P1, E_P1, A_P1, 0)
    tank_P2 = Tank(WIDTH - 100, HEIGHT // 2, 120, 80, GREEN, 'Jeu de tank/assets/MainCharacters/Tank/tank_base_P2.png', 'Jeu de tank/assets/MainCharacters/Tank/tank_turret_P2.png', Z_P2, S_P2, D_P2, Q_P2, E_P2, A_P2, 180)
    bullets_P1 = []
    bullets_P2 = []
    box = Boite(200)  # Création de la boîte

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        tank_P1.move(keys)
        tank_P2.move(keys)

        if keys[pygame.K_SPACE]:
            bullet_P1 = tank_P1.fire()
            if bullet_P1:
                bullets_P1.append(bullet_P1)
        if keys[pygame.K_RETURN]:
            bullet_P2 = tank_P2.fire()
            if bullet_P2:
                bullets_P2.append(bullet_P2)

        for bullet_P1 in bullets_P1:
            bullet_P1.move()
            if not (0 <= bullet_P1.x <= WIDTH and 0 <= bullet_P1.y <= HEIGHT):
                bullets_P1.remove(bullet_P1)

        for bullet_P2 in bullets_P2:
            bullet_P2.move()
            if not (0 <= bullet_P2.x <= WIDTH and 0 <= bullet_P2.y <= HEIGHT):
                bullets_P2.remove(bullet_P2)

        # Gestion des collisions avec la boîte
        box.check_collision(bullets_P1, [tank_P1, tank_P2])
        box.check_collision(bullets_P2, [tank_P1, tank_P2])

        window.fill(BLACK)
        tank_P1.draw(window)
        for bullet_P1 in bullets_P1:
            bullet_P1.draw(window)
        tank_P2.draw(window)
        for bullet_P2 in bullets_P2:
            bullet_P2.draw(window)
        box.draw(window)  # Dessiner la boîte

        fps_surface = fps_font.render(str(int(clock.get_fps())), True, WHITE)
        window.blit(fps_surface, (0, 0))

        reload_status_P1 = tank_P1.get_reload_status()
        reload_surface_P1 = status_font.render(reload_status_P1, True, WHITE)
        window.blit(reload_surface_P1, (WIDTH - reload_surface_P1.get_width() - 10, 10))

        reload_status_P2 = tank_P2.get_reload_status()
        reload_surface_P2 = status_font.render(reload_status_P2, True, WHITE)
        window.blit(reload_surface_P2, (WIDTH - reload_surface_P2.get_width() - 10, 40))

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    clock = pygame.time.Clock()
    fps_surface = fps_font.render('0', True, WHITE)
    main(window, clock, fps_surface)
