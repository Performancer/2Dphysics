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

    def getNormal(self, edge: vec.Vector) -> vec.Vector:
        normal = vec.Vector(-edge.y, edge.x, 0).normalize()  
        if edge.cross(normal).z > 0:
            return normal.scale(-1.0)
        return normal
        
    def collidesWithOtherPolygon(self, other: 'Polygon') -> bool:
        selfVerts = self.getVerticesAsVec()
        otherVerts = other.getVerticesAsVec()
        
        for i in range(0, len(selfVerts)):
            iNext = (i + 1) % len(selfVerts)
            normal = self.getNormal(selfVerts[iNext] - selfVerts[i])

            sHighest = -90000
            sLowest = 90000

            for j in range(0, len(selfVerts)):
                length = selfVerts[j].dot(normal)
                if length > sHighest:
                    sHighest = length
                if length < sLowest:
                    sLowest = length

            oHighest = -90000
            oLowest = 90000 

            for j in range(0, len(otherVerts)):
                length = otherVerts[j].dot(normal)
                if length > oHighest:
                    oHighest = length
                if length < oLowest:
                    oLowest = length
                
            if oHighest - oLowest > 0 and oLowest - sHighest > 0:
                return False
            if oHighest - oLowest < 0 and oLowest - sHighest < 0:
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
