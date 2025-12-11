import pygame
import sys
import math
from entities import Bullet , Enemy
import random
pygame.init()

# --- colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
RED = (255, 0, 0)


# --- window setup ---
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Shooter")
clock = pygame.time.Clock()

#Entity Lists
bullets:list[Bullet] = []
enemies:list[Enemy]  = []

#Timer
ENEMY_SPAWN_INTERVAL = 60      #TIME BETWEEN SPAWNS (FRAMES)
spawn_timer = ENEMY_SPAWN_INTERVAL

# --- player setup ---
PLAYER_SIZE = 40
PLAYER_SPEED = 12

#Enemy Setup
ENEMY_BASE_SPEED = 3    #speed of median size enemy
ENEMY_SIZE = (20,100)    #min & max size for enemy
ENEMY_COLOR      = RED

#mouse marker setup
CURSOR_SIZE  = 10

# start in the middle of the screen
player = pygame.Rect(
    WIDTH // 2 - PLAYER_SIZE // 2,
    HEIGHT // 2 - PLAYER_SIZE // 2,
    PLAYER_SIZE,
    PLAYER_SIZE
)

# --- main loop ---
running = True
while running:
    # --- events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            bullets.append(Bullet.from_points(player.center,pygame.mouse.get_pos() , speed=15))
    

    # --- input / movement ---
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player.y -= PLAYER_SPEED
    if keys[pygame.K_s]:
        player.y += PLAYER_SPEED
    if keys[pygame.K_a]:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_d]:
        player.x += PLAYER_SPEED

    # keep player inside the window
    if player.left < 0:
        player.left = 0
    if player.right > WIDTH:
        player.right = WIDTH
    if player.top < 0:
        player.top = 0
    if player.bottom > HEIGHT:
        player.bottom = HEIGHT

    #Create Enemies
    if spawn_timer <= 0:
        spawn_timer = ENEMY_SPAWN_INTERVAL
        new_enemy = Enemy.spawn_at_edge(WIDTH,HEIGHT,(10,100),(player.centerx,player.centery),ENEMY_BASE_SPEED)
        enemies.append(new_enemy)

    #check Bullet-Enemy collision
    for e in enemies[:]:
        for b in bullets[:]:
            if e.hit_by(b):
                enemies.remove(e)
                bullets.remove(b)



    #Update entites & timer
    for b in bullets: b.update()

    # --- draw ---
    window.fill(BLACK)
    pygame.draw.rect(window, GREEN, player)
    for b in bullets : b.draw(window) 
    for e in enemies:
        e.update(WIDTH,HEIGHT)
        e.draw(window)
    spawn_timer -= 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
