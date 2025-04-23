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
from ui.vector2 import Vector2
from entities.jeep import Jeep
from entities.tourist import Tourist
import math


class Game:
    def __init__(self, width, height, difficulty="easy"):
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
        self.difficulty = difficulty

        self.speed_modes = {
            "hour": 1.0,
            "day": 5.0,
            "week": 20.0
        }
        self.current_speed_mode = "hour"

        self.world.generate_terrain()
        self.world.generate_grassy_areas()
        self.world.place_plants()

        # --- Add Zoom Buttons ---
        zoom_button_height = 48  # Increased height
        zoom_button_width = self.minimap.minimap_width // 2  # Increased width (already full minimap width)
        minimap_x, minimap_y = self.minimap.position
        minimap_w, minimap_h = self.minimap.minimap_width, self.minimap.minimap_height

        zoom_in_button = Button(
            "+",
            (minimap_x, minimap_y + minimap_h),
            (zoom_button_width, zoom_button_height),
            self.zoom_in,
            font_size=28  # Optional: make the "+" bigger
        )
        zoom_out_button = Button(
            "-",
            (minimap_x + zoom_button_width, minimap_y + minimap_h),
            (zoom_button_width, zoom_button_height),
            self.zoom_out,
            font_size=28  # Optional: make the "-" bigger
        )
        self.uiManager.addComponent(zoom_in_button)
        self.uiManager.addComponent(zoom_out_button)

        # --- Add Speed Mode Buttons (vertical, left of minimap, no space) ---
        speed_button_width = 60  # You can adjust this width as you like
        speed_button_height = self.minimap.minimap_height // 3  # 3 buttons fill minimap height
        speed_button_x = minimap_x - speed_button_width  # Directly left of minimap, no space
        speed_button_y = minimap_y

        def make_speed_button(label, mode, idx):
            return Button(
                label,
                (speed_button_x, speed_button_y + idx * speed_button_height),
                (speed_button_width, speed_button_height),
                lambda m=mode: self.set_speed_mode(m),
                font_size=20
            )

        self.hour_button = make_speed_button("Hour", "hour", 0)
        self.day_button = make_speed_button("Day", "day", 1)
        self.week_button = make_speed_button("Week", "week", 2)
        self.uiManager.addComponent(self.hour_button)
        self.uiManager.addComponent(self.day_button)
        self.uiManager.addComponent(self.week_button)

        self.time_of_day = 0.0  # 0.0 to 1.0, where 0.0 is midnight, 0.5 is noon
        self.day_length = 120.0  # seconds for a full day-night cycle (adjust as you like)
        self.is_night = False
        self.jeep_count = len(self.world.entities["Jeep"])
        self.pending_jeeps = []  # <-- Add this line

    def zoom_in(self):
        self.renderer.camera.zoom_in()

    def zoom_out(self):
        self.renderer.camera.zoom_out()

    def set_speed_mode(self, mode):
        self.current_speed_mode = mode

    def update(self, deltaTime: float):
        if self.uiManager.paused:
            return  # Skip updating game logic when paused
        if not self.uiManager.activeMenu:
            speed_factor = self.speed_modes[self.current_speed_mode]
            deltaTime *= speed_factor

            # --- Day/Night cycle update ---
            self.time_of_day += deltaTime / self.day_length
            if self.time_of_day > 1.0:
                self.time_of_day -= 1.0
            self.is_night = self.time_of_day < 0.25 or self.time_of_day > 0.75

            self.world.update(deltaTime)
            self.renderer.handleInput(deltaTime)

            # --- Deploy all jeeps (existing + pending) if all jeeps are at entrance ---
            if self.all_jeeps_at_entrance():
                entrance = self.world.road_entrance
                spacing = 50
                all_jeeps = self.world.entities["Jeep"] + self.pending_jeeps
                for i, jeep in enumerate(all_jeeps):
                    offset = i * spacing
                    jeep.position = Vector2(entrance.x + offset, entrance.y)
                    jeep.current_index = 0
                    jeep.state = "to_exit"
                    jeep.passengers = [Tourist(f"Tourist {j+1}") for j in range(4)]  # Reset passengers
                self.world.entities["Jeep"] = all_jeeps
                self.pending_jeeps.clear()

    def render(self, surface):
        surface.fill((238, 214, 175))  # Desert background
        self.renderer.render(surface, self)
        self.uiManager.render(surface)
        self.minimap.render(surface, self.renderer.camera, self.world, self.world.entities)

        # --- Day/Night overlay ---
        brightness = 0.4 + 0.6 * (math.cos(self.time_of_day * 2 * math.pi) + 1) / 2
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        night_alpha = int((1.0 - brightness) * 180)
        overlay.fill((0, 0, 40, night_alpha))
        surface.blit(overlay, (0, 0))

        # --- Stylish money bar (top-center) ---
        bar_width, bar_height = 140, 32  # Smaller bars
        padding = 10
        x = (self.width - bar_width) // 2
        y = padding

        # Money bar
        pygame.draw.rect(surface, (255, 255, 255), (x, y, bar_width, bar_height), border_radius=12)
        pygame.draw.rect(surface, (218, 165, 32), (x, y, bar_width, bar_height), 2, border_radius=12)
        coin_radius = 10
        coin_x = x + 12
        coin_y = y + bar_height // 2
        pygame.draw.circle(surface, (255, 215, 0), (coin_x, coin_y), coin_radius)
        pygame.draw.circle(surface, (218, 165, 32), (coin_x, coin_y), coin_radius, 2)
        font = pygame.font.Font(None, 22)
        money_text = font.render(f"${self.economy.money}", True, (0, 0, 0))
        surface.blit(money_text, (coin_x + coin_radius + 8, y + bar_height // 2 - money_text.get_height() // 2))

        # --- Jeep count bar (under money bar) ---
        jeep_bar_y = y + bar_height + 6
        pygame.draw.rect(surface, (255, 255, 255), (x, jeep_bar_y, bar_width, bar_height), border_radius=12)
        pygame.draw.rect(surface, (60, 60, 200), (x, jeep_bar_y, bar_width, bar_height), 2, border_radius=12)
        jeep_icon_x = x + 12
        jeep_icon_y = jeep_bar_y + bar_height // 2
        pygame.draw.rect(surface, (60, 60, 200), (jeep_icon_x - 6, jeep_icon_y - 7, 20, 14))
        # Draw wheels
        pygame.draw.circle(surface, (0, 0, 0), (jeep_icon_x, jeep_icon_y + 7), 3)
        pygame.draw.circle(surface, (0, 0, 0), (jeep_icon_x + 14, jeep_icon_y + 7), 3)
        jeep_text = font.render(f"x {self.jeep_count}", True, (0, 0, 0))
        surface.blit(jeep_text, (jeep_icon_x + 20, jeep_bar_y + bar_height // 2 - jeep_text.get_height() // 2))

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

    def all_jeeps_at_entrance(self):
        entrance = self.world.road_entrance
        if not entrance:
            return False
        for jeep in self.world.entities["Jeep"]:
            if not (jeep.state == "to_entrance" and jeep.position.distanceTo(entrance) < 20):
                return False
        return True


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


class ShopMenu:
    def __init__(self, game):
        self.game = game
        self.message = ""
        self.message_time = 0

    def purchase(self, item):
        if item == "Jeep":
            entrance = self.game.world.road_entrance
            road_path = sorted(self.game.world.entities["Road"], key=lambda r: r.position.x)
            if entrance and road_path:
                new_jeep = Jeep(entrance, [r.position for r in road_path])
                self.game.pending_jeeps.append(new_jeep)  # <-- Add to pending, not to world.entities
                self.game.jeep_count += 1
                self.message = "Purchased Jeep! Will join next tour."
                self.message_time = time.time()
            else:
                self.message = "No road entrance!"
                self.message_time = time.time()
            return


if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Main screen
    def start_game(difficulty="easy"):
        global main_screen_active, game
        main_screen_active = False
        game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, difficulty)  # Pass difficulty to Game

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

        # --- FIX: Get deltaTime at the start of the loop ---
        deltaTime = clock.tick(60) / 1000.0  # Limit to 60 FPS and get seconds since last frame

        # Update world
        game.update(deltaTime)  # Pass delta time in seconds

        # Draw world
        game.render(screen)

        pygame.display.flip()

    pygame.quit()