import lib.vector as vec
import math
class Polygon:
    def __init__(self, mass: float, inertia: float, vertices: int, radius: float):
        self.mass = mass
        self.inertia = inertia
        self.radius = radius
        self.vertices = []
        self.locateVertices(vertices)   
        self.position = vec.Vector(0,0,0)
        self.velocity = vec.Vector(0,0,0)
        self.angle = 0
        self.angular = 0

    def locateVertices(self, count: int):
        angle = 2.0 * math.pi / count
        for i in range(0, count):
            self.vertices.append(vec.Vector(-math.sin(angle * i), math.cos(angle * i), 0.0).scale(self.radius))

    def getVertices(self) -> []:
        result = []
        for i in range(0, len(self.vertices)):
            position = self.vertices[i].rotate(self.angle).add(self.position)
            result.append([position.x, position.y])
        return result

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
