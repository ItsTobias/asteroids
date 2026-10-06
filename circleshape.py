import pygame


class CircleShape(pygame.sprite.Sprite):

    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        pass

    def update(self, dt):
        pass

    def collision_with(self, other):
        distance_squared = self.position.distance_squared_to(other.position)
        radius_sum = self.radius + other.radius
        return distance_squared <= radius_sum * radius_sum
