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
                 
        self.locateVertices(vertices, radius)  

    #locates the vertices in an even distance
    def locateVertices(self, count: int, radius: float):
        self.vertices = []
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
        self.velocity = self.velocity.scale(0.99)
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

        return {'highest': highest, 'lowest': lowest}

    #checks if the polygon collides with another polygon
    def collides(self, other: 'Polygon') -> bool:
        for i in range(0, len(self.vertices)):
            normal = self.getNormal(self.getVertex((i+1) % len(self.vertices)) - self.getVertex(i))  
            sProj = self.getProjections(normal)
            oProj = other.getProjections(normal)
                        
            if oProj['highest'] - sProj['lowest'] > 0 and oProj['lowest'] - sProj['highest'] > 0:
                return False
            if oProj['highest'] - sProj['lowest'] < 0 and oProj['lowest'] - sProj['highest'] < 0:
                return False
                
        return True

    #gets the distance from a point to a line
    def getDistance(self, point: vec.Vector, start: vec.Vector, line: vec.Vector) -> float:
        sp = start - point
        n = line.normalize()    
        #FORMULA: d = |(s-p) - ((s-p) dot n)n|
        return (sp - n.scale(sp.dot(n))).magnitude()

    #gets the vertice and the edge of the collision contact point
    def findCollision(self, other: 'Polygon') -> vec.Vector:
        data = {'distance': sys.float_info.max, 'vertex': vec.Vector(0,0,0), 'edge': vec.Vector(0,0,0)}
        
        for i in range(0, len(self.vertices)):
            start = self.getVertex(i)
            edge = self.getVertex((i+1) % len(self.vertices)) - start
            for j in range(0, len(other.vertices)):
                vertex = other.getVertex(j)
                distance = self.getDistance(vertex, start, edge)
                
                if(distance < data['distance']):
                    data = {'distance': distance, 'vertex': vertex, 'edge': edge}
                              
        return data

    #handles collision between two polygons
    def onCollision(self, other: 'Polygon') -> vec.Vector:
        data = self.findCollision(other)
        alternative = other.findCollision(self)

        if alternative['distance'] < data['distance']:
           data = alternative

        contact = data['vertex']
        normal = self.getNormal(data['edge'])
        
        rA = contact - self.position
        rB = contact - other.position
        VAB = self.velocity + (vec.Vector(0, 0, self.angular).cross(rA)) - other.velocity + (vec.Vector(0, 0, other.angular).cross(rB))

        e = 0.8 #maybe this could be parameter
        impulse = -(e + 1) * (VAB.dot(normal) / ( 1/self.mass + (rA.cross(normal).magnitude()**2)/self.inertia + 1/other.mass + (rB.cross(normal).magnitude()**2)/other.inertia))

        self.velocity += normal.scale(impulse/self.mass)
        self.angular += impulse/self.inertia * rA.cross(normal).z
        
        other.velocity -= normal.scale(impulse/other.mass)
        other.angular -= impulse/other.inertia * rB.cross(normal).z

        return contact

    def collidesWithBorder(self, floorY:float, ceilingY:float, leftWallX:float, rightWallX:float):
        if self.velocity.y < 0:
            for i in range(0, len(self.vertices)):
                if self.getVertex(i).y < floorY:
                    return True
        else:
            for i in range(0, len(self.vertices)):
                if self.getVertex(i).y > ceilingY:
                    return True
        if self.velocity.x < 0:
            for i in range(0, len(self.vertices)):
                if self.getVertex(i).x < leftWallX:
                    return True
        else:
            for i in range(0, len(self.vertices)):
                if self.getVertex(i).x > rightWallX:
                    return True
                           
        return False

    def onBorderCollision(self, floorY:float, ceilingY:float, leftWallX:float, rightWallX:float):
        
        for i in range(0, len(self.vertices)):
            if self.getVertex(i).y < floorY:
                contact = self.getVertex(i)
                normal = vec.Vector(0, 1, 0)
            if self.getVertex(i).y > ceilingY:
                contact = self.getVertex(i)
                normal = vec.Vector(0, -1, 0)
            if self.getVertex(i).x < leftWallX:
                contact = self.getVertex(i)
                normal = vec.Vector(1, 0, 0)
            if self.getVertex(i).x > rightWallX:
                contact = self.getVertex(i)
                normal = vec.Vector(-1, 0, 0)
            
        rP = contact - self.position
        vertexVelocity = self.velocity + (vec.Vector(0, 0, self.angular).cross(rP))
        e = 0.7
        impulse = -(e + 1) * (vertexVelocity.dot(normal) / ( 1/self.mass + (rP.cross(normal).magnitude()**2)/self.inertia ))
        
        self.velocity = self.velocity + normal.scale(impulse/self.mass)
        self.angular = self.angular + rP.cross(normal).scale(impulse/self.inertia).magnitude()