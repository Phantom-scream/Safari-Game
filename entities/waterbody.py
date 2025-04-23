from ui.vector2 import Vector2
import pygame
from entities.entity import Entity
import random
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gamelogic.game_world import GameWorld
    from ui.camera import Camera

class WaterBody(Entity):
    def __init__(self, position: Vector2, size: float):
        super().__init__(position, size, 'WaterBody')
        self.color = (0, 0, 255)
        self.connected_cells = [position]  # Initialize with at least the center position
        
    def drink(self, amount: float) -> float:
        return amount

    def update(self, deltaTime: float, world: 'GameWorld'):
        pass

    def render(self, surface: pygame.Surface, camera: 'Camera'):
        screenPos = camera.worldToScreen(self.position)
        size = self.size * camera.zoom
        pygame.draw.rect(surface, self.color, (screenPos.x, screenPos.y, size, size))