import pygame

class StatusBar:
    def __init__(self, pos, size, color, tracked_value_fn, max_value):
        self.pos = pygame.Vector2(pos)
        self.size = pygame.Vector2(size)
        self.color = color
        self.tracked_value_fn = tracked_value_fn
        self.max_value = float(max_value)
        self.current_value = self.tracked_value_fn()

    def update(self):
        self.current_value = self.tracked_value_fn()

    def draw(self, surface):
        pygame.draw.rect(surface, (50, 50, 50), (*self.pos, *self.size))
        ratio = 0 if self.max_value == 0 else self.current_value / self.max_value
        ratio = max(0.0, min(1.0, ratio))
        fill_width = ratio * self.size.x
        pygame.draw.rect(surface, self.color, (self.pos.x, self.pos.y, fill_width, self.size.y))
