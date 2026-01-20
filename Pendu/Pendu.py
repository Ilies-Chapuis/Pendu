import pygame
import random

#mettre boucle randomn

def charger_mots(fichier_txt):
    fichier = open(fichier_txt, "r")
    mots= fichier.read().splitlines()
    fichier.close()
    return mots

def choisir_mots(liste_mots):
    return random.choice(liste_mots)

def mot_cache(mot_secret, lettres_trouvees):
    affichage = ""

    for lettre in mot_secret:
        if lettre in lettres_trouvees:
            affichage += lettre + " "
        else:
            affichage += "_ "

    return affichage

# pygame setup
pygame.init()
font = pygame.font.Font(None, 64)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

liste_mots=charger_mots("mots.txt")
mot_secret=choisir_mots(liste_mots)

running = True

lettres_trouvees=[]

 # poll for events
    # pygame.QUIT event means the user clicked X to close your window

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    
    texte=mot_cache(mot_secret, lettres_trouvees)
    texte_surface= font.render(texte, True, "black")
    screen.blit(texte_surface, (100, 300))

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()