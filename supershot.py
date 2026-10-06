from circleshape import CircleShape
from constants import *
import pygame

class Supershot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SUPER_SHOT_RADIUS)
    def draw(self, screen):
        pygame.draw.circle(screen, COLOR_SUPER_SHOT, (self.position.x, self.position.y), self.radius, LINE_WIDTH)
    def update(self, dt):
        self.position += self.velocity * dt

        if (
            self.position.x + self.radius < 0
            or self.position.x - self.radius > SCREEN_WIDTH
            or self.position.y + self.radius < 0
            or self.position.y - self.radius > SCREEN_HEIGHT
        ):
            self.kill()

