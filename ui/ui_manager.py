from typing import List

class UIComponent:
    def render(self, surface):
        pass

class Menu:
    def render(self, surface):
        pass

class UIManager:
    def __init__(self):
        self.components: List[UIComponent] = []
        self.activeMenu: Menu = None

    def addComponent(self, component: UIComponent):
        self.components.append(component)

    def removeComponent(self, component: UIComponent):
        self.components.remove(component)

    def showMenu(self, menuType):
        # Logic to show a specific menu
        pass

    def hideMenu(self):
        self.activeMenu = None

    def handleEvent(self, event) -> bool:
        # Logic to handle events
        return False

    def render(self, surface):
        for component in self.components:
            component.render(surface)
        if self.activeMenu:
            self.activeMenu.render(surface)