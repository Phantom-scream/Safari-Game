import pytest
import pygame
from ui.minimap import Minimap
from ui.vector2 import Vector2

@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    pygame.display.init()
    pygame.display.set_mode((800, 600))

def test_minimap_init():
    minimap = Minimap(2400, 1800, 800, 600)
    assert minimap.minimap_width == 200
    assert minimap.minimap_height == 150

def test_handle_click_moves_camera():
    minimap = Minimap(2400, 1800, 800, 600)
    class DummyCamera:
        def __init__(self):
            self.position = Vector2(0, 0)
            self.viewportWidth = 800
            self.viewportHeight = 600
        def moveTo(self, pos):
            self.position = pos
    camera = DummyCamera()
    minimap.handle_click((minimap.position[0] + 10, minimap.position[1] + 10), camera)
    assert isinstance(camera.position, Vector2)