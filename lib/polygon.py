import lib.vector as vec
class Polygon:
    def __init__(self, mass: float, inertia: float, vertices: int):
        self.mass = mass
        self.inertia = inertia

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
