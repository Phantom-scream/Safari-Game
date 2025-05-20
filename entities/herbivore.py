import pygame
import time
from entities.animal import Animal
from ui.vector2 import Vector2
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gamelogic.game_world import GameWorld
    from ui.camera import Camera

class Herbivore(Animal):
    def __init__(self, position: Vector2, size: float, speed: float):
        super().__init__(position, size, 'Herbivore', speed)

    def update(self, deltaTime: float, world: 'GameWorld'):
        if self.is_dead:
            return

        # Use timestamp for eating_timer
        if self.eating_timer is not None:
            if time.time() - self.eating_timer >= 3:
                self.eating_timer = None
                self.hungry_level = 100
                print(f"{self.entityType} at {self.position} finished eating and resumed moving.")
            else:
                return

        self.update_hunger(deltaTime)

        if self.hungry_level < 30:
            print(f"{self.entityType} is hungry (hunger level: {self.hungry_level}). Searching for food...")
            self.find_food(world)

        self.eat_food(world)

        super().update(deltaTime, world)

    def eat_food(self, world):
        if self.eating_timer is None:
            for plant_type in ['Bush', 'Tree']:
                for plant in world.entities.get(plant_type, []):
                    if self.position.distanceTo(plant.position) < self.size:
                        self.eating_timer = time.time()  # <-- Use timestamp!
                        world.removeEntity(plant)
                        print(f"{self.entityType} ate a {plant_type} at {plant.position}.")
                        return

    def render(self, surface: pygame.Surface, camera: 'Camera'):
        screenPos = camera.worldToScreen(self.position)
        size = self.size * camera.zoom
        if hasattr(self, "sprite"):
            scaled_sprite = pygame.transform.scale(self.sprite, (int(size), int(size)))
            surface.blit(scaled_sprite, (screenPos.x, screenPos.y))
        else:
            pygame.draw.rect(surface, self.color, (screenPos.x, screenPos.y, size, size))

class Bison(Herbivore):
    limit = 5

    def __init__(self, position: Vector2):
        super().__init__(position, 40, 100)
        self.color = (139, 69, 19)
        self.sprite = pygame.image.load("assets/bison.png")
        self.sprite.set_colorkey((0, 0, 0))
        self.sprite = self.sprite.convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))

class Zebra(Herbivore):
    limit = 5

    def __init__(self, position: Vector2):
        super().__init__(position, 50, 110)
        self.color = (255, 255, 255)
        self.sprite = pygame.image.load("assets/zebra.png")
        self.sprite.set_colorkey((0, 0, 0))
        self.sprite = self.sprite.convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))

class Antelope(Herbivore):
    limit = 5
    
    def __init__(self, position: Vector2):
        super().__init__(position, 65, 120)
        self.color = (210, 180, 140)
        self.sprite = pygame.image.load("assets/antelope.png")
        self.sprite.set_colorkey((0, 0, 0))
        self.sprite = self.sprite.convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
