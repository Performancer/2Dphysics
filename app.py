#!/usr/bin/env python3
import lib.vector as vec
import lib.polygon as pol
from matplotlib import pyplot
from matplotlib import animation

polygons = []

polygons.append(pol.Polygon(1, 0, 4, 2))
polygons[0].position = vec.Vector(3,5,0)
polygons[0].angular = 5
polygons.append(pol.Polygon(8, 1, 3, 2))
polygons[1].position = vec.Vector(6,5,0)
polygons[1].angular = -5

fig = pyplot.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = pyplot.axes(xlim=(0, 10), ylim=(0, 10))

patches = []
patches.append(pyplot.Polygon(polygons[0].getVertices()))
patches.append(pyplot.Polygon(polygons[1].getVertices()))

def init():
    ax.add_patch(patches[0])
    ax.add_patch(patches[1])
    return []

def animate(i, square, triangle):
    polygons[0].update(20 / 1000, 9.81)
    polygons[1].update(20 / 1000, 9.81)

    print('Collision?: ' + str(polygons[0].collidesWithOtherPolygon(polygons[1])))

    patches[0].set_xy(polygons[0].getVertices())
    patches[1].set_xy(polygons[1].getVertices())
    return []


anim = animation.FuncAnimation(fig, animate, 
                               init_func=init,
                               frames=1,
                               fargs=(patches[0], patches[1],),
                               interval=1000,
                               blit=True,
                               repeat=True)

pyplot.show()
