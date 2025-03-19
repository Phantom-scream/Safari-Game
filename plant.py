import pygame

class Plant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0, 255, 0)  # Green for plants

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 15, 15))