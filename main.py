import pygame
import sys

pygame.init()

#RGB color definitions
BLUE = (0, 0, 255)
SKY_BLUE = (135, 206, 235)
GREEN = (50, 205, 50)
BLACK =  (0,0,0)

# --- window setup ---
WIDTH, HEIGHT = 800, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Runner")

clock = pygame.time.Clock()


#world Setuup
GROUND_Y = HEIGHT - (HEIGHT // 10)

#Define Player
player = pygame.Rect(WIDTH//3, GROUND_Y - 50, 50, 50)  # x, y, width, height
player_vel_y = 0
GRAVITY = 1
JUMP_STRENGTH = -18
on_ground = True

#Define Ground
ground = pygame.Rect(0,GROUND_Y,WIDTH,HEIGHT//10)

#Define simple obstacle
obstacle_height= 50
obstacle_width = 50
obstacle = pygame.Rect(WIDTH+obstacle_width,GROUND_Y-obstacle_height,obstacle_width,obstacle_height)
obstacle_speed = 10

# --- main game loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((SKY_BLUE))  # sky blue background
    
    #Handle Keypresses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and on_ground:
        player_vel_y = JUMP_STRENGTH
        on_ground = False
    
    #Move obstacle
    obstacle.x -= obstacle_speed
    if obstacle.x <=-obstacle_width: obstacle.x += WIDTH+obstacle_width
    pygame.draw.rect(window,BLACK,obstacle)


    # apply gravity
    player_vel_y += GRAVITY
    player.y += player_vel_y

    # collide with ground
    if player.bottom >= GROUND_Y:
        player.bottom = GROUND_Y
        player_vel_y = 0
        on_ground = True

    #Draw Player and Ground
    pygame.draw.rect(window,GREEN,ground)
    pygame.draw.rect(window,BLUE,player)

    if player.colliderect(obstacle):
        print("HIT!")


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
