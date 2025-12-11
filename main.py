import pygame
import sys

pygame.init()

# RGB color definitions
BLUE = (0, 0, 255)
SKY_BLUE = (135, 206, 235)
GREEN = (50, 205, 50)
BLACK = (0, 0, 0)

# --- base (virtual) resolution ---
BASE_WIDTH, BASE_HEIGHT = 800, 400

# resizable window (can be any size, we'll scale into it)
window = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Runner")

# surface we actually draw the game onto (fixed resolution)
game_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))

clock = pygame.time.Clock()

# world setup (all in base resolution coordinates)
GROUND_Y = BASE_HEIGHT - (BASE_HEIGHT // 10)
paused =  False
game_over = False
score = 0
obstacle_passed = False  # has the current obstacle been counted for score?

# --- player images & rect ---
player_img1 = pygame.image.load("images/guy.png").convert_alpha()
player_img2 = pygame.image.load("images/guy2.png").convert_alpha()
player_img1 = pygame.transform.scale(player_img1, (50, 50))
player_img2 = pygame.transform.scale(player_img2, (50, 50))
player_imgs = [player_img1, player_img2]

player = pygame.Rect(BASE_WIDTH // 3, GROUND_Y - 50, 50, 50)  # x, y, width, height
player_vel_y = 0
GRAVITY = 1
JUMP_STRENGTH = -14
on_ground = True

# simple 2-frame animation state
current_frame = 0
frame_timer = 0
FRAME_SPEED = 8  # frames before swapping 0 <-> 1

# --- ground ---
ground = pygame.Rect(0, GROUND_Y, BASE_WIDTH, BASE_HEIGHT // 10)

# --- obstacle ---
obstacle_height = 50
obstacle_width = 50
obstacle_img = pygame.image.load("images/rock.png").convert_alpha()
obstacle_img = pygame.transform.scale(obstacle_img, (50, 50))

obstacle = pygame.Rect(
    BASE_WIDTH + obstacle_width,
    GROUND_Y - obstacle_height,
    obstacle_width,
    obstacle_height
)
obstacle_speed = 10

font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)

# --- main game loop ---
running = True
while running:
    # --- events / input ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keydown events
        if event.type == pygame.KEYDOWN:
            # toggle pause with ESC (only if not game over)
            if event.key == pygame.K_ESCAPE and not game_over:
                paused = not paused
            
            if event.key == pygame.K_SPACE:
                if game_over:
                    # reset everything
                    player.x = BASE_WIDTH // 3
                    player.y = GROUND_Y - 50
                    player_vel_y = 0
                    on_ground = True
                    obstacle.x = BASE_WIDTH + obstacle_width
                    game_over = False
                    score = 0
                    obstacle_passed = False
                    current_frame = 0
                    frame_timer = 0
                else:
                    # jump (only if not game over and on ground)
                    if on_ground:
                        player_vel_y = JUMP_STRENGTH
                        on_ground = False

    # --- update game state (only if not game over) ---
    if not game_over and not paused:
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
            obstacle.x = BASE_WIDTH + obstacle_width
            obstacle_passed = False  # new obstacle coming, not counted yet

        # check collision
        if player.colliderect(obstacle):
            game_over = True

        # scoring: obstacle has fully passed the player
        if not obstacle_passed and obstacle.right < player.left:
            score += 1
            obstacle_passed = True

        # update 2-frame animation
        frame_timer += 1
        if frame_timer >= FRAME_SPEED:
            frame_timer = 0
            current_frame = (current_frame + 1) % 2  # swap 0 <-> 1

    # --- draw everything onto game_surface (virtual resolution) ---
    game_surface.fill(SKY_BLUE)  # sky blue background

    pygame.draw.rect(game_surface, GREEN, ground)
    game_surface.blit(obstacle_img, obstacle)
    game_surface.blit(player_imgs[current_frame], player)

    # draw score (always visible)
    score_text = font.render(f"Score: {score}", True, BLACK)
    game_surface.blit(score_text, (10, 10))

    if game_over:
        text = big_font.render("GAME OVER - Press SPACE", True, BLACK)
        text_rect = text.get_rect(center=(BASE_WIDTH // 2, BASE_HEIGHT // 2))
        game_surface.blit(text, text_rect)

    elif paused:
        text = big_font.render("PAUSED", True, BLACK)
        text_rect = text.get_rect(center=(BASE_WIDTH // 2, BASE_HEIGHT // 2))
        game_surface.blit(text, text_rect)

    # --- scale game_surface to window size ---
    win_w, win_h = window.get_size()
    scale_x = win_w / BASE_WIDTH
    scale_y = win_h / BASE_HEIGHT
    scale = min(scale_x, scale_y)  # keep aspect ratio

    scaled_w = int(BASE_WIDTH * scale)
    scaled_h = int(BASE_HEIGHT * scale)

    scaled_surface = pygame.transform.scale(game_surface, (scaled_w, scaled_h))

    # center the scaled game on the window
    offset_x = (win_w - scaled_w) // 2
    offset_y = (win_h - scaled_h) // 2

    window.fill(BLACK)  # letterbox background
    window.blit(scaled_surface, (offset_x, offset_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
