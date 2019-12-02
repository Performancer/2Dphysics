import lib.vector as vec
import lib.polygon as pol

a = vec.Vector(3, 4)
a = a.scale(10)
a.x = 5
print('toimii: ' + str(a.x) + ' ' + str(a.y))