import pytest
import pygame
from unittest.mock import MagicMock
from entities.carnivore import Lion, Hyena, Crocodile
from ui.vector2 import Vector2

@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    pygame.display.init()
    pygame.display.set_mode((1, 1))
    dummy_surface = pygame.Surface((1, 1))
    monkeypatch.setattr(pygame.image, "load", lambda *a, **k: dummy_surface)
    monkeypatch.setattr(pygame.transform, "scale", lambda surf, size: dummy_surface)

def test_lion_init():
    lion = Lion(Vector2(10, 20))
    assert lion.position.x == 10
    assert lion.position.y == 20
    assert lion.color == (255, 165, 0)

def test_hyena_init():
    hyena = Hyena(Vector2(5, 15))
    assert hyena.position.x == 5
    assert hyena.position.y == 15
    assert hyena.color == (128, 128, 128)

def test_crocodile_init():
    croc = Crocodile(Vector2(1, 2))
    assert croc.position.x == 1
    assert croc.position.y == 2
    assert croc.color == (0, 100, 0)