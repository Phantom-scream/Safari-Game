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
    last_reproduction_times = {}

    def __init__(self, position: Vector2, size: float, entityType: str, speed: float):
        super().__init__(position, size, entityType)
        self.speed = speed
        self.target = Vector2(random.uniform(0, 800), random.uniform(0, 600)) 
        self.color = (200, 50, 50) 
        self.vision_range = 100
        self.known_water_sources = []
        self.reproduction_timer = time.time() 
        self.is_reproducing = False 
        self.limit = 0 
        self.is_dead = False  # Attribute to track if the animal is dead
        self.thirst_level = 100  # New attribute: thirst level (max 100)

        if type(self).__name__ not in Animal.species_list:
            Animal.species_list.append(type(self).__name__)

    @classmethod
    def get_number(cls):
        return random.randint(1, cls.limit)

    def move(self):
        if self.is_reproducing or self.is_dead:
            return  # Stop moving if reproducing or dead

        dx, dy = self.target.x - self.position.x, self.target.y - self.position.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 2:
            self.position.x += (dx / distance) * self.speed
            self.position.y += (dy / distance) * self.speed
        else:
            # Update target to cover the entire map dimensions
            self.target = Vector2(
                random.uniform(0, 1600),  # WORLD_WIDTH from settings
                random.uniform(0, 1200)  # WORLD_HEIGHT from settings
            )

    def find_water(self, world):
        if self.is_dead:
            return  # Dead animals cannot find water

        for water in world.entities['WaterBody']:
            distance = self.position.distanceTo(water.position)
            if distance < self.vision_range and water.position not in self.known_water_sources:
                self.known_water_sources.append(water.position)

    def go_to_water(self):
        if self.is_dead:
            return  # Dead animals cannot move to water

        if self.known_water_sources:
            self.target = min(self.known_water_sources, key=lambda w: self.position.distanceTo(w))

    def drink_water(self):
        """Increase thirst level when drinking water."""
        self.thirst_level = 100  # Reset thirst level to maximum

        
    def update_thirst(self, deltaTime: float):
        """Decrease thirst level over time."""
        self.thirst_level -= deltaTime * 5  # Decrease thirst level (adjust rate as needed)
        if self.thirst_level < 0:
            self.thirst_level = 0  # Ensure thirst level does not go below 0

    def reproduce(self, world):
        if self.is_dead:  # Dead animals cannot reproduce
            return

        current_time = time.time()
        species_name = type(self).__name__

        # Initialize timer if not present
        if species_name not in Animal.last_reproduction_times:
            Animal.last_reproduction_times[species_name] = 0

        # Enforce species-wide 8-second cooldown
        if current_time - Animal.last_reproduction_times[species_name] < 8:
            return

        # Look for a partner nearby
        nearby_animals = [
            animal for animal in world.entities.get(species_name, [])
            if animal != self and not animal.is_reproducing and not animal.is_dead and self.position.distanceTo(animal.position) < self.size * 2
        ]

        if nearby_animals:
            partner = nearby_animals[0]
            self.is_reproducing = True
            partner.is_reproducing = True

            # Update global species reproduction time
            Animal.last_reproduction_times[species_name] = current_time

            # Create baby in between
            mid_x = (self.position.x + partner.position.x) / 2
            mid_y = (self.position.y + partner.position.y) / 2
            new_position = Vector2(
                mid_x + random.uniform(-20, 20),
                mid_y + random.uniform(-20, 20)
            )
            new_animal = type(self)(new_position)  # New animals are created without age
            world.addEntity(new_animal)

            print(f"{species_name} pair reproduced at {new_position}. Total {species_name}: {len(world.entities[species_name])}")

    def mark_as_dead(self):
        """Mark the animal as dead."""
        self.is_dead = True

    def update(self, deltaTime: float, world: 'GameWorld'):
        if self.is_dead:
            return  # Dead animals do not update

        # Update thirst level
        self.update_thirst(deltaTime)

        # If thirst level is below 30, prioritize going to water
        if self.thirst_level < 30:
            self.go_to_water()

        # If near a water source, drink water
        for water in world.entities['WaterBody']:
            if self.position.distanceTo(water.position) < self.size:
                self.drink_water()
                break

        if self.is_reproducing and time.time() - self.reproduction_timer > 4:
            self.is_reproducing = False

        self.move()
        self.find_water(world)
        self.reproduce(world)

    def render(self, surface: pygame.Surface, camera: 'Camera'):
        screenPos = camera.worldToScreen(self.position)
        size = self.size * camera.zoom  # Scale size by zoom
        pygame.draw.rect(surface, self.color, (screenPos.x, screenPos.y, size, size))