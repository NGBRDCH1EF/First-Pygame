import pygame

class Character:
    def __init__(self, name: str, pos: pygame.Vector2):
        self.name = name
        self.pos = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(0, 0)

        self.race = None
        self.rpg_class = None

        self.base_speed = 600
        
        self.max_health = 100
        self.max_mana = 100
        self.max_stamina = 100
        
        self.health = self.max_health
        self.mana = self.max_mana
        self.stamina = self.max_stamina


        self.inventory = []
        self.equipped_items = {}

    def get_speed(self) -> float:
        speed = self.base_speed
        if self.race is not None:
            speed += getattr(self.race, "speed_bonus", 0)
        if self.rpg_class is not None:
            speed += getattr(self.rpg_class, "speed_bonus", 0)
        return speed

    def update(self, dt: float):
        self.pos += self.velocity * dt

    def draw(self,surface):
        pygame.draw.circle(surface, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), 15)



