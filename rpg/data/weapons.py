from dataclasses import dataclass

@dataclass(frozen=True)
class Weapon:
    name: str
    damage: int
    reach: float          # pixels
    arc_deg: float        # total arc in degrees
    cooldown: float       # seconds
    art:str               # path to art asset


# Example weapons

DAGGER = Weapon(
    name="Dagger",
    damage=15,
    reach=40,
    arc_deg=60,
    cooldown=0.3,
    art = "rpg/assets/weapons/dagger.png"
)

SWORD = Weapon(
    name="Sword",
    damage=25,
    reach=60,
    arc_deg=100,
    cooldown=0.5,
    art = "rpg/assets/weapons/sword.png"
)

HALBERD = Weapon(
    name="Halberd",
    damage=35,
    reach=90,
    arc_deg=70,
    cooldown=0.8,
    art = "rpg/assets/weapons/halberd.png"
)
