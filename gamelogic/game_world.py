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
from entities.jeep import Jeep  # Add this import

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
            "Jeep": [],  # Add Jeep list to entities
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

        # Find the road path from left to right (sorted by x)
        road_path = sorted(self.entities["Road"], key=lambda r: r.position.x)
        road_positions = [r.position for r in road_path]

        # 4. Define entrance and exit for the road
        self.road_entrance = road_positions[0] if road_positions else None
        self.road_exit = road_positions[-1] if road_positions else None

        # Create a Jeep at the entrance (leftmost road tile) with 4 tourists
        if road_positions:
            jeep = Jeep(self.road_entrance, road_positions)
            self.entities["Jeep"].append(jeep)

    def is_on_road(self, position: Vector2) -> bool:
        # Check if the position is close to any road tile
        for road in self.entities["Road"]:
            if abs(position.x - road.position.x) < self.cell_size and abs(position.y - road.position.y) < self.cell_size:
                return True
        return False

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
        """Generate a single wide road from left to right, only in the central 50% of the map height."""
        road_width = self.cell_size * 5  # Make the road 5 times wider than before
        road_x = 0
        min_y = int(self.height * 0.25)
        max_y = int(self.height * 0.75)
        road_y = (min_y + max_y) // 2
        num_cells = self.width // self.cell_size

        for i in range(num_cells):
            # Place one wide road object per column
            road_pos = Vector2(road_x, road_y - road_width // 2)
            self.entities["Road"].append(Road(road_pos, road_width))
            road_x += self.cell_size
            if random.random() < 0.4:
                direction = random.choice([-1, 0, 1])
                new_road_y = road_y + direction * self.cell_size
                if min_y + road_width // 2 <= new_road_y <= max_y - road_width // 2:
                    road_y = new_road_y