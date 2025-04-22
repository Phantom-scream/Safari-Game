import pygame
from ui.vector2 import Vector2
from entities.waterbody import WaterBody

class Minimap:
    def __init__(self, world_width, world_height, viewport_width, viewport_height):
        self.world_width = world_width
        self.world_height = world_height
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self.minimap_width = 200
        self.minimap_height = 150
        self.position = (viewport_width - self.minimap_width - 10, 10)  # Top-right corner
        
        # Calculate the navigable area (where camera center can go)
        self.navigable_min_x = 0 
        self.navigable_min_y = 0
        self.navigable_max_x = world_width - viewport_width / 2
        self.navigable_max_y = world_height - viewport_height / 2
        self.navigable_width = self.navigable_max_x - self.navigable_min_x
        self.navigable_height = self.navigable_max_y - self.navigable_min_y

    def render(self, surface, camera, world, entities):
        # Draw minimap background (will be covered by terrain)
        pygame.draw.rect(surface, (50, 50, 50), (*self.position, self.minimap_width, self.minimap_height))

        # Draw terrain
        cell_size_x = world.width / self.minimap_width
        cell_size_y = world.height / self.minimap_height

        for y in range(self.minimap_height):
            for x in range(self.minimap_width):
                world_x = int(x * cell_size_x)
                world_y = int(y * cell_size_y)
                grid_x = int(world_x // world.cell_size)
                grid_y = int(world_y // world.cell_size)
                if 0 <= grid_x < world.grid_width and 0 <= grid_y < world.grid_height:
                    terrain = world.terrain_grid[grid_y][grid_x]
                    if isinstance(terrain, WaterBody):
                        color = (0, 0, 255)  # Blue for lakes
                    elif terrain == "grass":
                        color = (34, 139, 34)  # Green for grass
                    elif terrain == "hill":
                        color = (139, 137, 137)  # Gray for hills
                    else:
                        color = (238, 214, 175)  # Default background
                    surface.set_at((self.position[0] + x, self.position[1] + y), color)

        # Scale factors for world-to-minimap conversion
        scale_x = self.minimap_width / self.navigable_width
        scale_y = self.minimap_height / self.navigable_height

        # Draw entities
        for entity_list in entities.values():
            for entity in entity_list:
                # Only draw entities within the navigable area
                if (self.navigable_min_x <= entity.position.x <= self.navigable_max_x and
                    self.navigable_min_y <= entity.position.y <= self.navigable_max_y):
                    
                    # Convert world position to minimap position
                    rel_x = entity.position.x - self.navigable_min_x
                    rel_y = entity.position.y - self.navigable_min_y
                    
                    minimap_x = self.position[0] + rel_x * scale_x
                    minimap_y = self.position[1] + rel_y * scale_y
                    
                    # Draw entity dot
                    pygame.draw.rect(surface, entity.color, (minimap_x, minimap_y, 3, 3))

        # Draw camera viewport on minimap
        # Calculate camera position relative to navigable area
        rel_camera_x = (camera.position.x - self.navigable_min_x) * scale_x
        rel_camera_y = (camera.position.y - self.navigable_min_y) * scale_y
        
        # Calculate viewport size on minimap
        viewport_width_minimap = (camera.viewportWidth / self.navigable_width) * self.minimap_width
        viewport_height_minimap = (camera.viewportHeight / self.navigable_height) * self.minimap_height
        
        # Draw camera viewport rectangle
        camera_rect = pygame.Rect(
            self.position[0] + rel_camera_x - viewport_width_minimap/2,
            self.position[1] + rel_camera_y - viewport_height_minimap/2,
            viewport_width_minimap,
            viewport_height_minimap
        )
        pygame.draw.rect(surface, (255, 255, 255), camera_rect, 1)

        pygame.draw.rect(
            surface,
            (255, 215, 0),  # Gold/yellow color for visibility
            (self.position[0], self.position[1], self.minimap_width, self.minimap_height),
            3  # Thickness of the border
        )

    def handle_click(self, mouse_pos, camera):
        if self.position[0] <= mouse_pos[0] <= self.position[0] + self.minimap_width and \
           self.position[1] <= mouse_pos[1] <= self.position[1] + self.minimap_height:
            
            # Convert click position to world coordinates
            rel_x = (mouse_pos[0] - self.position[0]) / self.minimap_width * self.navigable_width
            rel_y = (mouse_pos[1] - self.position[1]) / self.minimap_height * self.navigable_height
            
            # Calculate world position
            world_x = rel_x + self.navigable_min_x
            world_y = rel_y + self.navigable_min_y
            
            # Clamp position to ensure it's within navigable area
            world_x = max(self.navigable_min_x, min(world_x, self.navigable_max_x))
            world_y = max(self.navigable_min_y, min(world_y, self.navigable_max_y))
            
            # Move camera to clicked point
            camera.moveTo(Vector2(world_x, world_y))