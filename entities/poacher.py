from entities.entity import Entity
from ui.vector2 import Vector2
import random
import pygame
import math
import time

class Poacher(Entity):
    def __init__(self, position: Vector2, size: float, speed: float):
        super().__init__(position, size, 'Poacher')
        self.speed = speed
        self.target = Vector2(random.uniform(0, 800), random.uniform(0, 600))
        self.color = (255, 0, 0)  # Red color for poachers
        self.isrect = True
        self.last_hunt_time = time.time()  # Timer to track the last hunt

    def move(self):
        dx, dy = self.target.x - self.position.x, self.target.y - self.position.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 2:
            self.position.x += (dx / distance) * self.speed
            self.position.y += (dy / distance) * self.speed
        else:
            self.target = Vector2(random.uniform(50, 750), random.uniform(50, 550))

    def hunt(self, world):
        """Poacher hunts and kills one animal every 7 seconds."""
        current_time = time.time()
        if current_time - self.last_hunt_time < 7:  # Wait for 7 seconds before hunting again
            return

        # Iterate through all animals in the world
        for entity_type in ['Bison', 'Zebra', 'Antelope', 'Lion', 'Hyena', 'Crocodile']:
            for animal in list(world.entities.get(entity_type, [])):  # Use a copy of the list to avoid modifying it during iteration
                distance = self.position.distanceTo(animal.position)
                if distance < self.size * 2:  # Check if the poacher is close enough to "kill" the animal
                    world.removeEntity(animal)  # Remove the animal from the world
                    print(f"Poacher killed {animal.entityType} at {animal.position}")
                    self.last_hunt_time = current_time  # Reset the hunt timer
                    return  # Stop after killing one animal

    def update(self, deltaTime: float, world: 'GameWorld'):
        self.move()
        self.hunt(world)

    def render(self, surface: pygame.Surface, camera: 'Camera'):
        screenPos = camera.worldToScreen(self.position)
        pygame.draw.circle(surface, self.color, (int(screenPos.x), int(screenPos.y)), int(self.size / 2))