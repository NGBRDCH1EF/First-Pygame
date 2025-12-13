from entities.character import Character
import pygame


class Enemy(Character):
    def think(self, player_pos: pygame.Vector2):
        # super-simple “chase player” AI
        direction = (player_pos - self.pos)
        if direction.length_squared() > 0:
            direction = direction.normalize()
        self.velocity = direction * (self.get_speed()*0.75)

        #avoid overlapping with player
        dist_to_player = (player_pos - self.pos).length()
        if dist_to_player < 30 and dist_to_player > 20:
            self.velocity = pygame.Vector2(0, 0)

    def take_damage(self, amount: int):
        self.health -= amount
        print(f"{self.name} takes {amount} damage! Health is now {self.health}.")
        if self.health <= 0:
            self.die()

    def die(self):
        self.alive = False
        self.velocity = pygame.Vector2(0, 0)
        print(f"{self.name} has died.")

    