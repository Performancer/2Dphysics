class Polygon:
    def __init__(self, mass: float, inertia: float, vertices: int)
        self.mass = mass
        self.inertia = inertia

    def setPosition(self, position: Vector)
        self.position = position

    def setVelocity(self, velocity: Vector)
        self.velocity = velocity

    def setAngle(self, angle: float)
        self.angle = angle

    def setAngular(self, angular: float)
        self.angular = angular

    def update(self, deltaTime: float)
        return

    def draw(self)
        return

    def collides(self, other: Polygon) -> bool
        return false

    def collides(self, wall) -> bool
        return false

    def onCollision()
        return
