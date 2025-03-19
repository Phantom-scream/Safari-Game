import pygame
import random
import math
import time  # For thirst timer

class Animal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target = (random.uniform(0, 800), random.uniform(0, 600))  # Random walk target
        self.color = (200, 50, 50)  # Red for now
        self.vision_range = 100  # Can see 100 pixels around
        self.known_water_sources = []  # Remembers found water
        self.thirst_timer = time.time()  # Tracks thirst time

    def move(self):
        """Move smoothly towards the target"""
        dx, dy = self.target[0] - self.x, self.target[1] - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 2:  # Move only if far
            self.x += (dx / distance) * 2
            self.y += (dy / distance) * 2
        else:
            self.target = (random.uniform(50, 750), random.uniform(50, 550))  # New target

    def find_water(self, world):
        """Detect nearby water and remember locations"""
        for water in world.water_sources:
            distance = math.sqrt((water.x - self.x)**2 + (water.y - self.y)**2)
            if distance < self.vision_range and (water.x, water.y) not in self.known_water_sources:
                self.known_water_sources.append((water.x, water.y))

    def go_to_water(self):
        """Go to the closest remembered water source"""
        if self.known_water_sources:
            self.target = min(self.known_water_sources, key=lambda w: math.dist((self.x, self.y), w))

    def update(self, world):
        """Update movement and check thirst every frame"""
        self.move()
        self.find_water(world)

        # Every 8 seconds, go to water
        if time.time() - self.thirst_timer > 8:
            self.go_to_water()
            self.thirst_timer = time.time()  # Reset thirst timer

    def draw(self, screen):
        """Draw the animal"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, 15, 15))