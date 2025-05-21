import pytest
import pygame
from ui.main_screen import MainScreen

@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    pygame.display.init()
    pygame.display.set_mode((800, 600))
    pygame.font.init() 
    dummy_surface = pygame.Surface((300, 300))
    monkeypatch.setattr(pygame.image, "load", lambda *a, **k: dummy_surface)
    monkeypatch.setattr(pygame.transform, "scale", lambda surf, size: dummy_surface)

def test_main_screen_init():
    screen = pygame.display.get_surface()
    ms = MainScreen(screen, lambda d: None, lambda: None, lambda: None)
    assert ms.selected_difficulty == "easy"
    assert len(ms.buttons) > 0

def test_select_difficulty():
    screen = pygame.display.get_surface()
    ms = MainScreen(screen, lambda d: None, lambda: None, lambda: None)
    ms.select_difficulty("hard")
    assert ms.selected_difficulty == "hard"