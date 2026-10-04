from constants import *
from circleshape import *
from logger import log_event
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    def draw(self, screen):
        if self.radius == ASTEROID_RARE_RADIUS:
            color = COLOR_ASTEROID_RARE
        else:
            color = COLOR_ASTROIDS
        pygame.draw.circle(screen, color, (self.position.x, self.position.y), self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt   
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        random_angle = random.uniform(20, 50)
        first_velocity = self.velocity.rotate(random_angle)
        second_velocity = self.velocity.rotate(-1*random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS 
        first_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        second_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        first_asteroid.velocity = first_velocity * SPLITTED_ASTEROID_VELOCITY_MULTIPLIER
        second_asteroid.velocity = second_velocity * SPLITTED_ASTEROID_VELOCITY_MULTIPLIER