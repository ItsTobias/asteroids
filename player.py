import pygame
import random
from circleshape import CircleShape
from constants import *
from shot import Shot
from supershot import Supershot

class Player(CircleShape):
    def __init__(self, x, y, asteroids):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0.0
        self.timer = 0
        self.teleport_timer = 0
        self.super_shoot_timer = 0
        self.asteroids = asteroids

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen) :
        pygame.draw.polygon(screen, COLOR_PLAYER, self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        self.timer -= dt
        self.teleport_timer -= dt
        self.super_shoot_timer -= dt
        keys = pygame.key.get_pressed()
        if keys[pygame.key.key_code(LEFT)]:
            self.rotate((-1 * dt))
        if keys[pygame.key.key_code(RIGHT)]:
            self.rotate(dt)
        if keys[pygame.key.key_code(FORWARD)]:
            self.move(dt)
        if keys[pygame.key.key_code(BACKWARDS)]:
            self.move((dt * -1))
        if keys[pygame.key.key_code(SHOOT)]:
            self.shoot()
        if keys[pygame.key.key_code(BOOST)]:
            self.move((dt * BOOST_AMP))
        if keys[pygame.key.key_code(TELEPORT)] and self.teleport_timer <= 0:
            self.teleport()
        if keys[pygame.key.key_code(SUPER_SHOOT)]:
            self.super_shoot()

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_vector_with_speed = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_vector_with_speed
    
    def shoot(self):
        if self.timer <= 0.0: 
            self.timer = PLAYER_SHOOT_COOLDOWN_SECONDS
            shot = Shot(self.position.x, self.position.y)
            vector = pygame.Vector2(0, 1)
            rotated_vector = vector.rotate(self.rotation)
            rotated_vector_with_speed = rotated_vector * SHOT_SPEED
            shot.velocity = rotated_vector_with_speed

    def super_shoot(self):
        if self.super_shoot_timer <= 0.0:
            self.super_shoot_timer = SUPER_SHOT_TIMER
            shot = Supershot(self.position.x, self.position.y)
            vector = pygame.Vector2(0, 1)
            rotated_vector = vector.rotate(self.rotation)
            rotated_vector_with_speed = rotated_vector * SUPER_SHOT_SPEED
            shot.velocity = rotated_vector_with_speed

    def teleport(self):
        while True:
            self.position.x = random.randint(0, SCREEN_WIDTH)
            self.position.y = random.randint(0, SCREEN_HEIGHT)

            collision = False
            
            for asteroid in self.asteroids:
                if self.collision_with(asteroid):
                    collision = True
                    break
            
            if not collision:
                self.teleport_timer = TELEPORT_COOLDOWN
                break