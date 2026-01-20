import pygame
import random


MOTS_FILE = "mots.txt"

def load_words():
    with open(MOTS_FILE, "r", encoding="utf-8") as f:
        return [w.strip().lower() for w in f if w.strip()]

def save_word(word):
    with open(MOTS_FILE, "a", encoding="utf-8") as f:
        f.write(word.lower() + "\n")

def game():
    max_errors = choose_difficulty()
    word = random.choice(load_words())
    guessed = set()
    errors = 0
    score = 0

    while True:
        screen.fill(WHITE)
        draw_pendu(errors)

        display_word = " ".join([l if l in guessed else "_" for l in word])
        draw_text(display_word, 200)
        draw_text(f"Erreurs: {errors}/{max_errors}", 260)
        draw_text(f"Score: {score}", 310)

        pygame.display.flip()
        CLOCK.tick(60)

        if "_" not in display_word:
            score += 50
            end_game(True, score)
            return

        if errors >= max_errors:
            end_game(False, score, word)
            return

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                letter = event.unicode.lower()
                if letter.isalpha() and letter not in guessed:
                    guessed.add(letter)
                    if letter in word:
                        score += 10
                    else:
                        errors += 1
                        error_animation()

def end_game(win, score, word=None):
    name = ""
    while True:
        screen.fill(WHITE)
        if win:
            draw_text("GAGNÉ !", 150)
        else:
            draw_text("PERDU !", 150)
            draw_text(f"Mot : {word}", 200)

        draw_text("Entrez votre nom :", 300)
        draw_text(name, 350)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    save_score(name, score)
                    return
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10:
                        name += event.unicode

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