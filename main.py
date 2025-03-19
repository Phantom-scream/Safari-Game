import pygame
from game import GameWorld
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Create game world
world = GameWorld(SCREEN_WIDTH, SCREEN_HEIGHT)

running = True
while running:
    screen.fill((120, 180, 255))  # Light blue background (temporary)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update world
    world.update()

    # Draw world
    world.draw(screen)

    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()