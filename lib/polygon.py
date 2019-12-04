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

    def getVertexArray(self) -> []:
        result = []
        for i in range(0, len(self.vertices)):
            position = self.position + self.vertices[i].rotate(self.angle)
            result.append([position.x, position.y])
        return result

    def getVertices(self) -> []:
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
        selfVerts = self.getVertices()
        otherVerts = other.getVertices()
        
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
        vertices = self.getVertices()
        
        if self.velocity.y < 0:
            for i in range(0, len(vertices)):
                if vertices[i].y < 0:
                    return True
                           
        return False

    def findClosest(self, other: 'Polygon') -> vec.Vector:
        shortestD = (99999, vec.Vector(0,0,0), vec.Vector(0,0,0))
        otherVerts = other.getVertices()
        selfVerts = self.getVertices()
        for i in range(0, len(selfVerts)):
            for u in range(0, len(otherVerts)):
                uNext = (u + 1) % len(selfVerts)
                edge = otherVerts[uNext] - otherVerts[u]
                numerator = math.fabs((edge.x * (selfVerts[i].y - otherVerts[u].y)) - edge.y * (selfVerts[i].x - otherVerts[u].x))
                denomirator = math.sqrt(math.pow(edge.x, 2) + math.pow(edge.y, 2))
                d = numerator/denomirator
                if(d < shortestD[0]):
                    shortestD = (d, selfVerts[i], otherVerts[uNext] - otherVerts[u])
        return (shortestD[1], shortestD[2])

    def onCollision(self, other: 'Polygon'):
        #how to know which vertice has collide with which edge


        collision = self.findClosest(other)[0]
        edge = self.findClosest(other)[1]

        #there are two possible normals, inside and outside
        #how to determine the one that points outside?   
        normal = vec.Vector(edge.y, -edge.x, 0).normalize()

        rA = collision - self.position
        rB = collision - other.position
        VAB = self.velocity + (vec.Vector(0, 0, self.angular).cross(rA)) - other.velocity + (vec.Vector(0, 0, other.angular).cross(rB))

        e = 1
        I = -(e + 1) * (VAB.dot(normal)
           / ( 1/self.mass + (rA.cross(normal).magnitude()**2)/self.inertia
              + 1/other.mass + (rB.cross(normal).magnitude()**2)/other.inerta))

        self.velocity += normal.scale(I/self.mass)
        self.angular += I/self.inertia * rA.cross(normal).z
        
        other.velocity += normal.scale(I/other.mass)
        other.angular += I/other.inerta * rB.cross(normal).z
