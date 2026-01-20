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