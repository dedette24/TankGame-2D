from MEU.parametre import *

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