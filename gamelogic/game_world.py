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
from entities.road import Road
from entities.jeep import Jeep
from entities.plant import Bush, Tree

class GameWorld:
    def __init__(self, width, height, economy=None):
        self.width = width
        self.height = height
        self.cell_size = 20
        self.grid_width = math.ceil(width / self.cell_size) + 2
        self.grid_height = math.ceil(height / self.cell_size) + 2
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
            'Bush': [],
            'Tree': [],
            'Poacher' : [Poacher(Vector2(random.randint(0, width), random.randint(0, height)), 20, 1.2) for _ in range(NUM_POACHERS)],
            "Road": [],
            "Jeep": [],
            "Herbivore": [],
            "Carnivore": []
        }
        self.road_segments = []  # Store all road segments
        self.max_roads = 3
        self.visible_roads = 0
        self.reserved_road_cells = set()

        self.add_multiple_roads(self.max_roads)
        self.generate_terrain()
        self.place_plants()
        self.economy = economy

        for _ in range(NUM_WATER_SOURCES):
            while True:
                pos = Vector2(random.randint(0, width), self.height // 2 + random.randint(-height//2, height//2))
                if not self.is_on_road(pos):
                    self.entities['WaterBody'].append(WaterBody(pos, 20))
                    break

        visible_road_segments = [seg for seg in self.road_segments if seg and seg[0].visible]
        if visible_road_segments:
            road_path = random.choice(visible_road_segments)
            road_positions = [r.position for r in road_path]
            self.road_entrance = road_positions[0]
            self.road_exit = road_positions[-1]
            jeep = Jeep(self.road_entrance, road_positions)
            self.entities["Jeep"].append(jeep)
        else:
            self.road_entrance = None
            self.road_exit = None

    def is_on_road(self, position: Vector2) -> bool:
        for road in self.entities["Road"]:
            if abs(position.x - road.position.x) < self.cell_size and abs(position.y - road.position.y) < self.cell_size:
                return True
        return False

    def generate_terrain(self):
        scale = 15.0
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if (x, y) in self.reserved_road_cells:
                    self.terrain_grid[y][x] = "soil"  # Always soil for roads
                    continue
                n = self.simplex.noise2(x / scale, y / scale)
                world_x = x * self.cell_size
                world_y = y * self.cell_size
                if n < -0.6:
                    self.terrain_grid[y][x] = WaterBody(Vector2(world_x, world_y), self.cell_size)
                elif n < 0.5:
                    self.terrain_grid[y][x] = "soil"
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

    def add_multiple_roads(self, count):
        road_width = self.cell_size * 5
        min_y = int(self.height * 0.25)
        max_y = int(self.height * 0.75)
        for i in range(count):
            road_y = min_y + (max_y - min_y) * (i + 1) // (count + 1)
            road_path = []
            road_x = 0
            num_cells = self.width // self.cell_size
            for j in range(num_cells):
                road_pos = Vector2(road_x, road_y - road_width // 2)
                grid_x = int(road_pos.x // self.cell_size)
                grid_y = int(road_pos.y // self.cell_size)
                if 0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height:
                    # Reserve this cell for road
                    self.reserved_road_cells.add((grid_x, grid_y))
                    road = Road(road_pos, road_width)
                    road.visible = False
                    self.entities["Road"].append(road)
                    road_path.append(road)
                road_x += self.cell_size
            if len(road_path) > int(num_cells * 0.8):
                self.road_segments.append(road_path)

    def is_on_water_or_hill(self, position: Vector2) -> bool:
        x = int(position.x // self.cell_size)
        y = int(position.y // self.cell_size)
        if 0 <= y < self.grid_height and 0 <= x < self.grid_width:
            cell = self.terrain_grid[y][x]
            return isinstance(cell, WaterBody) or cell == "hill"
        return False

    def place_plants(self, num_bushes=40, num_trees=30, num_grass_areas=50):
        placed_positions = set()
        for PlantClass, count in [(Bush, num_bushes), (Tree, num_trees)]:
            for _ in range(count):
                tries = 0
                while tries < 1000:
                    x = random.randint(0, self.grid_width - 1)
                    y = random.randint(0, self.grid_height - 1)
                    if (x, y) in self.reserved_road_cells:
                        tries += 1
                        continue
                    cell = self.terrain_grid[y][x]
                    pos = Vector2(x * self.cell_size, y * self.cell_size)
                    if (
                        cell == "soil"
                        and not self.is_on_road(pos)
                        and not self.is_on_water_or_hill(pos)
                        and not self.is_near_water(x, y, radius=2)
                        and not self.is_near_road(x, y, radius=2)
                        and (x, y) not in placed_positions
                    ):
                        plant = PlantClass(pos)
                        self.entities[type(plant).__name__].append(plant)
                        placed_positions.add((x, y))
                        break
                    tries += 1

    def generate_grassy_areas(self, num_patches=8, min_size=10, max_size=30):
        for _ in range(num_patches):
            patch_size = random.randint(min_size, max_size)
            tries = 0
            while tries < 100:
                x = random.randint(0, self.grid_width - 1)
                y = random.randint(0, self.grid_height - 1)
                if (
                    self.terrain_grid[y][x] == "soil"
                    and not self.is_on_road(Vector2(x * self.cell_size, y * self.cell_size))
                    and not self.is_near_road(x, y, radius=2)
                ):
                    break
                tries += 1
            else:
                continue

            cells = set()
            cells.add((x, y))
            self.terrain_grid[y][x] = "grass"
            for _ in range(patch_size):
                cx, cy = random.choice(list(cells))
                nx = min(max(cx + random.choice([-1, 0, 1]), 0), self.grid_width - 1)
                ny = min(max(cy + random.choice([-1, 0, 1]), 0), self.grid_height - 1)
                if (
                    self.terrain_grid[ny][nx] == "soil"
                    and not self.is_on_road(Vector2(nx * self.cell_size, ny * self.cell_size))
                    and not self.is_near_road(nx, ny, radius=2)
                ):
                    self.terrain_grid[ny][nx] = "grass"
                    cells.add((nx, ny))

    def is_near_road(self, x, y, radius=2):
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                nx, ny = x + dx, y + dy
                if 0 <= ny < self.grid_height and 0 <= nx < self.grid_width:
                    pos = Vector2(nx * self.cell_size, ny * self.cell_size)
                    if self.is_on_road(pos):
                        return True
        return False

    def is_near_water(self, x, y, radius=2):
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                nx, ny = x + dx, y + dy
                if 0 <= ny < self.grid_height and 0 <= nx < self.grid_width:
                    cell = self.terrain_grid[ny][nx]
                    if isinstance(cell, WaterBody):
                        return True
        return False

    def spawn_animals(self):
        for _ in range(Bison.get_number()):
            pos = Vector2(random.randint(0, self.width), random.randint(0, self.height))
            bison = Bison(pos)
            self.entities["Bison"].append(bison)
            self.entities["Herbivore"].append(bison)

        for _ in range(Zebra.get_number()):
            pos = Vector2(random.randint(0, self.width), random.randint(0, self.height))
            zebra = Zebra(pos)
            self.entities["Zebra"].append(zebra)
            self.entities["Herbivore"].append(zebra)

        for _ in range(Antelope.get_number()):
            pos = Vector2(random.randint(0, self.width), random.randint(0, self.height))
            antelope = Antelope(pos)
            self.entities["Antelope"].append(antelope)
            self.entities["Herbivore"].append(antelope)

        for _ in range(Lion.get_number()):
            pos = Vector2(random.randint(0, self.width), random.randint(0, self.height))
            lion = Lion(pos)
            self.entities["Lion"].append(lion)
            self.entities["Carnivore"].append(lion)

        for _ in range(Hyena.get_number()):
            pos = Vector2(random.randint(0, self.width), random.randint(0, self.height))
            hyena = Hyena(pos)
            self.entities["Hyena"].append(hyena)
            self.entities["Carnivore"].append(hyena)

        for _ in range(Crocodile.get_number()):
            pos = Vector2(random.randint(0, self.width), random.randint(0, self.height))
            croc = Crocodile(pos)
            self.entities["Crocodile"].append(croc)
            self.entities["Carnivore"].append(croc)