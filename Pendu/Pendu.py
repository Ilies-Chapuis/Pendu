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

def enregistrer_les_scores(mot, erreurs, max_erreurs):
    score = max_erreurs - erreurs
    with open("score.txt", "a", encoding="utf-8") as f:
        f.write(f"{mot},{score},{erreurs}\n")

def lire_historique():
    historique = []
    try:
        with open("score.txt", "r", encoding="utf-8") as f:
            for ligne in f:
                mot, score, erreurs = ligne.strip().split(",")
                historique.append((mot, int(score), int(erreurs)))
    except FileNotFoundError:
        pass
    return historique

def afficher_les_scores(screen, font):
    screen.fill("white")

    titre = font.render("SCORES", True, "black")
    screen.blit(titre, (520, 100))

    historique = lire_historique()
    y = 200

    if not historique:
        screen.blit(font.render("Aucun score enregistré", True, "red"), (450, y))
    else:
        for mot, score, erreurs in historique[-5:]:
            texte = f"Mot : {mot} | Score : {score} | Erreurs : {erreurs}"
            screen.blit(font.render(texte, True, "black"), (300, y))
            y += 50

    screen.blit(font.render("ECHAP - Retour au menu", True, "blue"), (420, 600))

def dessin_pendu(screen, erreurs):
    if erreurs >= 1:
        pygame.draw.line(screen, "black", (850, 500), (1100, 500), 5)
        if erreurs >= 2:
            pygame.draw.line(screen, "black", (900, 500), (900, 150), 5)
            if erreurs >= 3:
                pygame.draw.line(screen, "black", (900, 150), (1050, 150), 5)
                if erreurs >= 4:
                    pygame.draw.line(screen, "black", (1050, 150), (1050, 200), 5)
                    if erreurs >= 5:
                        pygame.draw.circle(screen, "black", (1050, 240), 40, 5)
                        if erreurs >= 6:
                            pygame.draw.line(screen, "black", (1050, 280), (1050, 380), 5)
                            if erreurs >= 7:
                                pygame.draw.line(screen, "black", (1050, 310), (1000, 350), 5)
                                pygame.draw.line(screen, "black", (1050, 310), (1100, 350), 5)
                                pygame.draw.line(screen, "black", (1050, 380), (1000, 450), 5)
                                pygame.draw.line(screen, "black", (1050, 380), (1100, 450), 5)

def afficher_le_menu(screen, font):
    screen.fill("white")
    screen.blit(font.render("JEU DU PENDU", True, "black"), (450, 200))
    screen.blit(font.render("1 - Jouer", True, "blue"), (500, 300))
    screen.blit(font.render("2 - Scores", True, "green"), (500, 370))
    screen.blit(font.render("3 - Quitter", True, "red"), (500, 440))

def afficher_difficulte(screen, font):
    screen.fill("white")
    screen.blit(font.render("Choisir la difficulté", True, "black"), (430, 200))
    screen.blit(font.render("1 - Facile (10 erreurs)", True, "green"), (430, 300))
    screen.blit(font.render("2 - Normal (7 erreurs)", True, "blue"), (430, 370))
    screen.blit(font.render("3 - Difficile (5 erreurs)", True, "red"), (430, 440))

# ---------- SETUP ----------

pygame.init()
font = pygame.font.Font(None, 64)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

icone_menu = pygame.image.load("home.png")
icone_menu = pygame.transform.scale(icone_menu, (64, 64))
icone_menu_rect = icone_menu.get_rect(topleft=(15, 15))

liste_mots = charger_mots("mots.txt")

lettres_trouvees = []
lettres_ratees = []

Max_Erreurs = 7
partie_terminee = False
message = ""

bouton_rect = pygame.Rect(500, 400, 280, 70)

running = True
etat = "menu"

# ---------- BOUCLE PRINCIPALE ----------

while running:

    # ---------- MENU ----------
    if etat == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    etat = "difficulte"
                elif event.key == pygame.K_2:
                    etat = "scores"
                elif event.key == pygame.K_3:
                    running = False

        afficher_le_menu(screen, font)
        pygame.display.flip()
        clock.tick(60)
        continue

    # ---------- DIFFICULTÉ ----------
    if etat == "difficulte":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    Max_Erreurs = 10
                elif event.key == pygame.K_2:
                    Max_Erreurs = 7
                elif event.key == pygame.K_3:
                    Max_Erreurs = 5
                else:
                    continue

                mot_secret = choisir_mots(liste_mots)
                lettres_trouvees = []
                lettres_ratees = []
                partie_terminee = False
                message = ""
                etat = "jeu"

        afficher_difficulte(screen, font)
        pygame.display.flip()
        clock.tick(60)
        continue

    # ---------- SCORES ----------
    if etat == "scores":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                etat = "menu"

        afficher_les_scores(screen, font)
        pygame.display.flip()
        clock.tick(60)
        continue

    # ---------- JEU ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not partie_terminee:
            lettre = event.unicode.lower()
            if lettre.isalpha():
                if lettre in mot_secret and lettre not in lettres_trouvees:
                    lettres_trouvees.append(lettre)
                elif lettre not in mot_secret and lettre not in lettres_ratees:
                    lettres_ratees.append(lettre)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if icone_menu_rect.collidepoint(event.pos):
                etat = "menu"

            if partie_terminee and bouton_rect.collidepoint(event.pos):
                etat = "difficulte"

    erreurs = len(lettres_ratees)

    gagne = True
    for lettre in mot_secret:
        if lettre not in lettres_trouvees:
            gagne = False

    if not partie_terminee:
        if erreurs >= Max_Erreurs:
            partie_terminee = True
            message = "Perdu, le mot était : " + mot_secret
            enregistrer_les_scores(mot_secret, erreurs, Max_Erreurs)
        elif gagne:
            partie_terminee = True
            message = "Félicitations vous avez gagné"
            enregistrer_les_scores(mot_secret, erreurs, Max_Erreurs)

    screen.fill("white")
    dessin_pendu(screen, erreurs)

    screen.blit(font.render(f"Erreurs : {erreurs} / {Max_Erreurs}", True, "black"), (30, 100))
    screen.blit(font.render("Lettres ratées : " + " ".join(lettres_ratees), True, "red"), (50, 630))
    screen.blit(font.render(mot_cache(mot_secret, lettres_trouvees), True, "black"), (100, 300))

    if partie_terminee:
        screen.blit(font.render(message, True, "blue"), (100, 200))
        pygame.draw.rect(screen, "green", bouton_rect)
        screen.blit(font.render("Rejouer", True, "black"), (bouton_rect.x + 50, bouton_rect.y + 15))

    screen.blit(icone_menu, icone_menu_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
