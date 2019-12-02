import lib.vector as vec
import lib.polygon as pol

a = vec.Vector(3, 4, 0)
b = vec.Vector(2, 8, 0)

sub = a.subtract(b)
print('subtract: ' + str(sub.x) + ' ' + str(sub.y))

dot = a.dot(b)
print('dot ' + str(dot))

scale = a.scale(10)
print('scale ' + str(scale.x) + ' ' + str(scale.y))

cross = a.cross(b)
print('cross: ' + str(cross.x) + ' ' + str(cross.y) + ' ' + str(cross.z))
