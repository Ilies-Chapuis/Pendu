import pygame
import random

# ---------- FONCTIONS ----------

def charger_mots(fichier_txt):
    fichier = open(fichier_txt, "r")
    mots = fichier.read().splitlines()
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


# ---------- PYGAME SETUP ----------

pygame.init()
font = pygame.font.Font(None, 64)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

liste_mots = charger_mots("mots.txt")
mot_secret = choisir_mots(liste_mots)

lettres_trouvees = []
lettres_ratees = []

Max_Erreurs = 6
partie_terminee = False
message = ""

running = True

bouton_rect = pygame.Rect(500, 400, 280, 70)

# ---------- BOUCLE PRINCIPALE ----------

while running:

    # --- EVENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not partie_terminee:
            lettre = event.unicode.lower()

            if lettre != "" and lettre.isalpha():
                if lettre in mot_secret and lettre not in lettres_trouvees:
                    lettres_trouvees.append(lettre)
                elif lettre not in mot_secret and lettre not in lettres_ratees:
                    lettres_ratees.append(lettre)

        if event.type ==pygame.MOUSEBUTTONDOWN and partie_terminee:
            if bouton_rect.collidepoint(event.pos):
                mot_secret = choisir_mots(liste_mots)
                lettres_trouvees = []
                lettres_ratees = []
                partie_terminee = False
                message = ""

    # --- LOGIQUE ---
    erreurs = len(lettres_ratees)

    gagne = True
    for lettre in mot_secret:
        if lettre not in lettres_trouvees:
            gagne = False

    if not partie_terminee:
        if erreurs >= Max_Erreurs:
            partie_terminee = True
            message = "Perdu, le mot était : " + mot_secret
        elif gagne:
            partie_terminee = True
            message = "Félicitations vous avez gagné"

    # --- AFFICHAGE ---
    screen.fill("white")

    texte_erreurs = f"Erreurs : {erreurs} / {Max_Erreurs}"
    screen.blit(font.render(texte_erreurs, True, "black"), (50, 50))

    texte_ratees = "Lettres ratées : " + " ".join(lettres_ratees)
    screen.blit(font.render(texte_ratees, True, "red"), (50, 630))

    texte = mot_cache(mot_secret, lettres_trouvees)
    screen.blit(font.render(texte, True, "black"), (100, 300))

    if partie_terminee:
        screen.blit(font.render(message, True, "blue"), (100, 200))
        pygame.draw.rect(screen, "green", bouton_rect)
        screen.blit(font.render("Rejouer", True, "black"), (bouton_rect.x + 50, bouton_rect.y + 15))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
