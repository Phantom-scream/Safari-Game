from abc import ABC
from ui.vector2 import Vector2
import pygame
from entities.entity import Entity

class Plant(Entity, ABC):  # Inherit from ABC
    def __init__(self, position: Vector2, size: float, nutritionalValue: float):
        super().__init__(position, size, 'Plant')
        self.nutritionalValue = nutritionalValue
        self.color = (255, 255, 0)

    def beEaten(self, amount: float) -> float:
        eaten = min(amount, self.nutritionalValue)
        self.nutritionalValue -= eaten
        return eaten

    def getNutritionalValue(self) -> float:
        return self.nutritionalValue

    def update(self, deltaTime: float, world: 'GameWorld'):
        pass

    def render(self, surface: pygame.Surface, camera: 'Camera'):
        screenPos = camera.worldToScreen(self.position)
        size = self.size * camera.zoom
        pygame.draw.rect(surface, self.color, (screenPos.x, screenPos.y, size, size))

# --- New plant types ---

class Bush(Entity):
    def __init__(self, position: Vector2):
        super().__init__(position, 24, "Bush")
        self.color = (34, 139, 34)  # Add a green color for bush
        if not hasattr(Bush, "sprite"):
            Bush.sprite = pygame.image.load("assets/Bush.png").convert_alpha()
        self.sprite = Bush.sprite

    def update(self, deltaTime: float, world: 'GameWorld'):
        pass  # Bush does not need to update

    def render(self, surface, camera):
        screenPos = camera.worldToScreen(self.position)
        size = int(self.size * camera.zoom)
        scaled_sprite = pygame.transform.scale(self.sprite, (size, size))
        surface.blit(scaled_sprite, (screenPos.x, screenPos.y))

class Tree(Entity):
    def __init__(self, position: Vector2):
        super().__init__(position, 40, "Tree")
        self.color = (0, 100, 0)  # Add a dark green color for tree
        if not hasattr(Tree, "sprite"):
            Tree.sprite = pygame.image.load("assets/Tree.png").convert_alpha()
        self.sprite = Tree.sprite

    def update(self, deltaTime: float, world: 'GameWorld'):
        pass  # Tree does not need to update

    def render(self, surface, camera):
        screenPos = camera.worldToScreen(self.position)
        size = int(self.size * camera.zoom)
        scaled_sprite = pygame.transform.scale(self.sprite, (size, size))
        surface.blit(scaled_sprite, (screenPos.x, screenPos.y))

