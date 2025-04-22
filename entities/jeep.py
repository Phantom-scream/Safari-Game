from ui.vector2 import Vector2
from entities.tourist import Tourist

class Jeep:
    def __init__(self, position: Vector2, road_path: list):
        self.position = position
        self.road_path = road_path  # List of Vector2 positions along the road
        self.passengers = [Tourist(f"Tourist {i+1}") for i in range(4)]
        self.state = "to_exit"  # or "to_entrance"
        self.current_index = 0  # Index in the road_path
        self.color = (60, 60, 200)  # Add this line for minimap and rendering
        self.size = 28  # Make the jeep bigger (was 18)
        self.move_timer = 0.0  # Timer for movement
        self.move_interval = 0.25  # Move every 0.25 seconds (slower)

    def move(self):
        if self.state == "to_exit":
            if self.current_index < len(self.road_path) - 1:
                self.current_index += 1
                self.position = self.road_path[self.current_index]
            else:
                self.state = "to_entrance"
                self.passengers = []  # Tourists leave at exit
        elif self.state == "to_entrance":
            if self.current_index > 0:
                self.current_index -= 1
                self.position = self.road_path[self.current_index]
            else:
                self.state = "to_exit"
                self.passengers = [Tourist(f"Tourist {i+1}") for i in range(4)]

    def has_passengers(self):
        return len(self.passengers) > 0

    def update(self, deltaTime, world):
        # Move the jeep at a slower rate using a timer
        self.move_timer += deltaTime
        if self.move_timer >= self.move_interval:
            self.move()
            self.move_timer = 0.0