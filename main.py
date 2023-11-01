import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("music/lobby.mp3")
pygame.mixer.music.play(-1)


def definescore():
    global SCORE
    SCORE = 0


# Constants
WIDTH, HEIGHT = 1920, 1080
PLAYER_SPEED = 2
ENEMY_SPEED = 2
font = pygame.font.Font(None, 36)
run_once = 0
if run_once == 0:
    definescore()
    run_once = 1
# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge The Balls")
# Load the logo image
logo_img = pygame.image.load("sprites/logo.png")
logo_rect = logo_img.get_rect()
logo_rect.center = (WIDTH // 2, HEIGHT // 2)
# Enemies
enemies = []
enemy_img = pygame.image.load("sprites/ball.png")


# Initialize player function
def initialize_player():
    player_img = pygame.image.load("sprites/jonesy.png")
    player_rect = player_img.get_rect()
    player_rect.centerx = WIDTH // 2
    player_rect.bottom = HEIGHT - 10
    return player_img, player_rect


# Title screen function
def title_screen():
    title = True
    while title:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            title = False
        # Display the "Press Space to Start" message and logo
        screen.fill(WHITE)
        screen.blit(logo_img, logo_rect)
        text = font.render("Press Space to Start", True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(text, text_rect)
        pygame.display.update()


# Initialize player
player_img, player_rect = initialize_player()
# Call the title screen function
title_screen()
# Initialize the score
definescore()
# Game loop
running = True
game_over = False
while running:
    score_text = font.render(f'Score: {SCORE}', True, (0, 255, 255))
    screen.blit(score_text, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player_rect.x += PLAYER_SPEED
        player_rect.x = max(0, min(player_rect.x, WIDTH - player_rect.width))
        # Enemy spawning
        if random.randint(1, 100) <= 2:
            enemy = enemy_img.get_rect(midtop=(random.randint(0, WIDTH), 0))
            enemies.append(enemy)
        # Move enemies and remove those that go off the screen
        new_enemies = []
        for enemy in enemies:
            enemy.y += ENEMY_SPEED
            if enemy.y <= 1080:
                new_enemies.append(enemy)
            else:
                SCORE += 1  # Increment the score when an enemy goes off the screen
        enemies = new_enemies
        # Collision detection
        for enemy in enemies:
            if player_rect.colliderect(enemy):
                game_over = True
                pygame.mixer.music.load("sfx/death.mp3")
                pygame.mixer.music.play(0)
        # Clear the screen
        screen.fill(WHITE)
        # Draw player
        screen.blit(player_img, player_rect)
        # Draw enemies
        for enemy in enemies:
            screen.blit(enemy_img, enemy)
        screen.blit(score_text, (0, 0))
        pygame.display.update()

    if game_over:
        text = font.render("Game Over! Press R to restart or X to quit.", True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.update()
        # Check for game restart
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            pygame.mixer.music.load("music/lobby.mp3")
            pygame.mixer.music.play(-1)
            enemies = []
            game_over = False
            definescore()  # Reset the score when restarting
            player_img, player_rect = initialize_player()
        if keys[pygame.K_x]:
            pygame.quit()
# Quit Pygame
pygame.quit()
