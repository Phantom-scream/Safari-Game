import pygame
import time
from entities.animal import Animal
from ui.vector2 import Vector2

class Herbivore(Animal):
    def __init__(self, position: Vector2, size: float, speed: float):
        super().__init__(position, size, 'Herbivore', speed)
        self.eating_elapsed = 0

    def update(self, deltaTime: float, world: 'GameWorld'):
        if self.is_dead:
            return  # Dead animals do not update

        # Eating logic using deltaTime
        if self.eating_timer is not None:
            self.eating_elapsed += deltaTime
            if self.eating_elapsed >= 3:  # Eat for 3 simulated seconds
                self.eating_timer = None
                self.eating_elapsed = 0
                self.hungry_level = 100  # Reset hunger level to maximum
                print(f"{self.entityType} at {self.position} finished eating and resumed moving.")
            else:
                return  # Skip other updates while eating

        # Update hunger level
        self.update_hunger(deltaTime)

        # If hunger level is below 30, prioritize finding food
        if self.hungry_level < 30:
            print(f"{self.entityType} is hungry (hunger level: {self.hungry_level}). Searching for food...")
            self.find_food(world)

        # If near a plant, start eating
        self.eat_food(world)

        # Continue with normal behavior
        super().update(deltaTime, world)

    def eat_food(self, world):
        if self.eating_timer is None:
            for plant_type in ['Bush', 'Tree']:
                for plant in world.entities.get(plant_type, []):
                    if self.position.distanceTo(plant.position) < self.size:
                        self.eating_timer = True
                        self.eating_elapsed = 0
                        world.removeEntity(plant)
                        print(f"{self.entityType} ate a {plant_type} at {plant.position}.")
                        return

    def render(self, surface: pygame.Surface, camera: 'Camera'):
        screenPos = camera.worldToScreen(self.position)
        size = self.size * camera.zoom
        if hasattr(self, "sprite"):
            # Scale the sprite to the current zoom
            scaled_sprite = pygame.transform.scale(self.sprite, (int(size), int(size)))
            surface.blit(scaled_sprite, (screenPos.x, screenPos.y))
        else:
            pygame.draw.rect(surface, self.color, (screenPos.x, screenPos.y, size, size))

class Bison(Herbivore):
    limit = 5

    def __init__(self, position: Vector2):
        super().__init__(position, 40, 100)  # <-- Set speed to 100
        self.color = (139, 69, 19)
        
        # Load image first
        self.sprite = pygame.image.load("assets/elephent.png")
        
        # Make the black background transparent 
        # Do this BEFORE scaling for best results
        self.sprite.set_colorkey((0, 0, 0))
        
        # Convert after setting colorkey
        self.sprite = self.sprite.convert_alpha()
        
        # Now scale the image
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
    
    def render(self, surface: pygame.Surface, camera: 'Camera'):
        screenPos = camera.worldToScreen(self.position)
        size = self.size * camera.zoom
        if hasattr(self, "sprite"):
            scaled_sprite = pygame.transform.scale(self.sprite, (int(size), int(size)))
            surface.blit(scaled_sprite, (screenPos.x, screenPos.y))
        else:
            pygame.draw.rect(surface, self.color, (screenPos.x, screenPos.y, size, size))

class Zebra(Herbivore):
    limit = 5

    def __init__(self, position: Vector2):
        super().__init__(position, 20, 110)  # <-- Set speed to 110
        self.color = (255, 255, 255)

class Antelope(Herbivore):
    limit = 5
    
    def __init__(self, position: Vector2):
        super().__init__(position, 20, 120)  # <-- Set speed to 120
        self.color = (210, 180, 140)
