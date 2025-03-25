import random
import pygame
from gamelogic.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT
from gamelogic.time_manager import TimeManager
from ui.ui_manager import UIManager
from gamelogic.game_world import GameWorld
from gamelogic.economy import Economy
from ui.renderer import Renderer

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.timeManager = TimeManager()
        self.world = GameWorld(WORLD_WIDTH, WORLD_HEIGHT)
        self.economy = Economy()
        self.renderer = Renderer(WORLD_WIDTH, WORLD_HEIGHT, width, height)
        self.uiManager = UIManager()

    def update(self, deltaTime: float):
        """Update all objects (animals, etc.)"""
        self.timeManager.update()
        deltaTime = self.timeManager.get_delta_time()

        self.world.update(deltaTime)
        self.economy.update(deltaTime)
        self.renderer.handleInput(deltaTime)

    def render(self, surface):
        """Render all objects"""
        surface.fill((238, 214, 175))  # desert background
        self.renderer.render(self)
        self.uiManager.render(surface)

    def handleEvents(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True

if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Create game world
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)

    running = True
    while running:
        # Handle events
        running = game.handleEvents()

        # Update world
        game.update(clock.get_time() / 1000.0)  # Pass delta time in seconds

        # Draw world
        game.render(screen)

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()