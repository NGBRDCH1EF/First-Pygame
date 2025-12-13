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
GOBLIN_DAGGER = Weapon(
    name="Goblin Dagger",
    damage=1,
    reach=90,
    arc_deg=50,
    cooldown=0.5,
    stamina_cost=3,
    art = "")


DAGGER = Weapon(
    name="Dagger",
    damage=10,
    reach=90,
    arc_deg=60,
    cooldown=0.5,
    stamina_cost=5,
    art = "rpg/assets/dagger.png"
)

SWORD = Weapon(
    name="Sword",
    damage=20,
    reach=120,
    arc_deg=100,
    cooldown=0.8,
    stamina_cost=10,
    art = "rpg/assets/sword.png"
)

HALBERD = Weapon(
    name="Halberd",
    damage=30,
    reach=180,
    arc_deg=120,
    cooldown=1,
    stamina_cost=20,
    art = "rpg/assets/halberd.png"
)
