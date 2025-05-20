from entities.entity import Entity
from ui.vector2 import Vector2
import random
import pygame
import math
import time
from gamelogic.settings import WORLD_WIDTH, WORLD_HEIGHT
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gamelogic.game_world import GameWorld
    from ui.camera import Camera

class Poacher(Entity):
    def __init__(self, position: Vector2, size: float, speed: float):
        super().__init__(position, size, 'Poacher')
        self.speed = speed
        self.target = Vector2(
            random.uniform(0, WORLD_WIDTH),
            random.uniform(0, WORLD_HEIGHT)
        )
        self.color = (255, 0, 0)  # Red color for poachers
        self.visible = True  # Start as invisible
        self.detection_range = 150  # Range at which tourists/rangers can see the poacher
        self.hunting_range = 100  # Range for shooting animals
        self.capture_range = 40  # Range for capturing animals
        self.last_hunt_time = time.time()
        self.has_captured_animal = None  # Store reference to captured animal
        self.escape_point = None  # Point where poacher will escape with captured animal
        self.return_point = None
        self._world = None
        self.current_path = []
        self.state = "hunting"
        self._clear_captured_next_update = False

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

    def check_visibility(self, world):
        """Poacher is visible only if a tourist is within detection range."""
        self.visible = False  # Default to invisible
        # Check for tourists in all jeeps
        for jeep in world.entities.get("Jeep", []):
            for tourist in getattr(jeep, "passengers", []):
                # Assume jeep.position is the tourist's position
                if self.position.distanceTo(jeep.position) < self.detection_range:
                    self.visible = True
                    return

    def hunt(self, world):
        current_time = time.time()
        if current_time - self.last_hunt_time < 7:
            return

        # If poacher already has a captured animal, handle escape logic
        if self.has_captured_animal:
            if self.escape_point is None:
                # Set escape point OUTSIDE the map
                if self.position.x < WORLD_WIDTH / 2:
                    escape_x = -40
                else:
                    escape_x = WORLD_WIDTH + 40
                self.escape_point = Vector2(escape_x, random.uniform(0, WORLD_HEIGHT))
            self.target = self.escape_point
            return

        # Find closest alive animal to hunt
        closest_animal = None
        closest_distance = float('inf')
        target_animals = ['Antelope', 'Zebra', 'Bison', 'Lion', 'Hyena', 'Crocodile']
        for entity_type in target_animals:
            for animal in list(world.entities.get(entity_type, [])):
                if getattr(animal, "is_dead", False):
                    continue
                distance = self.position.distanceTo(animal.position)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_animal = animal

        if closest_animal:
            self.has_captured_animal = closest_animal
            self.has_captured_animal.mark_as_dead()  # Mark as dead immediately
            self.has_captured_animal.visible = False  # Make animal invisible
            print(f"Poacher captured {closest_animal.entityType} at {closest_animal.position}")
            self.last_hunt_time = current_time
            self.state = "escaping"
            if self.position.x < WORLD_WIDTH / 2:
                escape_x = -40
            else:
                escape_x = WORLD_WIDTH + 40
            self.escape_point = Vector2(escape_x, random.uniform(0, WORLD_HEIGHT))
            self.target = self.escape_point

    def move(self):
        USE_PATHFINDING = False  # Set to True to enable A* pathfinding

        # Determine the current destination based on state
        if self.state == "hunting":
            destination = self.target
        elif self.state == "escaping" and self.escape_point:
            destination = self.escape_point
        elif self.state == "returning" and self.return_point:
            destination = self.return_point
        else:
            # Invalid state, reset everything
            self.state = "hunting"
            self.has_captured_animal = None
            self.escape_point = None
            self.return_point = None
            self.target = Vector2(
                random.uniform(0, WORLD_WIDTH),
                random.uniform(0, WORLD_HEIGHT)
            )
            self.current_path = []
            return

        # Pathfinding logic
        if USE_PATHFINDING:
            if not self.current_path or (self.current_path and self.current_path[-1].distanceTo(destination) > 10):
                self.current_path = self.astar_pathfinding(self.position, destination, self._world)
            if self.current_path:
                next_point = self.current_path[0]
                if self.position.distanceTo(next_point) < 2:
                    self.current_path.pop(0)
                    if not self.current_path:
                        return
                    next_point = self.current_path[0]
                direction = next_point.subtract(self.position).normalize()
                self.position = self.position.add(Vector2(direction.x * self.speed, direction.y * self.speed))
            else:
                direction = destination.subtract(self.position).normalize()
                self.position = self.position.add(Vector2(direction.x * self.speed, direction.y * self.speed))
        else:
            if self.position.distanceTo(destination) > 2:
                direction = destination.subtract(self.position).normalize()
                self.position = self.position.add(Vector2(direction.x * self.speed, direction.y * self.speed))
            else:
                if self.state == "hunting":
                    self.target = Vector2(
                        random.uniform(0, WORLD_WIDTH),
                        random.uniform(0, WORLD_HEIGHT)
                    )
                elif self.state == "escaping":
                    # Arrived at escape point (outside world), remove animal and reset to returning
                    # Only remove animal if poacher is FULLY outside the map
                    outside = (
                        self.position.x < 0 or self.position.x > WORLD_WIDTH or
                        self.position.y < 0 or self.position.y > WORLD_HEIGHT
                    )
                    if outside:
                        if self.has_captured_animal:
                            entity_type = type(self.has_captured_animal).__name__
                            if (entity_type in self._world.entities and
                                self.has_captured_animal in self._world.entities[entity_type]):
                                self._world.removeEntity(self.has_captured_animal)
                        # Do NOT set self.has_captured_animal = None here!
                        # Instead, set a flag to clear it after rendering
                        self._clear_captured_next_update = True
                        self.escape_point = None
                        self.state = "returning"
                        self.return_point = Vector2(
                            random.uniform(0, WORLD_WIDTH),
                            random.uniform(0, WORLD_HEIGHT)
                        )
                        self.target = self.return_point
                        self.current_path = []
                elif self.state == "returning":
                    # Arrived at return point, reset to hunting
                    self.state = "hunting"
                    self.return_point = None
                    self.target = Vector2(
                        random.uniform(0, WORLD_WIDTH),
                        random.uniform(0, WORLD_HEIGHT)
                    )
                    self.current_path = []

    def update(self, deltaTime: float, world: 'GameWorld'):
        self._world = world
        self.check_visibility(world)

        # If captured animal is gone, reset state
        if self.has_captured_animal:
            entity_type = type(self.has_captured_animal).__name__
            if (entity_type not in world.entities or
                self.has_captured_animal not in world.entities[entity_type]):
                self.has_captured_animal = None
                self.state = "returning"
                self.escape_point = None
                self.return_point = Vector2(
                    random.uniform(0, WORLD_WIDTH),
                    random.uniform(0, WORLD_HEIGHT)
                )
                self.target = self.return_point
                self.current_path = []

        # Failsafe: If stuck in a state with no target, reset to hunting
        if (self.state == "escaping" and not self.escape_point) or \
           (self.state == "returning" and not self.return_point) or \
           (self.state not in ["hunting", "escaping", "returning"]):
            self.state = "hunting"
            self.has_captured_animal = None
            self.escape_point = None
            self.return_point = None
            self.target = Vector2(
                random.uniform(0, WORLD_WIDTH),
                random.uniform(0, WORLD_HEIGHT)
            )
            self.current_path = []

        self.move()
        if self.state == "hunting":
            self.hunt(world)
        if self.has_captured_animal:
            self.has_captured_animal.position = self.position

        # Clear captured animal after rendering if flagged
        if self._clear_captured_next_update:
            self.has_captured_animal = None
            self._clear_captured_next_update = False

    def render(self, surface: pygame.Surface, camera: 'Camera'):
        if not self.visible:
            return  # Don't render if not visible
            
        screenPos = camera.worldToScreen(self.position)
        radius = int(self.size / 2 * camera.zoom)
        pygame.draw.circle(surface, self.color, (int(screenPos.x), int(screenPos.y)), radius)
        
        # Draw captured animal if exists
        if self.has_captured_animal:
            pygame.draw.circle(surface, self.has_captured_animal.color, 
                             (int(screenPos.x), int(screenPos.y)), 
                             int(self.size / 4 * camera.zoom))
