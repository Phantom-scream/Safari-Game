from ui.camera import Camera
from ui.vector2 import Vector2
import pygame

class Renderer:
    def __init__(self, worldWidth, worldHeight, viewportWidth, viewportHeight):
        self.camera = Camera(Vector2(viewportWidth // 2, viewportHeight // 2), viewportWidth, viewportHeight, worldWidth, worldHeight)
        self.spriteCache = {}
        self.minimapEnabled = False

    def initialize(self):
        pass

    def render(self, gameState):
        self.renderEntities(gameState.world.entities)
        self.renderUI(gameState.uiManager)

    def renderEntities(self, entities):
        for entity_list in entities.values():
            for entity in entity_list:
                screenPos = self.camera.worldToScreen(entity.position)
                pygame.draw.rect(pygame.display.get_surface(), entity.color, (screenPos.x, screenPos.y, entity.size, entity.size))

    def renderUI(self, uiManager):
        uiManager.render(pygame.display.get_surface())

    def loadSprite(self, name: str) -> pygame.Surface:
        if name not in self.spriteCache:
            self.spriteCache[name] = pygame.image.load(name)
        return self.spriteCache[name]

    def handleInput(self, deltaTime: float):
        self.camera.handleInput(deltaTime)