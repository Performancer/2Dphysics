#!/usr/bin/env python3
import lib.vector as vec
import lib.polygon as pol
from matplotlib import pyplot
from matplotlib import animation

polygons = []

polygons.append(pol.Polygon(1, 1, 4, 2))
polygons[0].position = vec.Vector(2,5,0)
polygons[0].velocity = vec.Vector(10,0,0)


polygons.append(pol.Polygon(8, 1, 3, 2))
polygons[1].position = vec.Vector(8,5,0)


fig = pyplot.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = pyplot.axes(xlim=(0, 10), ylim=(0, 10))

patches = []
patches.append(pyplot.Polygon(polygons[0].getVertexArray()))
patches.append(pyplot.Polygon(polygons[1].getVertexArray()))

def init():
    ax.add_patch(patches[0])
    ax.add_patch(patches[1])
    return []

def animate(i, square, triangle):
    polygons[0].update(20 / 1000, 9.81)
    polygons[1].update(20 / 1000, 9.81)

    if polygons[0].collidesWithOtherPolygon(polygons[1]) and polygons[1].collidesWithOtherPolygon(polygons[0]):
        polygons[0].onCollision(polygons[1])

    patches[0].set_xy(polygons[0].getVertexArray())
    patches[1].set_xy(polygons[1].getVertexArray())
    return []


anim = animation.FuncAnimation(fig, animate, 
                               init_func=init,
                               frames=1,
                               fargs=(patches[0], patches[1],),
                               interval=20,
                               blit=True,
                               repeat=True)

pyplot.show()
