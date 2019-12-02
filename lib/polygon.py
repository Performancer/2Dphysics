import lib.vector as vec
import math
class Polygon:
    def __init__(self, mass: float, inertia: float, amountOfVertices: int, radius: float):
        self.mass = mass
        self.inertia = inertia
        self.amountOfVertices = amountOfVertices
        self.radius = radius
        self.vertices = []
        self.locateVertices(amountOfVertices)   

    def locateVertices(self, count: int):
        angle = 2.0 * math.pi / self.amountOfVertices
        for i in range(0, count):
            self.vertices.append(vec.Vector(
                - math.sin(angle * i), 
                math.cos(angle * i), 0.0).scale(self.radius))

    def setPosition(self, position: vec.Vector):
        self.position = position

    def setVelocity(self, velocity: vec.Vector):
        self.velocity = velocity

    def setAngle(self, angle: float):
        self.angle = angle

    def setAngular(self, angular: float):
        self.angular = angular

    def update(self, deltaTime: float):
        return

    def draw(self):
        return

    def collidesWithOther(self, other: 'Polygon') -> bool:
        return False

    def collidesWithWall(self, wall) -> bool:
        return False

    def onCollision(self):
        return
