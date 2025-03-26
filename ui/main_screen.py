import pygame
from ui.ui_manager import Button

class MainScreen:
    def __init__(self, screen, start_game_callback, show_rules_callback, exit_game_callback):
        self.screen = screen
        self.start_game_callback = start_game_callback
        self.show_rules_callback = show_rules_callback
        self.exit_game_callback = exit_game_callback

        # Buttons
        self.buttons = [
            Button("Start Game", (50, 200), (200, 50), self.start_game_callback),
            Button("Exit", (50, 300), (200, 50), self.exit_game_callback),
            Button("Rules", (50, 400), (200, 50), self.show_rules_callback),
        ]

        # Load an image (placeholder for now)
        self.image = pygame.image.load("ui/haci.png")  # Replace with your image path
        self.image = pygame.transform.scale(self.image, (300, 300))  # Resize the image

    def render(self):
        # Background color
        self.screen.fill((238, 214, 175))

        # Title
        font = pygame.font.Font(None, 72)
        title_surface = font.render("Safari Game", True, (0, 0, 0))
        self.screen.blit(title_surface, (50, 50))

        # Render buttons
        for button in self.buttons:
            button.render(self.screen)

        # Render image on the right side
        self.screen.blit(self.image, (500, 150))

    def handle_event(self, event):
        for button in self.buttons:
            button.handleEvent(event)