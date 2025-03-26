from entities.animal import Animal
from ui.vector2 import Vector2

class Herbivore(Animal):
    def __init__(self, position: Vector2, size: float, speed: float):
        super().__init__(position, size, 'Herbivore', speed)

class Bison(Herbivore):
    limit = 3

    def __init__(self, position: Vector2):
        super().__init__(position, 20, 1.5)
        self.color = (139, 69, 19)

class Zebra(Herbivore):
    limit = 2

    def __init__(self, position: Vector2):
        super().__init__(position, 20, 2.0)
        self.color = (255, 255, 255)

class Antelope(Herbivore):
    limit = 2
    
    def __init__(self, position: Vector2):
        super().__init__(position, 20, 2.5)
        self.color = (210, 180, 140)
