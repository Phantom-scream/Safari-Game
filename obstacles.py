import pygame

class Water:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0, 0, 255)  # Blue

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 20, 20))

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (100, 100, 100)  # Gray for mountains

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 25, 25))