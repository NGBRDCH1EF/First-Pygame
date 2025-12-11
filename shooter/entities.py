from dataclasses import dataclass
import pygame
import math
import random

@dataclass
class Bullet:
    rect: pygame.Rect
    dx: float
    dy: float
    speed: float

    @classmethod
    def from_points(cls, origin:tuple[int,int], destination:tuple[int,int], speed:int=10):
        """Create a bullet from origin -> destination, auto-normalized."""
        ox, oy = origin
        dx = destination[0] - ox
        dy = destination[1] - oy

        length = math.hypot(dx, dy)
        if length == 0:
            dx, dy = 0, -1  # default direction
        else:
            dx /= length
            dy /= length

        bullet_rect = pygame.Rect(ox, oy, 8, 8)

        return cls(bullet_rect, dx, dy, speed)

    def update(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)

@dataclass
class Enemy:
    rect: pygame.Rect
    dx: float
    dy: float
    speed: float

    @classmethod
    def spawn_at_edge(
        cls,
        width: int,
        height: int,
        size: int,
        destination: tuple[int, int],
        speed: float,
    ):
        """Spawn enemy at random edge of the screen that moves toward destination."""
        side = random.choice(["top", "bottom", "left", "right"])

        match side:
            case "top":
                ox = random.randint(0, width - size)
                oy = -size          # fully above screen
            case "bottom":
                ox = random.randint(0, width - size)
                oy = height         # fully below screen
            case "left":
                ox = -size
                oy = random.randint(0, height - size)
            case "right":
                ox = width
                oy = random.randint(0, height - size)

        rect = pygame.Rect(ox, oy, size, size)

        # direction vector toward destination
        dx = destination[0] - ox
        dy = destination[1] - oy

        length = math.hypot(dx, dy)
        if length == 0:
            dx, dy = 0, -1  # default direction
        else:
            dx /= length
            dy /= length

        return cls(rect, dx, dy, speed)

    def update(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)


