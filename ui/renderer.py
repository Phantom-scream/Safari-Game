from ui.camera import Camera
from ui.vector2 import Vector2
import pygame
from entities.waterbody import WaterBody

class Renderer:
    def __init__(self, worldWidth, worldHeight, viewportWidth, viewportHeight):
        self.camera = Camera(Vector2(viewportWidth // 2, viewportHeight // 2), viewportWidth, viewportHeight, worldWidth, worldHeight)
        self.spriteCache = {}
        self.minimapEnabled = False

    def initialize(self):
        pass

    def render(self, surface, gameState):
        camera = self.camera
        cell_size = gameState.world.cell_size
        world_width = gameState.world.width
        world_height = gameState.world.height

        for y in range(gameState.world.grid_height):
            for x in range(gameState.world.grid_width):
                world_x = x * cell_size
                world_y = y * cell_size

                # Check if cell is within world bounds before proceeding
                if world_x < world_width and world_y < world_height:
                    terrain = gameState.world.terrain_grid[y][x]
                    
                    color = None # Determine color based on terrain type
                    if isinstance(terrain, WaterBody):
                        color = terrain.color  # Use the color from the WaterBody instance
                    elif terrain == "grass":
                        color = (34, 139, 34)
                    elif terrain == "hill":
                        color = (139, 137, 137)
                    # Add other terrain types here if needed
                    
                    if color: # If a valid color was found for this terrain
                        # Calculate screen position based on camera (assuming camera.position is top-left)
                        screen_x = world_x - camera.position.x
                        screen_y = world_y - camera.position.y
                        
                        # Calculate clipped rectangle size for drawing
                        rect_width = min(cell_size, world_width - world_x)
                        rect_height = min(cell_size, world_height - world_y)
                        
                        # Only draw if the rectangle has positive dimensions
                        if rect_width > 0 and rect_height > 0:
                            # Check if the rectangle is visible on screen (optional optimization)
                            if (screen_x < camera.viewportWidth and screen_x + rect_width > 0 and
                                screen_y < camera.viewportHeight and screen_y + rect_height > 0):
                                rect = pygame.Rect(screen_x, screen_y, rect_width, rect_height)
                                pygame.draw.rect(surface, color, rect)
                                
        # Render entities and UI on top
        self.renderEntities(surface, gameState.world.entities)
        self.renderUI(surface, gameState.uiManager)

    def renderEntities(self, surface, entities):
        # Draw roads first
        for road in entities.get("Road", []):
            road.render(surface, self.camera)
        # Draw water bodies next
        for water in entities.get("WaterBody", []):
            water.render(surface, self.camera)
        # Draw jeeps on top of the road and water
        for jeep in entities.get("Jeep", []):
            self.render_jeep(surface, jeep)
        # Draw all other entities
        for key, entity_list in entities.items():
            if key in ("Road", "WaterBody", "Jeep"):
                continue
            for entity in entity_list:
                entity.render(surface, self.camera)

    def render_jeep(self, surface, jeep):
        screen_pos = self.camera.worldToScreen(jeep.position)
        jeep_color = jeep.color
        pygame.draw.rect(surface, jeep_color, (screen_pos.x, screen_pos.y, jeep.size, jeep.size))
        font = pygame.font.Font(None, 18)
        text = font.render(str(len(jeep.passengers)), True, (255, 255, 255))
        surface.blit(text, (screen_pos.x + 2, screen_pos.y + 2))

    def renderUI(self, surface, uiManager):
        uiManager.render(surface)

    def loadSprite(self, name: str) -> pygame.Surface:
        if name not in self.spriteCache:
            self.spriteCache[name] = pygame.image.load(name)
        return self.spriteCache[name]

    def handleInput(self, deltaTime: float):
        self.camera.handleInput(deltaTime)