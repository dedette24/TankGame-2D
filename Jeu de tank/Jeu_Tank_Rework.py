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

WIDTH, HEIGHT = 1300, 1000
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
TOUCHE1 = [pygame.K_z, pygame.K_q, pygame.K_s, pygame.K_d, pygame.K_a, pygame.K_e]
TOUCHE2 = [pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_u, pygame.K_o]

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
        self.base = base
        self.original_image = pygame.image.load('Jeu de tank/assets/MainCharacters/Tank/tank_turret_P1.png').convert_alpha()
        self.image = self.original_image
        self.image = pygame.transform.scale(self.image, (110, 50))
        self.rect = self.image.get_rect(center=(self.base.x, self.base.y))
        self.angle = angle
        
    def update(self):
        self.rect.center = (self.base.x, self.base.y)
        
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
<<<<<<< HEAD
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
=======
        self.speed = BULLET_VEL
        self.owner = owner
>>>>>>> a254b830b9b8691cfa05dcebc9a4af9656bc6ebb

    def shoot(self, delta_time):
        radians = math.radians(self.angle)
<<<<<<< HEAD
        self.x += BULLET_VEL * math.cos(radians) * delta_time
        self.y -= BULLET_VEL * math.sin(radians) * delta_time
        self.rect.center = (self.x, self.y)

    def draw(self, window):
        window.blit(self.image, self.rect.topleft)

=======
        dx = self.speed * math.cos(radians)
        dy = -self.speed * math.sin(radians)
        self.rect.x += dx
        self.rect.y += dy

        # Vérifier si la balle quitte l'écran
        if not (0 <= self.rect.x <= WIDTH and 0 <= self.rect.y <= HEIGHT):
            self.kill()
>>>>>>> a254b830b9b8691cfa05dcebc9a4af9656bc6ebb

class Base(pygame.sprite.Sprite):
    def __init__(self, x, y, orientation):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load('Jeu de tank/assets/MainCharacters/Tank/tank_base_P1.png').convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = orientation
        self.x, self.y = x, y
<<<<<<< HEAD
        self.tourelle = Tourelle(self, self.angle)  # Créer la tourelle ici, attachée à cette base
        self.bullets = []
        self.last_shot_time = 0

=======
        self.tourelle = Tourelle(self, self.angle)
        self.last_shot_time = 0
        self.health = VIE  # Initialisation de la vie
>>>>>>> a254b830b9b8691cfa05dcebc9a4af9656bc6ebb

    def move(self, keys, objects, touche):
        if keys[touche[1]]:
            self.angle = (self.angle + ROTATION_VEL) % 360
            self.tourelle.angle = (self.tourelle.angle + ROTATION_VEL) % 360
        if keys[touche[3]]:
            self.angle = (self.angle - ROTATION_VEL) % 360
            self.tourelle.angle = (self.tourelle.angle - ROTATION_VEL) % 360
        
        if keys[touche[4]]:
            self.tourelle.rotate(TURRET_ROTATION_VEL)
        if keys[touche[5]]:
            self.tourelle.rotate(-TURRET_ROTATION_VEL)
        
        radians = math.radians(self.angle)
        dx, dy = 0, 0

        if keys[touche[0]]:
            dx = TANK_VEL * math.cos(radians)
            dy = -TANK_VEL * math.sin(radians)
        if keys[touche[2]]:
            dx = -TANK_VEL * math.cos(radians)
            dy = TANK_VEL * math.sin(radians)

        new_x = self.x + dx
        new_y = self.y + dy

        self.x, self.y = self.collision_realiste(new_x, new_y, objects)

        self.rect.center = (self.x, self.y)
        
        self.rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.rotated_image.get_rect(center=self.rect.center)
        
        self.tourelle.update()
        
    def draw(self, window):
        window.blit(self.rotated_image, self.rect.topleft)
        self.tourelle.draw(window)
        
    def collision_realiste(self, new_x, new_y, objects):
        if new_x < TANK_WIDTH // 2:
            new_x = TANK_WIDTH // 2
        elif new_x > WIDTH - TANK_WIDTH // 2:
            new_x = WIDTH - TANK_WIDTH // 2

        if new_y < TANK_HEIGHT:
            new_y = TANK_HEIGHT
        elif new_y > HEIGHT - TANK_HEIGHT:
            new_y = HEIGHT - TANK_HEIGHT

        for box in objects:
            if box.rect.collidepoint(new_x, new_y):
                # Vecteur de la collision
                dx = min(abs(box.rect.left - self.rect.right), abs(box.rect.right - self.rect.left))
                dy = min(abs(box.rect.bottom - self.rect.top), abs(box.rect.top - self.rect.bottom))

                # Déplacer le tank dans la direction opposée à la collision
                if dx < dy:
                    if self.x < box.x:
                        new_x -= dx
                    else:
                        new_x += dx
                else:
                    if self.y < box.y:
                        new_y -= dy
                    else:
                        new_y += dy

        return new_x, new_y
<<<<<<< HEAD
=======
    
    def fire(self, bullets):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= FIRE_DELAY:
            radians = math.radians(self.tourelle.angle)
            barrel_length = 60
            bullet_x = self.x + barrel_length * math.cos(radians)
            bullet_y = self.y - barrel_length * math.sin(radians)
            bullet = Bullet(bullet_x, bullet_y, self.tourelle.angle, self)
            bullets.add(bullet)
            self.last_shot_time = now
>>>>>>> a254b830b9b8691cfa05dcebc9a4af9656bc6ebb

    def fire(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > FIRE_DELAY:
            bullet_x = self.x + 50 * math.cos(math.radians(self.tourelle.angle))
            bullet_y = self.y - 50 * math.sin(math.radians(self.tourelle.angle))
            new_bullet = Bullet(bullet_x, bullet_y, self.tourelle.angle, 5, WHITE)
            self.bullets.append(new_bullet)
            self.last_shot_time = current_time
            
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
        return True  # Continuer la partie
    
    
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
<<<<<<< HEAD
box = Box(WIDTH / 2, HEIGHT / 2, 200, 200)
=======
box = Box(WIDTH /2 , HEIGHT / 2, 200, 200)
>>>>>>> a254b830b9b8691cfa05dcebc9a4af9656bc6ebb
#box2 = Box(300, 300, 200, 20)
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
#object_group.add(box2)


def main(window, clock):
    run = True
<<<<<<< HEAD
    delta_time = 0
    while run:
        delta_time = clock.get_time() / 15.0  # Temps écoulé en secondes
        # Mise à jour du fond
=======
    base1 = Base(100, 100, 0)
    base2 = Base(1100, 800, 180)
    curseur = Curseur()
    box = Box(WIDTH /2 , HEIGHT / 2, 200, 200)
    bullets = pygame.sprite.Group()
    base_group = pygame.sprite.Group()
    object_group = pygame.sprite.Group()
    base_group.add(base1)
    base_group.add(base2)
    object_group.add(box)

    while run:
>>>>>>> a254b830b9b8691cfa05dcebc9a4af9656bc6ebb
        window.fill(BLACK)
        
        keys = pygame.key.get_pressed()
        base1.move(keys, object_group, TOUCHE1)
        base2.move(keys, object_group, TOUCHE2)
        
<<<<<<< HEAD
        # Mise à jour des groupes
        curseur_group.update(col_curseur)
        object_group.update(col_box)
        
        # Dessin des groupes sur la fenêtre
=======
        if keys[pygame.K_SPACE]:
            base1.fire(bullets)
        if keys[pygame.K_RETURN]:
            base2.fire(bullets)
        
        bullets.update()
        
        # Collision entre le curseur (balle) et la base
        """if pygame.sprite.spritecollide(curseur, base_group, False):
            col_curseur = BLUE
            if pygame.sprite.spritecollide(curseur, base_group, False, pygame.sprite.collide_mask):  # Collision pixel-perfect
                col_curseur = RED
                """
        
        # Collision entre la base et les objets
        for objects in object_group:
            if pygame.sprite.spritecollide(objects, base_group, False):
                if pygame.sprite.spritecollide(objects, base_group, False, pygame.sprite.collide_mask):
                    objects.check_collision(base_group)
        
        for bullet in bullets:
            for tank in base_group:
                if bullet.owner != tank and bullet.rect.colliderect(tank.rect):
                    tank.health -= 1
                    if tank.health <= 0:
                        tank.kill()
                        base_group.remove(tank)
                        
                    bullet.kill()
                    break
            for box in object_group:
                if bullet.rect.colliderect(box.rect):
                    bullet.kill()
                    break
        
>>>>>>> a254b830b9b8691cfa05dcebc9a4af9656bc6ebb
        base1.draw(window)
        base2.draw(window)
        bullets.draw(window)
        object_group.draw(window)
        
<<<<<<< HEAD
        pygame.draw.rect(window, RED, base1.rect, 2)  # Pour visualiser la base1
        pygame.draw.rect(window, RED, base2.rect, 2)  # Pour visualiser la base2
        #pygame.draw.rect(window, GREEN, box.rect, 12)  # Pour visualiser la boîte
        
        # Mise à jour de l'affichage
=======
>>>>>>> a254b830b9b8691cfa05dcebc9a4af9656bc6ebb
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and run:
                    if isinstance(base1, Base):  # Vérifier que c'est bien un tank
                        base1.fire()  # Le tank tire

                if event.key == pygame.K_RETURN and run:
                    if isinstance(base2, Base):  # Vérifier que c'est bien un tank
                        base2.fire()  # Le tank tire

        # Gestion des balles
        for tank in base_group:
            if isinstance(tank, Base):  # Vérifier que l'objet est un tank
                tank.handle_bullets(tank, delta_time, box)

        # Rendre les balles à l'écran
        for tank in base_group:
            if isinstance(tank, Base):  # Vérifier que l'objet est un tank
                tank.handle_bullets(base_group, delta_time, box)  # Passer le groupe de tanks (base_group) au lieu d'un seul tank

        clock.tick(FPS)

main(window, clock)
pygame.quit()