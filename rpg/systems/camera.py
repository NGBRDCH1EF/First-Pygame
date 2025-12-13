import pygame

class Camera:
    def __init__(self, screen_size, world_size):
        self.screen_w, self.screen_h = screen_size
        self.world_w, self.world_h = world_size
        self.offset = pygame.Vector2(0, 0)

    def follow(self, target_pos: pygame.Vector2):
        # center target
        self.offset.x = target_pos.x - self.screen_w / 2
        self.offset.y = target_pos.y - self.screen_h / 2

        # clamp to world
        self.offset.x = max(0, min(self.offset.x, self.world_w - self.screen_w))
        self.offset.y = max(0, min(self.offset.y, self.world_h - self.screen_h))

    def apply(self, world_pos: pygame.Vector2) -> pygame.Vector2:
        return world_pos - self.offset

    