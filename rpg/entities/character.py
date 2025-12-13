import pygame
import data.colors as c
import data.weapons

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

        self.health_regen_rate = 1    # per second
        self.mana_regen_rate = 5      # per second
        self.stamina_regen_rate = 10   # per second


        self.inventory = []
        self.equipped_items = {}
        
        self.alive = True

    def get_speed(self) -> float:
        speed = self.base_speed
        if self.race is not None:
            speed += getattr(self.race, "speed_bonus", 0)
        if self.rpg_class is not None:
            speed += getattr(self.rpg_class, "speed_bonus", 0)
        return speed

    def update(self, dt: float):
        self.pos += self.velocity * dt

        self.health = min(self.max_health, self.health + self.health_regen_rate * dt)
        self.mana = min(self.max_mana, self.mana + self.mana_regen_rate * dt)
        self.stamina = min(self.max_stamina, self.stamina + self.stamina_regen_rate * dt)

        if self.health <= 0:
            self.alive = False
        if self.stamina < 0:
            self.stamina = 0
        if self.mana < 0:
            self.mana = 0

    def draw(self, surface, camera,color = c.WHITE):
        screen_pos = camera.apply(self.pos)
        pygame.draw.circle(
            surface,
            color,
            (int(screen_pos.x), int(screen_pos.y)),
            15
        )



