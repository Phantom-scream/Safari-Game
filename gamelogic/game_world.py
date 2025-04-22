from typing import List, Dict
import pygame
import opensimplex
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
from entities.road import Road  # 1. Import the Road class

class GameWorld:
    def __init__(self, width, height, cell_size=20):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        # Add +1 to make sure we cover the entire world and have an extra cell at edges
        self.grid_width = math.ceil(width / cell_size) + 2
        self.grid_height = math.ceil(height / cell_size) + 2
        self.terrain_grid = [[None for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.simplex = opensimplex.OpenSimplex(seed=random.randint(0, 10000))
        self.entities: Dict[str, List[Entity]] = {
            'Bison': [Bison(Vector2(random.randint(0, width), random.randint(0, height))) for _ in range(Bison.get_number())],
            'Zebra': [Zebra(Vector2(random.randint(0, width), random.randint(0, height))) for _ in range(Zebra.get_number())],
            'Antelope': [Antelope(Vector2(random.randint(0, width), random.randint(0, height))) for _ in range(Antelope.get_number())],
            'Lion': [Lion(Vector2(random.randint(0, width), random.randint(0, height))) for _ in range(Lion.get_number())],
            'Hyena': [Hyena(Vector2(random.randint(0, width), random.randint(0, height))) for _ in range(Hyena.get_number())],
            'Crocodile': [Crocodile(Vector2(random.randint(0, width), random.randint(0, height))) for _ in range(Crocodile.get_number())],
            'WaterBody': [],
            'Plant': [Plant(Vector2(random.randint(0, width), random.randint(0, height)), 15, 100) for _ in range(NUM_PLANTS)],
            'Poacher' : [Poacher(Vector2(random.randint(0, width), random.randint(0, height)), 20, 2.5) for _ in range(NUM_POACHERS)],
            "Road": [],
        }
        self.add_road()  # Call after initializing entities
        self.generate_terrain()  # Move terrain generation after road creation

        # Now generate water bodies, skipping road positions
        for _ in range(NUM_WATER_SOURCES):
            while True:
                pos = Vector2(random.randint(0, width), self.height // 2 + random.randint(-height//2, height//2))
                if not self.is_on_road(pos):
                    self.entities['WaterBody'].append(WaterBody(pos, 20))
                    break

    def is_on_road(self, position: Vector2) -> bool:
        road_center_y = self.height // 2
        return abs(position.y - road_center_y) <= self.cell_size  # Now covers three rows

    def generate_terrain(self):
        scale = 15.0  # Controls "zoom" of the noise
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                n = self.simplex.noise2(x / scale, y / scale)
                world_x = x * self.cell_size
                world_y = y * self.cell_size
                if n < -0.6:
                    # Place a WaterBody instance in the grid
                    self.terrain_grid[y][x] = WaterBody(Vector2(world_x, world_y), self.cell_size)
                elif n < 0.5:
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

    def add_road(self):
        """Add a horizontal road three cells wide from left-middle to right-middle."""
        road_center_y = self.height // 2
        road_size = self.cell_size
        num_cells = self.width // road_size
        for dy in [-road_size, 0, road_size]:  # Three rows: above, center, below
            road_y = road_center_y + dy
            for i in range(num_cells):
                road_x = i * road_size
                road_pos = Vector2(road_x, road_y)
                road = Road(road_pos, road_size)
                self.entities["Road"].append(road)