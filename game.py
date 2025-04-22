import random
import time
random.seed(time.time())
import pygame
from gamelogic.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT
from gamelogic.time_manager import TimeManager
from ui.ui_manager import UIManager
from gamelogic.game_world import GameWorld
from gamelogic.economy import Economy
from ui.renderer import Renderer
from ui.main_screen import MainScreen
from ui.minimap import Minimap
from ui.ui_manager import Button
from entities.plant import Plant 
from entities.plant import Bush 
from entities.plant import Tree 
from entities.animal import Animal


class Game:
    def __init__(self, width, height):
        Animal.species_list = []
        Animal.last_reproduction_times = {}
        Animal.current_species_index = 0
        Animal.reproduction_lock = None
        self.width = width
        self.height = height
        self.timeManager = TimeManager()
        self.economy = Economy()  # Starts with 1000 by default
        self.world = GameWorld(WORLD_WIDTH, WORLD_HEIGHT, self.economy)
        self.renderer = Renderer(WORLD_WIDTH, WORLD_HEIGHT, width, height)
        self.uiManager = UIManager()
        self.minimap = Minimap(WORLD_WIDTH, WORLD_HEIGHT, width, height)  # Add minimap
        self.running = True

        self.world.generate_terrain()
        self.world.generate_grassy_areas()
        self.world.place_plants()

        # --- Add Zoom Buttons ---
        button_width = 40
        button_height = 40
        minimap_x, minimap_y = self.minimap.position
        minimap_w, minimap_h = self.minimap.minimap_width, self.minimap.minimap_height
        spacing = 10

        zoom_in_button = Button(
            "+",
            (minimap_x, minimap_y + minimap_h + spacing),
            (button_width, button_height),
            self.zoom_in
        )
        zoom_out_button = Button(
            "-",
            (minimap_x + button_width + spacing, minimap_y + minimap_h + spacing),
            (button_width, button_height),
            self.zoom_out
        )
        self.uiManager.addComponent(zoom_in_button)
        self.uiManager.addComponent(zoom_out_button)

    def zoom_in(self):
        self.renderer.camera.zoom_in()

    def zoom_out(self):
        self.renderer.camera.zoom_out()

    def update(self, deltaTime: float):
        """Update all objects (animals, etc.)"""
        if not self.uiManager.activeMenu:  # Pause updates when the menu is active
            self.timeManager.update()
            deltaTime = self.timeManager.get_delta_time()

            self.world.update(deltaTime)
            # self.economy.update(deltaTime)  # <-- Remove or comment out this line
            self.renderer.handleInput(deltaTime)

    def render(self, surface):
        """Render all objects"""
        surface.fill((238, 214, 175))  # Desert background
        self.renderer.render(surface, self)
        self.uiManager.render(surface)
        self.minimap.render(surface, self.renderer.camera, self.world, self.world.entities)  # Render minimap

        # --- Stylish money bar (top-right corner) ---
        bar_width, bar_height = 220, 50
        padding = 20
        x = (self.width - bar_width) // 2  # Center horizontally
        y = padding

        # Draw rounded rectangle background
        pygame.draw.rect(surface, (255, 255, 255), (x, y, bar_width, bar_height), border_radius=18)
        pygame.draw.rect(surface, (218, 165, 32), (x, y, bar_width, bar_height), 3, border_radius=18)  # Gold border

        # Draw coin icon (simple yellow circle)
        coin_radius = 16
        coin_x = x + 20
        coin_y = y + bar_height // 2
        pygame.draw.circle(surface, (255, 215, 0), (coin_x, coin_y), coin_radius)
        pygame.draw.circle(surface, (218, 165, 32), (coin_x, coin_y), coin_radius, 3)

        # Draw money text
        font = pygame.font.Font(None, 36)
        money_text = font.render(f"${self.economy.money}", True, (0, 0, 0))
        surface.blit(money_text, (coin_x + coin_radius + 15, y + bar_height // 2 - money_text.get_height() // 2))

    def handleEvents(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.minimap.handle_click(pygame.mouse.get_pos(), self.renderer.camera)  # Handle minimap clicks
            if self.uiManager.handleEvent(event):
                return

    def place_plants(self, num_bushes=40, num_trees=30, num_grass_areas=20):
        placed_positions = set()
        for PlantClass, count, allowed_cell in [
            (Bush, num_bushes, "soil"),
            (Tree, num_trees, "soil"),
        ]:
            for _ in range(count):
                tries = 0
                while tries < 1000:
                    x = random.randint(0, self.grid_width - 1)
                    y = random.randint(0, self.grid_height - 1)
                    cell = self.terrain_grid[y][x]
                    pos = Vector2(x * self.cell_size, y * self.cell_size)
                    if (
                        cell == allowed_cell
                        and not self.is_on_road(pos)
                        and not self.is_on_water_or_hill(pos)
                        and not self.is_near_water(x, y, radius=2)
                        and not self.is_near_road(x, y, radius=5)  # <-- Even further from roads!
                        and (x, y) not in placed_positions
                    ):
                        plant = PlantClass(pos)
                        self.entities[type(plant).__name__].append(plant)
                        placed_positions.add((x, y))
                        break
                    tries += 1

def show_rules(screen):
    """Display the rules screen."""
    running = True
    font = pygame.font.Font(None, 36)
    rules_text = [
        "Rules of Safari Game:",
        "1. Explore the map.",
        "2. Interact with animals and objects.",
        "3. Survive and manage resources.",
        "Press ESC to return to the main screen."
    ]

    while running:
        screen.fill((238, 214, 175))
        y_offset = 50
        for line in rules_text:
            text_surface = font.render(line, True, (0, 0, 0))
            screen.blit(text_surface, (50, y_offset))
            y_offset += 50

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        pygame.display.flip()



if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Main screen
    def start_game():
        global main_screen_active, game
        main_screen_active = False
        game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)  # <-- Create a new Game (and GameWorld) each time

    def exit_game():
        pygame.quit()
        exit()

    main_screen = MainScreen(screen, start_game, lambda: show_rules(screen), exit_game)
    main_screen_active = True

    while main_screen_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            main_screen.handle_event(event)

        main_screen.render()
        pygame.display.flip()
        clock.tick(60)


    while game.running:
        # Handle events
        game.handleEvents()

        # Update world
        game.update(clock.get_time() / 1000.0)  # Pass delta time in seconds

        # Draw world
        game.render(screen)

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()