from entities.entity import Entity
from ui.vector2 import Vector2
import random
import pygame
import math
import time
from gamelogic.settings import WORLD_WIDTH, WORLD_HEIGHT

class Poacher(Entity):
    def __init__(self, position: Vector2, size: float, speed: float):
        super().__init__(position, size, 'Poacher')
        self.speed = speed
        self.target = Vector2(
            random.uniform(0, WORLD_WIDTH),
            random.uniform(0, WORLD_HEIGHT)
        )
        self.color = (255, 0, 0)  # Red color for poachers
        self.visible = False  # Start as invisible
        self.detection_range = 150  # Range at which tourists/rangers can see the poacher
        self.hunting_range = 100  # Range for shooting animals
        self.capture_range = 40  # Range for capturing animals
        self.last_hunt_time = time.time()
        self.has_captured_animal = None  # Store reference to captured animal
        self.escape_point = None  # Point where poacher will escape with captured animal
        self._world = None
        self.current_path = []

    def astar_pathfinding(self, start: Vector2, goal: Vector2, world: 'GameWorld') -> list[Vector2]:
        """A* pathfinding implementation for poacher movement"""
        def heuristic(a: Vector2, b: Vector2) -> float:
            return a.distanceTo(b)
    
        open_set = {start}
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        while open_set:
            current = min(open_set, key=lambda pos: f_score.get(pos, float('inf')))
        
            if current.distanceTo(goal) < 20:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path

            open_set.remove(current)
        
            # Generate neighbors in 8 directions
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,1), (1,-1), (-1,-1)]:
                neighbor = Vector2(current.x + dx * 20, current.y + dy * 20)
            
                # Check world boundaries
                if 0 <= neighbor.x < WORLD_WIDTH and 0 <= neighbor.y < WORLD_HEIGHT:
                    tentative_g_score = g_score[current] + current.distanceTo(neighbor)
                
                    if tentative_g_score < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        open_set.add(neighbor)
    
        return []  # No path found

    def move(self):
        """Simple movement without pathfinding"""
        if self.position.distanceTo(self.target) > 2:
            direction = self.target.subtract(self.position).normalize()
            self.position = self.position.add(Vector2(
                direction.x * self.speed,
                direction.y * self.speed
            ))
        else:
            # Set new random target when reached current target
            self.target = Vector2(
                random.uniform(0, WORLD_WIDTH),
                random.uniform(0, WORLD_HEIGHT)
            )

    def check_visibility(self, world):
        """Check if poacher should be visible based on nearby tourists/rangers"""
        for entity_type in ['Tourist', 'Ranger']:  # You'll need to implement these classes
            if entity_type in world.entities:
                for observer in world.entities[entity_type]:
                    distance = self.position.distanceTo(observer.position)
                    if distance < self.detection_range:
                        self.visible = True
                        return
        self.visible = False

    def hunt(self, world):
        """Poacher can either shoot animals from distance or capture them"""
        current_time = time.time()
        if current_time - self.last_hunt_time < 7:  # Cooldown between hunting attempts
            return

        # If poacher already has a captured animal, handle escape logic
        if self.has_captured_animal:
            if self.escape_point is None:
                # Set escape point at the nearest map border
                if self.position.x < WORLD_WIDTH/2:
                    escape_x = 0  # Escape to left border
                else:
                    escape_x = WORLD_WIDTH  # Escape to right border
                self.escape_point = Vector2(escape_x, random.randint(0, WORLD_HEIGHT))
        
            self.target = self.escape_point
        
            if self.position.distanceTo(self.escape_point) < 10:
                entity_type = type(self.has_captured_animal).__name__
                if (entity_type in world.entities and 
                    self.has_captured_animal in world.entities[entity_type]):
                    world.removeEntity(self.has_captured_animal)
                    self.has_captured_animal = None
                    self.escape_point = None
                    print("Poacher escaped with captured animal!")
            return

        # Find closest animal to hunt
        closest_animal = None
        closest_distance = float('inf')
    
        # Priority order for hunting (smaller animals first)
        target_animals = ['Antelope', 'Zebra', 'Bison', 'Lion', 'Hyena', 'Crocodile']
    
        for entity_type in target_animals:
            for animal in list(world.entities.get(entity_type, [])):
                distance = self.position.distanceTo(animal.position)
            
                if distance < closest_distance:
                    closest_distance = distance
                    closest_animal = animal

        # If found a target animal, try to hunt it
        if closest_animal:
            if closest_distance < self.capture_range:
                # Capture animal if very close
                self.has_captured_animal = closest_animal
                print(f"Poacher captured {closest_animal.entityType} at {closest_animal.position}")
                self.last_hunt_time = current_time
            
            elif closest_distance < self.hunting_range:
                # Shoot animal if within range
                world.removeEntity(closest_animal)
                print(f"Poacher shot {closest_animal.entityType} at {closest_animal.position}")
                self.last_hunt_time = current_time
            else:
                # Move towards the animal if it's spotted
                self.target = closest_animal.position

    def update(self, deltaTime: float, world: 'GameWorld'):
        self._world = world
        self.check_visibility(world)
        self.move()  # Using simple movement instead of A* pathfinding
        
        if not self.visible:  # Only hunt when not visible
            self.hunt(world)
        
        # Update captured animal position if exists
        if self.has_captured_animal:
            self.has_captured_animal.position = self.position

    def render(self, surface: pygame.Surface, camera: 'Camera'):
        if not self.visible:
            return  # Don't render if not visible
            
        screenPos = camera.worldToScreen(self.position)
        pygame.draw.circle(surface, self.color, (int(screenPos.x), int(screenPos.y)), int(self.size / 2))
        
        # Draw captured animal if exists
        if self.has_captured_animal:
            pygame.draw.circle(surface, self.has_captured_animal.color, 
                             (int(screenPos.x), int(screenPos.y)), 
                             int(self.size / 4))