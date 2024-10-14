# Création d'instances

base1 = Base(100, 100, 0)
curseur = Curseur()
box = Box(WIDTH /2 , HEIGHT / 2, 200, 200)
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
        #pygame.draw.rect(window, GREEN, box.rect, 12)  # Pour visualiser la boîte
        
        # Mise à jour de l'affichage
        pygame.display.flip()
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        clock.tick(FPS)

main(window, clock)
pygame.quit()