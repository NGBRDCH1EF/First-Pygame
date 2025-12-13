from dataclasses import dataclass

@dataclass(frozen=True)
class Weapon:
    name: str
    damage: int
    reach: float      # pixels
    arc_deg: float    # total arc
    cooldown: float   # seconds
    art: str  # path to art asset
    stamina_cost: int = 10  # default stamina cost per attack
    

# Example weapons

DAGGER = Weapon(
    name="Dagger",
    damage=15,
    reach=40,
    arc_deg=60,
    cooldown=0.3,
    stamina_cost=5,
    art = "rpg/assets/dagger.png"
)

SWORD = Weapon(
    name="Sword",
    damage=25,
    reach=60,
    arc_deg=100,
    cooldown=0.5,
    stamina_cost=15,
    art = "rpg/assets/sword.png"
)

HALBERD = Weapon(
    name="Halberd",
    damage=35,
    reach=90,
    arc_deg=70,
    cooldown=0.8,
    stamina_cost=25,
    art = "rpg/assets/halberd.png"
)
