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
            self.vertices.append(vec.Vector(0, self.radius, 0).rotate(angle * i))

    def getVertices(self) -> []:
        result = []
        for i in range(0, len(self.vertices)):
            position = self.position + self.vertices[i].rotate(self.angle)
            result.append([position.x, position.y])
        return result

    def getVerticesAsVec(self) -> []:
        result = []
        for i in range(0, len(self.vertices)):
            position = self.vertices[i].rotate(self.angle) + (self.position)
            result.append(vec.Vector(position.x, position.y, 0))
        return result

    def update(self, deltaTime: float, gravity: float):
        self.velocity += vec.Vector(0, -gravity * deltaTime, 0)
        self.position += self.velocity.scale(deltaTime)
        self.angle += self.angular * deltaTime

    def CollidesWithOtherPolygon(self, other: 'Polygon') -> bool:
        selfVerts = self.getVerticesAsVec()
        otherVerts = other.getVerticesAsVec()
        largestSelfDot = -999999
        #selfDots = []
        for i in range(0, len(selfVerts)):
            iNext = (i + 1) % len(selfVerts)
            edge = selfVerts[iNext] - selfVerts[i]
            normal = vec.Vector(-edge.y, edge.x, 0).normalize()
            if edge.cross(normal).z > 0:
                normal.scale(-1)
            if selfVerts[i].dot(normal) > largestSelfDot:
                largestSelfDot = selfVerts[i].dot(normal)
        for u in range(0, len(otherVerts)):
            print(largestSelfDot)
            print(otherVerts[u].dot(normal))
            if largestSelfDot <= otherVerts[u].dot(normal):
                return False
        return True

    def collidesWithFloor(self) -> bool:
        vertices = self.getVerticesAsVec()
        
        if self.velocity.y < 0:
            for i in range(0, len(vertices)):
                if vertices[i].y < 0:
                    return True;
                           
        return False

    def onCollision(self):
        return
