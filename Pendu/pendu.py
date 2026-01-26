import pygame
import random
import time


# Les FONCTIONS

def charger_mots(fichier_txt):
    #Charge les mots depuis un fichier
    try:
        with open(fichier_txt, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return []


def choisir_mots(liste_mots):
    #Choisit un mot aléatoire
    return random.choice(liste_mots)


def mot_cache(mot_secret, lettres_trouvees):
    #Affiche le mot caché
    affichage = ""
    for lettre in mot_secret:
        if lettre in lettres_trouvees:
            affichage += lettre + " "
        else:
            affichage += "_ "
    return affichage


def enregistrer_les_scores(mot, erreurs, max_erreurs):
    #Enregistre un score
    score = max_erreurs - erreurs
    with open("score.txt", "a", encoding="utf-8") as f:
        f.write(f"{mot},{score},{erreurs}\n")


def lire_historique():
    #Lit l'historique des scores
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
    #Affiche l'écran des scores
    screen.fill("white")
    screen.blit(font.render("SCORES", True, "black"), (520, 100))

    historique = lire_historique()
    y = 200

    if not historique:
        screen.blit(font.render("Aucun score enregistré", True, "red"), (430, y))
    else:
        for mot, score, erreurs in historique[-5:]:
            txt = f"{mot} | Score : {score} | Erreurs : {erreurs}"
            screen.blit(font.render(txt, True, "black"), (350, y))
            y += 50

    screen.blit(font.render("ECHAP - Retour menu", True, "blue"), (420, 600))


def meilleur_score():
    #Retourne le meilleur score
    historique = lire_historique()
    if not historique:
        return None
    return max(historique, key=lambda x: x[1])


def dessin_pendu(screen, erreurs):
    #Dessine le pendu selon les erreurs
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
    #Menu principal
    screen.fill("white")
    screen.blit(font.render("JEU DU PENDU", True, "black"), (450, 200))
    screen.blit(font.render("1 - Jouer", True, "blue"), (500, 300))
    screen.blit(font.render("2 - Scores", True, "green"), (500, 360))
    screen.blit(font.render("3 - Ajouter un mot", True, "purple"), (500, 420))
    screen.blit(font.render("4 - Quitter", True, "red"), (500, 480))


def afficher_difficulte(screen, font):
    #Choix de difficulté
    screen.fill("white")
    screen.blit(font.render("CHOIX DIFFICULTÉ", True, "black"), (430, 200))
    screen.blit(font.render("1 - Facile (5 min)", True, "green"), (450, 300))
    screen.blit(font.render("2 - Normal (2 min)", True, "orange"), (450, 360))
    screen.blit(font.render("3 - Difficile (30 sec)", True, "red"), (450, 420))


def ajouter_mot(fichier, mot):
    #Ajoute un mot avec gestion d'erreurs
    mot = mot.strip().lower()

    if mot == "":
        return False, "Mot vide"
    elif not mot.isalpha():
        return False, "Lettres uniquement"
    elif len(mot) < 3:
        return False, "Mot trop court"
    elif len(mot) > 24:
        return False, "Mot trop long"

    mots_existants = charger_mots(fichier)
    if mot in mots_existants:
        return False, "Mot déjà existant"

    with open(fichier, "a", encoding="utf-8") as f:
        f.write(mot + "\n")

    return True, "Mot ajouté !"



#  INITIALISATION

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Meilleur Pendu")
font = pygame.font.Font(None, 64)
clock = pygame.time.Clock()

icone_menu = pygame.image.load("home.png")
icone_menu = pygame.transform.scale(icone_menu, (64, 64))
icone_rect = icone_menu.get_rect(topleft=(5, 5))

liste_mots = charger_mots("mots.txt")

etat = "menu"
Max_Erreurs = 7
temps_max = 0
start_time = 0

lettres_trouvees = []
lettres_erronée = []
partie_terminee = False
message = ""

mot_a_ajouter = ""
message_ajout = ""
couleur_message = "red"

bouton_rect = pygame.Rect(500, 400, 280, 70)

running = True


#  BOUCLE PRINCIPALE =


while running:
    clock.tick(60)

    #  MENU
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
                    etat = "ajout"
                elif event.key == pygame.K_4:
                    running = False

        afficher_menu(screen, font)
        pygame.display.flip()
        continue

    #  DIFFICULTÉ
    if etat == "difficulte":
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    temps_max = 300
                elif event.key == pygame.K_2:
                    temps_max = 120
                elif event.key == pygame.K_3:
                    temps_max = 30
                else:
                    continue

                mot_secret = choisir_mots(liste_mots)
                lettres_trouvees = []
                lettres_erronée = []
                partie_terminee = False
                start_time = time.time()
                etat = "jeu"

        afficher_difficulte(screen, font)
        pygame.display.flip()
        continue

    #  AJOUT MOT
    if etat == "ajout":
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    success, message_ajout = ajouter_mot("mots.txt", mot_a_ajouter)
                    couleur_message = "green" if success else "red"
                    mot_a_ajouter = ""
                elif event.key == pygame.K_BACKSPACE:
                    mot_a_ajouter = mot_a_ajouter[:-1]
                elif event.key == pygame.K_ESCAPE:
                    etat = "menu"
                else:
                    mot_a_ajouter += event.unicode

        screen.fill("white")
        screen.blit(font.render("AJOUTER UN MOT", True, "black"), (420, 200))
        screen.blit(font.render(mot_a_ajouter, True, "blue"), (450, 300))
        screen.blit(font.render(message_ajout, True, couleur_message), (420, 360))
        pygame.display.flip()
        continue

    #  SCORES
    if etat == "scores":
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                etat = "menu"

        afficher_les_scores(screen, font)
        pygame.display.flip()
        continue

    #  JEU
    temps_restant = int(temps_max - (time.time() - start_time))
    if temps_restant <= 0 and not partie_terminee:
        partie_terminee = True
        message = "Temps écoulé !"

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and not partie_terminee:
            lettre = event.unicode.lower()
            if lettre.isalpha():
                if lettre in mot_secret and lettre not in lettres_trouvees:
                    lettres_trouvees.append(lettre)
                elif lettre not in mot_secret and lettre not in lettres_erronée:
                    lettres_erronée.append(lettre)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if icone_rect.collidepoint(event.pos):
                etat = "menu"

    erreurs = len(lettres_erronée)

    if not partie_terminee:
        if erreurs >= Max_Erreurs:
            partie_terminee = True
            message = f"Perdu ! Mot : {mot_secret}"
        elif all(l in lettres_trouvees for l in mot_secret):
            partie_terminee = True
            message = "Gagné !"

    screen.fill("white")
    dessin_pendu(screen, erreurs)

    screen.blit(font.render(f"Temps : {temps_restant}s", True, "black"), (30, 50))
    screen.blit(font.render(mot_cache(mot_secret, lettres_trouvees), True, "black"), (100, 300))
    screen.blit(font.render("Erreurs : " + " ".join(lettres_erronée), True, "red"), (50, 630))

    if partie_terminee:
        screen.blit(font.render(message, True, "blue"), (100, 200))

    screen.blit(icone_menu, icone_rect)
    pygame.display.flip()

pygame.quit()
