import pytest
import pygame
from unittest.mock import MagicMock
from entities.herbivore import Bison, Zebra, Antelope
from ui.vector2 import Vector2

@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    pygame.display.init()
    pygame.display.set_mode((1, 1))
    dummy_surface = pygame.Surface((1, 1))
    monkeypatch.setattr(pygame.image, "load", lambda *a, **k: dummy_surface)
    monkeypatch.setattr(pygame.transform, "scale", lambda surf, size: dummy_surface)

def test_bison_init():
    bison = Bison(Vector2(10, 20))
    assert bison.position.x == 10
    assert bison.position.y == 20
    assert bison.color == (139, 69, 19)

def test_zebra_init():
    zebra = Zebra(Vector2(5, 15))
    assert zebra.position.x == 5
    assert zebra.position.y == 15
    assert zebra.color == (255, 255, 255)

def test_antelope_init():
    antelope = Antelope(Vector2(1, 2))
    assert antelope.position.x == 1
    assert antelope.position.y == 2
    assert antelope.color == (210, 180, 140)