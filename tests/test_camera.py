import pytest
import pygame
from ui.camera import Camera
from ui.vector2 import Vector2

@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    pygame.display.init()
    pygame.display.set_mode((1, 1))

def test_camera_init():
    cam = Camera(Vector2(0, 0), 800, 600, 2400, 1800)
    assert cam.position.x == 0
    assert cam.viewportWidth == 800
    assert cam.viewportHeight == 600

def test_camera_world_to_screen_and_back():
    cam = Camera(Vector2(100, 100), 800, 600, 2400, 1800)
    world = Vector2(200, 200)
    screen = cam.worldToScreen(world)
    back = cam.screenToWorld(screen)
    assert abs(back.x - world.x) < 1e-5
    assert abs(back.y - world.y) < 1e-5

def test_camera_zoom():
    cam = Camera(Vector2(0, 0), 800, 600, 2400, 1800)
    cam.zoom_in()
    assert cam.zoom > 1.0
    cam.zoom_out()
    assert cam.zoom <= 1.1