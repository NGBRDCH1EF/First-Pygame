import pygame
from entities.character import Character
from entities.player import Player
from entities.enemy import Enemy
from entities.ui import StatusBar
import data.colors as c


#initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


#player setup
player = Player('Player1',pygame.Vector2(WIDTH//2,HEIGHT//2))


#entity lists
enemies:list[Enemy] = []

#ui objects
health_bar  = StatusBar((10,10), (200,20), c.RED,   lambda: player.health,  player.max_health)
stamina_bar = StatusBar((10,40), (200,20), c.GREEN, lambda: player.stamina, player.max_stamina)
mana_bar    = StatusBar((10,70), (200,20), c.BLUE,  lambda: player.mana,    player.max_mana)
status_bars = [health_bar,stamina_bar,mana_bar]

#main game loop
running = True
while running:
    dt = clock.tick(60) / 1000  # delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #input handling---------
    keys = pygame.key.get_pressed()
    player.handle_input(keys)


    #update-----------------
    player.update(dt)
    
    #update UI elements
    for bar in status_bars:
        if isinstance(bar, StatusBar):
            bar.update()


    #draw------------------
    window.fill((0, 0, 0))
    player.draw(window)

    #draw UI elements
    for bar in status_bars:
        bar.draw(window)
    
    pygame.display.flip()

