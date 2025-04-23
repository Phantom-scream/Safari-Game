from abc import ABC, abstractmethod
from ui.vector2 import Vector2
import pygame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gamelogic.game_world import GameWorld
    from ui.camera import Camera


class Entity(ABC):
    def __init__(self, position: Vector2, size: float, entityType: str):
        self.position = position
        self.size = size
        self.entityType = entityType
        self.isrect = False

    @abstractmethod
    def update(self, deltaTime: float, world: 'GameWorld'):
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface, camera: 'Camera'):
        pass

    def getPosition(self) -> Vector2:
        return self.position

    def setPosition(self, position: Vector2):
        self.position = position