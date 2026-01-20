import pygame
from pygame.locals import*


def scoremenu():
    print("Look at your high score : 1")
    print("Look at your recent scores : 2")
    Choice = input("Choose between the 2 choices : ")

    if Choice == K_1:
        highscore()

    elif Choice == K_2:
        recentscores()


def highscore():
    with open("scores.txt", "r", encoding="utf-8"):


def recentscores():
    with open("scores.txt", "r", encoding="utf-8"):