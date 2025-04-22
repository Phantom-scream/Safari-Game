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

class Bush(Plant):
    def __init__(self, position: Vector2, size: float = 15, nutritionalValue: float = 60):
        super().__init__(position, size, nutritionalValue)
        self.color = (34, 139, 34)  # Forest green

class Tree(Plant):
    def __init__(self, position: Vector2, size: float = 22, nutritionalValue: float = 120):
        super().__init__(position, size, nutritionalValue)
        self.color = (0, 100, 0)  # Dark green

