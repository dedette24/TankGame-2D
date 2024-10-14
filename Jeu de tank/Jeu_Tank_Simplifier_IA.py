import pygame
import sys
import math
from pygame.time import get_ticks
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
FPS = 60  # Fixer le FPS à 100
TANK_VEL = 4
ROTATION_VEL = 2.5
TURRET_ROTATION_VEL = 3
BULLET_VEL = 8
FIRE_DELAY = 2000  # 2 seconde
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

    def check_collision_tank(self, tanks):
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
                
    def collision_bullet(self, bullets):
        """
        Vérifie si le tank est touché par une balle et réduit sa vie en conséquence.
        """
        for bullet in bullets: #on faut ca car j'ai une liste de balle
            if self.rect.colliderect(bullet.rect):
                bullets.remove(bullet)
                return True
        return False
        

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

    def shoot(self, delta_time):
        radians = math.radians(self.angle)
        self.x += BULLET_VEL * math.cos(radians) * delta_time
        self.y -= BULLET_VEL * math.sin(radians) * delta_time
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
        self.base_image = pygame.image.load(base_image_path).convert_alpha()
        self.base_image = pygame.transform.scale(self.base_image, (width, height))
        self.original_base_image = self.base_image.copy()
        self.rect = self.base_image.get_rect(center=(120, 90))
        self.last_shot_time = 0
        self.keys = {
            'avancer': avancer,
            'reculer': reculer,
            'droit': droit,
            'gauche': gauche,
            'aiguille': aiguille,
            'c_aiguille': c_aiguille
        }
        self.bullets = []  # Initialisation des balles

    def draw(self, window):
        # Dessiner la base du tank
        rotated_base_image = pygame.transform.rotate(self.original_base_image, self.angle)
        new_rect = rotated_base_image.get_rect(center=self.rect.center)
        window.blit(rotated_base_image, new_rect.topleft)
        
        # Dessiner la tourelle
        self.turret.draw(window)

        # Dessiner les balles
        for bullet in self.bullets:
            bullet.draw(window)


    def handle_bullets(self, tanks, delta_time, box):
        for bullet in self.bullets:
            bullet.shoot(delta_time)
            if bullet.rect.left < 0 or bullet.rect.right > WIDTH or bullet.rect.top < 0 or bullet.rect.bottom > HEIGHT:
                self.bullets.remove(bullet)
            else:
                for tank in tanks:
                    if tank is not self and bullet.rect.colliderect(tank.rect):
                        tank.vie -= 1
                        self.bullets.remove(bullet)
                        if tank.vie <= 0:
                            return False  # Signaler la fin du jeu
                        break
                        
                for bullet in self.bullets:
                    if bullet.rect.colliderect(box.rect):
                        self.bullets.remove(bullet)
        return True  # Continuer la partie

                    
    def get_reload_status(self):
        current_time = get_ticks()
        time_since_last_fire = current_time - self.last_shot_time
        if time_since_last_fire >= FIRE_DELAY:
            return "Prêt à tirer"
        else:
            remaining_time = (FIRE_DELAY - time_since_last_fire) / 1000
            return f"chargement : {remaining_time:.1f}s"

    def move(self, delta_time, box):
        keys = pygame.key.get_pressed()
        if keys[self.keys['avancer']]:
            radians = math.radians(self.angle)
            new_x = self.x + TANK_VEL * math.cos(radians)
            new_y = self.y - TANK_VEL * math.sin(radians)
            self.collision_realiste(new_x, new_y, box)
        if keys[self.keys['reculer']]:
            radians = math.radians(self.angle)
            new_x = self.x - TANK_VEL * math.cos(radians)
            new_y = self.y + TANK_VEL * math.sin(radians)
            self.collision_realiste(new_x, new_y, box)
        if keys[self.keys['gauche']]:
            self.angle += ROTATION_VEL 
            self.turret.rotate(ROTATION_VEL)
        if keys[self.keys['droit']]:
            self.angle -= ROTATION_VEL 
            self.turret.rotate(-ROTATION_VEL)
        if keys[self.keys['aiguille']]:
            self.turret.rotate(-TURRET_ROTATION_VEL * delta_time)
        if keys[self.keys['c_aiguille']]:
            self.turret.rotate(TURRET_ROTATION_VEL * delta_time)
        
        self.rect.center = (self.x, self.y)
        self.turret.rect.center = self.rect.center

    def fire(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > FIRE_DELAY:
            bullet_x = self.x + 50 * math.cos(math.radians(self.turret.angle))
            bullet_y = self.y - 50 * math.sin(math.radians(self.turret.angle))
            new_bullet = Bullet(bullet_x, bullet_y, self.turret.angle, 5, WHITE)
            self.bullets.append(new_bullet)
            self.last_shot_time = current_time
            
    def collision_realiste(self, new_x, new_y, box):
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

        # Gestion de la collision avec la boîte
        if self.rect.colliderect(box.rect):
            # Vecteur de la collision
            dx = min(abs(self.rect.left - box.rect.right), abs(self.rect.right - box.rect.left))
            dy = min(abs(self.rect.bottom - box.rect.top), abs(self.rect.top - box.rect.bottom))

            # Déplacer le tank dans la direction opposée à la collision
            if dx < dy:
                if self.x < box.x:
                    self.x -= dx
                else:
                    self.x += dx
            else:
                if self.y < box.y:
                    self.y -= dy
                else:
                    self.y += dy

            # Ajuster la position du rectangle du tank
            self.rect.center = (self.x, self.y)
            self.turret.rect.center = (self.x, self.y)

        self.rect.center = (self.x, self.y)
        self.turret.rect.center = (self.x, self.y)
            
def draw_health_bar(window, x, y, vie, max_vie):
    bar_width = 50
    bar_height = 10
    fill = (vie / max_vie) * bar_width
    outline_rect = pygame.Rect(x, y, bar_width, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(window, RED, fill_rect)
    pygame.draw.rect(window, WHITE, outline_rect, 2)
    
def draw_reload_bar(window, x, y, reload_time, reload_left):
    bar_width = 50
    bar_height = 10
    
    # Vérifier si reload_time est différent de zéro pour éviter une division par zéro
    if reload_time != 0:
        fill = (reload_left / reload_time) * bar_width
    else:
        fill = 0
    
    outline_rect = pygame.Rect(x, y, bar_width, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(window, RED, fill_rect)
    pygame.draw.rect(window, WHITE, outline_rect, 2)
    
def main():
    clock = pygame.time.Clock()
    running = True
    delta_time = 0

    tank1 = Tank(100, HEIGHT // 2, 80, 80, color_P1, 'Jeu de tank/assets/MainCharacters/Tank/tank_base_P1.png', 'Jeu de tank/assets/MainCharacters/Tank/tank_turret_P1.png', Z_P1, S_P1, D_P1, Q_P1, E_P1, A_P1, 0)
    tank2 = Tank(WIDTH - 100, HEIGHT // 2, 80, 80, color_P2, 'Jeu de tank/assets/MainCharacters/Tank/tank_base_P2.png', 'Jeu de tank/assets/MainCharacters/Tank/tank_turret_P2.png', Z_P2, S_P2, D_P2, Q_P2, E_P2, A_P2, 180)
    tanks = [tank1, tank2]
    bullets = []

    en_jeu = False
    menu_actif = True
    
    box = Boite(140)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_debut.collidepoint(event.pos):
                    en_jeu = True
                    menu_actif = False
                elif quitter_bouton.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif parametre.collidepoint(event.pos):
                    print("Parametre")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and en_jeu:
                    bullet1 = tank1.fire()
                    if bullet1:
                        bullet1.append(bullets)
                if event.key == pygame.K_RETURN and en_jeu:
                    bullet2 = tank2.fire()
                    if bullet2:
                        bullet2.append(bullets)
        
        if menu_actif:
            menu_principal()
        else:
            window.fill(BLACK)
            if en_jeu:
                delta_time = clock.get_time() / 15.0  # Temps écoulé en secondes

                for tank in tanks:
                    tank.move(delta_time, box)
                    if not tank.handle_bullets(tanks, delta_time, box):
                        running = False  # Si un tank meurt, arrêter la partie
                        pygame.quit()
                        sys.exit()

                    draw_health_bar(window, tank.rect.centerx - 25, tank.rect.centery + 50, tank.vie, VIE)
                    tank.draw(window)
                    
                for bullet in bullets:
                    bullet.move(delta_time)
                    bullet.draw(window)
                    bullet.check_collision_tank(tanks)
                    bullet.check_collision_box(bullets)
                    
                # Mise à jour du FPS
                fps_surface = fps_font.render(str(int(clock.get_fps())), True, WHITE)
                window.blit(fps_surface, (WIDTH - fps_surface.get_width() - 10, 10))
                
                # Gestion des collisions avec la boîte
                box.update_rect()
                box.check_collision_tank(tanks)

                reload_status_P1 = tank1.get_reload_status()
                reload_surface_P1 = status_font.render(reload_status_P1, True, WHITE)
                window.blit(reload_surface_P1, (10, HEIGHT - reload_surface_P1.get_height() - 60))
                
                reload_status_P2 = tank2.get_reload_status()
                reload_surface_P2 = status_font.render(reload_status_P2, True, WHITE)
                window.blit(reload_surface_P2, (WIDTH - reload_surface_P2.get_width() - 10, HEIGHT - reload_surface_P2.get_height() - 60))
                
                box.draw(window)

                pygame.display.flip()
                clock.tick(FPS)
            else:
                clock.tick(15)  # Limiter le FPS du menu principal
        
        
if __name__ == "__main__":
    main()

