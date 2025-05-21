import pytest
from unittest.mock import MagicMock
import pygame

from gamelogic.game_world import GameWorld
from gamelogic.settings import WORLD_WIDTH, WORLD_HEIGHT
from ui.vector2 import Vector2

@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    pygame.display.init()
    pygame.display.set_mode((1, 1))
    dummy_surface = pygame.Surface((1, 1))
    monkeypatch.setattr(pygame.image, "load", lambda *a, **k: dummy_surface)
    monkeypatch.setattr(pygame.transform, "scale", lambda surf, size: dummy_surface)
    
@pytest.fixture
def game_world():
    return GameWorld(WORLD_WIDTH, WORLD_HEIGHT)

def test_gameworld_init(game_world):
    assert game_world.width == WORLD_WIDTH
    assert game_world.height == WORLD_HEIGHT
    assert isinstance(game_world.terrain_grid, list)
    assert isinstance(game_world.entities, dict)

def test_add_and_remove_entity(game_world):
    class DummyEntity:
        def __init__(self):
            self.position = Vector2(0, 0)
    entity = DummyEntity()
    game_world.addEntity(entity)
    assert "DummyEntity" in game_world.entities
    assert entity in game_world.entities["DummyEntity"]
    game_world.removeEntity(entity)
    assert entity not in game_world.entities["DummyEntity"]

def test_get_entities_in_radius(game_world):
    class DummyEntity:
        def __init__(self, x, y):
            self.position = Vector2(x, y)
    e1 = DummyEntity(10, 10)
    e2 = DummyEntity(20, 20)
    game_world.addEntity(e1)
    game_world.addEntity(e2)
    found = game_world.getEntitiesInRadius(Vector2(10, 10), 5)
    assert e1 in found
    assert e2 not in found

def test_is_on_road_and_water_or_hill(game_world):
    pos = Vector2(0, 0)
    assert isinstance(game_world.is_on_road(pos), bool)
    assert isinstance(game_world.is_on_water_or_hill(pos), bool)