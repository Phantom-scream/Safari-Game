import pytest
import pygame
from ui.ui_manager import UIManager, Button

@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    pygame.display.init()
    pygame.display.set_mode((800, 600))
    pygame.font.init()

def test_ui_manager_init():
    ui = UIManager()
    assert hasattr(ui, "menuButton")
    assert hasattr(ui, "shopButton")
    assert hasattr(ui, "pauseButton")

def test_button_hover():
    btn = Button("Test", (0, 0), (100, 50), lambda: None)
    assert btn.is_hovered((10, 10))
    assert not btn.is_hovered((200, 200))