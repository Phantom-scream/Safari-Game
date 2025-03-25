import pygame

class TimeManager:
    def __init__(self):
        self.last_time = pygame.time.get_ticks()
        self.delta_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        self.delta_time = (current_time - self.last_time) / 1000.0  # Convert to seconds
        self.last_time = current_time

    def get_delta_time(self):
        return self.delta_time