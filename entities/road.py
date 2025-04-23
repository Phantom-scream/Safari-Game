import pygame
from ui.vector2 import Vector2
from entities.entity import Entity
from typing import TYPE_CHECKING
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gamelogic.game_world import GameWorld
    from ui.camera import Camera

class Road(Entity):
    """Represents a piece of road terrain."""
    def __init__(self, position: Vector2, size: float):
        super().__init__(position, size, 'Road')
        self.color = (139, 101, 8) # Brown color for road

    def update(self, deltaTime: float, world: 'GameWorld'):
        # Roads are static
        pass

    def render(self, surface: pygame.Surface, camera: 'Camera'):
        screen_pos = camera.worldToScreen(self.position)
        # Scale the road size with camera zoom
        road_width = self.size * camera.zoom
        road_height = self.size * camera.zoom
        road_rect = pygame.Rect(
            int(screen_pos.x),
            int(screen_pos.y),
            int(road_width + 1),
            int(road_height + 1)
        )
        pygame.draw.rect(surface, self.color, road_rect)