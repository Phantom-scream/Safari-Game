import pytest
import pygame
from entities.road import Road
from ui.vector2 import Vector2

@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    pygame.display.init()
    pygame.display.set_mode((1, 1))

def test_road_init():
    road = Road(Vector2(10, 20), 40)
    assert road.position.x == 10
    assert road.position.y == 20
    assert road.size == 40
    assert road.color == (139, 101, 8)
    assert road.visible is False