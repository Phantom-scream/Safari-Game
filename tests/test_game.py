import pytest
import pygame
from game import Game

@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    pygame.display.init()
    pygame.display.set_mode((800, 600))
    pygame.font.init()
    dummy_surface = pygame.Surface((10, 10))
    monkeypatch.setattr(pygame.image, "load", lambda *a, **k: dummy_surface)
    monkeypatch.setattr(pygame.transform, "scale", lambda surf, size: dummy_surface)

def test_game_init():
    game = Game(800, 600, difficulty="easy")
    assert game.width == 800
    assert game.height == 600
    assert game.difficulty == "easy"
    assert hasattr(game, "renderer")
    assert hasattr(game, "uiManager")
    assert hasattr(game, "minimap")
    assert hasattr(game, "economy")
    assert hasattr(game, "world")

def test_game_speed_modes():
    game = Game(800, 600)
    game.set_speed_mode("day")
    assert game.current_speed_mode == "day"
    game.set_speed_mode("week")
    assert game.current_speed_mode == "week"

def test_game_zoom():
    game = Game(800, 600)
    prev_zoom = game.renderer.camera.zoom
    game.zoom_in()
    assert game.renderer.camera.zoom > prev_zoom
    game.zoom_out()
    assert game.renderer.camera.zoom <= prev_zoom + 0.1  # Allow for float rounding

def test_game_update_paused():
    game = Game(800, 600)
    game.uiManager.paused = True
    game.update(0.1)  # Should do nothing and not crash

def test_game_render_runs():
    game = Game(800, 600)
    surface = pygame.Surface((800, 600))
    game.render(surface)  # Should not crash