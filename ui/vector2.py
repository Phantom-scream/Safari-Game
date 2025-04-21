class Vector2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def add(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x + other.x, self.y + other.y)

    def subtract(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x - other.x, self.y - other.y)

    def normalize(self) -> 'Vector2':
        length = self.distanceTo(Vector2(0, 0))
        if length == 0:
            return Vector2(0, 0)
        return Vector2(self.x / length, self.y / length)

    def distanceTo(self, other: 'Vector2') -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    def __eq__(self, other):
        return isinstance(other, Vector2) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((round(self.x, 4), round(self.y, 4)))