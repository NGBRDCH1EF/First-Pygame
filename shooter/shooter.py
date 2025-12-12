import pygame
import sys
import math
from entities import Bullet , Enemy
from ui import HealthBar,AmmoBar
import random
pygame.init()

# --- colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
RED = (255, 0, 0)
BACKGROUND = (183,118,242)


# --- window setup ---
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Shooter")
clock = pygame.time.Clock()

#Entity Lists
bullets:list[Bullet] = []
enemies:list[Enemy]  = []

#Timer
ENEMY_SPAWN_INTERVAL = 20      #TIME BETWEEN SPAWNS (FRAMES)
spawn_timer = ENEMY_SPAWN_INTERVAL

# --- player setup ---
PLAYER_SIZE   = 40
PLAYER_SPEED  = 8
PLAYER_HEALTH = 500
HEALTH_REGEN  = 35      #per second
MAX_AMMO      = 30
AMMO_REGEN    = 2       #per second
BULLET_SPEED  = 20

#UI setup
big_font = pygame.font.SysFont(None, 60)
HealthBar.load_assets()
health_bar = HealthBar.create(PLAYER_HEALTH,HEALTH_REGEN)
score = 0
AmmoBar.load_assets()
ammo_bar = AmmoBar.create(MAX_AMMO,AMMO_REGEN)


#Enemy Setup
ENEMY_BASE_SPEED = 6    #speed of median size enemy
ENEMY_SIZE = (40,180)    #min & max size for enemy
ENEMY_COLOR      = RED

#Pause and Gameover
game_over = False
paused = False

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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and ammo_bar.ammo > 0:
            bullets.append(Bullet.from_points(player.center,pygame.mouse.get_pos() , speed=BULLET_SPEED))
            ammo_bar.ammo -= 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not game_over:
                    paused = not paused
                if game_over:
                    game_over = False
                    #reset everything
                    enemies = []
                    bullets = []
                    health_bar.health = PLAYER_HEALTH
                    player = pygame.Rect(
                        WIDTH // 2 - PLAYER_SIZE // 2,
                        HEIGHT // 2 - PLAYER_SIZE // 2,
                        PLAYER_SIZE,
                        PLAYER_SIZE
                    )
                    paused = False
                    score = 0
                    ammo_bar.ammo = MAX_AMMO
            

    if not paused and not game_over:
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
            new_enemy = Enemy.spawn_at_edge(WIDTH,HEIGHT,ENEMY_SIZE,(player.centerx,player.centery),ENEMY_BASE_SPEED)
            enemies.append(new_enemy)
            print(new_enemy.rect.size)

        #check Bullet-Enemy collision
        for e in enemies[:]:
            for b in bullets[:]:
                if e.hit_by(b):
                    try:
                        score += e.rect.size[0]
                        enemies.remove(e)
                        bullets.remove(b)
                    except ValueError:
                        pass

        #Check Player-Enemy Collision
        for e in enemies[:]:
            if player.colliderect(e.rect):
                enemies.remove(e)
                if health_bar.health > 0: health_bar.health -= e.rect.size[0]
                else: game_over = not game_over
                if score > e.rect.size[0]:
                    score -= e.rect.size[0]
                else:
                    score = 0

        
        #Update entites & timer
        for b in bullets: b.update()
        for e in enemies: e.update(WIDTH,HEIGHT)

        #Health & ammo regen
        if health_bar.health < PLAYER_HEALTH:
            health_bar.update(dt / 1000)
        if ammo_bar.ammo < MAX_AMMO:
            ammo_bar.update(dt/1000)
    
    # --- draw ---
    window.fill(BACKGROUND)
    pygame.draw.rect(window, GREEN, player)
    for b in bullets : b.draw(window) 
    for e in enemies:
        e.draw(window)
    spawn_timer -= 1

    #handle game over and pause
    if game_over:
        text = big_font.render("GAME OVER - Press ESC", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(text, text_rect)
    elif paused:
        text = big_font.render("PAUSED", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(text, text_rect)

    health_bar.draw(window, 10, 10)
    ammo_bar.draw(window,10,80)

    #score
    score_text = big_font.render(f"Score: {score}", True, BLACK)
    score_rect = score_text.get_rect(right=WIDTH)
    window.blit(score_text, score_rect)


    pygame.display.flip()
    dt = clock.tick(60)

pygame.quit()
sys.exit()
