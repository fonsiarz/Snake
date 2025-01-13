import pygame
import sys
import random

# Initialize Pygame
# Inicjalizacja biblioteki Pygame, wymagane do korzystania z jej funkcji.
pygame.init()

# Constants
# Definiuje szerokość okna gry w pikselach.
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock
clock = pygame.time.Clock()

# Font for displaying score and messages
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72) 

def reset_game():
    global snake, snake_direction, food
    snake = [(100, 100), (80, 100), (60, 100)]  # Reset starting position
    snake_direction = (CELL_SIZE, 0)  # Reset direction
    food = (random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
            random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

def draw_food(food):
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

def draw_score(score):
    score_surface = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surface, (10, 10))

def check_collision(snake):
    head = snake[0]
    # Check wall collision
    if (head[0] < 0 or head[1] < 0 or
        head[0] >= SCREEN_WIDTH or head[1] >= SCREEN_HEIGHT):
        return True
    # Check self collision
    if head in snake[1:]:
        return True
    return False

def game_over_screen(score):
    screen.fill(BLACK)
    game_over_text = large_font.render("Game Over", True, RED)
    score_text = font.render(f"Your score: {score}", True, WHITE)
    replay_text = font.render("Press R to play again or Q to quit", True, WHITE)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(replay_text, (SCREEN_WIDTH // 2 - replay_text.get_width() // 2, SCREEN_HEIGHT // 1.5))
    pygame.display.flip()

def choose_difficulty():
    screen.fill(BLACK)
    easy_text = large_font.render("Press E for Easy", True, WHITE)
    hard_text = large_font.render("Press H for Hard", True, WHITE)

    screen.blit(easy_text, (SCREEN_WIDTH // 2 - easy_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(hard_text, (SCREEN_WIDTH // 2 - hard_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    return 10  # Easy mode: 10 FPS
                if event.key == pygame.K_h:
                    return 20  # Hard mode: 20 FPS

def main():
    global snake, snake_direction, food

    fps = choose_difficulty()

    reset_game()

    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and snake_direction != (0, CELL_SIZE):
            snake_direction = (0, -CELL_SIZE)
        if keys[pygame.K_DOWN] and snake_direction != (0, -CELL_SIZE):
            snake_direction = (0, CELL_SIZE)
        if keys[pygame.K_LEFT] and snake_direction != (CELL_SIZE, 0):
            snake_direction = (-CELL_SIZE, 0)
        if keys[pygame.K_RIGHT] and snake_direction != (-CELL_SIZE, 0):
            snake_direction = (CELL_SIZE, 0)

        # Move snake
        new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
        snake = [new_head] + snake[:-1]

        # Check food collision
        if new_head == food:
            snake.append(snake[-1])  # Grow snake
            food = (random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                    random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
            score += 1

        # Check collisions
        if check_collision(snake):
            game_over_screen(score)
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            reset_game()
                            score = 0
                            fps = choose_difficulty()
                            waiting = False
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()

        # Draw everything
        screen.fill(BLACK)
        draw_snake(snake)
        draw_food(food)
        draw_score(score)
        pygame.display.flip()

        # Control game speed
        clock.tick(fps)

main()
