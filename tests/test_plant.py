import pytest
import pygame
from entities.plant import Plant, Bush, Tree
from ui.vector2 import Vector2

@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    pygame.display.init()
    pygame.display.set_mode((1, 1))
    dummy_surface = pygame.Surface((1, 1))
    monkeypatch.setattr(pygame.image, "load", lambda *a, **k: dummy_surface)
    monkeypatch.setattr(pygame.transform, "scale", lambda surf, size: dummy_surface)

def test_bush_init():
    bush = Bush(Vector2(5, 5))
    assert bush.position.x == 5
    assert bush.position.y == 5
    assert bush.size == 24
    assert bush.color == (34, 139, 34)

def test_tree_init():
    tree = Tree(Vector2(10, 10))
    assert tree.position.x == 10
    assert tree.position.y == 10
    assert tree.size == 40
    assert tree.color == (0, 100, 0)

def test_plant_be_eaten():
    class DummyPlant(Plant):
        def update(self, deltaTime, world): pass
        def render(self, surface, camera): pass
    plant = DummyPlant(Vector2(0, 0), 10, 5)
    eaten = plant.beEaten(3)
    assert eaten == 3
    assert plant.getNutritionalValue() == 2