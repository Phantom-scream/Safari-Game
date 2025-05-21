import pytest
import pygame
from entities.poacher import Poacher
from ui.vector2 import Vector2

@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    pygame.display.init()
    pygame.display.set_mode((1, 1))

def test_poacher_init():
    poacher = Poacher(Vector2(10, 20), 30, 1.5)
    assert poacher.position.x == 10
    assert poacher.position.y == 20
    assert poacher.size == 30
    assert poacher.speed == 1.5
    assert poacher.color == (255, 0, 0)
    assert poacher.visible is True