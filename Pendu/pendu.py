import pygame
import random

# ---------- FONCTIONS ----------

def charger_mots(fichier_txt):
    try:
        fichier = open(fichier_txt, "r", encoding="utf-8")
        mots = fichier.read().splitlines()
        fichier.close()
        if not mots:
            print(f"Attention : {fichier_txt} est vide. Liste de mots par défaut utilisée.")
            return ["python", "pendu", "jeu"]
        return mots
    except FileNotFoundError:
        print(f"Attention : {fichier_txt} introuvable. Liste de mots par défaut utilisée.")
        return ["python", "pendu", "jeu"]
    except Exception as e:
        print(f"Erreur lors du chargement de {fichier_txt} :", e)
        return ["python", "pendu", "jeu"]

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
    try:
        with open("score.txt", "a", encoding="utf-8") as f:
            f.write(f"{mot},{score},{erreurs}\n")
    except Exception as e:
        print("Erreur lors de l'enregistrement du score :", e)

def lire_historique():
    historique = []

    try:
        with open("score.txt", "r", encoding="utf-8") as f:
            for ligne in f:
                mot, score, erreurs = ligne.strip().split(",")
                historique.append((mot, int(score), int(erreurs)))
    except FileNotFoundError:
        pass
    except Exception as e:
        print("Erreur lors de la lecture des scores :", e)

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

    retour = font.render("ECHAP - Retour au menu", True, "blue")
    screen.blit(retour, (420, 600))

def meilleur_score():
    historique = lire_historique()
    if not historique:
        return None
    return max(historique, key=lambda x: x[1])

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

    titre = font.render("JEU DU PENDU", True, "black")
    jouer = font.render("1 - Jouer", True, "blue")
    scores = font.render("2 - Scores", True, "green")
    ajouter = font.render("3 - Ajouter un mot", True, "orange")
    quitter = font.render("4 - Quitter", True, "red")

    screen.blit(titre, (450, 200))
    screen.blit(jouer, (500, 300))
    screen.blit(scores, (500, 370))
    screen.blit(ajouter, (500, 440))
    screen.blit(quitter, (500, 510))

def afficher_difficulte(screen, font):
    screen.fill("white")

    titre = font.render("DIFFICULTÉ", True, "black")
    facile = font.render("1 - Facile", True, "green")
    normal = font.render("2 - Normal", True, "blue")
    difficile = font.render("3 - Difficile", True, "red")

    screen.blit(titre, (480, 200))
    screen.blit(facile, (500, 300))
    screen.blit(normal, (500, 370))
    screen.blit(difficile, (500, 440))

# ---------- NOUVELLE FONCTION : AJOUTER UN MOT ----------

def ajouter_mot(fichier_txt, nouveau_mot):
    """
    Ajoute un mot à la liste si il est valide.
    Gestion d'erreurs : mot vide, chiffres ou caractères spéciaux, mot déjà existant.
    """
    nouveau_mot = nouveau_mot.strip().lower()

    if not nouveau_mot:
        print("Erreur : le mot ne peut pas être vide.")
        return False

    if not nouveau_mot.isalpha():
        print("Erreur : le mot doit contenir uniquement des lettres.")
        return False

    # Charger la liste existante
    mots = []
    try:
        with open(fichier_txt, "r", encoding="utf-8") as f:
            mots = [mot.strip().lower() for mot in f.readlines()]
    except FileNotFoundError:
        pass

    if nouveau_mot in mots:
        print("Erreur : le mot existe déjà dans la liste.")
        return False

    # Ajouter le mot
    try:
        with open(fichier_txt, "a", encoding="utf-8") as f:
            f.write(nouveau_mot + "\n")
        print(f"Mot '{nouveau_mot}' ajouté avec succès !")
        return True
    except Exception as e:
        print("Erreur lors de l'ajout du mot :", e)
        return False

# ---------- PYGAME SETUP ----------

try:
    pygame.init()
    font = pygame.font.Font(None, 64)
    screen = pygame.display.set_mode((1280, 720))
except Exception as e:
    print("Erreur lors de l'initialisation de Pygame :", e)
    exit()

clock = pygame.time.Clock()

try:
    icone_menu = pygame.image.load("home.png")
    icone_menu = pygame.transform.scale(icone_menu, (64, 64))
    icone_menu_rect = icone_menu.get_rect(topleft=(15, 15))
except Exception as e:
    print("Erreur lors du chargement de l'icône :", e)
    icone_menu = pygame.Surface((64, 64))
    icone_menu.fill((0, 0, 0))
    icone_menu_rect = icone_menu.get_rect(topleft=(15, 15))

# Gestion d'erreurs si mots.txt absent ou vide
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
                    etat = "ajouter"

                elif event.key == pygame.K_4:
                    running = False

        afficher_le_menu(screen, font)
        pygame.display.flip()
        clock.tick(60)
        continue

    # ---------- AJOUTER UN MOT ----------
    if etat == "ajouter":
        screen.fill("white")
        titre = font.render("Ajouter un mot", True, "black")
        instruction = font.render("Tapez le mot et appuyez sur Entrée", True, "blue")
        screen.blit(titre, (400, 200))
        screen.blit(instruction, (200, 300))
        pygame.display.flip()

        mot_temp = ""
        ajouter_en_cours = True

        while ajouter_en_cours:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    ajouter_en_cours = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if ajouter_mot("mots.txt", mot_temp):
                            liste_mots = charger_mots("mots.txt")
                        mot_temp = ""
                        ajouter_en_cours = False
                        etat = "menu"

                    elif event.key == pygame.K_BACKSPACE:
                        mot_temp = mot_temp[:-1]

                    else:
                        if event.unicode.isalpha():
                            mot_temp += event.unicode.lower()

            screen.fill("white")
            screen.blit(titre, (400, 200))
            screen.blit(instruction, (200, 300))
            texte_mot = font.render(mot_temp, True, "red")
            screen.blit(texte_mot, (500, 400))
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
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

    ETAPES_DESSIN = 7
    erreurs_dessin = int((erreurs / Max_Erreurs) * ETAPES_DESSIN)
    if erreurs_dessin > ETAPES_DESSIN:
        erreurs_dessin = ETAPES_DESSIN

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
    dessin_pendu(screen, erreurs_dessin)

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