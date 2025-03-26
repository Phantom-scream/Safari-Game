from abc import ABC, abstractmethod
from ui.vector2 import Vector2
import pygame
import random
import math
import time
from entities.entity import Entity

class Animal(Entity, ABC):
    reproduction_lock = None  
    species_list = [] 
    current_species_index = 0 

    def __init__(self, position: Vector2, size: float, entityType: str, speed: float):
        super().__init__(position, size, entityType)
        self.speed = speed
        self.target = Vector2(random.uniform(0, 800), random.uniform(0, 600)) 
        self.color = (200, 50, 50) 
        self.vision_range = 100
        self.known_water_sources = []
        self.thirst_timer = time.time()
        self.reproduction_timer = time.time() 
        self.is_reproducing = False 
        self.limit = 0 

        if type(self).__name__ not in Animal.species_list:
            Animal.species_list.append(type(self).__name__)

    @classmethod
    def get_number(cls):
        return random.randint(1, cls.limit)

    def move(self):
        if self.is_reproducing:
            return  # Stop moving while reproducing

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

    def reproduce(self, world):
        if Animal.reproduction_lock is None:
            Animal.reproduction_lock = Animal.species_list[Animal.current_species_index]

        if Animal.reproduction_lock == type(self).__name__:
            if time.time() - self.reproduction_timer > 10: 
                self.is_reproducing = True
                self.reproduction_timer = time.time()

                new_position = Vector2(
                    self.position.x + random.uniform(-50, 50),
                    self.position.y + random.uniform(-50, 50)
                )
                new_animal = type(self)(new_position)
                world.addEntity(new_animal)
                print(f"{self.entityType} reproduced at {new_position}. Total {type(self).__name__}: {len(world.entities[type(self).__name__])}")

                Animal.reproduction_lock = None
                Animal.current_species_index = (Animal.current_species_index + 1) % len(Animal.species_list)

    def update(self, deltaTime: float, world: 'GameWorld'):
        if self.is_reproducing and time.time() - self.reproduction_timer > 4:
            self.is_reproducing = False

        self.move()
        self.find_water(world)

        if time.time() - self.thirst_timer > 8:
            self.go_to_water()
            self.thirst_timer = time.time()

        self.reproduce(world)

    def render(self, surface: pygame.Surface, camera: 'Camera'):
        screenPos = camera.worldToScreen(self.position)
        pygame.draw.rect(surface, self.color, (screenPos.x, screenPos.y, self.size, self.size))