import lib.vector as vec
import lib.polygon as pol
import math

a = vec.Vector(3, 4, 0)
b = vec.Vector(2, 8, 0)

mag = a.magnitude(b)
print('magnitude: ' + str(mag))

sub = a.subtract(b)
print('subtract: ' + str(sub.x) + ' ' + str(sub.y))

dot = a.dot(b)
print('dot ' + str(dot))

scale = a.scale(10)
print('scale ' + str(scale.x) + ' ' + str(scale.y))

cross = a.cross(b)
print('cross: ' + str(cross.x) + ' ' + str(cross.y) + ' ' + str(cross.z))


pola = pol.Polygon(1, 0, 4, 1)
polb = pol.Polygon(1, 0, 3, 1)
polc = pol.Polygon(1, 0, 5, 1)

print('vertices in polygon a (4 vertices): \n\tfirst: ' + 
                                str(round(pola.vertices[0].x, 2)) + ' ' + 
                                str(round(pola.vertices[0].y, 2)) + ' ' + 
                                str(round(pola.vertices[0].z, 2)) + 
                                '\n\tsecond: ' + 
                                str(round(pola.vertices[1].x, 2)) + ' ' + 
                                str(round(pola.vertices[1].y, 2)) + ' ' + 
                                str(round(pola.vertices[1].z, 2)) +
                                '\n\tthird: '  + 
                                str(round(pola.vertices[2].x, 2)) + ' ' +
                                str(round(pola.vertices[2].y, 2)) + ' ' +
                                str(round(pola.vertices[2].z, 2)) +
                                '\n\tfourth: ' + 
                                str(round(pola.vertices[3].x, 2)) + ' ' +
                                str(round(pola.vertices[3].y, 2)) + ' ' +
                                str(round(pola.vertices[3].z, 2)))

print('vertices in polygon b (3 vertices): \n\tfirst: ' + 
                                str(round(polb.vertices[0].x, 2)) + ' ' + 
                                str(round(polb.vertices[0].y, 2)) + ' ' + 
                                str(round(polb.vertices[0].z, 2)) + 
                                '\n\tsecond: ' + 
                                str(round(polb.vertices[1].x, 2)) + ' ' + 
                                str(round(polb.vertices[1].y, 2)) + ' ' + 
                                str(round(polb.vertices[1].z, 2)) +
                                '\n\tthird: '  + 
                                str(round(polb.vertices[2].x, 2)) + ' ' +
                                str(round(polb.vertices[2].y, 2)) + ' ' +
                                str(round(polb.vertices[2].z, 2)))
                                

print('vertices in polygon c (5 vertices): \n\tfirst: ' + 
                                str(round(polc.vertices[0].x, 2)) + ' ' + 
                                str(round(polc.vertices[0].y, 2)) + ' ' + 
                                str(round(polc.vertices[0].z, 2)) + 
                                '\n\tsecond: ' + 
                                str(round(polc.vertices[1].x, 2)) + ' ' + 
                                str(round(polc.vertices[1].y, 2)) + ' ' + 
                                str(round(polc.vertices[1].z, 2)) +
                                '\n\tthird: '  + 
                                str(round(polc.vertices[2].x, 2)) + ' ' +
                                str(round(polc.vertices[2].y, 2)) + ' ' +
                                str(round(polc.vertices[2].z, 2)) +
                                '\n\tfourth: ' + 
                                str(round(polc.vertices[3].x, 2)) + ' ' +
                                str(round(polc.vertices[3].y, 2)) + ' ' +
                                str(round(polc.vertices[3].z, 2)) +
                                '\n\tfifth: ' + 
                                str(round(polc.vertices[4].x, 2)) + ' ' +
                                str(round(polc.vertices[4].y, 2)) + ' ' +
                                str(round(polc.vertices[4].z, 2)))


print('velocity test')
pola.position = vec.Vector(0,0,0)
pola.velocity = vec.Vector(0,0,0)
pola.angle = 0
pola.angular = 0
print(str(pola.position.x) + ' ' + str(pola.position.y))
pola.update(10, -9.81)
print(str(pola.position.x) + ' ' + str(pola.position.y))


newpola = pola.rotate(math.pi/2)

print(str(newpola[0]))
print(str(newpola[1]))
print(str(newpola[2]))
print(str(newpola[3]))