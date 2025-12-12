import pygame
from entities import Cannon,Projectile,StatusBar

pygame.init()


#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
OLIVE = (128, 128, 0)
SKY_BLUE = (135, 206, 235)

# --- window setup ---
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Artillery Game")
clock = pygame.time.Clock()

#main game loop
running = True
pause = False


#world setup    
PIXELS_PER_METER = 20  # scaling factor
GRAVITY_MPS2 = 9.81  # meters per second squared
GRAVITY = GRAVITY_MPS2 * PIXELS_PER_METER  # pixels per second squared
GROUND_THICKNESS = 50
GROUND_LEVEL = HEIGHT - GROUND_THICKNESS  # y-coordinate of the ground
MIDDLE_GROUND = HEIGHT-GROUND_THICKNESS//2
ground = pygame.Rect(0, GROUND_LEVEL, WIDTH, GROUND_THICKNESS)

#cannon setup
CANNON_BASE = pygame.image.load('artillery/assets/cannon_base.png')
CANNON_BARREL = pygame.image.load('artillery/assets/cannon_barrel.png')
cannon = Cannon(pygame.Vector2(100, GROUND_LEVEL), max_muzzle_velocity=40)
cannon.art.append(CANNON_BASE)
cannon.art.append(CANNON_BARREL)
MUZZLE_VELOCITY_INCREMENT =  1  # m/s per key press

#create status bars
power_bar = StatusBar((cannon.pos.x-32,MIDDLE_GROUND+10),(64,8),cannon.max_muzzle_velocity,RED)

#list to hold projectiles
projectiles:list[Projectile] = []

#main game loop
while running:
    dt=clock.tick(60)/1000  #delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_w:
                cannon.muzzle_velocity = min(cannon.muzzle_velocity + MUZZLE_VELOCITY_INCREMENT, cannon.max_muzzle_velocity)
                print(cannon.muzzle_velocity)
            elif event.key == pygame.K_s:
                cannon.muzzle_velocity = max(cannon.muzzle_velocity - MUZZLE_VELOCITY_INCREMENT, 0)
                print(cannon.muzzle_velocity)
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:  # scroll up
                cannon.muzzle_velocity = min(cannon.muzzle_velocity + MUZZLE_VELOCITY_INCREMENT, cannon.max_muzzle_velocity)
                print(cannon.muzzle_velocity)
            elif event.y < 0:  # scroll down
                cannon.muzzle_velocity = max(cannon.muzzle_velocity - MUZZLE_VELOCITY_INCREMENT, 0)
                print(cannon.muzzle_velocity)
        
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a]:
        cannon.angle = min(cannon.angle + 1, cannon.angle_bounds[1])
    if keys[pygame.K_d]:
        cannon.angle = max(cannon.angle - 1, cannon.angle_bounds[0])
    if keys[pygame.K_SPACE]:
        projectile = cannon.fire(Projectile, pygame.time.get_ticks()/1000)
        if projectile:
            projectiles.append(projectile)

    window.fill(SKY_BLUE)

    #update projectiles
    for projectile in projectiles:
        if projectile.alive:
            projectile.update(dt, gravity=GRAVITY, x_bounds=(0, WIDTH), y_bounds=(0, HEIGHT))
            if projectile.pos.y >  MIDDLE_GROUND:
                projectile.velocity.y = 0
                projectile.velocity.x *= 0.99  # simulate friction
        else:
            projectiles.remove(projectile)

    #update status bars
    power_bar.update(cannon.muzzle_velocity)

    #---draw---
    pygame.draw.rect(window, GREEN, ground)
    
    #draw cannon base
    base_rect = cannon.art[0].get_rect(center=(int(cannon.pos.x), int(cannon.pos.y)))
    window.blit(cannon.art[0], base_rect)    
    
    #draw cannon barrel
    barrel_rotated = pygame.transform.rotate(cannon.art[1], cannon.angle)
    barrel_rect = barrel_rotated.get_rect()
    barrel_rect.center = (int(cannon.pos.x), int(cannon.pos.y))
    window.blit(barrel_rotated, barrel_rect)

    #draw projectiles
    for projectile in projectiles:
        if projectile.alive:
            projectile.draw(window)

    #draw prediction path
    path_points = cannon.prediction_path(Projectile)
    for point in path_points:
        if point[1] > GROUND_LEVEL:
            break
        pygame.draw.circle(window, BLUE, (int(point[0]), int(point[1])), 3)
    
    #display muzzle velocity and angle
    power_bar.draw(window)
    
    
    #clock and flip
    pygame.display.flip()


    

pygame.quit()
