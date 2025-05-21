import pytest
import pygame
from entities.jeep import Jeep
from entities.road import Road
from ui.vector2 import Vector2

@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    pygame.display.init()
    pygame.display.set_mode((1, 1))
    dummy_surface = pygame.Surface((1, 1))
    monkeypatch.setattr(pygame.image, "load", lambda *a, **k: dummy_surface)
    monkeypatch.setattr(pygame.transform, "scale", lambda surf, size: dummy_surface)

def test_jeep_init():
    road_path = [Road(Vector2(0, 0), 40), Road(Vector2(40, 0), 40)]
    jeep = Jeep(Vector2(0, 0), road_path)
    assert jeep.position.x >= 0
    assert jeep.position.y >= 0
    assert jeep.size == 40
    assert len(jeep.passengers) == 4