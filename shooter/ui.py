from dataclasses import dataclass
import pygame

@dataclass
class HealthBar:
    max_health: float
    health: float
    regen_rate: float  # health per second

    @classmethod
    def load_assets(cls):
        cls.FRAME = pygame.transform.scale(
            pygame.image.load("shooter/assets/health_bar.png").convert_alpha(),
            (600, 60)
        )
        cls.FILL = pygame.transform.scale(
            pygame.image.load("shooter/assets/health_bar_fill.png").convert_alpha(),
            (600,60)
        )

    @classmethod
    def create(cls, max_health: float, regen_rate: float) -> "HealthBar":
        """Factory: start at full health."""
        return cls(max_health=max_health, health=max_health, regen_rate=regen_rate)

    def update(self, dt: float) -> None:
        """Optionally regenerate over time. dt = seconds since last frame."""
        if self.regen_rate > 0:
            self.health = min(self.max_health, self.health + self.regen_rate * dt)

    def draw(self, surface: pygame.Surface, x: int, y: int) -> None:
        """Draw the health bar at (x, y)."""
        # frame
        surface.blit(self.FRAME, (x, y))

        # clamp ratio between 0 and 1
        ratio = max(0.0, min(1.0, self.health / self.max_health))

        # how wide the fill should be
        full_width = self.FILL.get_width()
        fill_width = int(full_width * ratio)

        # take a slice of the fill image
        fill_src_rect = pygame.Rect(0, 0, fill_width, self.FILL.get_height())

        # position inside frame – tweak these offsets to match your art
        fill_x = x
        fill_y = y

        surface.blit(self.FILL, (fill_x, fill_y), fill_src_rect)
    


@dataclass
class AmmoBar:
    max_ammo: int
    ammo: int
    regen_rate: float  # bullets/second

    @classmethod
    def load_assets(cls):
        cls.FRAME = pygame.transform.scale(
            pygame.image.load("shooter/assets/ammo_bar.png").convert_alpha(),
            (600, 60)
        )
        cls.FILL = pygame.transform.scale(
            pygame.image.load("shooter/assets/ammo_bar_fill.png").convert_alpha(),
            (600,60)
        )

    @classmethod
    def create(cls, max_ammo: int, regen_rate: float) -> "AmmoBar":
        """Factory: start at full ammo."""
        return cls(max_ammo=max_ammo, ammo=max_ammo, regen_rate=regen_rate)

    def update(self, dt: float) -> None:
        """Optionally regenerate over time. dt = seconds since last frame."""
        if self.regen_rate > 0:
            # allow fractional regen but keep ammo as integer
            self.ammo += self.regen_rate * dt

    def draw(self, surface: pygame.Surface, x: int, y: int) -> None:
        """Draw the ammo bar at (x, y)."""
        # frame
        surface.blit(self.FRAME, (x, y))

        # clamp ratio between 0 and 1
        ratio = max(0.0, min(1.0, self.ammo / self.max_ammo))

        # how wide the fill should be
        full_width = self.FILL.get_width()
        fill_width = int(full_width * ratio)

        # take a slice of the fill image
        fill_src_rect = pygame.Rect(0, 0, fill_width, self.FILL.get_height())

        # position inside frame – tweak these offsets to match art
        fill_x = x
        fill_y = y

        surface.blit(self.FILL, (fill_x, fill_y), fill_src_rect)