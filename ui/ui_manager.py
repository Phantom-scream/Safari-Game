import pygame
from typing import List
import time

from entities.tourist import Tourist

PRICES = {
    "Tree": 150,
    "Bush": 100,
    "Grass": 50,
    "Antelope": 150,
    "Zebra": 100,
    "Bison": 170,
    "Lion": 200,
    "Hyena": 70,
    "Crocodile": 180,
    "Jeep": 300,
}

class UIComponent:
    def render(self, surface):
        pass


    def handleEvent(self, event):
        pass


class Button(UIComponent):
    def __init__(self, text, position, size, callback, font_size=16):
        self.text = text
        self.position = position
        self.size = size
        self.callback = callback
        self.font = pygame.font.Font(None, font_size)
        self.color = (200, 200, 200)
        self.hover_color = (150, 150, 150)

    def render(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.is_hovered(mouse_pos)
        color = self.hover_color if is_hovered else self.color
        pygame.draw.rect(surface, color, (*self.position, *self.size))
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(text_surface, (self.position[0] + 10, self.position[1] + 10))

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.is_hovered(mouse_pos):
                self.callback()

    def is_hovered(self, mouse_pos):
        x, y = self.position
        w, h = self.size
        mx, my = mouse_pos
        return x <= mx <= x + w and y <= my <= y + h

class Menu:
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager
        self.buttons = [
            Button("Continue", (300, 200), (200, 50), self.ui_manager.hideMenu),
            Button("Quit Game", (300, 300), (200, 50), self.quitGame)
        ]

    def render(self, surface):
        pygame.draw.rect(surface, (50, 50, 50), (250, 150, 300, 250)) 
        for button in self.buttons:
            button.render(surface)

    def handleEvent(self, event):
        for button in self.buttons:
            button.handleEvent(event)

    def quitGame(self):
        pygame.quit()
        exit()

class ShopMenu:
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager
        self.width = 180
        self.height = 340
        self.x = 50
        self.y = 80
        self.font = pygame.font.Font(None, 18)
        self.section_font = pygame.font.Font(None, 22)
        self.buttons = []
        self.message = ""
        self.message_time = 0

        self.plants_y = self.y + 30
        button_w, button_h = 70, 22
        button_x = self.x + 15
        self.buttons.append(Button("Tree", (button_x, self.plants_y), (button_w, button_h), lambda: self.purchase("Tree")))
        self.buttons.append(Button("Bush", (button_x, self.plants_y + 26), (button_w, button_h), lambda: self.purchase("Bush")))
        self.buttons.append(Button("Grass", (button_x, self.plants_y + 52), (button_w, button_h), lambda: self.purchase("Grass")))

        self.animals_title_y = self.plants_y + 80
        self.animals_y = self.animals_title_y + 24  
        self.animal_names = ["Antelope", "Zebra", "Bison", "Lion", "Hyena", "Crocodile"]
        for i, name in enumerate(self.animal_names):
            self.buttons.append(Button(name, (button_x, self.animals_y + i * 24), (90, button_h), lambda n=name: self.purchase(n)))

        self.jeep_title_y = self.animals_y + len(self.animal_names) * 24 + 10
        self.jeep_y = self.jeep_title_y + 24
        self.buttons.append(Button("Jeep", (button_x, self.jeep_y), (90, button_h), lambda: self.purchase("Jeep")))

    def render(self, surface):
        pygame.draw.rect(surface, (245, 245, 220), (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(surface, (218, 165, 32), (self.x, self.y, self.width, self.height), 2, border_radius=10)

        surface.blit(self.section_font.render("Plants", True, (0, 100, 0)), (self.x + 8, self.y + 8))
        surface.blit(self.section_font.render("Animals", True, (139, 69, 19)), (self.x + 8, self.animals_title_y))
        surface.blit(self.section_font.render("Jeep", True, (60, 60, 200)), (self.x + 8, self.jeep_title_y))

        for button in self.buttons:
            button.font = pygame.font.Font(None, 16)
            button.render(surface)

        if self.message and time.time() - self.message_time < 2:
            msg_font = pygame.font.Font(None, 20)
            msg_surface = msg_font.render(self.message, True, (200, 0, 0))
            surface.blit(msg_surface, (self.x + 10, self.y + self.height - 30))

    def handleEvent(self, event):
        for button in self.buttons:
            button.handleEvent(event)

    def purchase(self, item_name):
        game = self.ui_manager.get_game_instance()
        price = PRICES[item_name]

        from ui.vector2 import Vector2
        import random

        placed_pos = None  

        if item_name == "Jeep":
            entrance = game.world.road_entrance
            road_path = sorted(game.world.entities["Road"], key=lambda r: r.position.x)
            if not (entrance and road_path):
                self.message = "No road entrance!"
                self.message_time = time.time()
                return
            if game.economy.money < price:
                self.message = "Not enough balance!"
                self.message_time = time.time()
                return
            game.economy.spend_money(price)
            spacing = 50
            num_jeeps = len(game.world.entities["Jeep"])
            offset = num_jeeps * spacing
            jeep_pos = Vector2(entrance.x + offset, entrance.y)
            from entities.jeep import Jeep
            new_jeep = Jeep(jeep_pos, [r.position for r in road_path])
            new_jeep.current_index = 0
            new_jeep.state = "to_exit"
            new_jeep.passengers = [Tourist(f"Tourist {j+1}") for j in range(4)]
            game.world.entities["Jeep"].append(new_jeep)
            game.jeep_count += 1
            self.message = "Purchased Jeep! It's on the road."
            self.message_time = time.time()
            game.renderer.camera.moveTo(new_jeep.position)
            return

        if game.economy.money < price:
            self.message = "Not enough balance!"
            self.message_time = time.time()
            return
        game.economy.spend_money(price)

        if item_name in ["Tree", "Bush", "Grass"]:
            for _ in range(100):
                x = random.randint(0, game.world.grid_width - 1)
                y = random.randint(0, game.world.grid_height - 1)
                cell = game.world.terrain_grid[y][x]
                pos = Vector2(x * game.world.cell_size, y * game.world.cell_size)
                if cell == "soil" and not game.world.is_on_road(pos) and not game.world.is_on_water_or_hill(pos):
                    if item_name == "Tree":
                        from entities.plant import Tree
                        plant = Tree(pos)
                        game.world.entities["Tree"].append(plant)
                    elif item_name == "Bush":
                        from entities.plant import Bush
                        plant = Bush(pos)
                        game.world.entities["Bush"].append(plant)
                    elif item_name == "Grass":
                        pass
                    placed_pos = pos
                    self.message = f"Purchased {item_name}!"
                    self.message_time = time.time()
                    break
            else:
                self.message = "No valid spot found!"
                self.message_time = time.time()
                return

        animal_classes = {
            "Antelope": "Antelope",
            "Zebra": "Zebra",
            "Bison": "Bison",
            "Lion": "Lion",
            "Hyena": "Hyena",
            "Crocodile": "Crocodile"
        }
        if item_name in animal_classes:
            animal_module_map = {
                "Antelope": "herbivore",
                "Zebra": "herbivore",
                "Bison": "herbivore",
                "Lion": "carnivore",
                "Hyena": "carnivore",
                "Crocodile": "carnivore"
            }
            module_name = animal_module_map[item_name]
            module = __import__(f"entities.{module_name}", fromlist=[animal_classes[item_name]])
            AnimalClass = getattr(module, animal_classes[item_name])
            for _ in range(100):
                x = random.randint(0, game.world.grid_width - 1)
                y = random.randint(0, game.world.grid_height - 1)
                cell = game.world.terrain_grid[y][x]
                pos = Vector2(x * game.world.cell_size, y * game.world.cell_size)
                if cell == "soil" and not game.world.is_on_road(pos) and not game.world.is_on_water_or_hill(pos):
                    animal = AnimalClass(pos)
                    game.world.entities[item_name].append(animal)
                    placed_pos = pos
                    self.message = f"Purchased {item_name}!"
                    self.message_time = time.time()
                    break
            else:
                self.message = "No valid spot found!"
                self.message_time = time.time()
                return

        # Move camera to the new product if placed
        if placed_pos is not None:
            game.renderer.camera.moveTo(placed_pos)

class UIManager:
    def __init__(self):
        self.components: List[UIComponent] = []
        self.activeMenu: Menu = None
        button_w, button_h = 90, 40
        self.shopButton = Button("Shop", (10, 10), (button_w, button_h), self.toggleShop, font_size=20)
        self.menuButton = Button("Menu", (10 + button_w, 10), (button_w, button_h), self.toggleMenu, font_size=20)
        self.pauseButton = Button("Pause", (10 + 2 * button_w, 10), (button_w, button_h), self.togglePause, font_size=20)
        self.shopMenu = None
        self.paused = False

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

    def toggleShop(self):
        if self.shopMenu:
            self.hideShop()
        else:
            self.showShop()

    def showShop(self):
        self.shopMenu = ShopMenu(self)

    def hideShop(self):
        self.shopMenu = None

    def togglePause(self):
        self.paused = not self.paused

    def handleEvent(self, event) -> bool:
        if self.activeMenu:
            self.activeMenu.handleEvent(event)
            return True
        self.menuButton.handleEvent(event)
        self.shopButton.handleEvent(event)
        self.pauseButton.handleEvent(event)
        for component in self.components:
            component.handleEvent(event)
        if self.shopMenu:
            self.shopMenu.handleEvent(event)
        if self.paused and hasattr(self, "continueButton"):
            self.continueButton.handleEvent(event)
            return True
        return False

    def render(self, surface):
        self.menuButton.render(surface)
        self.shopButton.render(surface)
        self.pauseButton.render(surface)
        for component in self.components:
            component.render(surface)
        if self.activeMenu:
            self.activeMenu.render(surface)
        if self.shopMenu:
            self.shopMenu.render(surface)
        if self.paused:
            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            surface.blit(overlay, (0, 0))
            continue_w, continue_h = 200, 60
            screen_w, screen_h = surface.get_size()
            continue_x = (screen_w - continue_w) // 2
            continue_y = (screen_h - continue_h) // 2
            self.continueButton = Button("Continue", (continue_x, continue_y), (continue_w, continue_h), self.togglePause, font_size=28)
            self.continueButton.render(surface)

    def get_game_instance(self):
        import __main__
        return getattr(__main__, "game", None)