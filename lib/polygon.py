import lib.vector as vec
import math
import sys

class Polygon:
    def __init__(self, mass: float, inertia: float, radius: float, vertices: int):
        self.mass = mass
        self.inertia = inertia
        self.position = vec.Vector(0,0,0)
        self.velocity = vec.Vector(0,0,0)
        self.radius = radius
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
        if self.position.y - self.radius > 0:
            self.velocity += vec.Vector(0, -gravity * deltaTime, 0)
            
        #self.velocity = self.velocity - self.velocity.normalize().scale(0.5 * (self.velocity.magnitude() + 0.001)**2 * 0.4 * (2*self.radius)**2 * 1.204 * deltaTime/self.mass)
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
    def getDistance(self, point: vec.Vector, start: vec.Vector, end: vec.Vector) -> float:
        edge = end - start

        a = point - start
        b = edge.normalize()

        #FORMULA: a1 = (a dot b)b
        projection = b.scale(a.dot(b))
        #FORMULA: a2 = a - a1
        rejection = a - projection

        #the projection is to opposite direction than the edge, hypotenuse of projection and rejection is the distance
        if projection.dot(b) < 0:
            return vec.Vector(projection.magnitude(), rejection.magnitude(), 0).magnitude()
        #the projection is to the same direction but longer than the edge, hypotenuse of projection - edge and rejection is the distance
        if projection.magnitude() > edge.magnitude():
            return vec.Vector(projection.magnitude() - edge.magnitude(), rejection.magnitude(), 0).magnitude()

        #projection is to the same direction and does not exceed edge, rejection is the distance
        return rejection.magnitude()

    #gets the vertice and the edge of the collision contact point
    def findCollision(self, other: 'Polygon') -> vec.Vector:
        data = {'distance': sys.float_info.max, 'vertex': vec.Vector(0,0,0), 'edge': vec.Vector(0,0,0)}
        
        for i in range(0, len(self.vertices)):
            start = self.getVertex(i)
            end = self.getVertex((i+1) % len(self.vertices))
            edge = end - start
            for j in range(0, len(other.vertices)):
                vertex = other.getVertex(j)
                distance = self.getDistance(vertex, start, end)
                
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

    # collision between polygon and border
    def collidesWithBorder(self, bottom: float, top: float, left: float, right: float):
        if self.position.y - self.radius < bottom and self.velocity.y < 0:
            for i in range(len(self.vertices)):
                if self.getVertex(i).y < bottom:
                    return True
        if self.position.y + self.radius > top and self.velocity.y > 0:
            for i in range(0, len(self.vertices)):
                if self.getVertex(i).y > top:
                    return True
        if self.position.x - self.radius < left and self.velocity.x < 0:
            for i in range(0, len(self.vertices)):
                if self.getVertex(i).x < left:
                    return True
        if self.position.x + self.radius > right and self.velocity.x > 0:
            for i in range(0, len(self.vertices)):
                if self.getVertex(i).x > right:
                    return True
                           
        return False

    def onBorderCollision(self, bottom: float, top: float, left: float, right: float):
        
        for i in range(len(self.vertices)):
            if self.getVertex(i).y < bottom and self.velocity.y < 0:
                self.calsu(self.getVertex(i), vec.Vector(0, 1, 0))
                break
            if self.getVertex(i).y > top and self.velocity.y > 0:
                self.calsu(self.getVertex(i), vec.Vector(0, -1, 0))
                break

        for i in range(len(self.vertices)):
            if self.getVertex(i).x < left and self.velocity.x < 0:
                self.calsu(self.getVertex(i), vec.Vector(1, 0, 0))
                break      
            if self.getVertex(i).x > right and self.velocity.x > 0:
                self.calsu(self.getVertex(i), vec.Vector(-1, 0, 0))
                break


    def calsu(self, contact: vec.Vector, normal: vec.Vector):
        #distance from center of mass to the collision contact
        rP = contact - self.position
        #vertex velocity before the collision
        velocity = self.velocity + (vec.Vector(0, 0, self.angular).cross(rP))
        e = 0.8 #maybe this could be parameter
        impulse = -(e + 1) * (velocity.dot(normal) / ( 1/self.mass + (rP.cross(normal).magnitude()**2)/self.inertia ))
        
        self.velocity += normal.scale(impulse/self.mass)
        self.angular += rP.cross(normal).scale(impulse/self.inertia).z
