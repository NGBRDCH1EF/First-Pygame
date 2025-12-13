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

    def try_attack(self,enemies:list = None, camera:Camera=None):
        weapon = self.equipped_items.get('weapon', None)            
        if weapon is None:
            print(f"{self.name} has no weapon equipped!")
            return
        damage = weapon.damage
        if self.stamina < weapon.stamina_cost:
            damage = damage // 2  # half damage if low stamina
        self.stamina -= weapon.stamina_cost 

        mouse_pos = camera.screen_to_world(pygame.Vector2(pygame.mouse.get_pos()))
        attack_vec = mouse_pos - self.pos

        if attack_vec.length_squared() == 0:
            return
        
        attack_dir = attack_vec.normalize()

        if attack_dir.length_squared() == 0:
            return
        
        arc_cos = math.cos(math.radians(weapon.arc_deg / 2))

        for enemy in enemies:
            if not getattr(enemy, "alive", True):
                continue

            to_enemy = enemy.pos - self.pos
            dist = to_enemy.length()

            if dist > weapon.reach or dist == 0:
                continue

            if attack_dir.dot(to_enemy / dist) >= arc_cos:
                enemy.take_damage(damage)
                self.stamina -= weapon.stamina_cost

        

    def equip_weapon(self, weapon):
        self.equipped_items['weapon'] = weapon