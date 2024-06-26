import pygame
import sys
import math
from pygame.time import get_ticks
from PIL import Image, ImageFilter
import random
import time

# Initialisation de Pygame
pygame.init()

# Constantes de configuration
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (100, 255, 100)
BLUE = (0, 190, 255)
RED = (255, 0, 0)

WIDTH, HEIGHT = 800, 600
FPS = 120
TANK_VEL = 4
ROTATION_VEL = 2.5
TURRET_ROTATION_VEL = 2
BULLET_VEL = 8
FIRE_DELAY = 1000  # 1 seconde
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

# Boutons
bouton_debut = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 100)
quitter_bouton = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 100)
parametre = pygame.Rect((11), (11), 100 , 70)

# Fonts
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)
parametre_font = pygame.font.Font(None, 20)

def decompte(window, duration=3):
    for i in range(duration, 0, -1):
        window.fill(BLACK)
        countdown_text = font.render(str(i), True, WHITE)
        window.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(1000)  # Attend 1 seconde

def menu_principal():
    window.fill(WHITE)
    
    # Titre
    title_text = font.render("Menu d'accueil", True, BLACK)
    window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 10))
    
    # Boutons
    pygame.draw.rect(window, GREEN, bouton_debut)
    pygame.draw.rect(window, GREEN, quitter_bouton)
    pygame.draw.rect(window, WHITE, parametre)
    
    start = button_font.render("Commencer", True, BLACK)
    quitter = button_font.render("Quitter", True, BLACK)
    param = parametre_font.render("Parametre", True, BLACK)
    
    
    window.blit(start, (bouton_debut.x + bouton_debut.width // 2 - start.get_width() // 2, bouton_debut.y + bouton_debut.height // 2 - start.get_height() // 2))
    window.blit(quitter, (quitter_bouton.x + quitter_bouton.width // 2 - quitter.get_width() // 2, quitter_bouton.y + quitter_bouton.height // 2 - quitter.get_height() // 2))
    window.blit(param, (parametre.x + parametre.width // 2 - param.get_width() // 2, parametre.y + parametre.height // 2 - param.get_height() // 2))
    
    pygame.display.update()
    
#POUR l'IA #####################################################################################

#A faire : 
#reset fonction (pour rejouer)
#rewar fonction 
#play(action) -> direction
#game_iteration
#is collision (touche le tank adverse)


#POUR l'IA #####################################################################################

class Turret:
    def __init__(self, x, y, angle, image_path):
        super().__init__()
        self.x = x
        self.y = y
        self.angle = angle
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (110, 50))
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
        super().__init__()
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
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.angle = angle
        self.vie = VIE  # Initialisation de la vie
        self.turret = Turret(x, y, angle, turret_image_path)
        self.image = pygame.image.load(base_image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.last_fire_time = 0
        self.avancer = avancer
        self.reculer = reculer
        self.droit = droit
        self.gauche = gauche
        self.aiguille = aiguille
        self.c_aiguille = c_aiguille
        self.damage_animation = False
        self.damage_animation_time = 0
        
    def draw(self, window):
        if self.damage_animation:
            current_time = pygame.time.get_ticks()
            if current_time - self.damage_animation_time < 300:  # Animation de 300 ms
                scale_factor = 1.1  # Facteur de redimensionnement
                self.image = pygame.transform.scale(self.original_image, (int(self.width * scale_factor), int(self.height * scale_factor)))
            else:
                self.damage_animation = False
                self.image = self.original_image
        else:
            self.image = self.original_image
        
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
        # Gestion de la collision horizontale
        if new_x - self.width // 2 < 0:
            self.x = self.width // 2  # Empêche de dépasser le bord gauche
        elif new_x + self.width // 2 > WIDTH:
            self.x = WIDTH - self.width // 2  # Empêche de dépasser le bord droit
        else:
            self.x = new_x  # Mise à jour des coordonnées x

        # Gestion de la collision verticale
        if new_y - self.height // 2 < 0:
            self.y = self.height // 2  # Empêche de dépasser le bord supérieur
        elif new_y + self.height // 2 > HEIGHT:
            self.y = HEIGHT - self.height // 2  # Empêche de dépasser le bord inférieur
        else:
            self.y = new_y  # Mise à jour des coordonnées y

        self.rect.center = (self.x, self.y)
        self.turret.rect.center = (self.x, self.y)
        
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
            return "Prêt à tirer"
        else:
            remaining_time = (FIRE_DELAY - time_since_last_fire) / 1000
            return f"chargement : {remaining_time:.1f}s"
        
    def point_vie(self, x, y):
        health_bar_length = 200
        health_bar_height = 20

        # Calcul de la largeur de la barre de vie en fonction de la vie actuelle
        health_bar_width = health_bar_length * (self.vie / VIE)
        health_bar = pygame.Rect(x, y, health_bar_width, health_bar_height)
        pygame.draw.rect(window, RED, health_bar)
        return f"vie tank : {self.vie}"

    
    def hit(self, bullets):
        """
        Vérifie si le tank est touché par une balle et réduit sa vie en conséquence.
        """
        for bullet in bullets: #on faut ca car j'ai une liste de balle
            if self.rect.colliderect(bullet.rect):
                bullets.remove(bullet)
                self.vie -= 1
                self.damage_animation = True
                self.damage_animation_time = pygame.time.get_ticks()
                return True
        return False
        
class Boite:
    def __init__(self, size):
        super().__init__()
        self.size = size
        self.image = pygame.image.load('Jeu de tank/assets/Items/Boxes/Box'+str(random.randint(1,3))+'/Idle.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        print(f"{self.image}")
        self.rect = self.image.get_rect()  # Create a separate rect for collision detection
        self.rect = pygame.draw.rect(window , RED, self.rect)
        print(f"{self.rect}")
        self.rect.topleft = (random.randint(200, WIDTH - 200 - self.rect.width), random.randint(200, HEIGHT - 200 - self.rect.height))
        self.x = self.rect.x
        self.y = self.rect.y

    def draw(self, window):
        window.blit(self.image, self.rect.topleft)
        pygame.draw.rect(window, RED, self.rect)

    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def check_collision(self, bullets, tanks):
        for bullet in bullets:
            if self.rect.colliderect(bullet.rect):
                bullets.remove(bullet)

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
                tank.turret.rect.center = (tank.x, tank.y)
                
def generate_herbe_positions(num_herbes, size):
    positions = []
    for _ in range(num_herbes):
        x = random.randint(size, WIDTH - size)
        y = random.randint(size, HEIGHT - size)
        positions.append((x, y))
    return positions

def deco(window, herbe, positions):
    for pos in positions:
        window.blit(herbe, pos)
        
def draw_health_bar(window, x, y, vie, max_vie):
    bar_width = 50
    bar_height = 10
    fill = (vie / max_vie) * bar_width
    outline_rect = pygame.Rect(x, y, bar_width, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(window, RED, fill_rect)
    pygame.draw.rect(window, WHITE, outline_rect, 2)

def main(window, clock, fps_surface):
    window.fill(BLACK)
    
    """tank_P1 = Tank(vie=80)
    tank_P2 = Tank(vie=60)"""
    
    tank_P1 = Tank(100, HEIGHT // 2, 100, 60, GREEN, 'Jeu de tank/assets/MainCharacters/Tank/tank_base_P1.png', 'Jeu de tank/assets/MainCharacters/Tank/tank_turret_P1.png', Z_P1, S_P1, D_P1, Q_P1, E_P1, A_P1, 0)
    tank_P2 = Tank(WIDTH - 100, HEIGHT // 2, 100, 60, BLUE, 'Jeu de tank/assets/MainCharacters/Tank/tank_base_P2.png', 'Jeu de tank/assets/MainCharacters/Tank/tank_turret_P2.png', Z_P2, S_P2, D_P2, Q_P2, E_P2, A_P2, 180)
    bullets_P1 = []
    bullets_P2 = []
    
    box = Boite(140)  # Création de la boîte
    
    herbe = pygame.image.load("Jeu de tank/assets/Terrain/noBG_herbe.png").convert_alpha()

    # Nombre de sprites d'herbe
    num_herbes = 10
    size = 10

    # Générer les positions de l'herbe une seule fois
    herbe_positions = generate_herbe_positions(num_herbes, size)
    
    run = True
    while run:
        clock.tick(40)
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
        box.update_rect()
        box.check_collision(bullets_P1, [tank_P1, tank_P2])
        box.check_collision(bullets_P2, [tank_P1, tank_P2])
        
        # Vérifier les collisions entre les balles et les tanks
        if tank_P1.hit(bullets_P2) or tank_P2.hit(bullets_P1):
            print("Tu t'es fait touché")
            
        if tank_P1.vie == 0 or tank_P2.vie == 0:
            if tank_P1.vie == 0:
                gagnant = "JOUEUR 2"
            else:
                gagnant = "JOUEUR 1"
            print("La partie est finie !")
            window.fill(WHITE)
            affiche_fin = f"FIN DE LA PARTIE ! LE GAGNANT EST LE {gagnant} !"
            fin = status_font.render(affiche_fin, True, BLACK)
            # Obtenir la taille du texte
            taille_texte = fin.get_rect()
            # Calculer la position x et y pour centrer le texte
            text_x = (WIDTH - taille_texte.width) // 2
            text_y = (HEIGHT - taille_texte.height) // 2
            # Blitter le texte au centre de l'écran
            window.blit(fin, (text_x, text_y))
            pygame.display.update()
            pygame.time.wait(5000)
            main()

        window.fill(GREEN)
        
        deco(window, herbe, herbe_positions)
        
        tank_P1.draw(window)
        for bullet_P1 in bullets_P1:
            bullet_P1.draw(window)
        tank_P2.draw(window)
        for bullet_P2 in bullets_P2:
            bullet_P2.draw(window)
        box.draw(window)  # Dessiner la boîte

        fps_surface = fps_font.render(str(int(clock.get_fps())), True, BLACK)
        window.blit(fps_surface, (0, 0))

        reload_status_P1 = tank_P1.get_reload_status()
        reload_surface_P1 = status_font.render(reload_status_P1, True, BLACK)
        window.blit(reload_surface_P1, (10, HEIGHT - reload_surface_P1.get_height() - 60))

        reload_status_P2 = tank_P2.get_reload_status()
        reload_surface_P2 = status_font.render(reload_status_P2, True, BLACK)
        window.blit(reload_surface_P2, (WIDTH - reload_surface_P2.get_width() - 10, HEIGHT - reload_surface_P2.get_height() - 60))
        
        # Affichage des barres de vie
        info_vie_P1 = tank_P1.point_vie(10, HEIGHT - 50)
        """affiche_vie_P1 = status_font.render(info_vie_P1, True, BLACK)
        window.blit(affiche_vie_P1, (10, HEIGHT - 10))"""

        info_vie_P2 = tank_P2.point_vie(WIDTH - 210, HEIGHT - 50)
        """affiche_vie_P2 = status_font.render(info_vie_P2, True, BLACK)
        window.blit(affiche_vie_P2, (WIDTH - affiche_vie_P2.get_width() - 10, HEIGHT - 10))"""

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    clock = pygame.time.Clock()
    fps_surface = fps_font.render('0', True, WHITE)
    # Boucle du menu d'accueil
    menu = True
    while menu:
        menu_principal()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_debut.collidepoint(event.pos):
                    menu = False
                    #decompte(window)
                    main(window, clock, fps_surface)
                elif quitter_bouton.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif parametre.collidepoint(event.pos):
                    ...
pygame.quit()