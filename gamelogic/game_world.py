from typing import List, Dict
import pygame
import noise
import math
from entities.animal import Animal
from entities.poacher import Poacher
from entities.waterbody import WaterBody
from entities.plant import Plant
from entities.herbivore import Bison, Zebra, Antelope
from entities.carnivore import Lion, Hyena, Crocodile
from entities.entity import Entity
from gamelogic.settings import NUM_ANIMALS, NUM_WATER_SOURCES, NUM_PLANTS, NUM_POACHERS
from ui.vector2 import Vector2
import random

class GameWorld:
    def __init__(self, width, height, cell_size=20):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        # Add +1 to make sure we cover the entire world and have an extra cell at edges
        self.grid_width = math.ceil(width / cell_size) + 2
        self.grid_height = math.ceil(height / cell_size) + 2
        self.terrain_grid = [[None for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.generate_terrain()
        self.entities: Dict[str, List[Entity]] = {
            'Bison': [Bison(Vector2(random.randint(0, width), random.randint(0, height))) for _ in range(Bison.get_number())],
            'Zebra': [Zebra(Vector2(random.randint(0, width), random.randint(0, height))) for _ in range(Zebra.get_number())],
            'Antelope': [Antelope(Vector2(random.randint(0, width), random.randint(0, height))) for _ in range(Antelope.get_number())],
            'Lion': [Lion(Vector2(random.randint(0, width), random.randint(0, height))) for _ in range(Lion.get_number())],
            'Hyena': [Hyena(Vector2(random.randint(0, width), random.randint(0, height))) for _ in range(Hyena.get_number())],
            'Crocodile': [Crocodile(Vector2(random.randint(0, width), random.randint(0, height))) for _ in range(Crocodile.get_number())],
            'WaterBody': [WaterBody(Vector2(random.randint(0, width), random.randint(0, height)), 20) for _ in range(NUM_WATER_SOURCES)],
            'Plant': [Plant(Vector2(random.randint(0, width), random.randint(0, height)), 15, 100) for _ in range(NUM_PLANTS)],
            'Poacher' : [Poacher(Vector2(random.randint(0, width), random.randint(0, height)), 20, 2.5) for _ in range(NUM_POACHERS)]
        }

    def generate_terrain(self):
        scale = 20.0  # Controls "zoom" of the noise
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                n = noise.pnoise2(x / scale, y / scale, octaves=3, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=0)
                world_x = x * self.cell_size
                world_y = y * self.cell_size
                if n < -0.2:
                    # Place a WaterBody instance in the grid
                    self.terrain_grid[y][x] = WaterBody(Vector2(world_x, world_y), self.cell_size)                
                elif n < 0.35:
                    self.terrain_grid[y][x] = "grass"
                else:
                    self.terrain_grid[y][x] = "hill"

    def addEntity(self, entity: Entity):
        entity_type = type(entity).__name__
        if entity_type not in self.entities:
            self.entities[entity_type] = []
        self.entities[entity_type].append(entity)

    def removeEntity(self, entity: Entity):
        entity_type = type(entity).__name__
        if entity_type in self.entities:
            self.entities[entity_type].remove(entity)

    def getEntitiesInRadius(self, position: Vector2, radius: float) -> List[Entity]:
        result = []
        for entity_list in self.entities.values():
            for entity in entity_list:
                if position.distanceTo(entity.position) <= radius:
                    result.append(entity)
        return result

    def update(self, deltaTime: float):
        for entity_list in self.entities.values():
            for entity in entity_list:
                entity.update(deltaTime, self)