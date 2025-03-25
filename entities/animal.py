from abc import ABC, abstractmethod
from ui.vector2 import Vector2
import pygame
import random
import math
import time
from entities.entity import Entity

class Animal(Entity, ABC):
    def __init__(self, position: Vector2, size: float, entityType: str, speed: float):
        super().__init__(position, size, entityType)
        self.speed = speed
        self.target = Vector2(random.uniform(0, 800), random.uniform(0, 600)) 
        self.color = (200, 50, 50) 
        self.vision_range = 100
        self.known_water_sources = []
        self.thirst_timer = time.time()

    def move(self):
        dx, dy = self.target.x - self.position.x, self.target.y - self.position.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 2:
            self.position.x += (dx / distance) * self.speed
            self.position.y += (dy / distance) * self.speed
        else:
            self.target = Vector2(random.uniform(50, 750), random.uniform(50, 550))

    def find_water(self, world):
        for water in world.entities['WaterBody']:
            distance = self.position.distanceTo(water.position)
            if distance < self.vision_range and water.position not in self.known_water_sources:
                self.known_water_sources.append(water.position)

    def go_to_water(self):
        if self.known_water_sources:
            self.target = min(self.known_water_sources, key=lambda w: self.position.distanceTo(w))

    def update(self, deltaTime: float, world: 'GameWorld'):
        self.move()
        self.find_water(world)

        if time.time() - self.thirst_timer > 8:
            self.go_to_water()
            self.thirst_timer = time.time()

    def render(self, surface: pygame.Surface, camera: 'Camera'):
        screenPos = camera.worldToScreen(self.position)
        pygame.draw.rect(surface, self.color, (screenPos.x, screenPos.y, self.size, self.size))