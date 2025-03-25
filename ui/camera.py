from ui.vector2 import Vector2
import pygame

class Camera:
    def __init__(self, position: Vector2, viewportWidth: int, viewportHeight: int, worldWidth: int, worldHeight: int, zoom: float = 1.0):
        self.position = position
        self.viewportWidth = viewportWidth
        self.viewportHeight = viewportHeight
        self.worldWidth = worldWidth
        self.worldHeight = worldHeight
        self.zoom = zoom

    def moveTo(self, position: Vector2):
        self.position = position

    def setZoom(self, zoom: float):
        self.zoom = zoom

    def worldToScreen(self, worldPos: Vector2) -> Vector2:
        screenX = (worldPos.x - self.position.x) * self.zoom + self.viewportWidth / 2
        screenY = (worldPos.y - self.position.y) * self.zoom + self.viewportHeight / 2
        return Vector2(screenX, screenY)

    def screenToWorld(self, screenPos: Vector2) -> Vector2:
        worldX = (screenPos.x - self.viewportWidth / 2) / self.zoom + self.position.x
        worldY = (screenPos.y - self.viewportHeight / 2) / self.zoom + self.position.y
        return Vector2(worldX, worldY)

    def getBounds(self) -> pygame.Rect:
        left = self.position.x - self.viewportWidth / 2 / self.zoom
        top = self.position.y - self.viewportHeight / 2 / self.zoom
        width = self.viewportWidth / self.zoom
        height = self.viewportHeight / self.zoom
        return pygame.Rect(left, top, width, height)

    def handleInput(self, deltaTime: float):
        keys = pygame.key.get_pressed()
        moveSpeed = 200 * deltaTime
        if keys[pygame.K_LEFT]:
            self.position.x = max(0, self.position.x - moveSpeed)
        if keys[pygame.K_RIGHT]:
            self.position.x = min(self.worldWidth, self.position.x + moveSpeed)
        if keys[pygame.K_UP]:
            self.position.y = max(0, self.position.y - moveSpeed)
        if keys[pygame.K_DOWN]:
            self.position.y = min(self.worldHeight, self.position.y + moveSpeed)