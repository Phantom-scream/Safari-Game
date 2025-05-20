from entities.entity import Entity
from ui.vector2 import Vector2
from entities.tourist import Tourist
import pygame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gamelogic.game_world import GameWorld
    from ui.camera import Camera


class Jeep(Entity):
    def __init__(self, position, road_path):
        super().__init__(position, 20, "Jeep")
        self.just_arrived_at_exit = False
        self.road_path = road_path
        self.animals_seen = set()
        self.total_animals_seen = 0
        self.passengers = [Tourist(f"Tourist {i+1}") for i in range(4)]
        self.state = "to_exit"
        self.current_index = 0
        self.color = (60, 60, 200)
        self.size = 40  # Back to original size
        self.speed = 120
        self.position = Vector2(position.x + 0.5 * (road_path[0].size if hasattr(road_path[0], 'size') else 40), 
                                position.y + 0.5 * (road_path[0].size if hasattr(road_path[0], 'size') else 40))

    def move(self, deltaTime):
        # Move from center of one road cell to center of next
        if self.state == "to_exit":
            target_index = min(self.current_index + 1, len(self.road_path) - 1)
        else:
            target_index = max(self.current_index - 1, 0)

        # Center of the target road cell
        target_pos = Vector2(
            self.road_path[target_index].x + 0.5 * (self.road_path[target_index].size if hasattr(self.road_path[target_index], 'size') else 40),
            self.road_path[target_index].y + 0.5 * (self.road_path[target_index].size if hasattr(self.road_path[target_index], 'size') else 40)
        )
        direction = Vector2(target_pos.x - self.position.x, target_pos.y - self.position.y)
        distance = (direction.x ** 2 + direction.y ** 2) ** 0.5

        if distance > 0:
            direction.x /= distance
            direction.y /= distance
            move_dist = self.speed * deltaTime
            if move_dist >= distance:
                self.position = Vector2(target_pos.x, target_pos.y)
                self.current_index = target_index
                if self.state == "to_exit" and self.current_index == len(self.road_path) - 1:
                    self.just_arrived_at_exit = True
                    self.state = "to_entrance"
                    
                elif self.state == "to_entrance" and self.current_index == 0:
                    self.state = "to_exit"
                    self.passengers = [Tourist(f"Tourist {i+1}") for i in range(4)]
                    self.animals_seen.clear()         # <-- Add this line
                    self.total_animals_seen = 0      
            else:
                self.position.x += direction.x * move_dist
                self.position.y += direction.y * move_dist

    def has_passengers(self):
        return len(self.passengers) > 0

    def update(self, deltaTime, world):
        self.move(deltaTime)
        # Each step, check for animals nearby
        for animal_type in ["Bison", "Zebra", "Antelope", "Lion", "Hyena", "Crocodile"]:
            for animal in world.entities.get(animal_type, []):
                if self.position.distanceTo(animal.position) < 50:  # Adjust radius as needed
                    self.animals_seen.add(animal_type)
                    self.total_animals_seen += 1

        # At the end of the road, only if there are passengers
        if self.just_arrived_at_exit and self.has_passengers():
            base_revenue = 100
            diversity_bonus = 20 * len(self.animals_seen)
            animal_bonus = 5 * self.total_animals_seen
            total_revenue = base_revenue + diversity_bonus + animal_bonus
            world.economy.add_money(total_revenue)
            # Reset for next tour
            self.animals_seen.clear()
            self.total_animals_seen = 0
            self.passengers = []  # Now clear passengers
            self.just_arrived_at_exit = False
            
    def render(self, surface: pygame.Surface, camera: 'Camera'):
        screen_pos = camera.worldToScreen(self.position)
        size = self.size * camera.zoom
        pygame.draw.rect(surface, self.color, (screen_pos.x, screen_pos.y, size, size))
