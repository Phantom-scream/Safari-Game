from ui.vector2 import Vector2
import pygame
from entities.entity import Entity

class WaterBody(Entity):
    def __init__(self, position: Vector2, size: float):
        super().__init__(position, size, 'WaterBody')
        self.color = (0, 0, 255)

    def drink(self, amount: float) -> float:
        return amount

    def update(self, deltaTime: float, world: 'GameWorld'):
        pass

    def render(self, surface: pygame.Surface, camera: 'Camera'):
        screenPos = camera.worldToScreen(self.position)
        pygame.draw.rect(surface, self.color, (screenPos.x, screenPos.y, self.size, self.size))