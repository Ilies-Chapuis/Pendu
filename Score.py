import pygame
import sys
from pygame.locals import*

Score = 0
Attempts = 10

def scoremenu():

    print("Look at your high score : 1")
    print("Look at your recent scores : 2")

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                highscore()
            elif event.key == pygame.K_2:
                recentscores()
            elif event.key == pygame.K_3:
                menu()
            elif event.key == pygame.K_4:
                pygame.quit

def pointobtained():

    if guess in secret_word:
        Score += 1
        print(f"Good answer, your score : {Score}")
    else:
        Attempts -= 1
        print(f"Wrong answer, attempts left : {Attempts}")
    

def highscore():
    with open("scores.txt", "r", encoding="utf-8"):
        pass


def recentscores():
    with open("scores.txt", "r", encoding="utf-8"):
        pass