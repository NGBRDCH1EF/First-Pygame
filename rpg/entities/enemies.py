from entities.character import Character
import pygame
import data.weapons


class Melee_Enemy(Character):
    def think(self, target:Character):
        # super-simple “chase player” AI
        direction = (target.pos - self.pos)
        if direction.length_squared() > 0:
            direction = direction.normalize()
        self.velocity = direction * (self.get_speed() * 0.75)
       
        #avoid overlapping with player
        dist_to_player = (target.pos - self.pos).length()
        if dist_to_player < self.equipped_items['weapon'].reach / 2:
            self.velocity = pygame.Vector2(0, 0)

        #attack if in range
        if dist_to_player <= self.equipped_items['weapon'].reach:
            hits = self.melee_attack(target, direction)
            if hits:
                target.take_damage(hits[0])
                
            


    

    def die(self):
        self.alive = False
        self.velocity = pygame.Vector2(0, 0)
        print(f"{self.name} has died.")

class Goblin(Melee_Enemy):
    def __init__(self, name: str, pos: pygame.Vector2):
        super().__init__(name, pos)
        self.max_health = 50
        self.health = self.max_health
        self.base_speed = 400
        self.equipped_items['weapon'] = data.weapons.GOBLIN_DAGGER

        print(self.equipped_items['weapon'].damage)


