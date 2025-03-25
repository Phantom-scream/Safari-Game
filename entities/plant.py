from ui.vector2 import Vector2
import pygame
from entities.entity import Entity

class Plant(Entity):
    def __init__(self, position: Vector2, size: float, nutritionalValue: float):
        super().__init__(position, size, 'Plant')
        self.nutritionalValue = nutritionalValue
        self.color = (0, 255, 0)

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
        pygame.draw.rect(surface, self.color, (screenPos.x, screenPos.y, self.size, self.size))