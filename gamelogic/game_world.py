from typing import List, Dict
import pygame
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
    def __init__(self, width, height):
        self.width = width
        self.height = height
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