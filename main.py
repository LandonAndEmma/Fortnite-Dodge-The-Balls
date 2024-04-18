import pygame
import random
import sys
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("music/lobby.mp3")
pygame.mixer.music.play(-1)
WIDTH, HEIGHT = 1920, 1080
BASE_PLAYER_SPEED = 6
BASE_ENEMY_SPEED = 4
MAX_PLAYER_SPEED = 24
MAX_ENEMY_SPEED = 100
WHITE = (255, 255, 255)
RED = (255, 0, 0)
SCORE = 0
TIME_TO_INCREASE_SPEED = 6000
STARTING_BALL_SPAWN_PROBABILITY = 0.02
MAX_BALL_SPAWN_PROBABILITY = 0.2
BALL_SPAWN_INCREASE_RATE = 0.0001
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge The Balls")
font = pygame.font.Font(None, 36)
logo_img = pygame.image.load("sprites/logo.png")
player_img = pygame.image.load("sprites/jonesy.png")
enemy_img = pygame.image.load("sprites/ball.png")
def initialize_player():
    player_rect = player_img.get_rect(centerx=WIDTH // 2, bottom=HEIGHT - 10)
    return player_rect
def draw_text(text, color, x, y):
    score_text = font.render(text, True, color)
    screen.blit(score_text, (x, y))
def spawn_enemy():
    if random.random() < BALL_SPAWN_PROBABILITY:
        return enemy_img.get_rect(midtop=(random.randint(0, WIDTH), 0))
    return None
def game_over_screen():
    text = font.render("Game Over! Press R to restart or X to quit.", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
def restart_game():
    pygame.mixer.music.load("music/lobby.mp3")
    pygame.mixer.music.play(-1)
    global SCORE
    SCORE = 0
    return initialize_player(), []
player_rect = initialize_player()
enemies = []
run_title_screen = True
while run_title_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        run_title_screen = False
    screen.fill(WHITE)
    screen.blit(logo_img, (WIDTH // 2 - logo_img.get_width() // 2, HEIGHT // 2 - logo_img.get_height() // 2))
    draw_text("Press Space to Start", RED, WIDTH // 2, HEIGHT - 50)
    pygame.display.update()
running = True
game_over = False
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
ball_spawn_increase_timer = 0
while running:
    clock.tick(120)
    screen.fill(WHITE)
    draw_text(f'Score: {SCORE}', (0, 255, 255), 10, 10)
    elapsed_time = pygame.time.get_ticks() - start_time
    player_speed = min(BASE_PLAYER_SPEED + elapsed_time / TIME_TO_INCREASE_SPEED, MAX_PLAYER_SPEED)
    enemy_speed = min(BASE_ENEMY_SPEED + elapsed_time / TIME_TO_INCREASE_SPEED, MAX_ENEMY_SPEED)
    time_till_increase = max(0, TIME_TO_INCREASE_SPEED - elapsed_time)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if not game_over:
        BALL_SPAWN_PROBABILITY = min(STARTING_BALL_SPAWN_PROBABILITY + ball_spawn_increase_timer * BALL_SPAWN_INCREASE_RATE, MAX_BALL_SPAWN_PROBABILITY)
        draw_text(f'Player Speed: {player_speed:.2f}', (0, 255, 0), 10, 40)
        draw_text(f'Enemy Speed: {enemy_speed:.2f}', (0, 0, 255), 10, 80)
        draw_text(f'Enemy Probability: {BALL_SPAWN_PROBABILITY:.2f}', (255, 0, 0), 10, 120)
        keys = pygame.key.get_pressed()
        player_rect.x -= (keys[pygame.K_LEFT] - keys[pygame.K_RIGHT]) * player_speed
        player_rect.x = max(0, min(player_rect.x, WIDTH - player_rect.width))
        new_enemies = [enemy for enemy in enemies if enemy.y < HEIGHT]
        enemy = spawn_enemy()
        if enemy:
            new_enemies.append(enemy)
        enemies = new_enemies
        for enemy in enemies:
            enemy.y += enemy_speed
            if enemy.y >= HEIGHT:
                SCORE += 1
                enemies.remove(enemy)
        for enemy in enemies:
            if player_rect.colliderect(enemy):
                game_over = True
                pygame.mixer.music.load("sfx/death.mp3")
                pygame.mixer.music.play(0)
        screen.blit(player_img, player_rect)
        for enemy in enemies:
            screen.blit(enemy_img, enemy)
    if game_over:
        game_over_screen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            player_rect, enemies = restart_game()
            game_over = False
            start_time = pygame.time.get_ticks()
            ball_spawn_increase_timer = 0
        elif keys[pygame.K_x]:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    ball_spawn_increase_timer += 1
pygame.quit()
