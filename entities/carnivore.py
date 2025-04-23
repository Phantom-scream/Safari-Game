from entities.animal import Animal
from ui.vector2 import Vector2
import random
import math

class Carnivore(Animal):
    def __init__(self, position: Vector2, size: float, speed: float):
        super().__init__(position, size, 'Carnivore', speed)
        self.hunger_level = 100  # Maximum hunger level
        self.hunting_target = None  # Target herbivore to hunt

    def update_hunger(self, deltaTime: float):
        """Decrease hunger level over time."""
        self.hunger_level -= deltaTime * 5  # Decrease hunger level (adjust rate as needed)
        if self.hunger_level < 0:
            self.hunger_level = 0  # Ensure hunger level does not go below 0

    def find_prey(self, world):
        """Find the nearest herbivore to hunt."""
        nearest_prey = None
        nearest_distance = float('inf')

        for herbivore_type in ['Bison', 'Zebra', 'Antelope']:
            for herbivore in world.entities.get(herbivore_type, []):
                if not herbivore.is_dead:  # Only target alive herbivores
                    distance = self.position.distanceTo(herbivore.position)
                    if distance < nearest_distance and distance <= self.vision_range:
                        nearest_distance = distance
                        nearest_prey = herbivore

        if nearest_prey:
            self.hunting_target = nearest_prey
            self.target = nearest_prey.position  # Set the prey's position as the target
            print(f"{self.entityType} is hunting {nearest_prey.entityType} at {nearest_prey.position}.")
        else:
            self.hunting_target = None
            print(f"{self.entityType} could not find any prey nearby.")

    def hunt_prey(self, deltaTime: float, world):
        """Chase and kill the prey."""
        if self.hunting_target and not self.hunting_target.is_dead:
            distance_to_prey = self.position.distanceTo(self.hunting_target.position)
            if distance_to_prey < self.size:  # Attack range
                # Kill the prey
                self.hunting_target.mark_as_dead()
                world.removeEntity(self.hunting_target)
                self.hunting_target = None
                self.hunger_level = 100  # Reset hunger level after killing
                print(f"{self.entityType} has killed its prey and reset hunger level.")
            else:
                # Move toward the prey
                direction = Vector2(
                    self.hunting_target.position.x - self.position.x,
                    self.hunting_target.position.y - self.position.y
                ).normalize()
                self.position.x += direction.x * self.speed * deltaTime
                self.position.y += direction.y * self.speed * deltaTime
        else:
            self.hunting_target = None  # Reset target if prey is dead or unavailable

    def update(self, deltaTime: float, world: 'GameWorld'):
        if self.is_dead:
            return  # Dead animals do not update

        # Update hunger level
        self.update_hunger(deltaTime)

        # If hunger level is below 30, prioritize hunting
        if self.hunger_level < 30:
            if not self.hunting_target:
                self.find_prey(world)
            self.hunt_prey(deltaTime, world)
            return  # Skip other behaviors while hunting

        # Continue with normal behavior
        super().update(deltaTime, world)


class Lion(Carnivore):
    limit = 4

    def __init__(self, position: Vector2):
        super().__init__(position, 25, 110)  # Set speed to 110
        self.color = (255, 165, 0)


class Hyena(Carnivore):
    limit = 6

    def __init__(self, position: Vector2):
        super().__init__(position, 20, 115)  # Set speed to 115
        self.color = (128, 128, 128)


class Crocodile(Carnivore):
    limit = 4

    def __init__(self, position: Vector2):
        super().__init__(position, 30, 80)  # Set speed to 80
        self.color = (0, 100, 0)