from entities.animal import Animal
from ui.vector2 import Vector2

class Carnivore(Animal):
    def __init__(self, position: Vector2, size: float, speed: float):
        super().__init__(position, size, 'Carnivore', speed)

class Lion(Carnivore):
    limit = 2

    def __init__(self, position: Vector2):
        super().__init__(position, 25, 2.0)
        self.color = (255, 165, 0)

class Hyena(Carnivore):
    limit = 4

    def __init__(self, position: Vector2):
        super().__init__(position, 20, 2.5)
        self.color = (128, 128, 128)

class Crocodile(Carnivore):
    limit = 2

    def __init__(self, position: Vector2):
        super().__init__(position, 30, 1.0)
        self.color = (0, 100, 0)
