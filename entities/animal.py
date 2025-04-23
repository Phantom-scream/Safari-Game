from abc import ABC, abstractmethod
from ui.vector2 import Vector2
import pygame
import random
import math
import time
from entities.entity import Entity
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gamelogic.game_world import GameWorld
    from ui.camera import Camera

class Animal(Entity, ABC):
    reproduction_lock = None  
    species_list = [] 
    current_species_index = 0 
    last_reproduction_times = {}
    SLOW_FACTOR = 0.25  # Animals are 4x slower

    def __init__(self, position: Vector2, size: float, entityType: str, speed: float):
        super().__init__(position, size, entityType)
        self.speed = speed
        self.target = Vector2(random.uniform(0, 800), random.uniform(0, 600)) 
        self.color = (200, 50, 50)
        self.vision_range = 100
        self.known_water_sources = []
        self.known_plant_sources = []  # Initialize known plant sources
        self.reproduction_timer = time.time() 
        self.is_reproducing = False 
        self.limit = 0 
        self.is_dead = False  # Attribute to track if the animal is dead
        self.thirst_level = 100  # New attribute: thirst level (max 100)
        self.drinking_timer = None  # Timer to track drinking duration
        self.last_drink_time = 0
        self.drink_cooldown = 2.0  # seconds to wait before drinking again
        self.last_water_position = None  # Add this line
        self.hungry_level = 100  # New attribute: hunger level (max 100)
        self.eating_timer = None  # Timer to track eating duration
        self.age = random.uniform(0, 10)  # Set a random age between 0 and 10 years


        if type(self).__name__ not in Animal.species_list:
            Animal.species_list.append(type(self).__name__)

    @classmethod
    def get_number(cls):
        return random.randint(1, cls.limit)

    def move(self, deltaTime, world):
        dx, dy = self.target.x - self.position.x, self.target.y - self.position.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 2:
            # Predict next position
            step_x = self.position.x + (dx / distance) * self.speed * deltaTime
            step_y = self.position.y + (dy / distance) * self.speed * deltaTime

            # --- Simple obstacle avoidance: check for collision with obstacles ---
            collision = False
            # Example: avoid water and hills (customize as needed)
            for obstacle in world.entities.get('WaterBody', []):
                if Vector2(step_x, step_y).distanceTo(obstacle.position) < obstacle.size:
                    collision = True
                    break
            # You can add more checks for hills, rocks, or other animals here

            if collision:
                # Steer: pick a new random nearby target to avoid obstacle
                self.target = Vector2(
                    self.position.x + random.uniform(-100, 100),
                    self.position.y + random.uniform(-100, 100)
                )
            else:
                self.position.x = step_x
                self.position.y = step_y
        else:
            self.target = Vector2(
                random.uniform(0, 1600),
                random.uniform(0, 1200)
            )


    def find_food(self, world):
        current_plant_positions = set()
        for plant_type in ['Bush', 'Tree']:
            current_plant_positions.update(plant.position for plant in world.entities.get(plant_type, []))
        self.known_plant_sources = [
            pos for pos in self.known_plant_sources if pos in current_plant_positions
        ]
        for plant_type in ['Bush', 'Tree']:
            for plant in world.entities.get(plant_type, []):
                if self.position.distanceTo(plant.position) < self.vision_range and plant.position not in self.known_plant_sources:
                    self.known_plant_sources.append(plant.position)
        if self.known_plant_sources:
            closest = min(self.known_plant_sources, key=lambda pos: self.position.distanceTo(pos))
            self.target = closest


    def eat_food(self, world):
        if self.eating_timer is None:
            for plant_type in ['Bush', 'Tree']:
                for plant in world.entities.get(plant_type, []):
                    if self.position.distanceTo(plant.position) < max(self.size, plant.size):
                        self.eating_timer = time.time()
                        world.removeEntity(plant)
                        print(f"{self.entityType} at {self.position} started eating a {plant_type}.")
                        return

    def update_hunger(self, deltaTime: float):
        """Decrease hunger level over time."""
        self.hungry_level -= deltaTime * 5  # Decrease hunger level (adjust rate as needed)
        if self.hungry_level < 0:
            self.hungry_level = 0  # Ensure hunger level does not go below 0



    def find_water(self, world):
        current_water_positions = {water.position for water in world.entities.get('WaterBody', [])}
        self.known_water_sources = [
            pos for pos in self.known_water_sources if pos in current_water_positions
        ]
        for water in world.entities.get('WaterBody', []):
            if self.position.distanceTo(water.position) < self.vision_range and water.position not in self.known_water_sources:
                self.known_water_sources.append(water.position)

    def go_to_water(self):
        if self.known_water_sources:
            closest = min(self.known_water_sources, key=lambda pos: self.position.distanceTo(pos))
            self.target = closest

    def drink_water(self, water_position):
        if self.drinking_timer is None:
            self.drinking_timer = time.time()
            self.last_water_position = water_position

    def update(self, deltaTime: float, world: 'GameWorld'):
        deltaTime *= self.SLOW_FACTOR  # Slow down all animal logic

        print(f"Updating {self.entityType} at {self.position}, age: {self.age:.2f}, thirst: {self.thirst_level}, dead: {self.is_dead}")


        if self.is_dead:
            return  # Dead animals do not update

        # Update age
        self.update_age(deltaTime)

        
        # Handle drinking timer
        if self.drinking_timer is not None:
            if time.time() - self.drinking_timer >= 1:  # <-- Drink for only 1 second
                self.thirst_level = 100
                self.drinking_timer = None
                self.last_drink_time = time.time()
                # Set a new target AWAY from water
                if self.last_water_position:
                    dx = self.position.x - self.last_water_position.x
                    dy = self.position.y - self.last_water_position.y
                    length = math.sqrt(dx**2 + dy**2) or 1
                    # Move 100 units away in the opposite direction
                    self.target = Vector2(
                        self.position.x + (dx / length) * 100,
                        self.position.y + (dy / length) * 100
                    )
                else:
                    # fallback: random direction
                    self.target = Vector2(
                        self.position.x + random.randint(-100, 100),
                        self.position.y + random.randint(-100, 100)
                    )
            else:
                return

        # After drinking logic, before allowing to drink again:
        if time.time() - self.last_drink_time < self.drink_cooldown or (
            self.last_water_position and self.position.distanceTo(self.last_water_position) < self.size * 2
        ):
            # Skip drinking logic, allow movement away
            self.move(deltaTime, world)
            return

        # Prevent immediate re-drinking after cooldown
        if time.time() - self.last_drink_time < self.drink_cooldown:
            # Skip drinking logic, allow movement away
            self.move(deltaTime, world)
            return

        # Update thirst level
        self.thirst_level -= 10 * deltaTime  # 10 units per second, adjust as needed
        self.thirst_level = max(self.thirst_level, 0)

        # If thirst level is below 30, prioritize going to water
        if self.thirst_level < 30:
            self.find_water(world)      # <--- Ensure this is called every time when thirsty
            self.go_to_water()

        # If near a water source, start drinking water
        for water in world.entities['WaterBody']:
            if self.position.distanceTo(water.position) < self.size:
                # --- Repulsion: Check if another animal is already drinking here ---
                crowded = False
                for other in world.entities.get(type(self).__name__, []):
                    if other is not self and other.drinking_timer is not None:
                        if other.position.distanceTo(water.position) < self.size:
                            crowded = True
                            break
                if not crowded:
                    self.drink_water(water.position)  # Pass water position here
                else:
                    # Move away a bit to avoid crowding
                    self.target = Vector2(
                        self.position.x + random.uniform(-50, 50),
                        self.position.y + random.uniform(-50, 50)
                    )
                break

        if self.is_reproducing and time.time() - self.reproduction_timer > 4:
            self.is_reproducing = False

        self.move(deltaTime, world)
        self.find_water(world)
        self.reproduce(world)

    def update_age(self, deltaTime: float):
        """Increase the animal's age over time."""
        self.age += deltaTime / 60  # Convert deltaTime to years (assuming 1 second = 1 minute in-game)
        if self.age > 10:  # Example: animals die after 10 years
            self.mark_as_dead()

    def reproduce(self, world):
        if self.is_dead or self.age < 3:  # Dead animals or animals younger than 3 years cannot reproduce
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
            if animal != self and not animal.is_reproducing and not animal.is_dead and animal.age >= 3 and self.position.distanceTo(animal.position) < self.size * 2
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
            new_animal.age = 0  # Set the age of the new animal to 0
            world.addEntity(new_animal)


    def mark_as_dead(self):
        """Mark the animal as dead."""
        self.is_dead = True
        self.is_dead = True

    def render(self, surface: pygame.Surface, camera: 'Camera'):
        screenPos = camera.worldToScreen(self.position)
        size = self.size * camera.zoom  # Scale size by zoom
        pygame.draw.rect(surface, self.color, (screenPos.x, screenPos.y, size, size))