
import pygame
import random
import sys

# Initialize my pygame
pygame.init()

# setting my Screen dimensions to be adjustable
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Flying Jayar")

# Colors for my jayar game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
GREEN = (34, 139, 34)

# fonts am gonna use
font = pygame.font.SysFont("comicsansms", 40)
small_font = pygame.font.SysFont("comicsansms", 25)

# Clock (score)
clock = pygame.time.Clock()

# my sprite  (Dragon or bird) properties
bird_size = 60
bird_x = 100
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.5
lift = -8

# Obstacles (green ones)
pipe_width = 80
pipe_gap = 250  # increased gap to make it easier
pipe_velocity = 3  # start slow

#Loading my dragon sprite 
dragon_img = pygame.Surface((bird_size, bird_size), pygame.SRCALPHA)
pygame.draw.polygon(dragon_img, (200, 50, 50), [(0, bird_size//2), (bird_size-10, 10), (bird_size, bird_size//2), (bird_size-10, bird_size-10)])
pygame.draw.polygon(dragon_img, (255, 140, 0), [(bird_size//2, bird_size//2), (bird_size, bird_size//4), (bird_size, 3*bird_size//4)])



def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont("comicsansms", size)
    label = font.render(text, True, color)
    rect = label.get_rect(center=(x, y))
    screen.blit(label, rect)


def start_screen():
    while True:
        screen.fill(BLUE)
        draw_text("Flying jayar ", 60, WHITE, WIDTH // 2, HEIGHT // 2 - 100)
        draw_text("Press SPACE to Start", 40, WHITE, WIDTH // 2, HEIGHT // 2)
        draw_text("Press ESC to Quit", 30, WHITE, WIDTH // 2, HEIGHT // 2 + 80)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_game()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()


def main_game():
    global bird_y, bird_velocity, pipe_velocity
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipe_velocity = 3  #resets speed for each game

    #pipes or obstacles set to fewer and spaced further apart
    pipes = []
    for i in range(2):
        top_height = random.randint(150, HEIGHT - pipe_gap - 150)
        pipes.append([WIDTH + i * 400, top_height])

    score = 0
    running = True

    while running:
        screen.fill(BLUE)

        #Handling Events 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                bird_velocity = lift

        #bird or dragon movement
        bird_velocity += gravity
        bird_y += bird_velocity

        #Draw dragon
        screen.blit(dragon_img, (bird_x, int(bird_y)))

        #Move and draw pipes
        for i, pipe in enumerate(pipes):
            pipe[0] -= pipe_velocity
            if pipe[0] + pipe_width < 0:
                pipe[0] = WIDTH + 200
                pipe[1] = random.randint(150, HEIGHT - pipe_gap - 150)
                score += 1
                # Gradually increase difficulty
                pipe_velocity += 0.1
                

            #Top pipe
            pygame.draw.rect(screen, GREEN, (pipe[0], 0, pipe_width, pipe[1]))
            # bottom pipe
            pygame.draw.rect(screen, GREEN, (pipe[0], pipe[1] + pipe_gap, pipe_width, HEIGHT))

            #Handling Collision detection
            if bird_x + bird_size > pipe[0] and bird_x < pipe[0] + pipe_width:
                if bird_y < pipe[1] or bird_y + bird_size > pipe[1] + pipe_gap:
                    running = False

        #Check ground and ceiling collision for max and min movements
        if bird_y <= 0 or bird_y + bird_size >= HEIGHT:
            running = False

        #drawing score
        draw_text(str(score), 40, WHITE, WIDTH // 2, 50)

        pygame.display.flip()
        clock.tick(60)

    game_over_screen(score)


def game_over_screen(score):
    while True:
        screen.fill(BLACK)
        draw_text("Game Over", 60, WHITE, WIDTH // 2, HEIGHT // 2 - 120)
        draw_text(f"Score: {score}", 40, WHITE, WIDTH // 2, HEIGHT // 2 - 40)
        draw_text("Thank you for Playing Arthur's Game", 25, WHITE, WIDTH // 2, HEIGHT // 2 + 20)
        draw_text("Press SPACE to Play Again", 30, WHITE, WIDTH // 2, HEIGHT // 2 + 80)
        draw_text("Press ESC to Quit", 30, WHITE, WIDTH // 2, HEIGHT // 2 + 130)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_game()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()


if __name__ == "__main__":
    start_screen()
