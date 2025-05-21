import pytest
import pygame
from ui.renderer import Renderer
from ui.vector2 import Vector2

@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    pygame.display.init()
    pygame.display.set_mode((800, 600))
    pygame.font.init()
    dummy_surface = pygame.Surface((10, 10))
    monkeypatch.setattr(pygame.image, "load", lambda *a, **k: dummy_surface)
    monkeypatch.setattr(pygame.transform, "scale", lambda surf, size: dummy_surface)

def test_renderer_init():
    renderer = Renderer(2400, 1800, 800, 600)
    assert renderer.camera.viewportWidth == 800
    assert renderer.camera.viewportHeight == 600

def test_load_sprite():
    renderer = Renderer(2400, 1800, 800, 600)
    sprite = renderer.loadSprite("dummy.png")
    assert isinstance(sprite, pygame.Surface)