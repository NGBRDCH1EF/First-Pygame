from dataclasses import dataclass
import pygame
PIXELS_PER_METER = 20  # scaling factor
GRAVITY_MPS2 = 9.81  # meters per second squared
GRAVITY = GRAVITY_MPS2 * PIXELS_PER_METER  # pixels per second squared

class Projectile:
    
    def __init__(self, pos:pygame.Vector2, velocity:pygame.Vector2, radius:int=5, color:tuple=(0,0,0)):
        self.pos = pos
        self.velocity = velocity
        self.radius = radius
        self.color = color
        self.alive = True

    def update(self, dt:float, gravity:float,x_bounds:tuple,y_bounds:tuple):
        #update position based on velocity
        self.pos += self.velocity * dt

        #apply gravity to vertical velocity
        self.velocity.y += gravity * dt

        #check if projectile is out of bounds (below ground level)
        if self.pos.y > y_bounds[1] or self.pos.x < x_bounds[0] or self.pos.x > x_bounds[1]:
            self.alive = False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)


class Cannon:
    
    def __init__(self,pos:pygame.Vector2,max_muzzle_velocity:int):
        #core attributes
        self.pos = pos
        self.angle = 45                         # default angle in degrees
        self.muzzle_velocity = 0                # initial muzzle velocity m/s
        self.max_muzzle_velocity = max_muzzle_velocity   # maximum power
        self.angle_bounds = (10, 80)            # min and max angle
        self.reload_time = 0.5                 # seconds
        self.last_shot_time = -self.reload_time # initialize to allow immediate shooting
        self.barrel_length = 40                 # length of the cannon barrel

        #placeholder for art assets
        self.art = []
        

    def fire(self,projectile_class,current_time):
        if current_time - self.last_shot_time >= self.reload_time:
            #calculate initial velocity components
            direction = pygame.Vector2(1, 0).rotate(-self.angle)  # unit vector in the direction of the cannon
            velocity = direction * self.muzzle_velocity  # scale by power

            #create projectile
            barrel_end_offset = direction * self.barrel_length
            spawn_pos = self.pos + barrel_end_offset
            projectile = projectile_class(spawn_pos, velocity*PIXELS_PER_METER)

            #reset power and update last shot time
            self.last_shot_time = current_time

            return projectile
        return None
    
    def prediction_path(self, projectile_class, num_points:int=50, time_step:float=0.1):
        points = []
        direction = pygame.Vector2(1, 0).rotate(-self.angle)
        velocity = direction * self.muzzle_velocity * PIXELS_PER_METER
        barrel_end_offset = direction * self.barrel_length
        spawn_pos = self.pos + barrel_end_offset

        for i in range(num_points):
            t = i * time_step
            #calculate position at time t
            x = spawn_pos.x + velocity.x * t
            y = spawn_pos.y + velocity.y * t + 0.5 * GRAVITY * t**2
            points.append((x, y))
        
        return points
    
class StatusBar:
    def __init__(self, pos:pygame.Vector2, size:pygame.Vector2, max_value:int, color:tuple):
        self.pos = pygame.Vector2(pos)
        self.size = pygame.Vector2(size)
        self.max_value = max_value
        self.current_value = max_value
        self.color = color

    def update(self, value:int):
        self.current_value = value

    def draw(self, surface):
        #draw background
        pygame.draw.rect(surface, (50, 50, 50), (self.pos.x, self.pos.y, self.size.x, self.size.y))
        #draw filled portion
        fill_width = (self.current_value / self.max_value) * self.size.x
        pygame.draw.rect(surface, self.color, (self.pos.x, self.pos.y, fill_width, self.size.y))