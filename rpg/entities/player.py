from entities.character import Character
import pygame
from systems.camera import Camera
import math

class Player(Character):
    def handle_input(self, keys):
        direction = pygame.Vector2(
            (keys[pygame.K_d] - keys[pygame.K_a]),
            (keys[pygame.K_s] - keys[pygame.K_w]),
        )
        if direction.length_squared() > 0:
            direction = direction.normalize()
        self.velocity = direction * self.get_speed()

    def melee_aim(self, camera: Camera):
        mouse_pos = pygame.mouse.get_pos()
        world_mouse_pos = camera.screen_to_world(mouse_pos)
        attack_dir = world_mouse_pos - self.pos
        return attack_dir.normalize() if attack_dir.length_squared() > 0 else pygame.Vector2(0, 0)

    def equip_weapon(self, weapon):
        self.equipped_items['weapon'] = weapon