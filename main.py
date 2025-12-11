import pygame
import sys

pygame.init()

# RGB color definitions
BLUE = (0, 0, 255)
SKY_BLUE = (135, 206, 235)
GREEN = (50, 205, 50)
BLACK = (0, 0, 0)

# --- window setup ---
WIDTH, HEIGHT = 800, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Runner")

clock = pygame.time.Clock()

# world setup
GROUND_Y = HEIGHT - (HEIGHT // 10)
game_over = False

# Define Player
player = pygame.Rect(WIDTH // 3, GROUND_Y - 50, 50, 50)  # x, y, width, height
player_vel_y = 0
GRAVITY = 1
JUMP_STRENGTH = -14
on_ground = True

# Define Ground
ground = pygame.Rect(0, GROUND_Y, WIDTH, HEIGHT // 10)

# Define simple obstacle
obstacle_height = 50
obstacle_width = 50
obstacle = pygame.Rect(
    WIDTH + obstacle_width,
    GROUND_Y - obstacle_height,
    obstacle_width,
    obstacle_height
)
obstacle_speed = 10

font = pygame.font.SysFont(None, 60)

# --- main game loop ---
running = True
while running:
    # --- events / input ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keydown events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    # reset everything
                    player.x = WIDTH // 3
                    player.y = GROUND_Y - 50
                    player_vel_y = 0
                    on_ground = True
                    obstacle.x = WIDTH + obstacle_width
                    game_over = False
                else:
                    # jump (only if not game over and on ground)
                    if on_ground:
                        player_vel_y = JUMP_STRENGTH
                        on_ground = False

    # --- update game state (only if not game over) ---
    if not game_over:
        # apply gravity
        player_vel_y += GRAVITY
        player.y += player_vel_y

        # collide with ground
        if player.bottom >= GROUND_Y:
            player.bottom = GROUND_Y
            player_vel_y = 0
            on_ground = True

        # move obstacle
        obstacle.x -= obstacle_speed
        if obstacle.x <= -obstacle_width:
            obstacle.x += WIDTH + obstacle_width

        # check collision
        if player.colliderect(obstacle):
            game_over = True

    # --- draw ---
    window.fill(SKY_BLUE)  # sky blue background

    pygame.draw.rect(window, GREEN, ground)
    pygame.draw.rect(window, BLACK, obstacle)
    pygame.draw.rect(window, BLUE, player)

    if game_over:
        text = font.render("GAME OVER - Press SPACE", True, BLACK)
        window.blit(text, (WIDTH // 6, HEIGHT // 3))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
