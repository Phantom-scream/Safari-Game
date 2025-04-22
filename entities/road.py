import pygame
from ui.vector2 import Vector2
from entities.entity import Entity
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.camera import Camera
    # Add GameWorld type hint if needed in update, though it's unused now
    # from gamelogic.game_world import GameWorld

class Road(Entity):
    """Represents a piece of road terrain."""
    def __init__(self, position: Vector2, size: float):
        super().__init__(position, size, 'Road')
        self.color = (139, 101, 8) # Brown color for road

    def update(self, deltaTime: float, world: 'GameWorld'):
        # Roads are static
        pass

    def render(self, surface: pygame.Surface, camera: 'Camera'):
        """Draws the road cell relative to the camera."""
        # Convert world position to screen position using the camera
        # Note: worldToScreen might return the top-left corner for drawing
        screen_pos = camera.worldToScreen(self.position)

        # Create a rectangle at the calculated screen position with the entity's size
        road_rect = pygame.Rect(screen_pos.x, screen_pos.y, self.size, self.size)

        # Draw the rectangle on the provided surface with the road's color
        pygame.draw.rect(surface, self.color, road_rect)