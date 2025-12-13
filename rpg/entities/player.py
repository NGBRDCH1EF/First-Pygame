from entities.character import Character
import pygame

class Player(Character):
    def handle_input(self, keys):
        direction = pygame.Vector2(
            (keys[pygame.K_d] - keys[pygame.K_a]),
            (keys[pygame.K_s] - keys[pygame.K_w]),
        )
        if direction.length_squared() > 0:
            direction = direction.normalize()
        self.velocity = direction * self.get_speed()