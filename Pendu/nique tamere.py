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
        f.write(f"{mot},{score}, {erreurs}\n")


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

                                # jambes
                                pygame.draw.line(screen, "black", (1050, 380), (1000, 450), 5)
                                pygame.draw.line(screen, "black", (1050, 380), (1100, 450), 5)


# ---------- PYGAME SETUP ----------

pygame.init()
font = pygame.font.Font(None, 64)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

liste_mots = charger_mots("mots.txt")
mot_secret = choisir_mots(liste_mots)

lettres_trouvees = []
lettres_ratees = []

Max_Erreurs = 7
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

        if event.type == pygame.MOUSEBUTTONDOWN and partie_terminee:
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
            enregistrer_les_scores(mot_secret, erreurs, Max_Erreurs)

        elif gagne:
            partie_terminee = True
            message = "Félicitations vous avez gagné"
            enregistrer_les_scores(mot_secret, erreurs, Max_Erreurs)

    # --- AFFICHAGE ---
    screen.fill("white")
    dessin_pendu(screen, erreurs)

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
