from dataclasses import dataclass
import pygame
import math
import random
import statistics

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
    color:tuple[int,int,int]  #RGB value for color


    @classmethod
    def spawn_at_edge(
        cls,
        width: int,
        height: int,
        size_range: tuple[int,int] | int,   #min and max size or set size
        destination: tuple[int, int],
        speed: float,
        color:tuple[int,int,int]=(255,0,0)  #RGB value for color

    ):
        """Spawn enemy at random edge of the screen that moves toward destination."""
        side = random.choice(["top", "bottom", "left", "right"])
        
        if isinstance(size_range,tuple):
            rand_size = random.randint(size_range[0],size_range[1])
            ratio = statistics.mean(size_range) / rand_size  # bigger size → smaller ratio
            ratio = max(0.5, min(ratio, 1.5))   # keep multiplier between 0.5x and 1.5x
            speed *= ratio
        else: 
            rand_size = size_range
        

        match side:
            case "top":
                ox = random.randint(0, width - rand_size)
                oy = -rand_size          # fully above screen
            case "bottom":
                ox = random.randint(0, width - rand_size)
                oy = height         # fully below screen
            case "left":
                ox = -rand_size
                oy = random.randint(0, height - rand_size)
            case "right":
                ox = width
                oy = random.randint(0, height - rand_size)

        rect = pygame.Rect(ox, oy, rand_size, rand_size)

        # direction vector toward destination
        dx = destination[0] - ox
        dy = destination[1] - oy

        length = math.hypot(dx, dy)
        if length == 0:
            dx, dy = 0, -1  # default direction
        else:
            dx /= length
            dy /= length

        return cls(rect, dx, dy, speed,color)

    def update(self, width, height):
        # Move enemy
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        # Bounce left wall
        if self.rect.left <= 0 and self.dx < 0:
            self.dx *= -1

        # Bounce right wall
        if self.rect.right >= width and self.dx > 0:
            self.dx *= -1

        # Bounce top wall
        if self.rect.top <= 0 and self.dy < 0:
            self.dy *= -1

        # Bounce bottom wall
        if self.rect.bottom >= height and self.dy > 0:
            self.dy *= -1
        

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def hit_by(self, bullet):
        return self.rect.colliderect(bullet.rect)

