import pygame
from ui.ui_manager import Button

class MainScreen:
    def __init__(self, screen, start_game_callback, show_rules_callback, exit_game_callback):
        self.screen = screen
        self.start_game_callback = start_game_callback
        self.show_rules_callback = show_rules_callback
        self.exit_game_callback = exit_game_callback

        # Difficulty selection
        self.selected_difficulty = "easy"

        # Buttons
        self.buttons = [
            Button("Easy", (50, 150), (200, 40), lambda: self.select_difficulty("easy")),
            Button("Medium", (50, 200), (200, 40), lambda: self.select_difficulty("medium")),
            Button("Hard", (50, 250), (200, 40), lambda: self.select_difficulty("hard")),
            Button("Start Game", (50, 320), (200, 50), self.start_game),
            Button("Rules", (50, 390), (200, 50), self.show_rules_callback),
            Button("Exit", (50, 460), (200, 50), self.exit_game_callback),
        ]

        # Load an image (placeholder for now)
        self.image = pygame.image.load("ui/haci.png")
        self.image = pygame.transform.scale(self.image, (300, 300))

    def select_difficulty(self, difficulty):
        self.selected_difficulty = difficulty

    def start_game(self):
        # Pass the selected difficulty to the callback
        self.start_game_callback(self.selected_difficulty)

    def render(self):
        self.screen.fill((238, 214, 175))
        font = pygame.font.Font(None, 72)
        title_surface = font.render("Safari Game", True, (0, 0, 0))
        self.screen.blit(title_surface, (50, 50))
        for button in self.buttons:
            button.render(self.screen)
        # Highlight selected difficulty
        font = pygame.font.Font(None, 28)
        diff_text = font.render(f"Selected: {self.selected_difficulty.title()}", True, (0, 0, 0))
        self.screen.blit(diff_text, (270, 160))
        self.screen.blit(self.image, (500, 150))

    def handle_event(self, event):
        for button in self.buttons:
            button.handleEvent(event)