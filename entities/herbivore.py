import pygame
from entities.animal import Animal
from ui.vector2 import Vector2

class Herbivore(Animal):
    def __init__(self, position: Vector2, size: float, speed: float):
        super().__init__(position, size, 'Herbivore', speed)

    def render(self, surface: pygame.Surface, camera: 'Camera'):
        screenPos = camera.worldToScreen(self.position)
        size = self.size * camera.zoom
        if hasattr(self, "sprite"):
            # Scale the sprite to the current zoom
            scaled_sprite = pygame.transform.scale(self.sprite, (int(size), int(size)))
            surface.blit(scaled_sprite, (screenPos.x, screenPos.y))
        else:
            pygame.draw.rect(surface, self.color, (screenPos.x, screenPos.y, size, size))

class Bison(Herbivore):
    limit = 5

    def __init__(self, position: Vector2):
        super().__init__(position, 40, 100)  # <-- Set speed to 100
        self.color = (139, 69, 19)
        
        # Load image first
        self.sprite = pygame.image.load("assets/elephent.png")
        
        # Make the black background transparent 
        # Do this BEFORE scaling for best results
        self.sprite.set_colorkey((0, 0, 0))
        
        # Convert after setting colorkey
        self.sprite = self.sprite.convert_alpha()
        
        # Now scale the image
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
    
    def render(self, surface: pygame.Surface, camera: 'Camera'):
        screenPos = camera.worldToScreen(self.position)
        size = self.size * camera.zoom
        if hasattr(self, "sprite"):
            scaled_sprite = pygame.transform.scale(self.sprite, (int(size), int(size)))
            surface.blit(scaled_sprite, (screenPos.x, screenPos.y))
        else:
            pygame.draw.rect(surface, self.color, (screenPos.x, screenPos.y, size, size))

class Zebra(Herbivore):
    limit = 5

    def __init__(self, position: Vector2):
        super().__init__(position, 20, 110)  # <-- Set speed to 110
        self.color = (255, 255, 255)

class Antelope(Herbivore):
    limit = 5
    
    def __init__(self, position: Vector2):
        super().__init__(position, 20, 120)  # <-- Set speed to 120
        self.color = (210, 180, 140)
