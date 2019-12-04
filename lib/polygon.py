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
            position = self.vertices[i].rotate(self.angle).add(self.position)
            result.append([position.x, position.y])
        return result

    def getVerticesAsVec(self) -> []:
        result = []
        for i in range(0, len(self.vertices)):
            position = self.vertices[i].rotate(self.angle).add(self.position)
            result.append(vec.Vector(position.x, position.y, 0))
        return result

    def update(self, deltaTime: float, gravity: float):
        self.velocity = self.velocity.add(vec.Vector(0, -gravity * deltaTime, 0))
        self.position = self.position.add(self.velocity.scale(deltaTime))
        self.angle = self.angle + self.angular * deltaTime

    def sortFirst(self, val):
        return val[0]

    def findShortest(self, other: 'Polygon'):
        # distance of each vertex of the first polygon
        # from every side of the other polygon, needed 
        # to decide the side we want to check collision on
        d = []
        otherVerts = other.getVerticesAsVec()
        selfVerts = self.getVerticesAsVec()
        print('amount of vertices in \'self\': ' + str(len(selfVerts)))
        print('amount of vertices in \'other\': ' + str(len(otherVerts)))
        for i in range(0, len(self.vertices)):
            for u in range(0, len(otherVerts)):
                if u == len(otherVerts)-1:
                    next = 0
                else:
                    next = u + 1
                y = math.fabs(((otherVerts[next].x - otherVerts[u].x)
                            * (selfVerts[i].y - otherVerts[u].y))
                            - ((selfVerts[i].x - otherVerts[u].x)
                            * (otherVerts[next].y - otherVerts[u].y)))
                a = math.sqrt(math.pow(otherVerts[next].x - otherVerts[u].x, 2)
                            + math.pow(otherVerts[next].y - otherVerts[u].x, 2))
                d.append((y/a, i, u))
        print(d)
        d.sort(key = self.sortFirst, reverse = True)
        print('\n\n' + str(d))
        print('length of distance array: ' + str(len(d)))
        print('closest combination vertex point of self and first vertex of line in other: ' + str(d[0]))
        return d[0]

    def collidesWithOtherPolygon(self, other: 'Polygon') -> bool:
        d = findShortest(self, other)
        
        return False

    def collidesWithWall(self, wall) -> bool:
        return False

    def onCollision(self):
        return
