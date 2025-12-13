import pygame
import random
from entities.character import Character
from entities.player import Player
from entities.ui import StatusBar
from entities.enemies import Goblin
import data.colors as c
from systems.camera import Camera
import data.weapons



#initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


#player setup
player = Player('Player1',pygame.Vector2(WIDTH//2,HEIGHT//2))
player.equipped_items['weapon'] = data.weapons.HALBERD

#entity lists
enemies = []
weapons_in_world:list[data.weapons.Weapon] = []

#ui objects
health_bar  = StatusBar((10,10), (200,20), c.RED,   lambda: player.health,  player.max_health)
stamina_bar = StatusBar((10,40), (200,20), c.GREEN, lambda: player.stamina, player.max_stamina)
mana_bar    = StatusBar((10,70), (200,20), c.BLUE,  lambda: player.mana,    player.max_mana)
status_bars = [health_bar,stamina_bar,mana_bar]


#systems
camera = Camera((WIDTH, HEIGHT), (2000, 2000))

#world setup
world_background = pygame.Surface((2000, 2000))
background_image = pygame.image.load('rpg/assets/gradient.png').convert()
background_image = pygame.transform.scale(background_image, (2000, 2000))
world_background.blit(background_image, (0, 0))

#weapons


#main game loop
running = True
while running:
    dt = clock.tick(60) / 1000  # delta time in seconds
    
    
    #input handling---------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                attack_dir = player.melee_aim(camera)
                attack_dir = player.melee_aim(camera)
                damage,hits = player.melee_attack(enemies, attack_dir)
                for enemy in hits:
                    enemy.take_damage(damage)

    keys = pygame.key.get_pressed()
    player.handle_input(keys)
   
   
    #update-----------------
    player.update(dt)
    

    if  len(enemies) < 5:
        spawn_pos = pygame.Vector2(random.randint(0,2000),random.randint(0,2000))
        enemies.append(Goblin(f"Goblin{len(enemies)+1}",spawn_pos))
    for enemy in enemies:
        enemy.think(player.pos)
        enemy.update(dt)
        if not enemy.alive:
            enemies.remove(enemy)

    #update UI elements
    for bar in status_bars:
        if isinstance(bar, StatusBar):
            bar.update()


    #draw------------------
    # window.fill((0, 0, 0))
    window.blit(world_background, camera.apply(pygame.Vector2(0, 0)))
    camera.follow(player.pos)
    player.draw(window, camera)

    for enemy in enemies:
        enemy.draw(window, camera, c.RED)
    
    
    #draw UI elements
    for bar in status_bars:
        bar.draw(window)
    
    pygame.display.flip()

