import pygame
from entities.animal import Animal
from ui.vector2 import Vector2
import random
import math

class Carnivore(Animal):
    def __init__(self, position: Vector2, size: float, speed: float):
        super().__init__(position, size, 'Carnivore', speed)
        self.hunger_level = 100
        self.hunting_target = None

    def update_hunger(self, deltaTime: float):
        self.hunger_level -= deltaTime * 5
        if self.hunger_level < 0:
            self.hunger_level = 0

    def find_prey(self, world):
        nearest_prey = None
        nearest_distance = float('inf')
        for herbivore_type in ['Bison', 'Zebra', 'Antelope']:
            for herbivore in world.entities.get(herbivore_type, []):
                if not herbivore.is_dead:
                    distance = self.position.distanceTo(herbivore.position)
                    if distance < nearest_distance and distance <= self.vision_range:
                        nearest_distance = distance
                        nearest_prey = herbivore
        if nearest_prey:
            self.hunting_target = nearest_prey
            self.target = nearest_prey.position
            print(f"{self.entityType} is hunting {nearest_prey.entityType} at {nearest_prey.position}.")
        else:
            self.hunting_target = None
            self.target = Vector2(
                self.position.x + random.uniform(-200, 200),
                self.position.y + random.uniform(-200, 200)
            )
            print(f"{self.entityType} could not find any prey nearby, wandering randomly.")

    def hunt_prey(self, deltaTime: float, world):
        if self.hunting_target and not self.hunting_target.is_dead:
            distance_to_prey = self.position.distanceTo(self.hunting_target.position)
            if distance_to_prey < self.size:
                self.hunting_target.mark_as_dead()
                world.removeEntity(self.hunting_target)
                self.hunting_target = None
                self.hunger_level = 100
                print(f"{self.entityType} has killed its prey and reset hunger level.")
            else:
                direction = Vector2(
                    self.hunting_target.position.x - self.position.x,
                    self.hunting_target.position.y - self.position.y
                ).normalize()
                self.position.x += direction.x * self.speed * deltaTime
                self.position.y += direction.y * self.speed * deltaTime
        else:
            self.hunting_target = None

    def update(self, deltaTime: float, world: 'GameWorld'):
        if self.is_dead:
            return
        self.update_hunger(deltaTime)
        if self.hunger_level < 30:
            if not self.hunting_target:
                self.find_prey(world)
            self.hunt_prey(deltaTime, world)
            return
        super().update(deltaTime, world)

    def render(self, surface: pygame.Surface, camera: 'Camera'):
        screenPos = camera.worldToScreen(self.position)
        size = self.size * camera.zoom
        if hasattr(self, "sprite"):
            scaled_sprite = pygame.transform.scale(self.sprite, (int(size), int(size)))
            surface.blit(scaled_sprite, (screenPos.x, screenPos.y))
        else:
            pygame.draw.rect(surface, self.color, (screenPos.x, screenPos.y, size, size))

class Lion(Carnivore):
    limit = 4
    def __init__(self, position: Vector2):
        super().__init__(position, 60, 110)
        self.color = (255, 165, 0)
        self.sprite = pygame.image.load("assets/lion.png")
        self.sprite.set_colorkey((0, 0, 0))
        self.sprite = self.sprite.convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))

class Hyena(Carnivore):
    limit = 6
    def __init__(self, position: Vector2):
        super().__init__(position, 35, 115)
        self.color = (128, 128, 128)
        self.sprite = pygame.image.load("assets/hyena.png")
        self.sprite.set_colorkey((0, 0, 0))
        self.sprite = self.sprite.convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))

class Crocodile(Carnivore):
    limit = 4
    def __init__(self, position: Vector2):
        super().__init__(position, 45, 80)
        self.color = (0, 100, 0)
        self.sprite = pygame.image.load("assets/crocodile.png")
        self.sprite.set_colorkey((0, 0, 0))
        self.sprite = self.sprite.convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))