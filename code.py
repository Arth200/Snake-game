import pygame
import random
import pygame_menu

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Définition de la taille de l'écran
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Définition de la taille d'une cellule du serpent
CELL_SIZE = 20

# Définition de la vitesse de déplacement
SNAKE_SPEED = 10

# Définition de la police de caractères
font = pygame.font.SysFont(None, 36)

# Définition du thème personnalisé pour le jeu
game_theme = pygame_menu.themes.THEME_GREEN.copy()
game_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
game_theme.title_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
game_theme.widget_margin = (0, 5)
game_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
game_theme.title_offset = (5, -5)

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Fonction pour initialiser le serpent dans une zone sûre au centre de l'écran
def initialize_snake():
    x = SCREEN_WIDTH // 2
    y = SCREEN_HEIGHT // 2
    snake = [(x, y), (x - CELL_SIZE, y), (x - 2 * CELL_SIZE, y)]
    return snake

# Fonction principale pour exécuter le jeu
def game():
    # Position initiale du serpent
    snake = initialize_snake()
    snake_direction = "RIGHT"

    # Position initiale de la pomme
    apple_position = (random.randint(0, (SCREEN_WIDTH - CELL_SIZE) // CELL_SIZE - 1) * CELL_SIZE,
                      random.randint(0, (SCREEN_HEIGHT - CELL_SIZE) // CELL_SIZE - 1) * CELL_SIZE)

    # Variable pour savoir si le jeu est terminé
    game_over = False

    # Score initial
    score = 0

    # Boucle principale du jeu
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Gestion des touches pour changer la direction du serpent
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                    snake_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                    snake_direction = "RIGHT"
                elif event.key == pygame.K_UP and snake_direction != "DOWN":
                    snake_direction = "UP"
                elif event.key == pygame.K_DOWN and snake_direction != "UP":
                    snake_direction = "DOWN"

        # Déplacement du serpent en fonction de sa direction
        head = snake[0]
        if snake_direction == "RIGHT":
            new_head = (head[0] + CELL_SIZE, head[1])
        elif snake_direction == "LEFT":
            new_head = (head[0] - CELL_SIZE, head[1])
        elif snake_direction == "UP":
            new_head = (head[0], head[1] - CELL_SIZE)
        elif snake_direction == "DOWN":
            new_head = (head[0], head[1] + CELL_SIZE)

        # Ajout de la nouvelle tête du serpent
        snake.insert(0, new_head)

        # Vérification des collisions avec les bords de l'écran
        if (new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or
                new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT):
            game_over = True

        # Vérification des collisions avec le corps du serpent
        if len(snake) != len(set(snake)):
            game_over = True

        # Vérification si le serpent a mangé la pomme
        if new_head == apple_position:
            score += 1
            apple_position = (random.randint(0, (SCREEN_WIDTH - CELL_SIZE) // CELL_SIZE - 1) * CELL_SIZE,
                              random.randint(0, (SCREEN_HEIGHT - CELL_SIZE) // CELL_SIZE - 1) * CELL_SIZE)
        else:
            snake.pop()

        # Dessin de l'écran de jeu
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, (apple_position[0], apple_position[1], CELL_SIZE, CELL_SIZE))

        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

        # Affichage du score
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(SNAKE_SPEED)

    # Affichage de l'écran de fin de jeu
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.update()
    pygame.time.wait(2000)

    # Retourner au menu
    main_menu()

# Création du menu de démarrage
def main_menu():
    menu = pygame_menu.Menu(
        height=SCREEN_HEIGHT,
        width=SCREEN_WIDTH,
        title='Snake Game',
        theme=game_theme
    )

    menu.add.button('Jouer', game)
    menu.add.button('Quitter', pygame_menu.events.EXIT)

    menu.mainloop(screen)

# Lancer le menu principal
main_menu()
