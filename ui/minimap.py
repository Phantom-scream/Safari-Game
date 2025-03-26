import pygame
from ui.vector2 import Vector2

class Minimap:
    def __init__(self, world_width, world_height, viewport_width, viewport_height):
        self.world_width = world_width
        self.world_height = world_height
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self.minimap_width = 200
        self.minimap_height = 150
        self.position = (viewport_width - self.minimap_width - 10, 10)  # Top-right corner

    def render(self, surface, camera, entities):
        # Draw minimap background
        pygame.draw.rect(surface, (50, 50, 50), (*self.position, self.minimap_width, self.minimap_height))

        # Scale entities to minimap
        scale_x = self.minimap_width / self.world_width
        scale_y = self.minimap_height / self.world_height

        for entity_list in entities.values():
            for entity in entity_list:
                minimap_x = self.position[0] + entity.position.x * scale_x
                minimap_y = self.position[1] + entity.position.y * scale_y
                pygame.draw.rect(surface, entity.color, (minimap_x, minimap_y, 3, 3))  # Draw entity as a small dot

        # Draw camera viewport on minimap
        camera_rect = pygame.Rect(
            self.position[0] + camera.position.x * scale_x - (camera.viewportWidth / 2) * scale_x,
            self.position[1] + camera.position.y * scale_y - (camera.viewportHeight / 2) * scale_y,
            camera.viewportWidth * scale_x,
            camera.viewportHeight * scale_y,
        )
        pygame.draw.rect(surface, (255, 255, 255), camera_rect, 1)

    def handle_click(self, mouse_pos, camera):
        # Check if the click is inside the minimap
        if self.position[0] <= mouse_pos[0] <= self.position[0] + self.minimap_width and \
           self.position[1] <= mouse_pos[1] <= self.position[1] + self.minimap_height:
            # Calculate the world position based on the minimap click
            scale_x = self.world_width / self.minimap_width
            scale_y = self.world_height / self.minimap_height
            world_x = (mouse_pos[0] - self.position[0]) * scale_x
            world_y = (mouse_pos[1] - self.position[1]) * scale_y
            camera.moveTo(Vector2(world_x, world_y))