import pygame
import random
import sys


pygame.init()

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meilleur Pendu")

FONT = pygame.font.SysFont("arial", 32)
SMALL_FONT = pygame.font.SysFont("arial", 24)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)

CLOCK = pygame.time.Clock()

MOTS_FILE = "mots.txt"
SCORES_FILE = "scores.txt"

# fichier.txt/score
def load_words():
    with open(MOTS_FILE, "r", encoding="utf-8") as f:
        return [w.strip().lower() for w in f if w.strip()]

def save_word(word):
    with open(MOTS_FILE, "a", encoding="utf-8") as f:
        f.write(word.lower() + "\n")

def save_score(name, score):
    with open(SCORES_FILE, "a", encoding="utf-8") as f:
        f.write(f"{name}:{score}\n")

def load_scores():
    scores = []
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                name, score = line.strip().split(":")
                scores.append((name, int(score)))
    except:
        pass
    return sorted(scores, key=lambda x: x[1], reverse=True)

# dessin du pendu
def draw_pendu(errors):
    # potence
    pygame.draw.line(screen, BLACK, (150, 450), (350, 450), 5)
    pygame.draw.line(screen, BLACK, (250, 450), (250, 150), 5)
    pygame.draw.line(screen, BLACK, (250, 150), (350, 150), 5)
    pygame.draw.line(screen, BLACK, (350, 150), (350, 200), 5)

    if errors > 0:  # tête
        pygame.draw.circle(screen, BLACK, (350, 230), 30, 4)
    if errors > 1:  # corps
        pygame.draw.line(screen, BLACK, (350, 260), (350, 350), 4)
    if errors > 2:  # bras gauche
        pygame.draw.line(screen, BLACK, (350, 280), (320, 320), 4)
    if errors > 3:  # bras droit
        pygame.draw.line(screen, BLACK, (350, 280), (380, 320), 4)
    if errors > 4:  # jambe gauche
        pygame.draw.line(screen, BLACK, (350, 350), (320, 400), 4)
    if errors > 5:  # jambe droite
        pygame.draw.line(screen, BLACK, (350, 350), (380, 400), 4)

# animation lorsqu'on se trompe
def error_animation():
    for i in range(6):
        offset = (-5 if i % 2 == 0 else 5)
        screen.fill((255, 180, 180))
        pygame.display.update()
        pygame.time.delay(30)
        screen.scroll(offset, 0)
        pygame.display.update()

# menu
def draw_text(text, y):
    render = FONT.render(text, True, BLACK)
    rect = render.get_rect(center=(WIDTH//2, y))
    screen.blit(render, rect)

def menu():
    while True:
        screen.fill(WHITE)
        draw_text("MEILLEUR PENDU", 100)
        draw_text("1 - Jouer", 220)
        draw_text("2 - Ajouter un mot", 270)
        draw_text("3 - Tableau des scores", 320)
        draw_text("4 - Quitter", 370)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game()
                elif event.key == pygame.K_2:
                    add_word()
                elif event.key == pygame.K_3:
                    show_scores()
                elif event.key == pygame.K_4:
                    pygame.quit()
                    sys.exit()

def choose_difficulty():
    while True:
        screen.fill(WHITE)
        draw_text("Choisir difficulté", 150)
        draw_text("1 - Facile (6 erreurs)", 250)
        draw_text("2 - Moyen (5 erreurs)", 300)
        draw_text("3 - Difficile (4 erreurs)", 350)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 6
                elif event.key == pygame.K_2:
                    return 5
                elif event.key == pygame.K_3:
                    return 4


def add_word():
    word = ""
    while True:
        screen.fill(WHITE)
        draw_text("Ajouter un mot", 200)
        draw_text(word, 260)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and word.isalpha():
                    save_word(word)
                    return
                elif event.key == pygame.K_BACKSPACE:
                    word = word[:-1]
                else:
                    word += event.unicode

def show_scores():
    scores = load_scores()
    screen.fill(WHITE)
    draw_text("TABLEAU DES SCORES", 100)

    y = 180
    for name, score in scores[:10]:
        txt = SMALL_FONT.render(f"{name} : {score}", True, BLACK)
        screen.blit(txt, (WIDTH//2 - 100, y))
        y += 30

    pygame.display.flip()
    pygame.time.wait(3000)

menu()
