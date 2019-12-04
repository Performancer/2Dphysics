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
                
            if oHighest - sLowest > 0 and oLowest - sHighest > 0:
                return False
            if oHighest - sLowest < 0 and oLowest - sHighest < 0:
                return False
                
        return True

    def collidesWithFloor(self) -> bool:
        vertices = self.getVertices()
        
        if self.velocity.y < 0:
            for i in range(0, len(vertices)):
                if vertices[i].y < 0:
                    return True
                           
        return False

    def getDistance(self, point: vec.Vector, start: vec.Vector, end: vec.Vector) -> float:
        sp = start - point #vector from point to start of line
        n = (end - start).normalize() #normalized line
        
        #FORMULA: d = |(s-p) - ((s-p) dot n)n|
        return (sp - n.scale(sp.dot(n))).magnitude()
    
    def findCollision(self, other: 'Polygon') -> vec.Vector:
        selfVerts = self.getVertices()
        otherVerts = other.getVertices()
        
        shortest = 99999
        vertex = vec.Vector(0,0,0)
        edge = vec.Vector(0,0,0)
        
        for i in range(0, len(selfVerts)):
            for j in range(0, len(otherVerts)):
                distance = self.getDistance(selfVerts[i], otherVerts[j], otherVerts[(j + 1) % len(otherVerts)])
                
                if(distance < shortest):
                    shortest = distance
                    vertex = selfVerts[i]
                    edge = otherVerts[(j + 1) % len(otherVerts)] - otherVerts[j]

                distance = self.getDistance(otherVerts[j], selfVerts[i], selfVerts[(i + 1) % len(selfVerts)])

                if(distance < shortest):
                    shortest = distance
                    vertex = otherVerts[j]
                    edge = selfVerts[(i + 1) % len(selfVerts)] - selfVerts[i]
                              
        return (vertex, edge)

    def onCollision(self, other: 'Polygon') -> vec.Vector:
        data = self.findCollision(other)
        collision = data[0]
        edge = data[1]
        
        normal = self.getNormal(edge)

        rA = collision - self.position
        rB = collision - other.position
        VAB = self.velocity + (vec.Vector(0, 0, self.angular).cross(rA)) - other.velocity + (vec.Vector(0, 0, other.angular).cross(rB))

        e = 0.8 #maybe this could be parameter
        impulse = -(e + 1) * (VAB.dot(normal) / ( 1/self.mass + (rA.cross(normal).magnitude()**2)/self.inertia + 1/other.mass + (rB.cross(normal).magnitude()**2)/other.inertia))

        self.velocity += normal.scale(impulse/self.mass)
        self.angular += impulse/self.inertia * rA.cross(normal).z
        
        other.velocity -= normal.scale(impulse/other.mass)
        other.angular -= impulse/other.inertia * rB.cross(normal).z

        return collision
