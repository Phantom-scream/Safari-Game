from entities.animal import Animal
from ui.vector2 import Vector2

class Carnivore(Animal):
    def __init__(self, position: Vector2, size: float, speed: float):
        super().__init__(position, size, 'Carnivore', speed)

class Lion(Carnivore):
    limit = 4

    def __init__(self, position: Vector2):
        super().__init__(position, 25, 110)  # <-- Set speed to 110
        self.color = (255, 165, 0)

class Hyena(Carnivore):
    limit = 6

    def __init__(self, position: Vector2):
        super().__init__(position, 20, 115)  # <-- Set speed to 115
        self.color = (128, 128, 128)

class Crocodile(Carnivore):
    limit = 4

    def __init__(self, position: Vector2):
        super().__init__(position, 30, 80)  # <-- Set speed to 80
        self.color = (0, 100, 0)
