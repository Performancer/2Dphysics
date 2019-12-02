import math

class Vector:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def add(self, other: 'Vector') -> 'Vector':
        return self

    def subtract(self, other: 'Vector') -> 'Vector':
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def cross(self, other: 'Vector') -> 'Vector':
        return Vector(self.y*other.z - self.z*other.y,
                       self.z*other.x - self.x*other.z,
                       self.x*other.y - self.y*other.x)

    def dot(self, other: 'Vector') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def scale(self, scalar: float) -> 'Vector':
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def normalize(self) -> 'Vector':
        return self

    def magnitude(self, other: 'Vector') -> float:
        return (math.sqrt (self.x**2 + self.y**2 + self.z**2) )
