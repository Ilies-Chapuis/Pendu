import pygame
import random

# ---------- FONCTIONS ----------

def charger_mots(fichier_txt):
    try:
        with open(fichier_txt, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return []

def ajouter_mot(fichier_txt, mot):
    with open(fichier_txt, "a", encoding="utf-8") as f:
        f.write("\n" + mot)

def choisir_mot(liste_mots):
    return random.choice(liste_mots)

def mot_cache(mot_secret, lettres_trouvees):
    affichage = ""
    for lettre in mot_secret:
        if lettre in lettres_trouvees:
            affichage += lettre + " "
        else:
            affichage += "_ "
    return affichage

def enregistrer_score(mot, erreurs, max_erreurs):
    score = max_erreurs - erreurs
    with open("score.txt", "a", encoding="utf-8") as f:
        f.write(f"{mot},{score},{erreurs}\n")

def lire_scores():
    scores = []
    try:
        with open("score.txt", "r", encoding="utf-8") as f:
            for ligne in f:
                mot, score, erreurs = ligne.strip().split(",")
                scores.append((mot, int(score), int(erreurs)))
    except FileNotFoundError:
        pass
    return scores

def afficher_scores(screen, font):
    screen.fill("white")
    screen.blit(font.render("SCORES", True, "black"), (520, 100))

    scores = lire_scores()
    y = 200

    if not scores:
        screen.blit(font.render("Aucun score", True, "red"), (480, y))
    else:
        for mot, score, erreurs in scores[-5:]:
            texte = f"{mot} | Score : {score} | Erreurs : {erreurs}"
            screen.blit(font.render(texte, True, "black"), (300, y))
            y += 50

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

def afficher_menu(screen, font):
    screen.fill("white")
    screen.blit(font.render("JEU DU PENDU", True, "black"), (450, 200))
    screen.blit(font.render("1 - Jouer", True, "blue"), (500, 300))
    screen.blit(font.render("2 - Scores", True, "green"), (500, 370))
    screen.blit(font.render("3 - Ajouter un mot", True, "purple"), (500, 440))
    screen.blit(font.render("4 - Quitter", True, "red"), (500, 510))


# ---------- SETUP ----------

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Jeu du pendu")
font = pygame.font.Font(None, 64)
clock = pygame.time.Clock()

icone_menu = pygame.image.load("home.png")
icone_menu = pygame.transform.scale(icone_menu, (64, 64))
icone_menu_rect = icone_menu.get_rect(topleft=(15, 15))

liste_mots = charger_mots("mots.txt")

Max_Erreurs = 7
etat = "menu"
running = True

lettres_trouvees = []
lettres_ratees = []
partie_terminee = False
message = ""
mot_secret = ""
mot_ajout = ""

# ---------- BOUCLE PRINCIPALE ----------

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ---------- MAISON : RETOUR MENU ----------
        if event.type == pygame.MOUSEBUTTONDOWN:
            if icone_menu_rect.collidepoint(event.pos):
                etat = "menu"
                lettres_trouvees = []
                lettres_ratees = []
                partie_terminee = False
                message = ""

        # ---------- MENU ----------
        if etat == "menu" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mot_secret = choisir_mot(liste_mots)
                lettres_trouvees = []
                lettres_ratees = []
                partie_terminee = False
                message = ""
                etat = "jeu"

            elif event.key == pygame.K_2:
                etat = "scores"

            elif event.key == pygame.K_3:
                mot_ajout = ""
                etat = "ajout"

            elif event.key == pygame.K_4:
                running = False

        # ---------- AJOUT MOT ----------
        if etat == "ajout" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and mot_ajout != "":
                ajouter_mot("mots.txt", mot_ajout.lower())
                liste_mots = charger_mots("mots.txt")
                etat = "menu"

            elif event.key == pygame.K_BACKSPACE:
                mot_ajout = mot_ajout[:-1]

            elif event.unicode.isalpha():
                mot_ajout += event.unicode.lower()

        # ---------- JEU ----------
        if etat == "jeu" and event.type == pygame.KEYDOWN and not partie_terminee:
            lettre = event.unicode.lower()
            if lettre.isalpha():
                if lettre in mot_secret and lettre not in lettres_trouvees:
                    lettres_trouvees.append(lettre)
                elif lettre not in mot_secret and lettre not in lettres_ratees:
                    lettres_ratees.append(lettre)

    # ---------- LOGIQUE JEU ----------
    if etat == "jeu":
        erreurs = len(lettres_ratees)
        gagne = all(lettre in lettres_trouvees for lettre in mot_secret)

        if not partie_terminee:
            if erreurs >= Max_Erreurs:
                partie_terminee = True
                message = "Perdu : " + mot_secret
                enregistrer_score(mot_secret, erreurs, Max_Erreurs)

            elif gagne:
                partie_terminee = True
                message = "Gagné !"
                enregistrer_score(mot_secret, erreurs, Max_Erreurs)

    # ---------- AFFICHAGE ----------
    if etat == "menu":
        afficher_menu(screen, font)

    elif etat == "scores":
        afficher_scores(screen, font)

    elif etat == "ajout":
        screen.fill("white")
        screen.blit(font.render("Ajouter un mot :", True, "black"), (400, 250))
        screen.blit(font.render(mot_ajout, True, "blue"), (400, 320))

    elif etat == "jeu":
        screen.fill("white")
        dessin_pendu(screen, len(lettres_ratees))
        screen.blit(font.render(mot_cache(mot_secret, lettres_trouvees), True, "black"), (100, 300))
        screen.blit(font.render(f"Erreurs : {len(lettres_ratees)} / {Max_Erreurs}", True, "black"), (50, 100))
        screen.blit(font.render("Lettres Ratées : " + " ".join(lettres_ratees), True, "red"), (50, 630))

        if partie_terminee:
            screen.blit(font.render(message, True, "blue"), (100, 200))

    # ---------- ICÔNE MAISON ----------
    if etat != "menu":
        screen.blit(icone_menu, icone_menu_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
