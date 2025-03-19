import random
import pygame
from animal import Animal
from obstacles import Water, Obstacle
from plant import Plant
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, NUM_ANIMALS, NUM_WATER_SOURCES, NUM_OBSTACLES, NUM_PLANTS

class GameWorld:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.animals = [Animal(random.randint(50, width-50), random.randint(50, height-50)) for _ in range(NUM_ANIMALS)]
        self.water_sources = [Water(random.randint(50, width-50), random.randint(50, height-50)) for _ in range(NUM_WATER_SOURCES)]
        self.obstacles = [Obstacle(random.randint(50, width-50), random.randint(50, height-50)) for _ in range(NUM_OBSTACLES)]
        self.plants = [Plant(random.randint(50, width-50), random.randint(50, height-50)) for _ in range(NUM_PLANTS)]

    def update(self):
        """Update all objects (animals, etc.)"""
        for animal in self.animals:
            animal.update(self)

    def draw(self, screen):
        """Draw all objects as colored blocks"""
        for water in self.water_sources:
            water.draw(screen)

        for obstacle in self.obstacles:
            obstacle.draw(screen)

        for plant in self.plants:
            plant.draw(screen)

        for animal in self.animals:
            animal.draw(screen)