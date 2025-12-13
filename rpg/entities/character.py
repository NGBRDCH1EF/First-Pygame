import pygame
from rpg.data import colors as c

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
        
        self.melee_cooldown = 0.0

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
        
        self.melee_cooldown = max(0.0, self.melee_cooldown - dt)

    def take_damage(self, amount: int):
        self.health -= amount
        print(f"{self.name} takes {amount} damage! Health is now {self.health}.")
        if self.health <= 0:
            self.die()

    def draw(self, surface, camera,color = c.WHITE):
        screen_pos = camera.apply(self.pos)
        pygame.draw.circle(
            surface,
            color,
            (int(screen_pos.x), int(screen_pos.y)),
            15
        )

    def melee_attack(self, targets, attack_dir: pygame.Vector2):
        if self.melee_cooldown > 0.0:
            return 0, [] 
        else:
            weapon = self.equipped_items.get("weapon")
            if weapon is None:
                return 0, []
            self.melee_cooldown = weapon.cooldown

            if weapon is None:
                return 0, []

            if attack_dir.length_squared() == 0:
                return 0, []

            if self.stamina < weapon.stamina_cost:
                damage = weapon.damage // 2
            else:
                damage = weapon.damage

            attack_dir = attack_dir.normalize()
            arc_cos = math.cos(math.radians(weapon.arc_deg / 2))

            hits = []
            if isinstance(targets, Character):
                targets = [targets]
            for t in targets:
                if not getattr(t, "alive", True):
                    continue

                to_t = t.pos - self.pos
                dist = to_t.length()
                if dist == 0 or dist > weapon.reach:
                    continue

                if attack_dir.dot(to_t / dist) >= arc_cos:
                    hits.append(t)

            
            if hits:
                self.stamina =max(0, self.stamina - weapon.stamina_cost)

            return damage,hits



