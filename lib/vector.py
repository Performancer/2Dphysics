
class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def add(self, other: 'Vector') -> 'Vector':
        return self

    def subtract(self, other: 'Vector') -> 'Vector':
        return self

    def cross(self, other: 'Vector') -> 'Vector':
        return self

    def dot(self, other: 'Vector') -> 'Vector':
        return self

    def scale(self, scalar: float) -> 'Vector':
        return Vector(self.x * scalar, self.y * scalar)

    def normalize(self) -> 'Vector':
        return self

    def magnitude(self) -> float:
        return 0
