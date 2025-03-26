import pygame
from typing import List

class UIComponent:
    def render(self, surface):
        pass


    def handleEvent(self, event):
        pass


class Button(UIComponent):
    def __init__(self, text, position, size, callback):
        self.text = text
        self.position = position
        self.size = size
        self.callback = callback
        self.font = pygame.font.Font(None, 36)
        self.color = (200, 200, 200)
        self.hover_color = (150, 150, 150)

    def render(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.position[0] <= mouse_pos[0] <= self.position[0] + self.size[0] and \
                     self.position[1] <= mouse_pos[1] <= self.position[1] + self.size[1]
        color = self.hover_color if is_hovered else self.color
        pygame.draw.rect(surface, color, (*self.position, *self.size))
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(text_surface, (self.position[0] + 10, self.position[1] + 10))

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.position[0] <= mouse_pos[0] <= self.position[0] + self.size[0] and \
               self.position[1] <= mouse_pos[1] <= self.position[1] + self.size[1]:
                self.callback()

class Menu:
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager
        self.buttons = [
            Button("Continue", (300, 200), (200, 50), self.ui_manager.hideMenu),
            Button("Quit Game", (300, 300), (200, 50), self.quitGame)
        ]

    def render(self, surface):
        pygame.draw.rect(surface, (50, 50, 50), (250, 150, 300, 250))  # Menu background
        for button in self.buttons:
            button.render(surface)

    def handleEvent(self, event):
        for button in self.buttons:
            button.handleEvent(event)

    def quitGame(self):
        pygame.quit()
        exit()

class UIManager:
    def __init__(self):
        self.components: List[UIComponent] = []
        self.activeMenu: Menu = None
        self.menuButton = Button("Menu", (10, 10), (100, 50), self.toggleMenu)

    def addComponent(self, component: UIComponent):
        self.components.append(component)

    def removeComponent(self, component: UIComponent):
        self.components.remove(component)

    def toggleMenu(self):
        if self.activeMenu:
            self.hideMenu()
        else:
            self.showMenu()

    def showMenu(self):
        self.activeMenu = Menu(self)

    def hideMenu(self):
        self.activeMenu = None

    def handleEvent(self, event) -> bool:
        if self.activeMenu:
            self.activeMenu.handleEvent(event)
            return True
        self.menuButton.handleEvent(event)
        return False

    def render(self, surface):
        self.menuButton.render(surface)
        for component in self.components:
            component.render(surface)
        if self.activeMenu:
            self.activeMenu.render(surface)