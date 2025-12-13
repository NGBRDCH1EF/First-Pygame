from entities.character import Character
import pygame


class Enemy(Character):
    def think(self, player_pos: pygame.Vector2):
        # super-simple “chase player” AI
        direction = (player_pos - self.pos)
        if direction.length_squared() > 0:
            direction = direction.normalize()
        self.velocity = direction * (self.get_speed() * 0.6)