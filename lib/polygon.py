import lib.vector as vec
import math
class Polygon:
    def __init__(self, mass: float, inertia: float, vertices: int, radius: float):
        self.mass = mass
        self.inertia = inertia
        self.radius = radius
        self.vertices = []
        self.locateVertices(vertices)   

    def locateVertices(self, count: int):
        angle = 2.0 * math.pi / count
        for i in range(0, count):
            self.vertices.append(vec.Vector(-math.sin(angle * i), math.cos(angle * i), 0.0).scale(self.radius))

    def rotate(self, angle: float) -> []:
        newVertices = []
        for i in range(len(self.vertices)):
            newVertices.append([math.cos(angle) * self.vertices[i].x - math.sin(angle) * self.vertices[i].y, 
                                math.sin(angle) * self.vertices[i].x + math.cos(angle) * self.vertices[i].y, 0]) 
        return newVertices

    def setPosition(self, position: vec.Vector):
        self.position = position

    def setVelocity(self, velocity: vec.Vector):
        self.velocity = velocity

    def setAngle(self, angle: float):
        self.angle = angle

    def setAngular(self, angular: float):
        self.angular = angular

    def update(self, deltaTime: float, gravity: float):
        self.velocity = self.velocity.add(vec.Vector(0, -gravity * deltaTime, 0))
        self.position = self.position.add(self.velocity.scale(deltaTime))
        self.angle = self.angle + self.angular * deltaTime

    def collidesWithOther(self, other: 'Polygon') -> bool:
        return False

    def collidesWithWall(self, wall) -> bool:
        return False

    def onCollision(self):
        return
