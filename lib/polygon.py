import lib.vector as vec
import math
import sys

class Polygon:
    def __init__(self, mass: float, inertia: float, radius: float, vertices: int):
        self.mass = mass
        self.inertia = inertia
        self.position = vec.Vector(0,0,0)
        self.velocity = vec.Vector(0,0,0)
        self.angle = 0
        self.angular = 0
        self.vertices = []
                
        self.locateVertices(vertices, radius)  

    #locates the vertices in an even distance
    def locateVertices(self, count: int, radius: float):
        angle = 2.0 * math.pi / count
        for i in range(0, count):
            self.vertices.append(vec.Vector(0, radius, 0).rotate(angle * i))

    #gets the rotated and transformed vertex
    def getVertex(self, i: int) -> vec.Vector:
        return self.position + self.vertices[i].rotate(self.angle)

    #gets the rotated and transformed vertices
    def getVertices(self) -> []:
        vertices = []  
        for i in range(0, len(self.vertices)):
            vertices.append(self.getVertex(i))
        return vertices

    #handles the acceleration, velocity, angular velocity
    def update(self, deltaTime: float, gravity: float):
        self.velocity += vec.Vector(0, -gravity * deltaTime, 0)
        self.position += self.velocity.scale(deltaTime)
        self.angle += self.angular * deltaTime

    #gets the normal of an edge (counter-clockwise)
    def getNormal(self, edge: vec.Vector) -> vec.Vector:
        normal = vec.Vector(-edge.y, edge.x, 0).normalize()  
        if edge.cross(normal).z > 0:
            return normal.scale(-1.0)
        return normal

    #gets the highest and lowest value of vertices projected to an axis
    def getProjections(self, axis: vec.Vector):
        highest = sys.float_info.min
        lowest = sys.float_info.max

        for i in range(0, len(self.vertices)):
            length = self.getVertex(i).dot(axis)
            if length > highest:
                highest = length
            if length < lowest:
                lowest = length

        return (highest, lowest)

    #checks if the polygon collides with another polygon
    def collides(self, other: 'Polygon') -> bool:
        for i in range(0, len(self.vertices)):
            normal = self.getNormal(self.getVertex((i+1) % len(self.vertices)) - self.getVertex(i))  
            sProj = self.getProjections(normal)
            oProj = other.getProjections(normal)
                        
            if oProj[0] - sProj[1] > 0 and oProj[1] - sProj[0] > 0:
                return False
            if oProj[0] - sProj[1] < 0 and oProj[1] - sProj[0] < 0:
                return False
                
        return True

    #gets the distance from a point to a line
    def getDistance(self, point: vec.Vector, start: vec.Vector, end: vec.Vector) -> float:
        sp = start - point #vector from point to start of line
        n = (end - start).normalize() #normalized line
        
        #FORMULA: d = |(s-p) - ((s-p) dot n)n|
        return (sp - n.scale(sp.dot(n))).magnitude()

    #gets the vertice and the edge of the collision contact point
    def findCollision(self, other: 'Polygon') -> vec.Vector:
        shortest = sys.float_info.max
        vertex = vec.Vector(0,0,0)
        edge = vec.Vector(0,0,0)
        
        for i in range(0, len(self.vertices)):
            for j in range(0, len(other.vertices)):
                distance = self.getDistance(self.getVertex(i), other.getVertex(j), other.getVertex((j+1) % len(other.vertices)))
                
                if(distance < shortest):
                    shortest = distance
                    vertex = self.getVertex(i)
                    edge = other.getVertex((j + 1) % len(other.vertices)) - other.getVertex(j)

                distance = self.getDistance(other.getVertex(j), self.getVertex(i), self.getVertex((i+1) % len(self.vertices)))

                if(distance < shortest):
                    shortest = distance
                    vertex = other.getVertex(j)
                    edge = self.getVertex((i + 1) % len(self.vertices)) - self.getVertex(i)
                              
        return (vertex, self.getNormal(edge))

    #handles collision between two polygons
    def onCollision(self, other: 'Polygon') -> vec.Vector:
        data = self.findCollision(other)
        collision = data[0]
        normal = data[1]

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

    def collidesWithFloor(self) -> bool:
        if self.velocity.y < 0:
            for i in range(0, len(vertices)):
                if self.getVertex(i).y < 0:
                    return True
                           
        return False
