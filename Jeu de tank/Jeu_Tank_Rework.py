import pygame
import math
import random

# Initialisation de Pygame
pygame.init()

# Constantes de configuration
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (100, 255, 100)
BLUE = (0, 190, 255)
RED = (255, 0, 0)
GRAY = (111, 111, 111)

WIDTH, HEIGHT = 960, 540
FPS = 60
TANK_VEL = 4
ROTATION_VEL = 2.5
TURRET_ROTATION_VEL = 2
BULLET_VEL = 8
FIRE_DELAY = 1000  # 1 seconde
VIE = 3
TANK_WIDTH, TANK_HEIGHT = 120, 60

clock = pygame.time.Clock()

# Cacher le curseur
pygame.mouse.set_visible(False)

# Configuration des touches pour chaque joueur
TOUCHE1 = []
Z_P1 = pygame.K_z
TOUCHE1.append(Z_P1)
Q_P1 = pygame.K_q
TOUCHE1.append(Q_P1)
S_P1 = pygame.K_s
TOUCHE1.append(S_P1)
D_P1 = pygame.K_d
TOUCHE1.append(D_P1)
A_P1 = pygame.K_a
TOUCHE1.append(A_P1)
E_P1 = pygame.K_e
TOUCHE1.append(E_P1)

TOUCHE2 = []
Z_P2 = pygame.K_i
TOUCHE2.append(Z_P2)
Q_P2 = pygame.K_j
TOUCHE2.append(Q_P2)
S_P2 = pygame.K_k
TOUCHE2.append(S_P2)
D_P2 = pygame.K_l
TOUCHE2.append(D_P2)
A_P2 = pygame.K_u
TOUCHE2.append(A_P2)
E_P2 = pygame.K_o
TOUCHE2.append(E_P2)

# Configuration de la fenêtre
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Jeu De Tank")

# Polices pour l'affichage
fps_font = pygame.font.SysFont(None, 64)
status_font = pygame.font.SysFont(None, 32)
fps_surface = fps_font.render('0', True, WHITE)

#________________________________________________________________________________________________________________________________

class Tourelle(pygame.sprite.Sprite):
    def __init__(self, base, angle):
        pygame.sprite.Sprite.__init__(self)
        self.base = base  # Référence à la base
        self.original_image = pygame.image.load('Jeu de tank/assets/MainCharacters/Tank/tank_turret_P1.png').convert_alpha()
        self.image = self.original_image
        self.image = pygame.transform.scale(self.image, (110, 50))
        self.rect = self.image.get_rect(center=(self.base.x, self.base.y))
        self.angle = angle  # Angle initial de la tourelle
        
    def update(self):
        # La tourelle reste toujours au centre de la base
        self.rect.center = (self.base.x, self.base.y)
        
    def draw(self, window):
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        window.blit(rotated_image, new_rect.topleft)
        
    def rotate(self, angle):
        self.angle = (self.angle + angle) % 360  # Rotation indépendante
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, owner):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (2, 2), 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = BULLET_VEL
        self.owner = owner  # Référence au tank qui a tiré la bullet

    def update(self):
        radians = math.radians(self.angle)
        dx = self.speed * math.cos(radians)
        dy = -self.speed * math.sin(radians)
        self.rect.x += dx
        self.rect.y += dy
        # Remove bullet if it goes off-screen
        if not (0 <= self.rect.x <= WIDTH and 0 <= self.rect.y <= HEIGHT):
            self.kill()

class Base(pygame.sprite.Sprite):
    def __init__(self, x, y, orientation):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load('Jeu de tank/assets/MainCharacters/Tank/tank_base_P1.png').convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = orientation
        self.x, self.y = x, y
        self.tourelle = Tourelle(self, self.angle)  # Créer la tourelle ici, attachée à cette base


    def move(self, keys, objects, touche):
        # Rotation de la base
        if keys[touche[1]]:  # Rotation vers la gauche
            self.angle = (self.angle + ROTATION_VEL) % 360
            self.tourelle.angle = (self.tourelle.angle + ROTATION_VEL) % 360  # Synchroniser la tourelle
        if keys[touche[3]]:  # Rotation vers la droite
            self.angle = (self.angle - ROTATION_VEL) % 360
            self.tourelle.angle = (self.tourelle.angle - ROTATION_VEL) % 360  # Synchroniser la tourelle
        
        # Rotation indépendante de la tourelle
        if keys[touche[4]]:
            self.tourelle.rotate(TURRET_ROTATION_VEL)
        if keys[touche[5]]:
            self.tourelle.rotate(-TURRET_ROTATION_VEL)
        
        radians = math.radians(self.angle)
        dx, dy = 0, 0

        if keys[touche[0]]:  # Avancer
            dx = TANK_VEL * math.cos(radians)
            dy = -TANK_VEL * math.sin(radians)
        if keys[touche[2]]:  # Reculer
            dx = -TANK_VEL * math.cos(radians)
            dy = TANK_VEL * math.sin(radians)

        # Prédiction de la nouvelle position
        new_x = self.x + dx
        new_y = self.y + dy

        # Vérification des collisions et ajustement de la position
        self.x, self.y = self.collision_realiste(new_x, new_y, objects)

        # Mise à jour de la position
        self.rect.center = (self.x, self.y)
        
        # Rotation de l'image de la base
        self.rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.rotated_image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.rotated_image)
        
        # Mise à jour de la tourelle
        self.tourelle.update()
        
    def draw(self, window):
        # Dessiner la base
        window.blit(self.rotated_image, self.rect.topleft)
        # Dessiner la tourelle
        self.tourelle.draw(window)
        
    def collision_realiste(self, new_x, new_y, objects):
        # Handle wall collisions first (already sliding on walls as expected)
        if new_x < TANK_WIDTH // 2:
            new_x = TANK_WIDTH // 2
        elif new_x > WIDTH - TANK_WIDTH // 2:
            new_x = WIDTH - TANK_WIDTH // 2

        if new_y < TANK_HEIGHT:
            new_y = TANK_HEIGHT
        elif new_y > HEIGHT - TANK_HEIGHT:
            new_y = HEIGHT - TANK_HEIGHT

        return new_x, new_y
    
    def fire(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= FIRE_DELAY:
            # Calculer la position du bout de la tourelle
            radians = math.radians(self.tourelle.angle)
            barrel_length = 60  # Longueur de la tourelle
            bullet_x = self.x + barrel_length * math.cos(radians)
            bullet_y = self.y - barrel_length * math.sin(radians)
            # Créer et ajouter la bullet
            bullet = Bullet(bullet_x, bullet_y, self.tourelle.angle, self)
            bullets_group.add(bullet)
            self.last_shot_time = now

class Curseur(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self, colour):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos
        self.image.fill(colour)
        
class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        self.mask = pygame.mask.from_surface(self.image)
        self.x, self.y = x, y  # Position de la box
        self.rect.topleft = (self.x, self.y)  # Initialisation correcte de la position

    def update(self, colour):
        self.image.fill(colour)
        
    def check_collision(self, tanks):

        for tank in tanks:
            if self.rect.colliderect(tank.rect):
                # Vecteur de la collision
                dx = min(abs(self.rect.left - tank.rect.right), abs(self.rect.right - tank.rect.left))
                dy = min(abs(self.rect.bottom - tank.rect.top), abs(self.rect.top - tank.rect.bottom))

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
#________________________________________________________________________________________________________________________________

# Création d'instances

base1 = Base(100, 100, 0)
curseur = Curseur()
box = Box(500, 500, 200, 200)
box2 = Box(300, 300, 200, 20)
base2 = Base(1100, 800, 180)

# Création des groupes
base_group = pygame.sprite.Group()
curseur_group = pygame.sprite.Group()
object_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()

# Ajout des sprites aux groupes
base_group.add(base1)
base_group.add(base2)
curseur_group.add(curseur)
object_group.add(box)
object_group.add(box2)


def main(window, clock):
    run = True
    while run:
        # Mise à jour du fond
        window.fill(BLACK)
        
        # Définition des couleurs
        col_curseur = WHITE
        col_box = WHITE
        
        # Collision entre le curseur (balle) et la base
        if pygame.sprite.spritecollide(curseur, base_group, False):
            col_curseur = BLUE
            if pygame.sprite.spritecollide(curseur, base_group, False, pygame.sprite.collide_mask):  # Collision pixel-perfect
                col_curseur = RED
                
        
        # Collision entre la base et les objets
        for objects in object_group:
            if pygame.sprite.spritecollide(objects, base_group, False):
                col_box = BLUE 
                if pygame.sprite.spritecollide(objects, base_group, False, pygame.sprite.collide_mask):
                    col_box = GREEN
                    objects.check_collision(base_group)
            
        keys = pygame.key.get_pressed()
        base1.move(keys, object_group, TOUCHE1)
        base2.move(keys, object_group, TOUCHE2)
        
        # Mise à jour des bullets
        bullets_group.update()

        # Vérification des collisions entre bullets et tanks
        for bullet in bullets_group:
            # Collision avec les tanks
            for tank in base_group:
                if bullet.owner != tank and bullet.rect.colliderect(tank.rect):
                    tank.health -= 1
                    if tank.health <= 0:
                        tank.kill()
                        base_group.remove(tank)
                    bullet.kill()
                    break  # Sortir de la boucle des tanks

            # Collision avec les obstacles
            for box in object_group:
                if bullet.rect.colliderect(box.rect):
                    bullet.kill()
                    break  # Sortir de la boucle des obstacles
        
        # Mise à jour des groupes
        curseur_group.update(col_curseur)
        object_group.update(col_box)
        
        # Dessin des groupes sur la fenêtre
        base1.draw(window)
        base2.draw(window)
        bullets_group.draw(window)
        curseur_group.draw(window)
        object_group.draw(window)
        
        pygame.draw.rect(window, RED, base1.rect, 2)  # Pour visualiser la base1
        pygame.draw.rect(window, RED, base2.rect, 2)  # Pour visualiser la base2
        pygame.draw.rect(window, GREEN, box.rect, 12)  # Pour visualiser la boîte
        
        # Mise à jour de l'affichage
        pygame.display.flip()
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        clock.tick(FPS)

main(window, clock)
pygame.quit()